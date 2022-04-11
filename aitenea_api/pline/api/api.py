from datetime import datetime

from rest_framework import exceptions, viewsets, permissions, generics, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import response
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse

from pline.models import Pline, Step, AiteneaClass
from .serializers import PlineSerializer, StepSerializer, AiteneaClassSerializer

from pline.utils import get_connector, pline_setup, pline_update, validate_workflow, load_pipeline, fit_error_handler, fit_completion_report_handler, split_data, get_score
from reports.utils import create_pline_report, create_pline_report_metric, redis_pub

from aitenea_core import perpetuity

import os
from pathlib import Path
import csv

# Log configuration
from logsconf.log_conf import logging_config
import logging
from logging.config import dictConfig
loggtype = 'CONSOLE'

dictConfig(logging_config)
logger = logging.getLogger(loggtype)


class PlineViewSet(viewsets.ModelViewSet):
    """
    Lista todas las `pline` existentes en la BBDD.
    `List all Plines`.
    """
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = PlineSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'name', 'owner']

    def get_queryset(self):
        user = self.request._user
        plines = Pline.objects.all()
        if not user.is_staff:
            plines = Pline.objects.filter(owner=user)
        return plines

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(
        detail=False,
        methods=['POST'],
        name='Delete one or more Plines.',
        url_path='delete_bulk')
    def delete_bulk(self, request, *args, **kwargs):
        if len(request.data):
            Pline.objects.filter(pk__in=request.data).delete()
        return Response(None, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=['POST'],
        name='Create a Pline and fit.',
        url_path='fit')
    def fit(self, request, *args, **kwargs):
        response = None
        response_body = dict()
        context = request.data

        transform_type = False

        is_workflow_valid, error_msg = validate_workflow(context)
        if is_workflow_valid:
            start_time = datetime.now()
            pline_report = create_pline_report(context)

            connector = get_connector(context)
            count, x_result, y_result = connector.load()
            response, pipe, pfac, pline = pline_setup(context)
            if response is None:
                redis_pub(
                    pline, context["redis_topic"],
                    "Pline created, running training...", False, False)
                try:
                    train_size = context['origin']['options']['train_size']
                    # Dividir dataset en train y test datasets
                    x_train, x_test, y_train, y_test = split_data(
                        train_size, x_result, y_result)
                    pipe.fit(x_train, y_train)
                    data = None
                except Exception as err:
                    response, pline_report = fit_error_handler(
                        pline, pline_report, context["redis_topic"], err)
                else:
                    score = get_score(pipe, x_test, y_test)
                    response = pline_update(
                        context, pipe, pfac, pline, connector, data,
                        transform_type, score)
                    pline_report = fit_completion_report_handler(
                        pline, pline_report, start_time, score,
                        context["redis_topic"])
            else:
                # Actualizar informe de Pline
                pline_report.error_output = "The pipe already exists, change name in Pline-Set"
                pline_report.save()
        else:
            response_body["error"] = error_msg
            response = JsonResponse(response_body, status=status.HTTP_200_OK)

        return response

    @action(
        detail=False,
        methods=['POST'],
        name='Create a Pline, fit and predict.',
        url_path='fit_predict')
    def fit_predict(self, request, *args, **kwargs):
        response = None
        response_body = dict()
        context = request.data

        transform_type = False

        is_workflow_valid, error_msg = validate_workflow(context)
        if is_workflow_valid:
            start_time = datetime.now()
            pline_report = create_pline_report(context)

            connector = get_connector(context)
            count, x_result, y_result = connector.load()

            response, pipe, pfac, pline = pline_setup(context)
            if response is None:
                redis_pub(
                    pline, context["redis_topic"],
                    "Pline created, running training...", False, False)

                try:
                    train_size = context['origin']['options']['train_size']
                    # Dividir dataset en train y test datasets
                    x_train, x_test, y_train, y_test = split_data(train_size, x_result, y_result)
                    # Ejecutar fits
                    data = pipe.fit_predict(x_train, y_train)
                    # Score
                    data_test = None
                    if len(x_test) > 0:
                        data_test = pipe.predict(x_test)
                except Exception as err:
                    response, pline_report = fit_error_handler(
                        pline, pline_report, context["redis_topic"], err)
                else:
                    score = get_score(pipe, x_test, y_test)
                    response = pline_update(
                        context, pipe, pfac, pline, connector, data,
                        transform_type, score, data_test=data_test, test=(x_test, y_test))
                    pline_report = fit_completion_report_handler(
                        pline, pline_report, start_time, score,
                        context["redis_topic"])
            else:
                # Actualizar informe de Pline
                pline_report.error_output = "The pipe already exists, change name in Pline-Set"
                pline_report.save()
        else:
            response_body["error"] = error_msg
            response = JsonResponse(response_body, status=status.HTTP_200_OK)

        return response

    @action(
        detail=False,
        methods=['POST'],
        name='Create a Pline, fit and transform.',
        url_path='fit_transform')
    def fit_transform(self, request, *args, **kwargs):
        response = None
        response_body = dict()
        context = request.data

        transform_type = True
        score = None

        is_workflow_valid, error_msg = validate_workflow(context)
        if is_workflow_valid:
            start_time = datetime.now()
            pline_report = create_pline_report(context)
            
            connector = get_connector(context)
            count, x_result, y_result = connector.load()

            response, pipe, pfac, pline = pline_setup(context)
            if response is None:
                redis_pub(
                    pline, context["redis_topic"],
                    "Pline created, running training...", False, False)

                try:
                    data = pipe.fit_transform(x_result)

                except Exception as err:
                    response, pline_report = fit_error_handler(
                        pline, pline_report, context["redis_topic"], err)
                else:
                    response = pline_update(
                        context, pipe, pfac, pline, connector, data,
                        transform_type, score)
                    pline_report = fit_completion_report_handler(
                        pline, pline_report, start_time, score,
                        context["redis_topic"])
            else:
                # Actualizar informe de Pline
                pline_report.error_output = "The pipe already exists, change name in Pline-Set"
                pline_report.save()
        else:
            response_body["error"] = error_msg
            response = JsonResponse(response_body, status=status.HTTP_200_OK)

        return response

    @action(
        detail=False,
        methods=['POST'],
        name='Predict from an existing Pline.',
        url_path='predict')
    def predict(self, request, *args, **kwargs):
        response = None
        response_body = dict()
        context = request.data

        is_workflow_valid, error_msg = validate_workflow(context)
        if is_workflow_valid:
            pline = None
            try:
                pline = load_pipeline(context['pline']['id'])
            except IndexError:
                logger.error("Pipeline no existente.")
                response_body["error"] = "Error de índice de pipeline"
                response = JsonResponse(
                    response_body, status=status.HTTP_200_OK)
            else:
                if pline.fitted:
                    connector = get_connector(context)
                    count, x_result, y_result = connector.load()
                    if count == 0:
                        logger.info(
                            "The selected query does not return data, nothing is executed")
                        response_body["error"] = "The query does not return data"
                        response = JsonResponse(
                            response_body, status=status.HTTP_200_OK)
                    else:
                        user = pline.owner
                        perpetuity_handler = perpetuity.Perpetuity(
                            user.username)
                        pipe, metadata = perpetuity_handler.load_model(
                            pline.name)

                        output = None
                        msg = None

                        try:
                            data = pipe.predict(x_result)
                        except Exception as err:
                            msg = "Error " + str(err)
                            response_body["msg"] = "Model Not Fit"
                            response_body["out"] = None
                            logger.error("Error to predict {}.".format(err))
                        else:
                            msg, output = connector.handler_output(
                                data=data, pipeline=None,
                                predict_inputs=(x_result, y_result))
                        finally:
                            response_body["out"] = output
                            response_body["msg"] = msg
                            response = JsonResponse(
                                response_body, status=status.HTTP_200_OK)
                else:
                    response_body["msg"] = "Model Not Fit"
                    response_body["out"] = None
                    logger.error("Model not fit")
                    response = JsonResponse(
                        response_body, status=status.HTTP_200_OK)
        else:
            response_body["error"] = error_msg
            response = JsonResponse(response_body, status=status.HTTP_200_OK)

        return response

    @action(
        detail=False,
        methods=['POST'],
        name='Genetic Plines fit or fit predict',
        url_path='genetic')
    def genetic(self, request, *args, **kwargs):
        response_body = dict()
        context = request.data

        transform_type = False

        is_workflow_valid, error_msg = validate_workflow(context)
        if is_workflow_valid:
            start_time = datetime.now()
            pline_report = create_pline_report(context)

            connector = get_connector(context)
            count, x_result, y_result = connector.load()
 
        response_body["out"] = None
        response = JsonResponse(response_body, status=status.HTTP_200_OK)
        return response


class StepViewSet(viewsets.ModelViewSet):
    """
    Lista todos los `step` existentes en la `Pline`.
    También permite filtrar por `id` de `Pline`, así se ven todos los pasos que conforman una `Pline`.

    `List all pipelines steps`.
    You can also filter by pline_id.

    E.g. .../api/steps/?pline_id=2
    """
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = StepSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['pline_id', 'step_number', 'step_type']

    def get_queryset(self):
        user = self.request._user
        steps = Step.objects.all()
        if not user.is_staff:
            plines = Pline.objects.filter(owner=user)
            steps = Step.objects.filter(
                pline_id__in=plines).distinct()

        pline = self.request.query_params.get('pline')
        if pline is not None:
            steps = steps.filter(pline_id__id=pline)

        return steps


class AiteneaClassViewSet(viewsets.ModelViewSet):
    """
    Lista todas las clases incluidas en AItenea. Tanto `ai` como `transform`.
    """
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = AiteneaClassSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'class_name', 'type']
    queryset = AiteneaClass.objects.all()

class CSVViewset(viewsets.ViewSet):
    """
    Lista todos los CSVs disponibles en AITenea para cargar datos.
    """

    permission_classes = [
        permissions.IsAuthenticated
    ]

    def list(self, request):
        response_body = list()
        csv_folder_path = Path('../data/csv/')

        # Lista todos archivos por nombre sin extension
        for f in os.scandir(csv_folder_path):
            if os.path.isfile(f):
                response_body.append(os.path.splitext(f.name)[0])

        return Response(response_body, status=status.HTTP_200_OK)

    def create(self, request):
        response_body = dict()
        file = request.FILES.get('file')

        # Eliminamos cualquier path que pueda haber en el nombre del archivo y generamos la ruta de destino
        filename = os.path.basename(file.name)
        csv_path = Path('../data/csv/'+filename)

        # Guardamos el archivo
        if os.path.isfile(csv_path):
            response_body["error"] = "Index name already exists, choose another index name."
            response = JsonResponse(response_body, status=status.HTTP_400_BAD_REQUEST)
            return response
        else:
            try:
                with open(csv_path, 'wb') as file_obj:
                    file_obj.write(file.read())
                    file_obj.close()
            except Exception as e:
                response_body["error"] = "Error saving the CSV file."
                response = JsonResponse(response_body, status=status.HTTP_400_BAD_REQUEST)
                return response

        # Comprobar integridad del archivo
        if os.path.isfile(csv_path):
            with open(csv_path, newline='') as f:
                sniffer = csv.Sniffer()
                try:
                    f.seek(0)
                    # Identificar delimitador
                    sniffer.sniff(f.readline())
                    f.seek(0)
                except Exception as e:
                    response_body["error"] = "Corrupted file or incorrect encoding in CSV file."
                    response = JsonResponse(response_body, status=status.HTTP_400_BAD_REQUEST)
                    os.remove(csv_path)
                    return response

        response = JsonResponse(response_body, status=status.HTTP_200_OK)
        return response

    def retrieve(self, request, pk=None):
        response = None

        csv_path = Path('../data/csv/'+pk+'.csv')
        if os.path.isfile(csv_path):
            with open(csv_path, newline='') as f:
                sniffer = csv.Sniffer()
                try:
                    f.seek(0)
                    # Identificar delimitador
                    dialect = sniffer.sniff(f.readline())
                    f.seek(0)
                    # Devolver cabecera
                    reader = csv.reader(f, dialect)
                    row1 = next(reader)
                    response_body = list(row1)
                    response = Response(response_body, status=status.HTTP_200_OK)
                except Exception as e:
                    response_body = dict()
                    response_body["error"] = "Corrupted file or incorrect encoding in CSV file."
                    response = JsonResponse(response_body, status=status.HTTP_400_BAD_REQUEST)
        else:
            response_body = dict()
            response_body["error"] = "Missing CSV file."
            response = JsonResponse(response_body, status=status.HTTP_400_BAD_REQUEST)
                    
        return response