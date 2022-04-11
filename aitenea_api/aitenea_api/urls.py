"""aitenea_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

# DOCS
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

API_URL = r'^api/'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(API_URL, include('pline.api.urls')),
    url(API_URL, include('accounts.api.urls')),
    url(API_URL, include('reports.api.urls')),
    # OpenAPI:
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # DOCS:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    url(r'^docs/', include('docs.urls')),
    url(r'', include('frontend.urls')),
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
