from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from jsonfield import JSONField
from pline.models import Pline


# Create your models here.
class PlineReport(models.Model):
    """
    `PlineReport`
    Contiene toda la información relevante que resume la ejecución de la `Pline`.

    Args:
        `PlineReport` (JSON): JSON proporcionando los campos del modelo:
            * `pline_name`: nombre de la clase del paso. Mismo que `AiteneaClass.class_name`.
            * `owner`: Usuario que ha creado el reporte.
            * `steps`: Pasos relacionados con la `Pline` del `Report`.
            * `dataset_parameters`: Parámetros del `dataset` elegidos.
            * `created_at`: fecha de creación.
            * `execution_time`: Tiempo de ejecución de la `Pline`.
            * `train_dataset_percentage`: Porcentaje del `dataset` que se ha usado para el entrenamiento.
            * `test_dataset_percentage`: Porcentaje del `dataset` que se ha usado para test.
            * `origin_dataset`: Nombre del `dataset` origen.
            * `target_dataset`: Nombre del dataset destino.
            * `error_output`: Informacion del error en caso de que la ejecución de la Pline falle.
            * `pline`: `Pline` relacionado con este objeto.
    """

    pline_name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    steps = JSONField(default='')
    dataset_parameters = JSONField(default='')
    created_at = models.DateTimeField(auto_now_add=True, help_text="Creation date.")
    execution_time = models.DurationField(null=True)
    train_dataset_percentage = models.IntegerField(null=True)
    test_dataset_percentage = models.IntegerField(null=True)
    origin_dataset = models.CharField(max_length=100)
    target_dataset = models.CharField(max_length=100, null=True)
    error_output = models.TextField(null=True)
    pline = models.ForeignKey(Pline, related_name='pline_report', on_delete=models.SET_NULL, null=True)


class PlineReportMetric(models.Model):
    """
    `PlineReportMetric`
    Contiene toda la puntuación y nombre del algoritmo de `machine learning` relacionado con el reporte de la `Pline`.

    Args:
        `PlineReportMetric` (`SON`): JSON proporcionando los campos del modelo:
            * `metric_name`: nombre del algoritmo de puntuación.
            * `score`: puntuación del algoritmo.
            * `pline_report`: Report relacionado con este.
            * `pline`: `Pline` relacionado con este objeto.
    """

    metric_name = models.CharField(max_length=100)
    score = ArrayField(models.DecimalField(max_digits=30, decimal_places=16), null=True)
    pline_report = models.ForeignKey(PlineReport, related_name='pline_report_metric', on_delete=models.CASCADE, null=True)
    pline = models.ForeignKey(Pline, related_name='pline_metric', on_delete=models.SET_NULL, null=True)


class PlineStatus(models.Model):
    """
    `PlineStatus`
    Contiene el estado actual de la `Pline` relacionada.

    Args:
        `PlineStatus` (JSON): JSON proporcionando los campos del modelo:
            * `pline`: `id` de la `Pline` a la que se quiere hacer pertenecer este status.
            * `redis_topic`: `id` único que identifica el topic en `Redis`.
            * `last_update`: datetime que almacena la última modificación del `Pline`.
            * `status_info`: texto detallado sobre la tarea en ejecución.
            * `completed`: boolean que indica si se ha completado la ejecución de la `Pline`.
            * `error`: boolean que indica si ha fallado la ejecución de la `Pline`.
    """

    pline = models.ForeignKey(Pline, related_name='status', on_delete=models.CASCADE, null=True)
    pline_name = models.CharField(max_length=100)
    owner = models.CharField(max_length=100)
    redis_topic = models.CharField(max_length=100)
    last_update = models.DateTimeField()
    status_info = models.TextField()
    completed = models.BooleanField(default=False)
    error = models.BooleanField(default=False)

