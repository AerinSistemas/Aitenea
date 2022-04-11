# Utiles para trabajar con datos
import dask.dataframe as dd
import dask.array as dda
import pandas as pd
import numpy as np
import ast

from elastictools.aerastic.elastic_index import ElasticIndex, InsertData
from elastictools.aerastic.elastic_query import ElasticQuery

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
                logger.error(
                    "Error in query {}. match_all will be used".format(err))
                x["query"] = {"match_all": {}}
            x_values = self.options_source["X"]
            y_values = self.options_source["y"]
            count, result = connector.raw_query(
                self.options_source['index'], x)
            if count is None:
                load_values =  0, None, None
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
            count, result = connector.raw_query(self.options_source['index'])

            if count is None:
                load_values =  0, None, None
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

    def handler_output(self, data, pipeline = None, predict_inputs = None, transform = False):
        if data is None:
            msg, out  = "Fit executed, data is None", None
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
            y_input  = y_input.reset_index(drop=True)
            columns = [name+"_output" for name in y_input.columns]
        if data_size[0] == rows_x:
            if len(data_size) == 1:
                data_column = dd.from_dask_array(data, columns=columns[0], index=x_input.index).to_frame()
                x_input[columns[0]] = data_column[columns[0]]
            else:
                for n, column in enumerate(columns):
                    data_column = dd.from_dask_array(data[:, n], columns=column).to_frame()
                    data_column= data_column.repartition(npartitions=x_input.npartitions).reset_index(drop=True)
                    x_input[column] = data_column[column]
            if y_input is not None:
                output = dd.concat([x_input, y_input], axis = 1)
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
    def __init__(self, data, options = None):
        self.data = data
        self.evaluation_dictionary = dict()
    
    def get_evaluation(self):
        counts = self.data[0] 
        dataframe_X = self.data[1]
        dataframe_y = self.data[2]
        self.evaluation_dictionary['total_counts'] = counts
        if counts > 0:
            self.describe(dataframe_X, target = False)
            self.describe(dataframe_y, target = True)
            self.cov(dataframe_X, dataframe_y)
        return self.evaluation_dictionary

    def describe(self, data, target = True):
        if data is not None:
            types_info = dict()
            if target:
                name = 'data type y'
                describe = 'data describe y'
            else:
                name = 'data type X'
                describe = 'data describe X'
            if self.check_empty(data):
                for column, dtype in zip(data.columns, data.dtypes):
                    types_info[column] = str(dtype)
                self.evaluation_dictionary[name] = types_info
                self.evaluation_dictionary[describe] = data.describe().compute().to_json()
    
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
            cov_matrix = all_matrix.corr()
            self.evaluation_dictionary['correlation'] = cov_matrix.compute().to_json()
        else:
            self.evaluation_dictionary['correlation'] = None
    
    def check_empty(self, dataset):
        return len(dataset.columns) > 0 

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
        result = dd.read_csv(csv_path, blocksize=100e6, sep=dialect.delimiter, assume_missing=True) 
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
                    print(e)
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
                    print(e)

        return header_names