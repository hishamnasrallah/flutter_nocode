# File: flutter_nocode/urls.py
"""
Master URL Configuration for Flutter No-Code Project
Organized and clean URL structure with modular API organization
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views  # Main application views
from core.views import api_test

urlpatterns = [
    # ============ ADMIN ============
    path('admin/', admin.site.urls),
    path('api/test/', api_test),
    path('health/', views.health_check, name='health_check'),
    path('api/info/', views.api_info, name='api_info'),

    # ============ MOCK API ROUTES ============
    # All mock APIs are organized under /api/mock/ with their own URL configurations
    path('api/mock/', include('core.api.mock.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)