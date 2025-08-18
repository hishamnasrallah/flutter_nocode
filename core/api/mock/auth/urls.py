
# =====================================
# File: core/api/mock/auth/urls.py
"""
URL Configuration for Authentication Mock APIs
"""

from django.urls import path
from . import views

app_name = 'mock_auth'

urlpatterns = [
    path('register/', views.mock_register, name='register'),
    path('login/', views.mock_login, name='login'),
    path('logout/', views.mock_logout, name='logout'),
    path('forgot-password/', views.mock_forgot_password, name='forgot_password'),
    path('reset-password/', views.mock_reset_password, name='reset_password'),
    path('profile/', views.mock_user_profile, name='user_profile'),
]