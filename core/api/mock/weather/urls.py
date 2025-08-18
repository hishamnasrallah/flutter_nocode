# File: core/api/mock/weather/urls.py
"""
URL configuration for Weather application mock APIs
"""

from django.urls import path
from . import views

app_name = 'weather'

urlpatterns = [
    # Weather data endpoints
    path('current', views.get_current_weather, name='current_weather'),
    path('forecast', views.get_forecast, name='forecast'),
    path('hourly', views.get_hourly_forecast, name='hourly_forecast'),

    # Location management
    path('locations', views.get_locations, name='locations'),
    path('locations/<str:location_id>', views.manage_location, name='manage_location'),
    path('locations/search', views.search_locations, name='search_locations'),

    # Alerts and warnings
    path('alerts', views.get_alerts, name='alerts'),

    # Air quality
    path('air-quality', views.get_air_quality, name='air_quality'),

    # Weather maps
    path('maps', views.get_weather_maps, name='weather_maps'),
    path('maps/<str:map_type>/tiles', views.get_map_tiles, name='map_tiles'),

    # User profile and preferences
    path('profile', views.get_user_profile, name='user_profile'),
    path('profile/update', views.update_user_profile, name='update_profile'),

    # Subscription
    path('subscriptions', views.get_subscription_plans, name='subscription_plans'),
    path('subscribe', views.subscribe, name='subscribe'),

    # Authentication
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('forgot-password', views.forgot_password, name='forgot_password'),
    path('change-password', views.change_password, name='change_password'),

    # Support
    path('support', views.send_support_message, name='support'),

    # Statistics
    path('stats', views.get_weather_stats, name='weather_stats'),

    # Test endpoint
    path('test', views.test_connection, name='test_connection'),
]