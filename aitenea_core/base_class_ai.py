# -*- coding:utf-8 -*-
'''
  @ Author: Aerin Sistemas <correo_para_estas_cosas@aerin.es
  @ Create Time:2020-12-17 19:40:10
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


class BaseClassAI(ABC):
    def __init__(self, name, class_parameters, user_parameters,
                 class_genetic_parameters=None, user_genetic_parameters=None):
        """La finalidad de obligar al programador a construir una clase
           de AI  de una forma determinada usando métodos abstractos. Si los métodos    
           no son implementados dará un error en tiempo de ejecución. La finalidad es poder
           usar estos métodos en una PIPE de scikit pero usando dask. 

        Arguments:
            ABC {Class} -- Para poder hacer métodos abstractos
            name {class name} -- Nombre de la clase hija
            class_parameters {dictionary} -- Parámetros de la clase según las necesidades del modelo: 'options': {diccionario de opciones}}
            el diccionario de opciones es como sigue {"nombre_opción": {"type": "int", "range": list/tupla/None, "default": value, "gen": True/False}}
            donde: "range": Una lista representa un conjunto de valores discretos, una tupla debe contener (min, max, resolución), si es None
            se tomara el rango y resolución del tipo. "gen" True si se quiere usar como gen en un algoritmo genético (solo se admiten con range
            diferentes a None)           
            user_parameters {dictionary} -- Diccionario que ha metido el programador cuando ha instanciado la clase
            genetic_values {dictionary} -- Valores para un posible algoritmo genético, si esta vacio se entiende que no participa en el
        """
        self.x_input = None
        self.y_input = None
        self.name = name
        self.parameters_values = dict()
        self.genetic_parameters_values = dict()
        self.check_parameters(
            user_parameters, class_parameters, user_genetic_parameters,
            class_genetic_parameters)

    def check_parameters(
            self, user_parameters, class_parameters, user_genetic_parameters,
            class_genetic_parameters):
        """
        This method checks if the dictionary introduced by the user contains the options imposed by the 
        programmer.

        Raises:
            ValidationError: Launches an error message if: user_parameters and class parameters are not in 
            a dictionary, if 'options' field is missing
        """
        
        if not isinstance(user_parameters, dict):
            raise ValidationError('The parameters are not a dictionary')
        elif not 'options' in user_parameters.keys():
            raise ValidationError('Missing options field')
        else:
            user_keys = user_parameters["options"].keys()
            class_keys = class_parameters["options"].keys()
            if not len(class_keys) == len(set(user_keys) & set(class_keys)):
                msg = 'The parameters dictionary is not valid ' + \
                    str(user_keys) + 'Vs' + str(class_keys)
                raise ValidationError(msg)
            self.parameters_values = user_parameters
        if class_genetic_parameters is not None and user_genetic_parameters is not None:
            if not isinstance(user_genetic_parameters, dict):
                raise ValidationError(
                    'The genetic parameters are not a dictionary')
            elif not 'options' in user_genetic_parameters.keys():
                raise ValidationError(
                    'Missing options field in genetic values')
            else:
                genetic_user_keys = user_genetic_parameters["options"].keys()
                genetic_class_keys = class_genetic_parameters["options"].keys()
            if not len(genetic_class_keys) == len(
                    set(genetic_user_keys) & set(genetic_class_keys)):
                msg = 'The genetic parameters dictionary is not valid ' + \
                    str(genetic_user_keys) + 'Vs' + str(genetic_class_keys)
                raise ValidationError(msg)
            self.genetic_parameters_values = user_genetic_parameters

    @abstractmethod
    def get_info(self):
        """
        Gives information about how to use this class and its parametes 
        """
        pass

    
    @abstractmethod
    def fit(self, X, y = None):
        """
        The *fit()* method takes the training data as arguments, which can be one array in the case of 
        unsupervised learning, or two arrays in the case of supervised learning, and fits the model. 
        In our AItenea class the model in the fit method can be as simple as solving a given equation 
        or as complicated as a machine learning model.  
        """
        pass
    

    @abstractmethod
    def fit_predict(self, X, y):
        pass


    @abstractmethod
    def predict(self, X):
        """
        Makes prediction of the model on new data, once applied *fit* 
        
        Args:
            X (array): Data on which prediction is made
        """
        pass

    @abstractmethod
    def fit_predict(self):
        """
        Performs *fit* and *predict* methods in the same step
        """
        pass

    @abstractmethod
    def score(self):
        """
        The evaluation function for the genetic algorithm 

        """
        pass