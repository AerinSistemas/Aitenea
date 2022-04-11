# -*- coding:utf-8 -*-
'''
  @ Author: Aerin Sistemas <aerin_proyectos@aerin.es>
  @ Create Time: 2021-06-18 15:00:10
  @ Modified time: 2022-01-11 10:29:51
  @ Project: AITENEA
  @ Description: AItenea tranformation. Markov matrix probability calculate.
  @ License: MIT License
 '''

from datetime import date
import pandas as pd
import numpy as np
from dask import dataframe as dd
from aitenea.aitenea_core.base_class_preprocessing import BaseClassPreprocessing
from aitenea.logsconf.log_conf import logging_config
from aitenea.exceptions.exceptions import NotFitError, NotOutputError
from aitenea.aitenea_core.emissions._emission_aux import _EmissionsAux
from aitenea.aitenea_core.decorators import fit_decorator

import logging
from logging.config import dictConfig
loggtype = 'CONSOLE'
dictConfig(logging_config)
logger = logging.getLogger(loggtype)


class Emissions(BaseClassPreprocessing):
    """This class is used for the preprocessing and transformation of emsition data recorded in RDE (real drive emission ) tests.
       Subsequently data will be used in Atenea machine learning models for predictions.
    Args:
        BaseClassPreprocessing : inherits from BaseClassPreprocessing
    """
    options = {
        "carbono":
        {"type": "float", "range": [1, 1, 1], "default": 1.0,  "gen": False},
        "hidrogeno":
        {"type": "float", "range": [1, 1, 1], "default": 1.89,  "gen": False},
        "oxigeno":
        {"type": "float", "range": [1, 1, 1], "default": 0.005,  "gen": False}
    }

    def __init__(self, user_parameters, user_genetic_parameters=None):
        class_options = {
            "carbono":
            {"type": "float", "range": [1, 1, 1], "default": 1.0, "gen": False},
            "hidrogeno":
            {"type": "float", "range": [1, 1, 1], "default": 1.89, "gen": False},
            "oxigeno":
            {"type": "float", "range": [1, 1, 1], "default": 0.005, "gen": False}
        }
        self.class_parameters = {'options': class_options}
        super(Emissions, self).__init__(
            self.__class__.__name__, self.class_parameters, user_parameters
        )
        self.mind = _EmissionsAux()

    def get_info(self):
        description = """
        Aitenea transformation class, for vehicle emission data registered in real drive emission test.
        """
        return description

    def init_selector(self):
        pass
    
    @fit_decorator
    def fit(self, X=None, y=None):
        """Sets transformation's parameters

        Args:
            X (dask dataframe): data to be transformed
        """
        options = self.parameters_values['options']
        a = options["carbono"]
        b = options["hidrogeno"]
        c = options["oxigeno"]
        self.mind.set_parameter(a, b, c)
        return self
        
    @fit_decorator
    def fit_transform(self, X, y=None):
        """Calls fit and transform methods in one step

        Args:
            X (dask dataframe): data to be transformed
        """

        self.fit(X)
        return self.transform(X)

    def transform(self, X):
        """Applies the fitted model on the data

        Args:
            X (dask dataframe: data to be transformed

        Returns:
            [dask dataframe]: the transformed data
        """
        return self.mind.calculate(X.compute())
