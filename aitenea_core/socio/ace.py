from dask_ml.preprocessing import StandardScaler
import dask 
from aitenea.aitenea_core.base_class_preprocessing import BaseClassPreprocessing
from aitenea.aitenea_core.decorators import fit_decorator
from aitenea.logsconf.log_conf import logging_config
from aitenea.aitenea_core.socio.ace_aux import _AceAux
import numpy as np

import logging
from logging.config import dictConfig

loggtype = 'CONSOLE'

dictConfig(logging_config)
logger = logging.getLogger(loggtype)


class Ace(BaseClassPreprocessing):
    options = {}

    def __init__(self, user_parameters, user_genetic_parameters=None):
        class_options = {}
        self.class_parameters = {'options': class_options}
        super(
            Ace, self).__init__(
            self.__class__.__name__, self.class_parameters, user_parameters)
        self.mind = _AceAux()    

    def get_info(self):
        pass

    def init_selector(self):
        pass

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
        self.mind.ace(X)
        return self.mind.calculate(X)