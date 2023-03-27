# -*- coding:utf-8 -*-
'''
  @ Author: Aerin Sistemas <correo_para_estas_cosas@aerin.es
  @ Create Time: 2020-12-17 20:47:31
  @ Modified time: 2021-11-08 11:13:42
  @ Project: AITENEA
  @ Description:
  @ License: MIT License
    
    0
    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:
    
    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.
    
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
'''

from sklearn.ensemble import RandomForestRegressor
from dask import array

from aitenea.aitenea_core.decorators import fit_decorator
from aitenea.aitenea_core.base_class_ai import BaseClassAI
from aitenea.logsconf.log_conf import logging_config
from aitenea.exceptions.exceptions import NotFitError, NotOutputError


import logging
from logging.config import dictConfig

loggtype = 'CONSOLE'

dictConfig(logging_config)
logger = logging.getLogger(loggtype)


class RandomForestRegress(BaseClassAI):
    """
    Method for linear regression.

    Arguments:
        * BaseClassAI {class} -- base class for construction
        * user_parameters {dictionary} -- Dictionary used by programmer when instantiated the class.

    """
    options = {
        'n_estimators':
            {"type": "int", "range": [1, None, 1],
             "default": 500, "gen": True},
        'max_depth':
            {"type": "int", "range": [0, None, 1],
             "default": 0, "gen": True},
        "min_samples_leaf":
            {"type": "int", "range": [1, None, 1],
             "default": 1, "gen": False},
        "min_samples_split":
            {"type": "int", "range": [1, None, 1],
             "default": 2, "gen": False},
        "max_features":
            {"type": "list", "range": ['auto', 'sqrt', 'log2'],
             "default": 'auto', "gen": False},
    }

    genetic_parameters = {"fitness_functions": {"type": "list", "range": [
        "r2_score"], "default": ["r2_score"]}}

    def __init__(self, user_parameters, user_genetic_parameters=None):
        class_options = {
            'n_estimators':
            {"type": "int", "range": None,
             "default": 500, "gen": True},
            'max_depth':
            {"type": "int", "range": None,
             "default": 0, "gen": True},
            "min_samples_leaf":
            {"type": "int", "range": None,
             "default": 1, "gen": False},
            "min_samples_split":
            {"type": "int", "range": None,
             "default": 2, "gen": False},
            "max_features":
            {"type": "list", "range": ['auto', 'sqrt', 'log2'],
             "default": 'auto', "gen": False},
        }
        self.class_parameters = {'options': class_options}
        class_genetic_parameters = {"fitness_functions": {
            "type": "list", "range": ["r2_score"], "default": ["r2_score"]}}
        self.class_genetic_parameters = {"options": class_genetic_parameters}
        super(
            RandomForestRegress, self).__init__(
            self.__class__.__name__, self.class_parameters, user_parameters,
            self.class_genetic_parameters, user_genetic_parameters)
        self.mind = None

    def get_info(self):
        """Gives information about how to use this class and its parametes 
        Returns:
            [type] -- [description]
        """
        description = """ """
        return description

    def init_selector(self):
        """[summary]
        """
        pass

    def transform(self, X):
        """
           The transform function applies the values of the parameters on the actual 
           data and gives the normalized value. 
           The fit_transform() function performs both in the same step. 

        Arguments:
            X {[type]} -- array to be transformed
        """
        pass

    @fit_decorator    
    def fit(self, X, y=None):
        """
        Build a forest of trees from the training set (X, y).

        Arguments:
            X {[array-like of shape (n_samples, n_features)]} -- The training input samples

        Keyword Arguments:
            y {[type]} -- [description] (default: {None})

        """
        if (y is None):
            raise NotOutputError('You must give "y" value in your fit method')
        logging.info("Init Linear regression fit")
        options = self.parameters_values['options']
        rf_estimators = options['n_estimators']
        rf_depth = options['max_depth']
        if rf_depth == 0:
            rf_depth = None
        rf_max_features = options['max_features']
        rf_min_samples_leaf = options['min_samples_leaf']
        rf_min_samples_split = options['min_samples_split']
        self.mind = RandomForestRegressor(
            n_estimators=rf_estimators, max_depth=rf_depth,
            min_samples_leaf=rf_min_samples_leaf,
            min_samples_split=rf_min_samples_split)
        X = X.compute()
        y = y.compute().astype('float64')
        self.mind.fit(X, y)
        return self

    
    def fit_transform(self, X, y=None):
        """[summary]

        Arguments:
            X {[type]} -- [description]

        Keyword Arguments:
            y {[type]} -- [description] (default: {None})

        Returns:
            [type] -- [description]
        """
        logging.info("Init clustering fit_transform, fit without effect")
        return self.fit_predict(X)

    @fit_decorator
    def fit_predict(self, X, y=None):
        """[summary]

        Arguments:
            X {[type]} -- [description]

        Keyword Arguments:
            y {[type]} -- [description] (default: {None})

        Returns:
            [type] -- [description]
        """
        self.fit(X, y)
        predict = self.mind.predict(X)
        predict = array.from_array(predict, chunks='100MB')
        return predict

    def predict(self, X):
        """The predicted regression target of an input sample is computed as 
        the mean predicted regression targets of the trees in the forest

        Args:
            X ([array-like of shape (n_samples, n_features)]): the input samples

        Raises:
            NotFitError: Error message if predict method is not correctly used

        Returns:
            [array, shape (n_samples,)]: predicted values
        """
        logging.info("Init linear regression predict")
        try:
            predict = self.mind.predict(X)
            predict = array.from_array(predict)
            return predict
        except Exception as err:
            logger.error("Error to predict, %s", err)
            raise NotFitError

    def score(self, X, y):
        """[summary]

        Args:
            X ([type]): [description]
            labels ([type]): [description]

        Returns:
            [type]: [description]
        """
        genetic_options = self.genetic_parameters_values['options']
        fitness_fun = genetic_options["fitness_functions"]
        if fitness_fun == "r2_score":
            return {
                "r2_score": abs(self.mind.score(X, y))}
