from dask_ml.preprocessing import StandardScaler
import dask 
from aitenea.aitenea_core.base_class_preprocessing import BaseClassPreprocessing
from aitenea.aitenea_core.decorators import fit_decorator
from aitenea.logsconf.log_conf import logging_config
import numpy as np

import logging
from logging.config import dictConfig

loggtype = 'CONSOLE'

dictConfig(logging_config)
logger = logging.getLogger(loggtype)


class StdScaler(BaseClassPreprocessing):
    options = {
        "with_mean":
            {"type": "bool",
             "default": True, "gen": False},
        "with_std":
            {"type": "bool",
             "default": True, "gen": False},
    }

    def __init__(self, user_parameters, user_genetic_parameters=None):
        class_options = {
            "with_mean":
            {"type": "bool",
             "default": True, "gen": False},
            "with_std":
            {"type": "bool",
             "default": True, "gen": False},
        }
        self.class_parameters = {'options': class_options}
        super(
            StdScaler, self).__init__(
            self.__class__.__name__, self.class_parameters, user_parameters)
        self.mind = None
        self.init_selector()
    

    def get_info(self):
        pass

    def init_selector(self):
        options = self.parameters_values['options']
        with_mean = options["with_mean"]
        with_std = options["with_std"]
        self.mind = StandardScaler(with_mean=with_mean, with_std=with_std)

    @fit_decorator
    def fit(self, X, y=None):
        self.init_selector()
        self.mind.fit(X)
        return self

    @fit_decorator
    def fit_transform(self, X, y=None):
        self.fit(X)
        return self.mind.transform(X)
            
    def transform(self, X):
        return self.mind.transform(X)