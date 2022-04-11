# -*- coding:utf-8 -*-
'''
  @ Author: Aerin Sistemas <correo_para_estas_cosas@aerin.es
  @ Create Time: 2020-12-17 20:47:31
  @ Modified time: 2022-01-11 18:24:33
  @ Project: AITENEA
  @ Description:
  @ License: MIT License
    
    0
    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Softwarcalculate_optima_nclasses
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
'''

from dask_ml.cluster import KMeans
from sklearn.metrics import calinski_harabasz_score

from aitenea.aitenea_core.base_class_ai import BaseClassAI
from aitenea.logsconf.log_conf import logging_config
from aitenea.exceptions.exceptions import NotFitError
from aitenea.aitenea_core.decorators import fit_decorator


import logging
from logging.config import dictConfig

loggtype = 'CONSOLE'

dictConfig(logging_config)
logger = logging.getLogger(loggtype)

class Kmeans(BaseClassAI):
    options = {
            'num_cluster':
            {"type": "int", "range": [1, 1, 1],
             "default": 2, "gen": True},
            'method':
            {"type": "list", "range": ["k-means||", "k-means++"],
             "default": "k-means++", "gen": True},
            "auto_optimal_cluster":
            {"type": "bool", "range": None, "default": False, "gen": False}, }

    genetic_parameters = {"fitness_functions": {"type": "list", "range": [
            "calinski-harabasz"], "default": ["calinski-harabasz"]}}
    
    def __init__(self, user_parameters, user_genetic_parameters=None):
        """[summary]

        Arguments:
            BaseClassAI {[type]} -- [description]
            user_parameters {[type]} -- [description]
        """
        class_options = {
            'num_cluster':
            {"type": "int", "range": [1, None, 1],
             "default": 2, "gen": True},
            'method':
            {"type": "list", "range": ["k-means||", "k-means++"],
             "default": "k-means--", "gen": True},
            "auto_optimal_cluster":
            {"type": "bool", "range": None, "default": False, "gen": False}, }
        self.class_parameters = {'options': class_options}
        class_genetic_parameters = {"fitness_functions": {"type": "list", "range": [
            "calinski-harabasz"], "default": ["calinski-harabasz"]}}
        self.class_genetic_parameters = {"options": class_genetic_parameters}
        super(
            Kmeans, self).__init__(
            self.__class__.__name__, self.class_parameters, user_parameters,
            self.class_genetic_parameters, user_genetic_parameters)
        self.mind = None

    def get_info(self):
        """[summary]
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
        """[summary]

        Arguments:
            X {[type]} -- [description]
        """
        pass
    
    @fit_decorator
    def fit(self, X, y=None):
        """[summary]

        Arguments:
            X {[type]} -- [description]

        Keyword Arguments:
            y {[type]} -- [description] (default: {None})

        Returns:
            [type] -- [description]
        """
        logging.info("Init clustering fit")
        options = self.parameters_values['options']
        automatic = options['auto_optimal_cluster']
        method = options['method']
        num_cluster = options['num_cluster']
        if automatic:
            if num_cluster <= 2:
                num_cluster = 2
            else:
                num_cluster = self.calculate_optima_nclasses(
                    X, method, num_cluster)
        logger.info("Start K-Means clustering for %s class", num_cluster)
        self.mind = KMeans(n_clusters=num_cluster,
                           init=method, random_state=0)
        self.mind.fit(X)
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
        self.fit(X)
        return self.mind.predict(X)
        

    def fit_predict(self, X, y=None):
        """[summary]

        Arguments:
            X {[type]} -- [description]

        Keyword Arguments:
            y {[type]} -- [description] (default: {None})

        Returns:
            [type] -- [description]
        """
        logging.info("Init clustering fit_transform, fit without effect")
        return self.fit_transform(X)
    
    def predict(self, X):
        logging.info("Init clustering predict")
        try:
            return self.mind.predict(X)
        except Exception as err:
            logger.error("Error to fit transform, %s", err)
            raise NotFitError

    def score(self, X, y = None):
        """[summary]

        Args:
            X ([type]): [description]
            labels ([type]): [description]

        Returns:
            [type]: [description]
        """
        genetic_options = self.genetic_parameters_values['options']
        fitness_fun = genetic_options["fitness_functions"]
        labels = self.predict(X)
        if fitness_fun == "calinski-harabasz":
            return { 
                "calinski_harabasz_score": calinski_harabasz_score(X, labels)}

    def calculate_optima_nclasses(
            self, dataframe, method, max_class, tolerance=0.2):
        """[summary]

        Arguments:
            dataframe {[type]} -- [description]
            method {[type]} -- [description]
            max_class {[type]} -- [description]

        Keyword Arguments:
            tolerance {float} -- [description] (default: {0.2})

        Returns:
            [type] -- [description]
        """
        wcss = []
        slope = []
        for i in range(1, max_class):
            brain = KMeans(n_clusters=i, init=method,
                           random_state=0)
            brain.fit(dataframe)
            wcss.append(brain.inertia_)
        for n in range(0, len(wcss)-1):
            slope.append(wcss[n]-wcss[n+1])
        min_slope = min(slope)
        position_min = slope.index(min_slope)
        for n in range(position_min-1, -1, -1):
            if abs(slope[n] - min_slope) < min_slope*tolerance:
                return n
        return position_min
