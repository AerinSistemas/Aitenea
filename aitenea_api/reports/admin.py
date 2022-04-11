from django.contrib import admin
from .models import PlineReport, PlineReportMetric, PlineStatus

admin.site.register(PlineReport)
admin.site.register(PlineReportMetric)
admin.site.register(PlineStatus)
# Register your models here.