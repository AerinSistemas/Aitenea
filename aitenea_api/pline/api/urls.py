from django import views
from django.urls import path

from rest_framework import routers
from .api import PlineViewSet, StepViewSet, AiteneaClassViewSet, CSVViewset
from pline.views import elastic_get_index, data_evaluation


app_name = 'pline'
router = routers.DefaultRouter()
router.register('pline', PlineViewSet, 'pline')
router.register('steps', StepViewSet, 'steps')
router.register('csv', CSVViewset, 'csv')

urlpatterns = [
    path('classes/', AiteneaClassViewSet.as_view({ 'get': 'list'})),
    path('classes/<int:pk>/', AiteneaClassViewSet.as_view({ 'get': 'retrieve'})),
    path('elastic_get_index/', elastic_get_index),
    path('data_evaluation/', data_evaluation),
]

urlpatterns += router.urls