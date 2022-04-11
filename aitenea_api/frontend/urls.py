from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    # match the root
    url(r'', views.index),
    # match all other pages
    url(r'^(?:.*)/?$', views.index),
]
