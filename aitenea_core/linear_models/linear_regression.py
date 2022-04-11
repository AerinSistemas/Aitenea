# -*- coding:utf-8 -*-
'''
  @ Author: Aerin Sistemas <correo_para_estas_cosas@aerin.es
  @ Create Time: 2020-12-17 20:47:31
  @ Modified time: 2021-11-05 12:51:15
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

from dask_ml.linear_model import LinearRegression

from aitenea.aitenea_core.decorators import fit_decorator
from aitenea.aitenea_core.base_class_ai import BaseClassAI
from aitenea.logsconf.log_conf import logging_config
from aitenea.exceptions.exceptions import NotFitError, NotOutputError


import logging
from logging.config import dictConfig

loggtype = 'CONSOLE'

dictConfig(logging_config)
logger = logging.getLogger(loggtype)


class LRegression(BaseClassAI):
    """
    Method for linear regression.

    Arguments:
        * BaseClassAI {class} -- base class for construction
        * user_parameters {dictionary} -- Dictionary used by programmer when instantiated the class.
                                        
    """
    options = {
            'penalty':
            {"type": "list", "range": ["l1","l2"],
             "default": "l2", "gen": True},
            'tol':
            {"type": "float", "range": [1, 1, 1],
             "default": 0.0001, "gen": False},
            "solver":
            {"type": "list", "range":['admm', 'gradient_descent', 'newton', 'lbfgs', 'proximal_grad'], 
            "default": 'admm', "gen": True}, }

    genetic_parameters = {"fitness_functions": {"type": "list", "range": [
            "r2_score"], "default": ["r2_score"]}}

    def __init__(self, user_parameters, user_genetic_parameters=None):
        class_options = {
            'penalty':
            {"type": "list", "range": ["l1","l2"],
             "default": "l2", "gen": True},
            'tol':
            {"type": "float", "range": [1, 1, 1],
             "default": 0.0001, "gen": False},
            "solver":
            {"type": "list", "range":['admm', 'gradient_descent', 'newton', 'lbfgs', 'proximal_grad'], 
            "default": 'admm', "gen": True}, }
        self.class_parameters = {'options': class_options}
        class_genetic_parameters = {"fitness_functions": {"type": "list", "range": [
            "r2_score"], "default": ["r2_score"]}}
        self.class_genetic_parameters = {"options": class_genetic_parameters}
        super(
            LRegression, self).__init__(
            self.__class__.__name__, self.class_parameters, user_parameters,
            self.class_genetic_parameters, user_genetic_parameters)
        self.mind = None

    def get_info(self):
        """Gives information about how to use this class 
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
        Fit linear model
         
        Arguments:
            X {[{array-like of shape (n_samples, n_features)]} -- Training data

        Keyword Arguments:
            y {[type]} -- [description] (default: {None})

        """
        if (y is None): 
            raise NotOutputError('You must give "y" value in your fit method')
        logging.info("Init Linear regression fit")
        options = self.parameters_values['options']
        lr_penalty = options['penalty']
        lr_tol = options['tol']
        lr_solver = options['solver']
        self.mind = LinearRegression(penalty=lr_penalty, tol=lr_tol, solver=lr_solver)
        self.mind.fit(X.to_dask_array(lengths=True), y.to_dask_array(lengths=True))
        return self

    
    def fit_transform(self, X, y=None):
        """Joins the fit and transform in one step

        Arguments:
            X {[array]} -- [description]

        Keyword Arguments:
            y {[type]} -- [description] (default: {None})

        Returns:
            [type] -- [description]
        """
        pass
        
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
        return self.predict(X)

    def predict(self, X):
        """Predict using the linear model.

        Args:
            X ([array-like of shape (n_samples, n_features)]): samples

        Raises:
            NotFitError: Error message if predict method is not correctly used

        Returns:
            [array, shape (n_samples,)]: predicted values
        """
        logging.info("Init linear regression predict")
        try:
            return self.mind.predict(X.to_dask_array(lengths=True))
        except Exception as err:
            logger.error("Error to predict, %s", err)
            raise NotFitError

    def score(self, X, y):
        """The fitness function to be used in genetic algorithm

        Args:
            X ([type]): [description]
            labels ([type]): [description]

        Returns:
            [type]: [description]
        """
        genetic_options = self.genetic_parameters_values['options']
        fitness_fun = genetic_options["fitness_functions"]
        if fitness_fun == "r2_score":
            return  {
                "r2_score": abs(self.mind.score(X.to_dask_array(lengths=True), y.to_dask_array(lengths=True)))}