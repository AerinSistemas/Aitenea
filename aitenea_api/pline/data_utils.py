# Utiles para trabajar con datos
import dask.dataframe as dd
import dask.array as dda
from numpy import partition
import pandas as pd
import numpy as np
import ast
import json
import pyodbc
import time
import sys
import mysql.connector
from mysql.connector import FieldType
from elastictools.aerastic.elastic_index import ElasticIndex, InsertData
from elastictools.aerastic.elastic_query import ElasticQuery
from .sql_type_casting import sql_type_mapping
from logsconf.log_conf import logging_config
from dask.dataframe.core import DataFrame
from dask.array.core import Array

import os
from pathlib import Path
import csv

import logging
from logging.config import dictConfig
loggtype = 'CONSOLE'

dictConfig(logging_config)
logger = logging.getLogger(loggtype)


class SourceConnector(object):
    """Clase para gestionar conexiones con bases de datos desde la Pline

    Args:
        source ([JSON]): JSON que debe contener las keys `type` y `options`
    """

    def __init__(self, source, target=None):
        self.type_source = source['type']
        self.options_source = source['options']
        self.type_target = None
        self.option_target = None
        if target is not None:
            self.type_target = target['type']
            self.option_target = target['options']

    def load(self):
        """Método para obtener datos desde una base de datos compatible con la Pline de AItenea

        Actualmente compatible con Elasticsearch.

        Returns:
            [dask]: dask dataframe con los datos solicitados
        """
        if self.type_source == 'elastic':
            connection = self.options_source['connection']
            connector = ElasticQuery(
                host=connection['host'],
                port=connection['port'],
                user=connection['user'],
                password=connection['password'],
                dask=True)
            q = self.options_source['q']
            x = dict()
            x["_source"] = q["_source"]
            if 'all' in x["_source"] or 'none' in x["_source"]:
                x["_source"] = []
            try:
                x["query"] = ast.literal_eval(q["query"])
            except Exception as err:
                logger.info(
                    "Empty query {}. match_all will be used".format(err))
                x["query"] = {"match_all": {}}
            x_values = self.options_source["X"]
            y_values = self.options_source["y"]
            count, result = connector.raw_query(
                self.options_source['index'], x)
            if count is None:
                load_values = 0, None, None
            else:
                if 'all' in x_values:
                    x_result = result
                else:
                    x_result = result[x_values]
                if 'all' in y_values:
                    y_result = result
                elif 'none' in y_values:
                    y_result = None
                else:
                    y_result = result[y_values]
                load_values = count, x_result, y_result
        elif self.type_source == 'manual data':
            X = self.options_source.get('X')
            y = self.options_source.get('y')
            count = 0
            if X is not None:
                X = dd.from_pandas(pd.DataFrame.from_dict(X), npartitions=1)
                count = len(X)
            if y is not None:
                y = dd.from_pandas(pd.DataFrame.from_dict(y), npartitions=1)
            load_values = count, X, y
        elif self.type_source == 'csv':
            x_values = self.options_source["X"]
            y_values = self.options_source["y"]

            connector = CSVQuery()
            try:
                count, result = connector.raw_query(
                    self.options_source['index'])
            except FileNotFoundError as err:
                load_values = 0, None, None
                logger.info(
                    f'There is not file to load. Check it again. {err}')
            else:
                if count is None:
                    load_values = 0, None, None
                else:
                    if 'all' in x_values:
                        x_result = result
                    else:
                        x_result = result[x_values]
                    if 'all' in y_values:
                        y_result = result
                    elif 'none' in y_values:
                        y_result = None
                    else:
                        y_result = result[y_values]
                    load_values = count, x_result, y_result

        if self.type_source == 'sql':
            connection = self.options_source['connection']
            table = self.options_source['index']
            connector = DBSQLConnector(
                connection['dbmanager'], connection, None)
            connection_setter = connector.create_connection()
            cursor = connection_setter.cursor()
            q = self.options_source['q']
            x_values = self.options_source["X"]
            y_values = self.options_source["y"]
            if q['advanced'] == "yes":
                text_query = q["query"]
                output_search = connector.search_advanced_query(
                    cursor, text_query)
                raw_data_type = connector.sql_type_conversor_dict(
                    output_search[1], connection['dbmanager'])
                raw_dask_dataframe = connector.query_output(
                    output_search[2], output_search[0], raw_data_type)
                x_raw_data, y_raw_data = connector.get_sets_dataframes(
                    raw_dask_dataframe, x_values, y_values)
            else:
                if x_values[0] == 'all':
                    x_values = connector.get_column_names(cursor, table)
                raw_data_type = connector.get_type_raw_columns(cursor, table)
                x_data_type = connector.get_type_set_columns(
                    x_values, raw_data_type)
                y_data_type = connector.get_type_set_columns(
                    y_values, raw_data_type)
                x_data_type = connector.sql_type_conversor(
                    x_data_type, connection['dbmanager'])
                y_data_type = connector.sql_type_conversor(
                    y_data_type, connection['dbmanager'])
                x_query, y_query = connector.get_raw_query(
                    x_values, y_values, table, cursor)
                x_search = connector.search_query(cursor, x_query)
                x_raw_data = connector.query_output(
                    cursor, x_values, x_data_type)
                y_search = connector.search_query(cursor, y_query)
                y_raw_data = connector.query_output(
                    cursor, y_values, y_data_type)
            try:
                count = len(x_raw_data)
            except Exception as err:
                logger.info(
                    f'An exception has been arisen getting size of data: {err}')
                load_values = 0, None, None
                return load_values
            else:
                if count is None:
                    load_values = 0, None, None
                else:
                    load_values = count, x_raw_data, y_raw_data
        return load_values

    def dump(self, dataframe):
        """Método para volcar los datos de una predicción en una base de datos compatible con la Pline de AItenea

        Actualmente compatible con Elasticsearch.

        Args:
            dataframe (dask.dataframe): dataframe original utilizado para hacer la predicción
            prediction (dask.array): array con la predicción obtenida con el dataframe original
        """
        if self.type_target == 'elastic':
            connection = self.option_target['connection']
            elas = ElasticIndex(
                host=connection['host'],
                port=connection['port'],
                user=connection['user'],
                password=connection['password'],
                dask=True)
            pandas_head = dataframe.head()
            if self.option_target['update_index']:
                elas.delete_index(self.option_target['index'])

            index_map, types_dictionary = elas.get_index(
                self.option_target['index'])
            if index_map.get("empty", None) is not None:
                elas.set_index_from_pandas(
                    self.option_target['index'],
                    pandas_head)
                ingest = InsertData(
                    host=connection['host'],
                    port=connection['port'],
                    user=connection['user'],
                    password=connection['password'], timeout=6000)
                ingest.insert_dask(
                    dataframe, self.option_target['index'],
                    "dask", index_id=True)
        elif self.type_target == 'CSV':
            csv = CSVwrite()
            csv.write_csv(
                dataframe, self.option_target['index'], self.option_target['singleOutputFile'], self.option_target['separator'])

    def get_index(self, source=True):
        if source:
            connection = self.options_source['connection']
        else:
            connection = self.option_target['connection']
        index_list = []
        elas = ElasticIndex(
            host=connection['host'],
            port=connection['port'],
            user=connection['user'],
            password=connection['password'],
            dask=True)
        for index_ in elas.get_all_index():
            if not '.' in index_:
                index_list.append(index_)
        return index_list

    def get_attributes(self, index, source=True):
        if source:
            connection = self.options_source['connection']
        else:
            connection = self.option_target['connection']
        connector = ElasticIndex(
            host=connection['host'],
            port=connection['port'],
            user=connection['user'],
            password=connection['password'],
            dask=True)
        index_map = connector.get_maptypes(index)[0][index]
        attributes_values = []
        attributes_str = []
        for att, types in index_map["mappings"]["properties"].items():
            attributes_str.append(att + " - " + types["type"])
            attributes_values.append(att)
        return attributes_str, attributes_values


class HandlerData(SourceConnector):
    def __init__(self, source, target):
        super(HandlerData, self).__init__(source, target)
        self.source = source
        self.target = target

    def handler_output(self, data, pipeline=None, predict_inputs=None, transform=False):
        if data is None:
            msg, out = "Fit executed, data is None", None
        else:
            if transform:
                msg, out = self.interfaz_output(data)
                self.handler_database(data)
            else:
                if predict_inputs is not None:
                    x_input, y_input = predict_inputs
                else:
                    x_input, y_input = pipeline.get_input()
                output = self.set_output(data, x_input, y_input)
                msg, out = self.interfaz_output(output)
        return msg, out

    def set_output(self, data, x_input, y_input):
        rows_x = x_input.shape[0].compute()
        data_size = data.shape
        x_input = x_input.reset_index(drop=True)
        if len(data_size) == 1:
            n_columns = 1
        else:
            n_columns = data_size[1]
        if y_input is None:
            columns = [str(n)+"_output" for n in range(0, n_columns)]
        else:
            y_input = y_input.reset_index(drop=True)
            columns = [name+"_output" for name in y_input.columns]
        if data_size[0] == rows_x:
            if len(data_size) == 1:
                data_column = dd.from_dask_array(
                    data, columns=columns[0], index=x_input.index).to_frame()
                x_input[columns[0]] = data_column[columns[0]]
            else:
                for n, column in enumerate(columns):
                    data_column = dd.from_dask_array(
                        data[:, n], columns=column).to_frame()
                    data_column = data_column.repartition(
                        npartitions=x_input.npartitions).reset_index(drop=True)
                    x_input[column] = data_column[column]
            if y_input is not None:
                output = dd.concat([x_input, y_input], axis=1)
            else:
                output = x_input
        else:
            output = dd.from_dask_array(data)
            output.columns = columns

        self.handler_database(output)
        return output

    def handler_database(self, output):
        if self.target is not None:
            target_type = self.target["type"]
            if target_type == 'elastic':
                self.dump(output)
            elif target_type == 'CSV':
                self.dump(output)

    def interfaz_output(self, data):
        try:
            if isinstance(data, Array):
                size = data.shape[0]
            else:
                size = data.shape[0].compute()
        except Exception as err:
            out = None
            msg = "Error " + str(err)
        else:
            size = min(200, size)
            try:
                if isinstance(data, DataFrame):
                    out = data.head(size).to_json(date_format='iso')
                elif isinstance(data, Array):
                    out = data.compute().tolist()
                else:
                    out = None
                    msg = "Error, the output is not a dask dataset"
            except Exception as err:
                out = None
                msg = "Error " + str(err)
            else:
                msg = "Ok"
        return msg, out


class DataEvaluation(object):
    def __init__(self, data, options=None):
        self.data = data
        self.evaluation_dictionary = dict()

    def get_evaluation(self):
        counts = self.data[0]
        dataframe_X = self.data[1]
        dataframe_y = self.data[2]
        self.evaluation_dictionary['total_counts'] = counts
        if counts > 0:
            self.show_values(dataframe_X, target=False)
            self.show_values(dataframe_y, target=True)
            self.check_nan_values(dataframe_X, target=False)
            self.check_nan_values(dataframe_y, target=True)
            self.describe(dataframe_X, target=False)
            self.describe(dataframe_y, target=True)
            self.cov(dataframe_X, dataframe_y)
        return self.evaluation_dictionary

    def describe(self, data, target=True):
        if data is not None:
            types_info = dict()
            if target:
                name = 'data type y'
                describe = 'data describe y'
                nan_values = json.loads(
                    self.evaluation_dictionary['NaN Values of y'])
            else:
                name = 'data type X'
                describe = 'data describe X'
                nan_values = json.loads(
                    self.evaluation_dictionary['NaN Values of x'])
            if self.check_empty(data):
                for column, dtype in zip(data.columns, data.dtypes):
                    types_info[column] = str(dtype)
                self.evaluation_dictionary[name] = types_info
                for key, value in nan_values.items():
                    if value == len(data):
                        key_all_nan, nan_flag = key, True
                        data = data.drop([key], axis=1)
                        if len(data.columns) == 0:
                            data = None
                    else:
                        nan_flag = False
                try:
                    if data is not None:
                        self.evaluation_dictionary[describe] = data.describe(
                            include='all').compute().to_json()
                    if nan_flag:
                        message = 'All the column contains NaNs. Data describe can not be achieved for this column.'
                        if 'data describe y' in self.evaluation_dictionary:
                            self.describer_tester(
                                describe, key_all_nan, message)
                        else:
                            if 'data describe X' in self.evaluation_dictionary and not target:
                                self.describer_tester(
                                    describe, key_all_nan, message)
                            else:
                                self.evaluation_dictionary[describe] = message
                                self.evaluation_dictionary[describe] = json.dumps(
                                    self.evaluation_dictionary[describe])
                except Exception as err:
                    logger.warning(f'An exception has been raised: {err}')

    def describer_tester(self, describe, key_all_nan, message):
        self.evaluation_dictionary[describe] = json.loads(
            self.evaluation_dictionary[describe])
        self.evaluation_dictionary[describe][key_all_nan] = message
        self.evaluation_dictionary[describe] = json.dumps(
            self.evaluation_dictionary[describe])

    def cov(self, data_X, data_y):
        if data_y is not None and data_X is not None:
            all_matrix = data_X.join(data_y, lsuffix='_X', rsuffix='_y')
        elif data_X is not None:
            all_matrix = data_X
        elif data_y is not None:
            all_matrix = data_y
        else:
            self.evaluation_dictionary['correlation'] = None
        if self.check_empty(all_matrix):
            if 'float64' in all_matrix.dtypes.values:
                cov_matrix = all_matrix.corr()
                self.evaluation_dictionary['correlation'] = cov_matrix.compute(
                ).to_json()
        else:
            self.evaluation_dictionary['correlation'] = None

    def check_empty(self, dataset):
        return len(dataset.columns) > 0

    def check_nan_values(self, data, target=True):
        if data is not None:
            if target:
                name = 'NaN Values of y'
            else:
                name = 'NaN Values of x'
            if self.check_empty(data):
                nan_values = data.isnull().sum()
                self.evaluation_dictionary[name] = nan_values.compute(
                ).to_json()

    def show_values(self, data, target=True):
        if data is not None:
            if target:
                name = 'Header of values of y'
            else:
                name = 'Header of values of x'
            if self.check_empty(data):
                header = data.head(10)
                self.evaluation_dictionary[name] = header.to_json(
                    date_format='iso')
                if len(data) >= 10:
                    header = data.head(10)
                else:
                    header = data.head(len(data))
                self.evaluation_dictionary[name] = header.to_json()


class CSVQuery(object):
    def __init__(self):
        """Class to manage elastic queries."""
        self.count = 0

    def raw_query(self, index):
        dialect = '\t'
        csv_path = Path('../data/csv/'+index+'.csv')
        with open(csv_path, newline='') as f:
            sniffer = csv.Sniffer()
            f.seek(0)
            dialect = sniffer.sniff(f.readline())
        result = dd.read_csv(csv_path, blocksize=100e6,
                             sep=dialect.delimiter, assume_missing=True)
        count = len(result.index)
        return count, result

    def get_dialect(self, index):
        dialect = None
        csv_path = Path('../data/csv/'+index+'.csv')
        if os.path.isfile(csv_path):
            with open(csv_path, newline='') as f:
                sniffer = csv.Sniffer()
                try:
                    f.seek(0)
                    # Identificar delimitador
                    dialect = sniffer.sniff(f.readline())
                except Exception as e:
                    logger.warning(f'An exception has been raised: {e}')
        return dialect

    def get_header_names(self, index):
        header_names = None
        csv_path = Path('../data/csv/'+index+'.csv')
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
                    header_names = list(row1)
                except Exception as e:
                    logger.warning(f'An exception has been raised: {e}')

        return header_names


class CSVwrite(object):
    def __init__(self):
        """Class to write results of transformation or prediction in a CSV file"""

    def write_csv(self, data_to_write, csv_name, singleoutput, separator):
        csv_path = Path('../data/csv/')
        if separator == 'Tabulator':
            sep = '\t'
        singleoutput = json.loads(singleoutput)

        if singleoutput == True:
            csv_name = csv_name + '.csv'
        elif singleoutput == False:
            csv_name = csv_name + '-*.csv'

        full = os.path.join(csv_path, csv_name)

        try:
            data_to_write.to_csv(
                full, single_file=singleoutput, sep=sep, index=False)
        except Exception:
            pass


class DBSQLConnector(object):
    """This class allows manage connections with SQL databases.

    Args:
        source (variable): it defines the type of 
        SQL database manager
        dict_options (dict): this dictionary contains 
        the connection parameters
        query: a query must be passed to create SQL queries
    """

    def __init__(self, source, dict_options, query):
        self.source = source
        self.dict_options = dict_options
        self.query = query

    def create_connection(self):
        """This method allows to create a connection with SQL database.
        Currently, there are three managers: MySQL, MSSQL, and PostgreSQL.

        Returns:
            cursor: connector where the connection has been performed
        """
        if self.source == 'mssql':
            DRIVER_ = 'ODBC Driver 18 for SQL Server'
            flag_connector = True
        elif self.source == 'postgresql':
            DRIVER_ = 'PostgreSQL Unicode'
            flag_connector = True
        else:
            DRIVER_ = 'MySQL ODBC 8.0 ANSI Driver'
            flag_connector = False
        if flag_connector:
            server = self.dict_options.get(
                'host', None) + str(',') + str(self.dict_options.get('port', None),)
            connector = pyodbc.connect(
                DRIVER=DRIVER_,
                SERVER=server,
                DATABASE=self.dict_options.get('database', None),
                UID=self.dict_options.get('user', None),
                PWD=self.dict_options.get('password', None),
                TrustServerCertificate='yes',
                timeout=1,
            )
        else:
            connector = mysql.connector.connect(
                user=self.dict_options.get('user', None),
                password=self.dict_options.get('password', ''),
                host=self.dict_options.get('host', None),
                database=self.dict_options.get('database', None),
                connection_timeout=60,
                port=self.dict_options.get('port', None))
        return connector

    def get_db_names(self):
        """This method allows to get the available databases after connection.

        Returns:
            cursor: it contains a pyodbc element with the available databases
        """
        db_names_query = """SELECT DISTINCT TABLE_CATALOG
                            FROM INFORMATION_SCHEMA.TABLES"""
        df_db_names = self.create_connection().execute(db_names_query)
        return df_db_names

    def get_tbl_names(self, cursor):
        """This method allows to get all the table names.

        Args: 
            cursor (variable): pyodbc cursor with the database connection.

        Returns:
            list_table_names (list): it contains a list with the table names

        """
        if 'public' in self.get_table_schema(cursor):
            table_names_query_public = """SELECT DISTINCT TABLE_NAME 
                                        FROM INFORMATION_SCHEMA.COLUMNS
                                        WHERE TABLE_SCHEMA = 'public'
                                        ORDER BY TABLE_NAME """
            cursor.execute(table_names_query_public)
        else:
            table_names_query_private = """SELECT DISTINCT TABLE_NAME 
                                        FROM INFORMATION_SCHEMA.COLUMNS
                                        ORDER BY TABLE_NAME """
            cursor.execute(table_names_query_private)
        table_names_output = cursor.fetchall()
        list_table_names = []
        for element in range(0, len(table_names_output)):
            list_table_names.append(table_names_output[element][0])
        return list_table_names

    def get_table_schema(self, cursor):
        """This method allows to get all the table schemas from database.

        Args: 
            cursor (variable): pyodbc cursor with the database connection.

        Returns:
            list_table_names (list): it contains a list with the table schemas.

        """
        schema_query = """SELECT distinct table_schema 
                          FROM INFORMATION_SCHEMA.columns
                          ORDER BY table_schema """
        cursor.execute(schema_query)
        table_schemas_output = cursor.fetchall()
        list_table_schemas = []
        for element in range(0, len(table_schemas_output)):
            list_table_schemas.append(table_schemas_output[element][0])
        return list_table_schemas

    def get_column_names(self, cursor, table):
        """This method allows to get all the column names from database.

        Args: 
            cursor (variable): pyodbc cursor with the database connection.
            table (str): it contains the name of the table in order to get its columns.

        Returns:
            list_column_names (list): it contains a list with the column names for a specific table.

        """
        column_names_query = f"""SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS 
                                 WHERE TABLE_NAME = '{table}'                                         
                                 ORDER BY COLUMN_NAME """
        cursor.execute(column_names_query)
        column_names_output = cursor.fetchall()
        list_column_names = []
        for element in range(0, len(column_names_output)):
            list_column_names.append(column_names_output[element][0])
        return list_column_names

    def get_raw_query(self, x, y, table, cursor):
        """This method allows to get the queries in order to extract data from database.

        Args: 
            x (list): contains the name elements to be searched for the 'X' set
            y (list): contains the name elements to be searched for the 'Y' set
            table (str): it contains the name of the table in order to get its columns.
            cursor (variable): pyodbc cursor with the database connection.

        Returns:
            The output of this method contains two variables where each one
            contain a specific query to be performed.

        """
        if 'all' in x and 'none' in y:
            x_query = f"""SELECT * FROM {table}"""
            y_query = None
        elif 'all' in x and 'none' not in y:
            x_query = f"""SELECT * FROM {table}"""
            y_query = f"""SELECT {', '.join(str(column) for column in y)} FROM {table}"""
        elif 'all' not in x and 'none' in y:
            x_query = f"""SELECT {', '.join(str(column) for column in x)} FROM {table}"""
            y_query = None
        else:
            x_query = f"""SELECT {', '.join(str(column) for column in x)} FROM {table}"""
            y_query = f"""SELECT {', '.join(str(column) for column in y)} FROM {table}"""

        return x_query, y_query

    def search_query(self, cursor, query_int):
        """This method allows to search the queries that previously were defined.

        Args:             
            cursor (variable): pyodbc cursor with the database connection.
            query_int: contain the specific query to be searched.

        Returns:
            query_result: it is a pyodbc element where the search has been achieved.

        """
        if query_int is None:
            cursor = None
        else:
            cursor.execute(query_int)
        return cursor

    def search_advanced_query(self, cursor, query_int):
        """This method allows to perform more advanced queries.

        Args:             
            cursor (variable): pyodbc cursor with the database connection.
            query_int: contain the specific query to be searched.

        Returns:
            query_result: it contains three elements (list with column names, 
            dictionary with the type of each column, and finally a pyodbc element with
            the entire search).

        """
        if query_int is None:
            query_result = None
        else:
            list_names = []
            dict_type = {}
            cursor.execute(query_int)
            for result in cursor.description:
                list_names.append(result[0])
                if self.source == 'mysql':
                    dict_type[result[0]] = FieldType.get_info(
                        result[1]).lower()
                else:
                    dict_type[result[0]] = result[1].__name__
            query_result = list_names, dict_type, cursor
        return query_result

    def query_output(self, cursor, columns, columns_type):
        """This method allows to get the data after the queries.

        Args:             
            output: pyodbc element with the query.
            columns (list): it contains the columns names.

        Returns:
            dataframe: it is a dask dataframe with all the data.

        """
        if columns[0] == 'none':
            dataframe = None
            return dataframe
        else:
            row = ""
            list_data = []
            dataframe = None
            cont = 0
            dask_list = dda.from_array([])
            while row is not None:
                if (len(list_data) == 100000):
                    df = pd.DataFrame.from_records(list_data, columns=columns)
                    if dataframe is None:
                        dataframe = dd.from_pandas(df, npartitions=100)
                        dataframe = dataframe.repartition(
                            partition_size='100MB')  # MB
                    else:
                        dataframe = dd.concat(
                            [dataframe, dd.from_pandas(df, npartitions=100)])
                        dataframe = dataframe.repartition(
                            partition_size='100MB')  # MB}
                    list_data = []
                    df = pd.DataFrame.from_records(list_data, columns=columns)
                    cont += 1

                row = cursor.fetchone()
                if row is not None:
                    list_data.append(row)
                    cont += 1

            df = pd.DataFrame.from_records(list_data, columns=columns)
            if dataframe is None:
                dataframe = dd.from_pandas(df, npartitions=1)
            else:
                dataframe = dd.concat(
                    [dataframe, dd.from_pandas(df, npartitions=1)])
            var_final_types = self.dict_type_creator(columns_type, columns)
            try:
                final_var_dict = dict()
                for key, value in var_final_types.items():
                    if key in columns:
                        if value.startswith('float32'):
                            final_var_dict[key] = np.float32
                        elif value.startswith('float64'):
                            final_var_dict[key] = np.float64
                        else:
                            final_var_dict[key] = value
                dataframe = dataframe.astype(final_var_dict)
            except Exception as err:
                logger.info(
                    f'There is an exception while the change of data type was performed: {err}')
            try:
                dataframe = dataframe.repartition(partition_size='500MB')  # MB
            except Exception as err:
                logger.info(
                    f'There is an exception while the dataframe repartition was performed: {err}', err)
                dataframe = None
            return dataframe

    def get_sets_dataframes(self, raw_df, x_names, y_names):
        """This method allows to split a dask dataframe.

        Args:             
            raw_df (dask dataframe): raw dataframe with the entire data.
            x_names (list): contains the column names for the 'X' set.
            y_names (list): contains the column names for the 'Y' set.

        Returns:
            dataframes: the output is formed by two dask dataframes where each one 
            corresponds for the 'X' and 'Y' sets.

        """
        if raw_df is not None:
            if 'all' in x_names and 'none' in y_names:
                x_df = raw_df
                y_df = None
            elif 'all' in x_names and 'none' not in y_names:
                x_df = raw_df
                y_df = raw_df[y_names]
            elif 'all' not in x_names and 'none' in y_names:
                x_df = raw_df[x_names]
                y_df = None
            else:
                x_df = raw_df[x_names]
                y_df = raw_df[y_names]
        else:
            x_df, y_df = None, None
        return x_df, y_df

    def get_type_raw_columns(self, cursor, table):
        """This method allows to get the type of a complete set of columns.

        Args:             
            cursor (variable): pyodbc cursor with the database connection.
            table (str): it contains the name of the table in order to get its columns.            

        Returns:
            dict_table_names (dict): it contains a dictionary where the keys 
            are the column name and the value is the column type.

        """
        type_columns_query = f"""SELECT COLUMN_NAME, DATA_TYPE 
                                 FROM INFORMATION_SCHEMA.COLUMNS
                                 WHERE TABLE_NAME = '{table}'
                                 ORDER BY TABLE_NAME """
        cursor.execute(type_columns_query)
        table_names_output = cursor.fetchall()
        dict_table_names = {}
        for element in range(0, len(table_names_output)):
            dict_table_names[table_names_output[element]
                             [0]] = table_names_output[element][1]
        return dict_table_names

    def get_type_set_columns(self, set, dict_):
        """This method allows to get the type of a set of columns.

        Args:             
            set (list): contains the columns name of a set.
            dict_ (dict): contains the column and type names where they are 
            the key and value respectively.

        Returns:
            list_data_type (list): contains the column type for a specific type

        """
        if set[0] == "none":
            list_data_type = None
            return list_data_type
        else:
            list_data_type = []
            for column in set:
                list_data_type.append(dict_[column])
            return list_data_type

    def sql_type_conversor(self, list_sql_types, type_source):
        if list_sql_types is not None:
            list_sql_types_changed = []
            data_conversor_dict = sql_type_mapping(type_source)
            for list_sql_type in list_sql_types:
                if list_sql_type in data_conversor_dict:
                    list_sql_types_changed.append(
                        data_conversor_dict[list_sql_type])
                else:
                    list_sql_types_changed.append(list_sql_type)
        else:
            list_sql_types_changed = None
        return list_sql_types_changed

    def sql_type_conversor_dict(self, dict_type, type_source):
        data_conversor_dict = sql_type_mapping(type_source)
        for key, value in dict_type.items():
            if value in data_conversor_dict:
                dict_type[key] = data_conversor_dict[value]
            else:
                dict_type[key] = value
        return dict_type

    def dict_type_creator(self, column_types, column_names):
        if type(column_types) == dict:
            opt_column_types = []
            for key, value in column_types.items():
                opt_column_types.append(value)
            column_types = opt_column_types
        final_dict_type = dict()
        for column_iter in range(0, len(column_names)):
            final_dict_type[column_names[column_iter]
                            ] = column_types[column_iter]
        return final_dict_type
