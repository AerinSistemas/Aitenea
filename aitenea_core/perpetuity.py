# -*- coding:utf-8 -*-
'''
  @ Author: Aerin Sistemas <aerin_proyectos@aerin.es>
  @ Create Time: 2021-03-07 20:38:11
  @ Modified time: 2021-06-17 15:37:05
  @ Project: AITENEA
  @ Description: Clase encargada de la persistencia de los modelos
  @ License: MIT License
 '''
 
import os
from pathlib import Path
from dotenv import load_dotenv
import pickle

env_path = Path('../')
load_dotenv()

from aitenea.logsconf.log_conf import logging_config
from aitenea.exceptions.exceptions import PerpetuityError

import logging
from logging.config import dictConfig

loggtype = 'CONSOLE'

dictConfig(logging_config)
logger = logging.getLogger(loggtype)


class Perpetuity(object):
    def __init__(self, user):
        PATH = os.getenv("PATH_MODELS")
        self.user_path = PATH + "/" + user
        if os.path.isdir(self.user_path):
          logger.info("The perpetuity user model folder exist ")
        else:
          try:
            os.makedirs(self.user_path)
          except OSError as err:
            logger.error("Creation of the folder failed. %s", err)
          

    def save_model(self, metadata, model):
      try:
        model_name = metadata["info_model"]["model_name"]
      except KeyError:
        raise PerpetuityError("No name error")
      else:
        model_path_name = self.user_path + '/' + model_name + '.ait'
        model_to_save = {"aitenea_model" : model, "metadata": metadata}
        try:
          file_model = open(model_path_name, 'wb')
        except IOError as err:
          logger.error("IOError. %s", err)
        else:
          try:
            pickle.dump(model_to_save, file_model, pickle.HIGHEST_PROTOCOL)
          except pickle.PickleError as err:
            raise PerpetuityError('pickle')
          else:
            logger.info("The model %s was saved", model_name)  
  
    def load_model(self, model_name):
      if not '.ait' in model_name:
        model_name = model_name + '.ait'
      model_path_name = self.user_path + '/' + model_name
      try:
        with open(model_path_name, 'rb') as model_file: 
          model = pickle.load(model_file)
      except pickle.UnpicklingError:
        raise PerpetuityError("Unpickle error")
      else:
        return model["aitenea_model"], model["metadata"]

    def list_models(self):
      files_ait = dict()
      for r, d, f in os.walk(self.user_path):
        for file_name in f:
          if '.ait' in file_name:
            files_ait[file_name] = self.get_metadata(file_name)
      return files_ait

    
    def get_metadata(self, ait_file):
      _, metadata = self.load_model(ait_file)
      return metadata
      

      

          
