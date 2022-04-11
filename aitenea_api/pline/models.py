from django.db import models
from django.contrib.auth.models import User
from jsonfield import JSONField

# Create your models here.

class Pline(models.Model):
    """
    `Pline` (abreviatura de pipeline). Conforma una `pline`.

    Parámetros:
        Pline (JSON): JSON proporcionando los campos del modelo:
            * `name`: nombre que le da el usuario a la `pline`.
            * `description`: breve descripción.
            * `path`: ruta para almacenar el modelo.
            * `fitted` (boolean): indicador de si el modelo está entrenado.
            * `owner`: usuario creador.
            * `creation_timestamp`: fecha de creación.
            * `update_timestamp`: fecha de actualización.
    """
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    fitted = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_timestamp = models.DateTimeField(auto_now_add=True)
    update_timestamp = models.DateTimeField(auto_now=True)
    metadata = JSONField(default='')


class AiteneaClass(models.Model):
    """Modelo para definir las clases de AItenea.

    Args:
        AiteneaClass (JSON): JSON proporcionando los campos del modelo:
            * `class_name`: nombre de la clase. Debe ser el nombre tras 'class ' en la definición de la clase.
            * `type`: tipo de la clase de AItenea {`aitenea_ai`, `aitenea_transform`, `external_ai`, `external_transform`}.
            * `options`: opciones de la clase en formato JSON.
    """
    CLASS_CHOICES = (
        ('aitenea_ai', 'Aitenea AI'),
        ('aitenea_transform', 'Aitenea Transform'),
        ('external_ai', 'External AI'),
        ('external_transform', 'External Transform'),
    )

    class_name = models.CharField(max_length=512)
    type = models.CharField(max_length=100, choices = CLASS_CHOICES)
    module_name = models.CharField(max_length=512)
    options = JSONField(default='')
    html_options = JSONField(default='')
    genetic_parameters = JSONField(default='')
    html_genetic_parameters = JSONField(default='')


class Step(models.Model):
    """
    `Step`
    Conforma un `Step` de la `pline`.

    Args:
        Step (JSON): JSON proporcionando los campos del modelo:
            * `pline_id`: `id` de la `Pline` a la que se quiere hacer pertenecer este paso.
            * `step_number`: orden del paso dentro de la `Pline`.
            * `step_name`: nombre de la clase del paso. Mismo que AiteneaClass.class_name.
            * `step_type`: tipo de la clase del paso: {`ai`, `transform`}. Mismo que AiteneaClass.type.
            * `step_options`: opciones de la clase. Mismas que AiteneaClass.options.
    """
    CLASS_CHOICES = (
        ('ai', 'ai'),
        ('transform', 'transform'),
    )
    pline_id = models.ForeignKey(Pline, related_name='steps', on_delete=models.CASCADE, null=True)
    step_number = models.IntegerField()
    step_name = models.CharField(max_length=100)
    step_type = models.CharField(max_length=100)
    module_name = models.CharField(max_length=100)
    step_options = JSONField(default='')
    step_genetic_parameters = JSONField(default='')

