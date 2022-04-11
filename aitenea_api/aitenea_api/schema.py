from django.utils.translation import gettext_lazy as _
from drf_spectacular.extensions import OpenApiAuthenticationExtension
from drf_spectacular.plumbing import build_bearer_security_scheme_object

#https://github.com/tfranzel/drf-spectacular/issues/264
#https://drf-spectacular.readthedocs.io/en/latest/blueprints.html
#https://github.com/tfranzel/drf-spectacular/blob/master/drf_spectacular/authentication.py
#https://github.com/James1345/django-rest-knox/blob/develop/knox/auth.py
# Anoto estas URLs para documentar de donde he sacado la información para sobreescribir la autenticación de Swagger
# Actualmente requiere introducir el token devuelto por /api/auth/login/
# En caso de querer añadir un login a Swagger que genere el Token se puede partir de la documentación en las URLs previas.

class KnoxTokenScheme(OpenApiAuthenticationExtension):
    target_class = 'knox.auth.TokenAuthentication'
    name = 'knoxTokenAuth'
    match_subclasses = True
    
    def get_security_definition(self, auto_schema):
        return build_bearer_security_scheme_object(
            header_name='Authorization',
            token_prefix='Token',
        )
