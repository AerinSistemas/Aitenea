# -*- coding:utf-8 -*-
'''
  @ Author: Aerin Sistemas <correo_para_estas_cosas@aerin.es
  @ Create Time: 2021-02-18 16:57:33
  @ Modified time: 2021-10-16 22:10:04
  @ Project: AITENEA
  @ Description:
  @ License: MIT License
 '''


from abc import ABC, abstractmethod

from aitenea.exceptions.exceptions import ValidationError
from aitenea.logsconf.log_conf import logging_config


import logging
from logging.config import dictConfig

loggtype = 'CONSOLE'

dictConfig(logging_config)
logger = logging.getLogger(loggtype)



class BaseClassPreprocessing(ABC):
    def __init__(self, name, class_parameters, user_parameters):
        """
        This class is responsible for establishing the structure that classes whose functionality is to transform data must implement.

        Args:
            name (str): name of the class
            class_parameters (dict): Dictionary with class parameters
            user_parameters (dict): Dictionary with user parameters
        """
        self.x_input = None
        self.y_input = None
        self.name = name
        self.parameters_values = dict()
        self.check_parameters(user_parameters, class_parameters)

    def check_parameters(self, user_parameters, class_parameters):
        """[summary]

        Args:
            user_parameters (dict): model parameters introduced by the user
            class_parameters (dict): class parameters introduced by programmer

        Raises:
            ValidationError: Launch error message when parameters are not a dictionary

            ValidationError: Launch error when field with class 'options' is missing
            
            ValidationError: Launch error message if parameters dictionary is not valid
        """
        if not isinstance(user_parameters, dict):
            raise ValidationError('The parameters are not a dictionary')
        elif not 'options' in user_parameters.keys():
            raise ValidationError('Missing options field')
        else:
            user_keys = user_parameters["options"].keys()
            class_keys = class_parameters["options"].keys()
            if not len(class_keys) == len(set(user_keys) & set(class_keys)):
                msg = 'The parameters dictionary is not valid ' + str(user_keys) + 'Vs' + str(class_keys)
                raise ValidationError(msg)
            else:    
                self.parameters_values = user_parameters
    

    @abstractmethod
    def get_info(self):
        """
        Gives information about how to use this class and its parametes 
        """
        pass
    
    @abstractmethod
    def init_selector(self):
        """
        This method is used for models that need prior initialization
        """
        pass

    @abstractmethod
    def fit(self):
        """
        Compute a transformation task to be used for later scalling. 
        """
        pass


    @abstractmethod
    def transform(self):
        """
        Parameters generated from *fit()* method, applied upon model to generate transformed data set
        """
        pass

    @abstractmethod
    def fit_transform(self):
        """
        Performs *fit* and *transform* methods in the same step.
        """
        pass


    
    
    
    
    