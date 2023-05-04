import json
from django.db import connection
from django.http import HttpResponse, JsonResponse
from requests import request
import pyodbc

from .models import AiteneaClass
from .data_utils import HandlerData, DataEvaluation, DBSQLConnector
from .aitenea_cleaning import NaNValues
from .utils import get_connector


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
        except KeyError as err:
            response['error'] = str(err)
        except pyodbc.ProgrammingError:
            response['error'] = 'The table that has been selected is not accesible '
        except pyodbc.OperationalError:
            response['error'] = 'Problem with the query. Check that the query has been well defined'
        else:
            evaluation = DataEvaluation(data)
            response['evaluation'] = evaluation.get_evaluation()
        return HttpResponse(
            json.dumps(response),
            content_type="application/json")


def nan_values(request):
    response = dict()
    if request.method == 'POST':
        request_dict = json.loads(request.body)
        connect_dict = dict()
        connect_dict['type'] = request_dict['origin']['type']
        connect_dict['options'] = request_dict['origin']['options']
        connector = get_connector(request_dict)
        data = connector.load()
        nan_approach = NaNValues(connect_dict, data)
        try:
            nan_handled = nan_approach.nan_handling()
        except ValueError as err:
            response['error'] = 'KeyError'
            logger.info(f'An exception has ocurred: {err}')
        except Exception as err:
            logger.info(f'An exception has ocurred: {err}')
        else:
            response['output'] = nan_handled
            data_nan = nan_approach.get()
            if data_nan['message'] == 'NaNs treated':
                handler_out = connector.handler_database(data_nan['dataframe'])
                response['To elastic'] = 'The dataset after NaNs handling has been sent to Elastic successfully '
            else:
                response['To elastic'] = 'Data has not been modified, therefore, it has not been sent toward Elastic'
        return HttpResponse(
            json.dumps(response),
            content_type="application/json")


def sql_get_db(request):
    response = dict()
    if request.method == "POST":
        request_dict = json.loads(request.body)
        elas_dict = dict()
        action = request_dict["source_connector"]["action"]
        elas_dict["type"] = request_dict["source_connector"]["type_connector"]
        elas_dict["options"] = request_dict["source_connector"]['connection']
        try:
            connector = DBSQLConnector(
                elas_dict["type"], elas_dict["options"], None)
            connection_setter = connector.create_connection()
            cursor = connection_setter.cursor()
        except pyodbc.OperationalError:
            response['error'] = 'Check connection parameters and BBDD manager'
        else:
            if action == "get-all-sql-tables":
                tbl_name = connector.get_tbl_names(cursor)
                response["data"] = tbl_name
            elif action == "get-columns":
                table = request_dict["source_connector"]["index"]
                column_names = connector.get_column_names(cursor, table)
                raw_data_type = connector.get_type_raw_columns(cursor, table)
                raw_data_type = connector.sql_type_conversor_dict(
                    raw_data_type, elas_dict["type"])
                response["data"] = {"names": column_names,
                                    "types": raw_data_type}
            elif action == "advanced-query":
                text_query = request_dict["source_connector"]["query"]
                try:
                    column_names = connector.search_advanced_query(
                        cursor, text_query)
                    raw_data_type = connector.sql_type_conversor_dict(
                        column_names[1], elas_dict["type"])
                except pyodbc.Error:
                    response['error'] = 'Invalid Query. Check syntax, column and table names, \
                    or verify that the table you are searching correponds to the previosluy selected server.'
                else:
                    response["data"] = {"names": column_names[0],
                                        "types": raw_data_type}
        return HttpResponse(json.dumps(response),
                            content_type="application/json")
