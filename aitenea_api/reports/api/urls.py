from rest_framework import routers
from .api import PlineReportViewSet, PlineReportMetricViewSet, PlineStatusViewSet


app_name = 'reports'
router = routers.DefaultRouter()
router.register('pline_report', PlineReportViewSet, 'pline_report')
router.register('pline_report_metric', PlineReportMetricViewSet, 'pline_report_metric')
router.register('pline_status', PlineStatusViewSet, 'pline_status')

urlpatterns = router.urls
