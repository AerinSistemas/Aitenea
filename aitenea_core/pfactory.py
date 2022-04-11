# -*- coding:utf-8 -*-
'''
  @ Author:Aerin Sistemas <correo_para_estas_cosas@aerin.es
  @ Create Time:  2020-12-25 13:10:47
  @ Project: AITENEA
  @ Description: 
  @ License: MIT License
 '''


import importlib
import inspect

from sklearn.pipeline import Pipeline, FeatureUnion, make_pipeline

from aitenea.exceptions.exceptions import NotClassError
from aitenea.logsconf.log_conf import logging_config

import logging
from logging.config import dictConfig

loggtype = 'CONSOLE'

dictConfig(logging_config)
logger = logging.getLogger(loggtype)


class PFactory(object):
    def __init__(self):
        """Class constructor
        """
        self.steps = []

    def add_pipe(self, class_name, class_group, options, genetic_parameters=None, class_module = None):
        """Add steep to pipe, this can be a transformation or an machine learning (ML) algorithm

        Args:
            class_name (str): Name of the class

            class_group (str): Class type, tranform or machine learning
            
            options (dict): Dictionary with class options

        Raises:
            NotClassError: Launches error message if class does not exist
        """
        try:
            module = importlib.import_module(class_module)
        except Exception as err:
            msg_error = str(err)
            raise NotClassError(msg_error)
        else:
            class_ = getattr(module, class_name)
            instance = None
            if genetic_parameters == None:
                instance = class_(options)
            else:
                instance = class_(options, genetic_parameters)
            logger.info("Add new step to pipeline: %s:%s", class_name, options)
            if len(self.steps) == 0:
                class_name =  class_name + '_' + '0'
            else:
                for step in self.steps:
                    if class_name in step[0]:
                        name_cont = step[0].split('_')
                        name_cont[1] = str(int(name_cont[1])  + 1)
                        class_name = name_cont[0] + '_' + name_cont[1]
                    else:
                        class_name =  class_name + '_' + '0'
            self.steps.append((class_name, instance))
    
    def add_external_pipe(self, class_name, options, external_type = "transform"):
        """
        This method adds external step (tasks) to pipeline. This task, which may be transformations or 
        ml models, are externally inherited from dask-ml. 

        Args:
            class_name (str): Class name (In these moment only dask_ml class)

            options (dict): Dictionary with options 
            
            external_type (str, optional): External type. Defaults to "transform".

        Raises:
            NotClassError: Te module/class does not exist
        """
        if external_type == "transform":
            module_name = "dask_ml.preprocessing"
        else:
            pass
        try:
            module = importlib.import_module(module_name)
        except Exception as err:
            msg_error = str(err)
            raise NotClassError(msg_error)
        else:
            class_ = getattr(module, class_name)
            params = inspect.signature(class_).parameters
            if options is None:
                instance = class_()
            else:
                options_dictionary = dict()
                for param_key, param in params.items():
                    try:
                        op = options[param.name]
                    except KeyError:
                        op = param.default
                    options_dictionary[param_key] = op
                instance = class_(**options_dictionary)
            logger.info("Add new external step to pipeline: %s:%s", class_name, options_dictionary)
        if len(self.steps) == 0:
                class_name =  class_name + '_' + '0'
        else:
            for step in self.steps:
                if class_name in step[0]:
                    name_cont = step[0].split('_')
                    name_cont[1] = str(int(name_cont[1])  + 1)
                    class_name = name_cont[0] + '_' + name_cont[1]
                else:
                    class_name =  class_name + '_' + '0'
        self.steps.append((class_name, instance))


    def compose_pipe_line(self, job_list):
        """Compose the pipeline, add the desired steps(tasks)

        Args:
            job_list (list): List of steps
        """         
        for job in job_list:
            job_type = job["type"]
            job_name = job["name"]
            job_module = job["module_name"]
            options = job["options"]
            genetic_parameters = job["genetic_parameters"]
            self.add_pipe(job_name, job_type, options, genetic_parameters, job_module)
    
    def make_pipe(self):
        """Creates the pipeline itself, establishing the main attributes. 

        Returns:
            [Pipeline]: The pipeline
        """
        return Pipeline(self.steps)
    
    def get_input(self, pos = 'end'):
        """Gets X and y from pipeline step
        Args:
            pos (str or int, optional): Position. Defaults to 'end'.

        Returns:
            [dask dataframe]: X and y dask dataframe
        """
        if isinstance(pos, int):
            return self.steps[pos][1].x_input, self.steps[pos][1].y_input 
        else:
            if pos == 'end':
                pos = -1
            else:
                pos = 0
            return self.steps[pos][1].x_input, self.steps[pos][1].y_input 