# File: flutter_nocode/urls.py
"""
Master URL Configuration for Flutter No-Code Project
Organized and clean URL structure with modular API organization
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views, auth_views
from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from core.views import api_test

urlpatterns = [
    # ============ ADMIN ============
    path('admin/', admin.site.urls),
    # API endpoints
    path('api/v1/', include('core.api_urls')),

    # Authentication
    path('api/auth/register/', auth_views.register, name='register'),
    path('api/auth/login/', auth_views.login, name='login'),
    path('api/auth/logout/', auth_views.logout, name='logout'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/me/', auth_views.me, name='me'),
    path('api/auth/update-profile/', auth_views.update_profile, name='update_profile'),
    path('api/auth/change-password/', auth_views.change_password, name='change_password'),
    path('api/auth/forgot-password/', auth_views.forgot_password, name='forgot_password'),
    path('api/auth/reset-password/', auth_views.reset_password, name='reset_password'),
    path('api/auth/verify-email/', auth_views.verify_email, name='verify_email'),

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

# Add this for better API root
urlpatterns = [
    path('', views.api_info, name='root'),
] + urlpatterns