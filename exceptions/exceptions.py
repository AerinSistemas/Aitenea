# -*- coding:utf-8 -*-
'''
  @ Author: Aerin Sistemas <aerin_proyectos@aerin.es>
  @ Create Time: 1970-01-01 01:00:00
  @ Modified time: 2021-10-16 20:24:36
  @ Project: AITENEA-AITea-ElasticTools-Aerastic
  @ Description:
  @ License: MIT License
 '''

from aitenea.logsconf.log_conf import logging_config
import logging
from logging.config import dictConfig

loggtype = 'CONSOLE'

dictConfig(logging_config)
logger = logging.getLogger(loggtype)


class ValidationError(Exception):
    def __init__(self, message):
        self.error = message
        super().__init__(message)

    def __str__(self):
        mssg = 'ValidationError:' + self.error
        return(mssg)


class MoreOneError(Exception):
    def __init__(self, message):
        self.error = message
        super().__init__(message)

    def __str__(self):
        mssg = 'MoreOneError:' + self.error
        return(mssg)


class CastingError(Exception):
    def __init__(self, message):
        self.error = message
        super().__init__(message)

    def __str__(self):
        mssg = 'CastingError:' + self.error
        return(mssg)


class NofreqError(Exception):
    def __init__(self):
        self.error = "The timestamp is not regular, trying out make a approx frequency"
        super().__init__(self.error)

    def __str__(self):
        mssg = 'No frequency: ' + self.error
        return(mssg)


class NotFitError(Exception):
    def __init__(self):
        self.error = "Impossible make a transformation or prediction, the model is not fit"
        super().__init__(self.error)

    def __str__(self):
        mssg = 'No fit: ' + self.error
        return(mssg)


class ModelNotExitError(Exception):
    def __init__(self):
        self.error = "The model not exist"
        super().__init__(self.error)

    def __str__(self):
        mssg = 'No model: ' + self.error
        return(mssg)


class NotClassError(Exception):
    def __init__(self, class_name_error):
        self.error = class_name_error
        super().__init__(self.error)

    def __str__(self):
        mssg = 'Not class error: ' + self.error
        return(mssg)


class PerpetuityError(Exception):
    def __init__(self, type_error=''):
        self.error = type_error
        super().__init__(self.error)
        if self.error == 'No name error':
            msg = self.error + ". The model name is empty. Is not possible save the model"
        elif self.error == 'Pickle error':
            msg = self.error + ". Unpicklable object"
        elif self.error == 'Unpickle error':
            msg = self.error + ". There is a problem unpickling the object"
        else:
            msg = self.error + ". There is a problem unpickling the object"
        logger.error(msg)

    def __str__(self):
        return(self.error)


class NotOutputError(Exception):
    def __init__(self, class_name_error):
        self.error = class_name_error
        super().__init__(self.error)

    def __str__(self):
        mssg = 'Not Output  Error: ' + self.error
        return(mssg)


class NotOptionsClassVisible(Exception):
    def __init__(self, class_name_error):
        self.error = class_name_error + "class has no options in the class attributes, will not be able to use it in the graphical environment"
        super().__init__(self.error)

    def __str__(self):
        mssg = 'Not Options in Class Atributtes Error: ' + self.error
        return(mssg)

class EmptyDataFrameError(Exception):
    """Dataframe empty error. When using an empty dataframe.
    """
    def __init__(self):
        self.error = "Probably trying to operate with an empty dataframe."
        super().__init__(self.error)

    def __str__(self):
        mssg = 'Empty dataframe Error: ' + self.error
        return(mssg)


class NoDaskError(Exception):
    """No dask error.
    """
    def __init__(self):
        self.error = "X or/and y are not a dask"
        super().__init__(self.error)

    def __str__(self):
        mssg = 'Not Dask Error: ' + self.error
        return(mssg)