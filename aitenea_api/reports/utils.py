import numpy as np
import redis
import json
import datetime
from .models import PlineReport, PlineReportMetric, PlineStatus
from django.contrib.auth.models import User
from django.forms.models import model_to_dict

import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path('../')
load_dotenv()

from logsconf.log_conf import logging_config

import logging
from logging.config import dictConfig
loggtype = 'CONSOLE'

dictConfig(logging_config)
logger = logging.getLogger(loggtype)


def create_pline_report(pline_json):
    origin_dataset = None
    target_dataset = None
    train_size = None
    parsed_train_size = None
    parsed_test_size = None
    steps = None
    dataset_parameters = None

    pline_report = None

    try:
        if "steps" in pline_json['pline']:
            steps = pline_json['pline']['steps']

        if "origin" in pline_json:
            origin_dataset = pline_json['origin']['options']['index']
            train_size = pline_json['origin']['options']['train_size']
            if "q" in pline_json['origin']['options']:
                dataset_parameters = {
                    "q": pline_json['origin']['options']['q'],
                    "X": pline_json['origin']['options']['X'],
                    "y": pline_json['origin']['options']['y']
                }
            else:
                dataset_parameters = {
                    "X": pline_json['origin']['options']['X'],
                    "y": pline_json['origin']['options']['y']
                }
                
        
        if "target" in pline_json:
            target_dataset = pline_json['target']['options']['index']
        
        if (train_size is not None):
            parsed_train_size = int(train_size * 100)
            parsed_test_size = 100 - int(train_size * 100)

        owner = User.objects.get(pk=pline_json['pline']['owner'])

        pline_report = PlineReport.objects.create(
            pline_name=pline_json['pline']['name'], 
            owner=owner, 
            dataset_parameters=dataset_parameters,
            steps=steps,
            train_dataset_percentage=parsed_train_size, 
            test_dataset_percentage=parsed_test_size, 
            origin_dataset=origin_dataset, 
            target_dataset=target_dataset
        )

    except Exception as err:
        logger.error("Error creating the Pline report.")
        logger.error(err)

    return pline_report


def create_pline_report_metric(pline_report, pline, score):
    try:
        # Almacenar puntuación del fit de la Pline en su algoritmo correspondiente
        for key, value in score.items():
            if isinstance(value, np.floating):
                PlineReportMetric.objects.create(
                    pline_report=pline_report,
                    pline=pline,
                    metric_name=key,
                    score=[value]
                )
            elif isinstance(value, np.ndarray):
                PlineReportMetric.objects.create(
                    pline_report=pline_report,
                    pline=pline,
                    metric_name=key,
                    score=value
                )
    except Exception as err:
        logger.error("Error creating the PlineReport metric.")
        logger.error(err)


def load_plinestatus(id):
    """
    Returns:
        p [aitenea_api.pline.models.PlineStatus]: objeto PlineStatus asociado a la Pline
    """
    pline_status = None
    try:
        pline_status = PlineStatus.objects.filter(pline=id)[0]
    except IndexError:
        pass
    return pline_status


def redis_pub(pline, redis_topic, status, completed, error):
    # connect with redis server
    REDIS_IP = os.getenv("REDIS_IP")
    REDIS_PORT = os.getenv("REDIS_PORT")
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
    conn = redis.Redis(host=REDIS_IP, port=REDIS_PORT, password=REDIS_PASSWORD, db=0)

    last_update = datetime.datetime.now()

    pline_status = load_plinestatus(pline.id)
    if pline_status is not None:
        pline_status.redis_topic = redis_topic
        pline_status.status_info = status
        pline_status.last_update = last_update
        pline_status.completed = completed
        pline_status.error = error
        pline_status.save()
    else:
        pline_status = PlineStatus.objects.create(
            pline=pline,
            pline_name=pline.name,
            owner=pline.owner.username,
            redis_topic=redis_topic,
            status_info=status,
            last_update=last_update,
            error=error,
            completed=completed
        )

    parsed_pline_status = model_to_dict(pline_status)
    if "id" in parsed_pline_status:
        del parsed_pline_status["id"]
    if "last_update" in parsed_pline_status:
        parsed_pline_status["last_update"] = parsed_pline_status["last_update"].strftime("%Y-%m-%d %H:%M:%S.%f")
        
    conn.publish(redis_topic, json.dumps(parsed_pline_status))

