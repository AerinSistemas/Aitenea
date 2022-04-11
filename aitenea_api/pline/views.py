import json
from django.db import connection
from django.http import HttpResponse, JsonResponse

from .models import AiteneaClass
from .data_utils import HandlerData, DataEvaluation

from .set_models import get_aitenea
from logsconf.log_conf import logging_config
import logging
from logging.config import dictConfig
loggtype = 'CONSOLE'

dictConfig(logging_config)
logger = logging.getLogger(loggtype)


# Create your views here.
# set_models.get_aitenea(model=AiteneaClass)
all_tablas = connection.introspection.table_names()
if all_tablas != []:
    if 'pline_aiteneaclass' in all_tablas:
        get_aitenea(model=AiteneaClass)


#########################
#                       #
#      ELASTICTOOLS     #
#                       #
#########################


def elastic_get_index(request):
    response = dict()
    if request.method == 'POST':
        request_dict = json.loads(request.body)
        elas_dict = dict()
        action = request_dict["source_connector"]["action"]
        elas_dict["type"] = "elastic"
        elas_dict["options"] = request_dict["source_connector"]
        connector = HandlerData(elas_dict, None)
        if action == "get-all-index":
            try:
                index_list = connector.get_index()
            except Exception as err:
                response["Error"] = str(err)
                return HttpResponse(
                    json.dumps(response),
                    content_type="application/json")
            else:
                response["data"] = index_list
                return HttpResponse(
                    json.dumps(response),
                    content_type="application/json")
        elif action == "get-attributes":
            index = request_dict["source_connector"]["index"]
            attributes_str, attributes_values = connector.get_attributes(index)
            response["data"] = {"names": attributes_str,
                                "values": attributes_values}
            return HttpResponse(
                json.dumps(response),
                content_type="application/json")
        elif action == "check-exists-index":
            try:
                index_list = connector.get_index()
            except Exception as err:
                response["Error"] = str(err)
                return HttpResponse(
                    json.dumps(response),
                    content_type="application/json")
            else:
                response["data"] = {"exists": False}
                if request_dict["source_connector"]["index"]["name"] in index_list:
                    response["data"] = {"exists": True}
                return HttpResponse(
                    json.dumps(response),
                    content_type="application/json")

def data_evaluation(request):
    response = dict()
    if request.method == 'POST':
        request_dict = json.loads(request.body)
        connect_dict = dict()
        connect_dict['type'] = request_dict['origin_type']
        connect_dict['options'] = request_dict['options']
        connector = HandlerData(connect_dict, None)
        try:
            data = connector.load()
        except Exception as err:
            response['error'] = str(err)
        else:
            evaluation = DataEvaluation(data)
            response['evaluation'] = evaluation.get_evaluation()
        return HttpResponse(
            json.dumps(response),
            content_type="application/json")
