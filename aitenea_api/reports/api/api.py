from rest_framework import viewsets, permissions, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from reports.models import PlineReport, PlineReportMetric, PlineStatus
from pline.models import Pline
from reports.models import PlineReport
from .serializers import PlineReportSerializer, PlineReportMetricSerializer, PlineStatusSerializer

import django_filters as filters


class PlineReportViewSet(viewsets.ModelViewSet):
    """
    Lista todas las `PlineReport` existentes en la BBDD.
    `List all PlineReport`.
    """
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = PlineReportSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'pline_name', 'owner',
                        'train_dataset_percentage', 'test_dataset_percentage',
                        'origin_dataset', 'target_dataset']

    def get_queryset(self):
        user = self.request._user
        plines_report = PlineReport.objects.all()

        if not user.is_staff:
            plines_report = PlineReport.objects.filter(owner=user)

        pline_name = self.request.query_params.get('pline_name')
        if pline_name is not None:
            plines_report = plines_report.filter(pline_name=pline_name)

        return plines_report
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(
        detail=False,
        methods=['POST'],
        name='Delete one or more PlineReports.',
        url_path='delete_bulk')
    def delete_bulk(self, request, *args, **kwargs):
        if len(request.data):
            PlineReport.objects.filter(pk__in=request.data).delete()
        return Response(None, status=status.HTTP_200_OK)


class ScoreFilter(filters.FilterSet):
    score = filters.NumberFilter(lookup_expr='icontains')
    class Meta:
        model = PlineReportMetric
        fields = ['id', 'pline_report', 'metric_name', 'score']


class PlineReportMetricViewSet(viewsets.ModelViewSet):
    """
    Lista todas las `PlineReportMetric` existentes en la BBDD.
    `List all PlineReportMetric`.
    """
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = PlineReportMetricSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ScoreFilter
    filterset_fields = ['id', 'pline_report', 'metric_name']

    def get_queryset(self):
        user = self.request._user
        plines_report_metrics = PlineReportMetric.objects.all()

        if not user.is_staff:
            plines_reports = PlineReport.objects.filter(owner=user)
            plines_report_metrics = PlineReportMetric.objects.filter(
                pline_report__in=plines_reports).distinct()

        pline_name = self.request.query_params.get('pline_name')
        if pline_name is not None:
            plines_report_metrics = plines_report_metrics.filter(pline_report__pline_name=pline_name)

        
        pline_report = self.request.query_params.get('report')
        if pline_report is not None:
            plines_report_metrics = plines_report_metrics.filter(pline_report=pline_report)

        return plines_report_metrics


class PlineStatusViewSet(viewsets.ModelViewSet):
    """
    Lista todas las `PlineStatus` existentes en la BBDD.
    `List all PlineStatus`.
    """
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = PlineStatusSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'pline', 'owner',
                        "pline_name", 'completed', 'error']

    def get_queryset(self):
        user = self.request._user
        plines_status = PlineStatus.objects.all()

        if not user.is_staff:
            plines = Pline.objects.filter(owner=user)
            plines_status = PlineStatus.objects.filter(
                pline__in=plines).distinct()

        pline = self.request.query_params.get('pline')
        if pline is not None:
            plines_status = plines_status.filter(pline__id=pline)

        return plines_status

