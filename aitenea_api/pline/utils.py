# Utils para la app Pline de AItenea
from datetime import datetime

from django.db import connection
from django.http import JsonResponse, HttpResponse
from rest_framework import response, status
from .models import Pline
from pline.api.serializers import PlineSerializerFull

from logsconf.log_conf import logging_config
from aitenea_core import pfactory as pipe
from aitenea_core import perpetuity
from rest_framework.exceptions import ValidationError
from dask_ml.model_selection import train_test_split

from .data_utils import HandlerData
from reports.utils import redis_pub, create_pline_report_metric

import logging
from logging.config import dictConfig
loggtype = 'CONSOLE'

dictConfig(logging_config)
logger = logging.getLogger(loggtype)


def compose_pline(context):
    """Compone una `Pline` a partir de un JSON recibido 

    Args:
        context ([JSON]): JSON que contendrá la key `Pline`. Dentro habrá otro JSON con el formato definido por serializers.PlineSerializerFull

    Returns:
        pfac [aitenea_core.pfactory]: tubería formada con los pasos indicados.
        p [aitenea_api.pline.models.Pline]: objeto `Pline` asociado a la tubería pfac.
    """
    pline = None
    p = None

    try:
        pline = context['pline']
        # Debajo se recorta el module_name para quitarle aitenea.aitenea_core o el que venga cuando vengan otros
        for step in pline['steps']:
            step['module_name'] = step['module_name'].replace('"', '')
        # Crea la pline con el serializador, sirve de comprobación de que los datos son los que deben ser
        p = create_pline(pline)
    except KeyError as err:
        logger.error("El objeto no contiene la clave pline.")
    pfac = pipe.PFactory()
    jobs = []
    for step in pline['steps']:
        options = step['step_options']
        aux = options.copy()
        # De momento se retiran los campos de algoritmia genética con el bucle for de debajo
        for i in aux.keys():
            if i[-4:] == "_gen":
                del options[i]
        options = {'options': options}

        genetic_parameters = {'options': step['step_genetic_parameters']}

        job = dict(
            {'type': step['step_type'],
             'module_name': step['module_name'],
             'name': step['step_name'],
             'options': options,
             'genetic_parameters': genetic_parameters})
        jobs.append(job)

        logger.debug("Añadido paso a la pipeline.")
    try:
        pfac.compose_pipe_line(jobs)
    except ValidationError as err:
        logger.error(
            "Error en la tubería, eliminandola de la base de datos: %s",
            str(err))
        Pline.objects.filter(id=p.id).delete()
        return None, "pLine err" + str(err)
    return pfac, p


def create_pline(pline):
    """Crea una `Pline` en base de datos a partir de un modelo de `Pline` y su serializador.

    Args:
        pline ([JSON]): `Pline` según definida en Pline AItenea.

    Returns:
        PlineSerializerFull [serializers.PlineSerializerFull]: Objeto de Django validado para ser `Pline`.
    """
    plineser = PlineSerializerFull(data=pline)  # hacer un serializer full
    if plineser.is_valid():
        p = plineser.save()
        logger.info("Creada pline en base de datos con id: %i", p.id)
        return p
    else:
        logger.error("Error al crear la pipeline %s", plineser.errors)


def load_pipeline(id):  # Puede ser útil cuando haga predict, de momento no
    """
    Returns:
        p [aitenea_api.pline.models.Pline]: objeto `Pline`.
    """
    p = Pline.objects.filter(id=id)[0]
    return p


def check_pipe_name(pipe_name):
    p = Pline.objects.filter(name=pipe_name)
    if len(p) > 0:
        return True
    else:
        return False


def validate_workflow(context):
    """
    Comprueba la estructura de la `Pline` e informa de los errores encontrados si esta es incorrecta.
    """

    is_workflow_valid = True
    error_msg = ""

    try:
        run_type = context.get("run_type", None)
        pline = context.get("pline", None)
        steps = pline.get("steps", None)
        pline_id = pline.get("id", None)

        if steps is not None:
            if (len(steps) > 0):
                ai_count = 0
                ai_found = False
                for step in steps:
                    if "_ai" in step["step_type"]:
                        ai_found = True
                        ai_count+=1

                    # Error AI class antes de TRANSFORM class
                    if "_transform" in step["step_type"] and ai_found:
                        is_workflow_valid = False
                        error_msg = "You can't use a Pline-step TRANSFORM class after a Pline-step AI class."
                        logger.error(error_msg)

                # Error multiple AI classes
                if ai_count > 1:
                    is_workflow_valid = False
                    error_msg = "You can't use more than 1 Pline-step AI class in the same workflow."
                    logger.error(error_msg)

                # Error AI class
                if "_ai" in steps[-1]["step_type"] and run_type != "fit" and run_type != "fit_predict":
                    is_workflow_valid = False
                    error_msg = "You can only use 'fit' or 'fit_predict' run types if the workflow ends with a Pline-step AI class."
                    logger.error(error_msg)

                # Error TRANSFORM class
                if "_transform" in steps[-1]["step_type"] and run_type != "fit" and run_type != "fit_transform":
                    is_workflow_valid = False
                    error_msg = "You can only use 'fit' or 'fit_transform' run types if the workflow ends with a Pline-step TRANSFORM class."
                    logger.error(error_msg)

        # Error model-get solo predict permitido
        elif pline_id is not None and run_type != "predict":
            is_workflow_valid = False
            error_msg = "You can only use 'predict' run type if the workflow uses a trained model."
            logger.error(error_msg)

    except Exception as err:
        is_workflow_valid = False
        logger.error("Error in the structure of the received Pline, check it's format.")
        logger.error(err)

    return is_workflow_valid, error_msg

def set_metadata(context, p, user):
    info_data = dict()
    data_info = context['origin']
    info_data["type"] = data_info["type"]
    info_data["table"] = data_info["options"]["index"]
    info_data["X"] = data_info["options"]["X"]
    info_data["y"] = data_info["options"]["y"]
    info_model = {
        "model_name": p.name, "description": p.description, "owner": user,
        "creation": p.creation_timestamp}
    metadata = {"info_model": info_model, "info_data": info_data}
    return metadata

def get_connector(context):
    """
    Devuelve el conector teniendo en cuenta el `origin` y `target`.
    """
    target = None
    try:
        target = context["target"]
    except KeyError:
        pass
    connector = HandlerData(context['origin'], target)
    return connector

def clean_plines(pline_name, overwrite):
    """
    Elimina las `Plines` con el mismo si se ha permitido sobreescribir.
    En el caso de que no deba sobreescribir la `Pline` devuelve `JsonResponse`.
    """
    response = None
    response_body = dict()
    try:
        if check_pipe_name(pline_name) and not overwrite:
            raise IndexError("The pipe already exists, change name in Pline-Set")
        elif check_pipe_name(pline_name) and overwrite:
            old_pline = Pline.objects.get(name=pline_name)
            old_pline.delete()
    except IndexError as err:
        msg = err.args
        response_body["error"] = msg
        logger.info(msg)
        response = JsonResponse(response_body, status=status.HTTP_200_OK)
    except Pline.DoesNotExist:
        logger.error("Pipeline no existe.")

    return response

def pline_setup(context):
    """
    Elimina las `Plines` antiguas con el mismo nombre y crea una nueva.
    """
    response = None
    pipe = None
    pfac = None
    pline = None
    response_body = dict()

    pline_name = context["pline"]["name"]
    overwrite = context["pline"]["update_index"]
    response = clean_plines(pline_name, overwrite)

    if response is None:
        pfac, pline = compose_pline(context)
        if pfac is None or pline is None:
            response_body["error"] = pline
            response = JsonResponse(response_body, status=status.HTTP_200_OK)
        else:
            response_body['pline_id'] = pline.id
            pipe = pfac.make_pipe()
    
    return response, pipe, pfac, pline

def fit_error_handler(pline, pline_report, redis_topic, err):
    """
    Almacena el error del `fit` en el reporte, el status de `Redis` y la respuesta, también elimina la `Pline`.
    """
    response = None
    response_body = dict()
    logger.error("Error to fit . %s", str(err))

    response_body["error"] = "Fit error. Verify that the inputs are correct and that there are not inappropriate types"
    response_body["out"] = None

    # Actualizar informe de Pline
    pline_report.error_output = "Fit error"
    pline_report.save()

    redis_pub(
        pline, redis_topic, "Fit error", False, True)

    Pline.objects.filter(id=pline.id).delete()

    response = JsonResponse(
        response_body, status=status.HTTP_200_OK)
    

    return response, pline_report

def pline_update(context, pipe, pfac, pline, connector, data, transform_type, score, **kwargs):
    """
    Almacena los datos de la `Pline` y devuelve el resultado después de una ejecución correcta del `fit`.
    """
    response = None
    response_body = dict()
    user = pline.owner
    perpetuity_handler = perpetuity.Perpetuity(user.username)
    metadata = set_metadata(context, pline, user.username)
    perpetuity_handler.save_model(metadata, pipe)
    pline.fitted = response_body['fitted'] = True
    pline.metadata = metadata
    pline.save()
    msg, output = connector.handler_output(pipeline=pfac, data=data, transform=transform_type)

    response_body["out"] = output
    response_body["msg"] = msg
    response_body["score"] = score
    response = JsonResponse(response_body, status=status.HTTP_200_OK)
    
    return response

def fit_completion_report_handler(pline, pline_report, start_time, score, redis_topic):
    """
    Actualizar el reporte de la `Pline` y status de `Redis` marcadolo como finalizado y guardando el tiempo de ejecución.
    """
    # Tiempo transcurrido en la ejecución de la pline
    pline_report.pline = pline
    pline_report.execution_time = datetime.now() - start_time
    pline_report.save()

    # Guardar métrica de algoritmo
    if score is not None:
        create_pline_report_metric(pline_report, pline, score)

    redis_pub(
        pline, redis_topic, "Pline fitted.", True, False)

    return pline_report


def split_data(train_size, x_result, y_result):
    x_train, x_test, y_train, y_test = None, None, None, None
    if y_result is None:
        x_train = x_result
    else:
        if x_result is not None:
            try:
                x_train, x_test, y_train, y_test = train_test_split(
                                x_result, y_result, train_size=train_size)
            except Exception:
                pass
    return x_train, x_test, y_train, y_test

def get_score(pipe, x_test, y_test):
    score = None
    try: 
        score = pipe.score(x_test, y_test)
    except Exception:
        pass
    return score