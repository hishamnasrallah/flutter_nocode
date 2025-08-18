# File: core/api/mock/media/urls.py
"""
URL Configuration for Media Upload Mock APIs
"""

from django.urls import path
from . import views

app_name = 'mock_media'

urlpatterns = [
    path('upload/', views.mock_upload_file, name='upload_file'),
    path('upload-multiple/', views.mock_upload_multiple, name='upload_multiple'),
    path('delete/<str:file_id>/', views.mock_delete_file, name='delete_file'),
]