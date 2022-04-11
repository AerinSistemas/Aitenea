# -*- coding:utf-8 -*-
'''
  @ Author: Aerin Sistemas <aerin_proyectos@aerin.es>
  @ Create Time: 2021-06-18 15:00:10
  @ Modified time: 2021-10-19 17:56:19
  @ Project: AITENEA
  @ Description: AItenea tranformation. Markov matrix probability calculate.
  @ License: MIT License
 '''

from datetime import date
import pandas as pd
import numpy as np
import dask as da

from aitenea.aitenea_core.base_class_preprocessing import BaseClassPreprocessing
from aitenea.aitenea_core.decorators import fit_decorator
from aitenea.logsconf.log_conf import logging_config
from aitenea.exceptions.exceptions import EmptyDataFrameError


import logging
from logging.config import dictConfig

loggtype = 'CONSOLE'

dictConfig(logging_config)
logger = logging.getLogger(loggtype)


class MarkovMatrixProb(BaseClassPreprocessing):
    options = {
        "window_size":
            {"type": "int", "range": [1, None, 1],
             "default": 2, "gen": False},
            "datetime_field": {"type": "str", "default": "", "gen": False},
            "main_attribute": {"type": "str", "default": "", "gen": False},
            "future_window": {"type": "int", "range": [1, None, 1], "default": 2, "gen": False}}
    
    genetic_parameters = {"fitness_functions": {
        "type": "list", "range": [""], "default": [""]}}

    def __init__(self, user_parameters, user_genetic_parameters=None):
        class_options = {
            "window_size":
            {"type": "int", "range": [1, None, 1],
             "default": 2, "gen": False},
            "datetime_field": {"type": "str", "default": "", "gen": False},
            "main_attribute": {"type": "str", "default": "", "gen": False},
            "future_window": {"type": "int", "range": [1, None, 1], "gen": False}}
        class_genetic_parameters = {"fitness_functions": {
            "type": "list", "range": [""], "default": [""]}}
        self.class_parameters = {'options': class_options}
        self.class_genetic_parameters = {"options": class_genetic_parameters}
        super(
            MarkovMatrixProb, self).__init__(
            self.__class__.__name__, self.class_parameters, user_parameters)
        self.mind = None
        self.X_copy = None

    def init_selector(self):
        pass

    def get_info(self):
        pass

    @fit_decorator    
    def fit(self, X, y=None):
        if X is None:
            raise EmptyDataFrameError
        self.X_copy = X.copy()
        probability_matrix = None
        logger.info("Init Markov matrix prob fit")
        options = self.parameters_values['options']
        win_size = options["window_size"]
        date_field = options["datetime_field"]
        main_attribute = options["main_attribute"]
        leng = self.X_copy.shape[0].compute()
        ids = np.arange(1, leng + 1)
        partitions = self.X_copy.npartitions
        pandas_count_index = pd.DataFrame(ids, columns=["id_"])
        count_index = da.dataframe.from_pandas(pandas_count_index, npartitions = partitions)
        count_index = count_index.repartition(npartitions=1)
        self.X_copy = self.X_copy.repartition(npartitions=1)
        count_index = count_index.reset_index(drop=True)
        self.X_copy = self.X_copy.reset_index(drop=True)   
        self.X_copy = self.X_copy.assign(id_=count_index.id_)
        count_index = count_index.repartition(npartitions=partitions)
        self.X_copy = self.X_copy.repartition(npartitions=partitions)
        self.X_copy = self.X_copy.assign(id_=count_index.id_)
        try:
            self.X_copy = self.X_copy.set_index(date_field)
        except Exception as err:
            logger.error("Error to set index with attribute %s, %s", date_field, str(err))
            return -1
        min_freq = self._chech_freq(self.X_copy.head(100))
        time_win_size = min_freq*win_size
        for n_part in range(0, partitions):
            npartions = self.X_copy.get_partition(n_part).compute()
            end_id = npartions.tail(1)
            if n_part + 1 < partitions:
                win_partition = self.X_copy.get_partition(n_part + 1)
                win_partition = win_partition.compute()
                init = win_partition.head(1).index.values[0]
                end = init + time_win_size
                win_partition = win_partition[:end]
                npartions = npartions.append(win_partition)
            total_size = npartions.shape[0]
            new_attributes = npartions[main_attribute].unique()
            if probability_matrix is None:
                attributes_size = new_attributes.shape[0]
                probability_matrix = pd.DataFrame(
                    np.zeros((attributes_size, attributes_size)),
                    columns=new_attributes, index=new_attributes)
                attributes = set(new_attributes)
            else:
                add_attributes = set(new_attributes).difference(attributes)
                if len(add_attributes) > 0:
                    for i, one_attribute in enumerate(add_attributes):
                        probability_matrix[one_attribute] = 0
                        new_row = pd.DataFrame(
                            np.zeros((1, len(attributes) + 1)),
                            columns=list(attributes) + [one_attribute],
                            index=[one_attribute])
                        probability_matrix = probability_matrix.append(new_row)
                        attributes = attributes | set([one_attribute])
            while len(npartions.index) > 0:
                first_value = npartions.head(1)
                if len(first_value.index) == 0 or first_value.index.values > end_id.index.values:
                    break
                first_id = first_value["id_"][0]
                firs_attribute = first_value[main_attribute][0]
                first_time = first_value.index[0] + min_freq
                end_time = first_time + time_win_size
                win_npartions = npartions[first_time: end_time]
                freq_wind = win_npartions.groupby([main_attribute])
                for ind in freq_wind.count().index:
                    prob_value = freq_wind.count().at[ind, "id_"]
                    probability_matrix.at[firs_attribute, ind] += prob_value
                npartions = npartions[npartions["id_"] != first_id]
        probability_matrix = probability_matrix.div(
            probability_matrix.sum(axis=1), axis=0)
        probability_matrix = probability_matrix.fillna(0)
        self.mind = da.dataframe.from_pandas(
            probability_matrix, npartitions=partitions)
        return self

    @fit_decorator 
    def fit_transform(self, X, y=None):
        self.fit(X)
        partitions = self.X_copy.npartitions
        X_test = self.X_copy.get_partition(partitions - 1).compute()
        X_test, end_time,  min_freq = self._x_prob(X_test)
        return self._transform(X_test, end_time, min_freq)

    def transform(self, X, y=None):
        options = self.parameters_values['options']
        date_field = options["datetime_field"]
        if X is None:
            raise EmptyDataFrameError
        try:
            X = X.set_index(date_field)
        except Exception as err:
            logger.error("Error to set index with attribute %s, %s", date_field, str(err))
            return -1
        X = X.compute()
        leng = len(X)
        X["id_"] = np.arange(1, leng + 1)
        X,  end_time, min_freq = self._x_prob(X)
        return self._transform(X, end_time, min_freq)

    def _chech_freq(self, date_serie):
        time_serie = date_serie.index.values[1:]
        date_serie = date_serie.index.values[0:-1]
        deltas = time_serie - date_serie
        zero_time = np.timedelta64(0)
        deltas = [t for t in deltas if t > zero_time]
        return min(deltas)

    def _x_prob(self, X):
        options = self.parameters_values['options']
        win_size = options["window_size"]
        date_field = options["datetime_field"]
        main_attribute = options["main_attribute"]
        min_freq = self._chech_freq(X.head(100))
        time_win_size = min_freq*win_size
        end_time = X.index[-1]
        init_time = end_time - time_win_size
        X = X[init_time: end_time]
        freq_test = X.groupby([main_attribute]).count()
        columns = self.mind.columns
        freq_test_index = freq_test.index
        x_array = []
        for column in columns:
            if column in freq_test_index:
                x_array.append(
                    freq_test[freq_test.index == column]["id_"].values[0])
            else:
                x_array.append(0)
        try:
            x_array = x_array/sum(x_array)
        except Exception as err:
            logger.error("{}".format(err))
        return da.array.from_array(x_array), end_time, min_freq

    def _transform(self, x_prob, end_time, min_freq):
        prediction_time = []
        options = self.parameters_values['options']
        win_size = options["window_size"]
        prediction_matrix = []
        pow_matrix = self.mind.to_dask_array(lengths=True)
        columns = self.mind.index.compute()
        for pow in range(0, win_size):
            prediction_time.append(end_time + (pow + 1)*min_freq)
            prediction_matrix.append(da.array.dot(x_prob, pow_matrix))
            pow_matrix = da.array.dot(
                self.mind.to_dask_array(lengths=True),
                pow_matrix)
        prediction_matrix = da.array.stack(prediction_matrix)
        prediction_matrix = pd.DataFrame(
            prediction_matrix.compute(),
            columns=columns, index=prediction_time)
        prediction_matrix["date"] = prediction_time
        return da.dataframe.from_pandas(prediction_matrix, npartitions=1) 
    

