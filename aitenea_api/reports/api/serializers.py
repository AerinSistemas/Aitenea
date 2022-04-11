from rest_framework import serializers
from reports.models import PlineReport, PlineReportMetric, PlineStatus

class PlineReportSerializer(serializers.ModelSerializer):
    dataset_parameters = serializers.JSONField()
    steps = serializers.JSONField()
    class Meta:
        model = PlineReport
        fields = '__all__'

class PlineReportMetricSerializer(serializers.ModelSerializer):
    score = serializers.ListField(child=serializers.DecimalField(max_digits=30, decimal_places=16))
    class Meta:
        model = PlineReportMetric
        fields = '__all__'


class PlineStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlineStatus
        fields = ['id', 'pline', 'owner', "pline_name", 'redis_topic', 'last_update', 'status_info', 'completed', 'error']

