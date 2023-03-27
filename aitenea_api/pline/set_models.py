# -*- coding:utf-8 -*-
'''
  @ Author: Aerin Sistemas <aerin_proyectos@aerin.es>
  @ Create Time: 2021-03-16 12:05:47
  @ Modified time: 2021-07-05 16:17:39
  @ Project: AITENEA-AITea-ElasticTools-Aerastic
  @ Description: Acrivo que adquiere todas las clases que pueden usarse en aitenea
  @ License: MIT License
 '''

import os
import importlib
import inspect
import json

from django.core.exceptions import ObjectDoesNotExist

from exceptions.exceptions import NotOptionsClassVisible
from logsconf.log_conf import logging_config
import logging
from logging.config import dictConfig

loggtype = 'CONSOLE'

dictConfig(logging_config)
logger = logging.getLogger(loggtype)


class_types_dict = {"BaseClassAI": "aitenea_ai",
                    "BaseClassPreprocessing": "aitenea_transform"}


def get_module(line, class_file):
    """Read an AItenea class and return the class name and the class info

    Args:
        line (str): File line
        class_file (str): Class file name

    Returns:
        [tupe]: class name, class info (module and type)
    """
    line = line.replace("):", "")
    line = line.replace("(", " ")
    line = line.split(' ')
    class_name = line[1]
    class_type = line[2]
    class_type = class_type.replace("\n", "")
    class_module = class_file[0].replace("..", "")
    class_module = class_module.replace("/", ".")
    class_module = class_module.replace(class_file[1], "")
    # Como se cambia la ruta surge un error que no crea bien 
    # el class_info por lo que si tiene 2 puntos hay que quitarle uno
    # asi no surge el error.
    if class_module[1] == ".":
        class_module = class_module[1:]
    class_file = class_file[1].replace(".py", "")
    class_info = {"class_module": "aitenea" + class_module + class_file}
    class_info["class_type"] = class_types_dict[class_type]
    return class_name, class_info


# def get_aitenea(model, path_core="../aitenea_core/"):
#./aitenea_core para production
#../aitenea_core para devel
def get_aitenea(model, path_core="../aitenea_core"):
    """Get all info to save in database AItenea class

    Args:
        model (model): Django model (AiteneaClass)
        path_core (str, optional): Aitenea core path. Defaults to "../aitenea_core/".
    """
    info_class_dict = dict()
    # Recoge la ruta de path_core y verifica si existe el directorio.
    # En el caso de que exista mantiene la path_core en el caso de que no la cambia por ./aitenea_core
    if os.path.isdir(path_core):
        dirs = [folder.path for folder in os.scandir(path_core) if (
            folder.is_dir() and folder.name[0] != "_" and not "test" in folder.name)]
    else:
        path_core = "./aitenea_core"
        dirs = [folder.path for folder in os.scandir(path_core) if (
            folder.is_dir() and folder.name[0] != "_" and not "test" in folder.name)]
    files = []
    for dir_path in dirs:

        files += [[file_name.path, file_name.name]
                  for file_name in os.scandir(dir_path)
                  if(
            file_name.is_file() and file_name.name[0] !=
            "_" and not "test" in file_name.name)]
    for class_file in files:
        with open(class_file[0], 'r') as file_class:
            for line in file_class:
                if line[0:5] == 'class':
                    class_name, class_info = get_module(line, class_file)
                    info_class_dict[class_name] = class_info
                    break
    info_class_dict = get_options(info_class_dict)
    save_model(info_class_dict, model)


def get_options(info_class_dict):
    """Acquire the class options

    Args:
        info_class_dict (dict): Info class dict

    Returns:
        [type]: Info class dict with options
    """
    for key, values in info_class_dict.items():
        module = importlib.import_module(values["class_module"])
        class_ = getattr(module, key)
        options = None
        genetic_parameters = None
        try:
            options = class_.__dict__["options"]
            if hasattr(class_, 'genetic_parameters'):
                genetic_parameters = class_.__dict__["genetic_parameters"]
        except KeyError:
            options = None
            logger.warning(
                "%s class has no options in the class attributes, will not be able to use it in the graphical environment",
                key)
            # raise NotOptionsClassVisible(key) Decidir si es error o no
        finally:
            class_info = info_class_dict[key]
            class_info["html_options"] = generate_html(options)
            class_info["options"] = options
            class_info["html_genetic_parameters"] = generate_html(genetic_parameters)
            class_info["genetic_parameters"] = genetic_parameters
            info_class_dict[key] = class_info
    return info_class_dict


def save_model(info_class_dict, model):
    """Save model

    Args:
        info_class_dict (dict): Info class dictionary
        model (model): Django model (AiteneaClass)
    """
    for key, value in info_class_dict.items():
        try:
            one_class = model.objects.get(class_name=key)
        except ObjectDoesNotExist:
            logger.debug("New class, add to aitenea class database")
            class_name = key
            class_type = value["class_type"]
            module_name = value["class_module"]
            options = value["options"]
            html_options = json.dumps(value["html_options"])
            genetic_parameters = value["genetic_parameters"]
            html_genetic_parameters = json.dumps(value["html_genetic_parameters"])
            data = model(
                class_name=class_name, type=class_type,
                module_name=module_name, options=options,
                html_options=html_options, genetic_parameters=genetic_parameters,
                html_genetic_parameters=html_genetic_parameters)
            data.save()
        else:
            old = one_class.options
            if old is None and value["options"] is None:
                continue
            else:
                one_class.options = value["options"]
                one_class.html_options = json.dumps(value["html_options"])
                one_class.genetic_parameters = value["genetic_parameters"]
                one_class.html_genetic_parameters = json.dumps(value["html_genetic_parameters"])
                one_class.save()
                logger.debug("Change %s options, update info", key)


def generate_html(options):
    """Generate html options label

    Args:
        model (model):  Info class dictionary

    Returns:
        [dict]: Dictionary with class and html options labels
    """
    html_list = []
    if not options == None:
        for key, value in options.items():
            html_list.append(convert_to_html(key, value))
    return html_list


def convert_to_html(key, value):
    """Convert a type and value to html input

    Args:
        key (str): Option name
        value (dict): Dictionary with type, range and default
    Returns:
        [str]: Html label 
    """
    type_field = value["type"]
    ret = '<label>{0}</label><br>'.format(key)
    if type_field in ['int', 'float']:
        range_values = value["range"]
        step = range_values[1]
        default = value["default"]
        if range_values[0] == range_values[2]:
            ret += '<input id="{0}" type="number" value={1} step={2}>'.format(
                key,
                default,
                step)
            ret += '<br>'
            if value["gen"]:
                ret += '<label>Use in GA:</label>'
                ret += '<input type="checkbox" id="{0}" value="{1}">'.format(
                    key + "_gen", key)
                ret += '<br>'
            return ret
        else:
            min_value = range_values[0]
            max_value = range_values[2]
            ret += '<input id="{0}" type="number" value={1} step={2} min={3} max={4}>'.format(
                key, default, step, min_value, max_value)
            ret += '<br>'
            if value["gen"]:
                ret += '<label>Use in GA:</label>'
                ret += '<input type="checkbox" id="{0}" value="{1}">'.format(
                    key + "_gen", key)
                ret += '<br>'
            return ret
    elif type_field == 'list':
        ret += '<select id="{0}">'.format(key)
        for val in value["range"]:
            selected = ""
            if val == value["default"]:
                selected = "selected"
            op = '<option value="{0}" {1}>{0}</option>'.format(val, selected)
            ret += op
        ret += '</select>'
        ret += '<br>'
        if "gen" in value:
            if value["gen"]:
                ret += '<label>Use in GA:</label>'
                ret += '<input type="checkbox" id="{0}" value="{1}">'.format(
                    key + "_gen", key)
                ret += '<br>'
        return ret
    elif type_field == 'bool':
        ret += '<select id="{0}">'.format(key)
        for val in ["True", "False"]:
            selected = ""
            if str(val) == str(value["default"]):
                selected = "selected"
            op = '<option value="{0}" {1}>{0}</option>'.format(val, selected)
            ret += op
        ret += '</select>'
        ret += '<br>'
        if value["gen"]:
            ret += '<label>Use in GA:</label>'
            ret += '<input type="checkbox" id="{0}" value="{1}">'.format(
                key + "_gen", key)
            ret += '<br>'
        return ret
    elif type_field == 'str':
        ret = '<label>{0}</label><br>'.format(key)
        default = value["default"]
        ret += '<input id="{0}" type="text" value={1} >'.format(key, default)
        ret += '<br>'
        if value["gen"]:
            ret += '<label>Use in GA:</label>'
            ret += '<input type="checkbox" id="{0}" value="{1}">'.format(
                key + "_gen", key)
            ret += '<br>'
        return ret


            
            
