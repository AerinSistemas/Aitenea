# -*- coding:utf-8 -*-
'''
  @ Author: Aerin Sistemas <correo_para_estas_cosas@aerin.es
  @ Create Time: 2020-12-17 12:14:22
  @ Project: AITENEA
  @ Description: Logs configuration file
  @ License: MIT License
  
    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:
    
    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.
    
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
 
 '''
CLASS_CONST = "logging.StreamHandler"
STREAM_CONST = "ext://sys.stdout"

logging_config = {
    "version": 1,
    "disable_existing_loggers": 0,
    "formatters": {
        "precise": {
            "format": " %(levelname)-8s : %(asctime)s %(filename)s %(module)s  line:%(lineno)d %(message)s"
        },
        "data": {
            "format": "%(levelname)-8s: %(message)s"
        },
        "report": {
            "format": "%(message)s"
        },
        "node": {
            "format": "AITEA-PYTHON %(levelname)-8s: %(message)s"
        },
    },
    "handlers": {
        "debugfile": {
            "class": "logging.FileHandler",
            "formatter": "precise",
            "mode": "a",
            "level": "DEBUG",
            "filename": "debug.log"
        },
        "console": {
            "formatter": "precise",
            "class": CLASS_CONST,
            "stream": STREAM_CONST,
            "level": "DEBUG"
        },
        "data": {
            "formatter": "data",
            "class": CLASS_CONST,
            "stream": STREAM_CONST,
            "level": "INFO",
        },
        "report": {
            "formatter": "report",
            "class": CLASS_CONST,
            "stream": STREAM_CONST,
            "level": "INFO",
        },
        "node": {
            "formatter": "node",
            "class": CLASS_CONST,
            "stream": STREAM_CONST,
            "level": "DEBUG"
        }
    },
    'loggers': {
        'VERBOSE': {
            'handlers': ['console', 'debugfile'],
            'level': 'DEBUG',
            'propagate': True
        },
        'TOFILE': {
            'handlers': ['debugfile'],
            'level': 'DEBUG',
            'propagate': True
        },
        'CONSOLE': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True
        },
        'REPORT': {
            'handlers': ['report'],
            'level': 'DEBUG',
            'propagate': False
        },
        'NODERED': {
            'handlers': ['node'],
            'level': 'DEBUG',
            'propagate': False
        }

    }
}