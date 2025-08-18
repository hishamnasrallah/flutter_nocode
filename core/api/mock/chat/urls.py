# File: core/api/mock/chat/urls.py
"""
URL Configuration for Chat Mock APIs
"""

from django.urls import path
from . import views

app_name = 'mock_chat'

urlpatterns = [
    path('conversations/', views.mock_conversations, name='conversations'),
    path('conversations/<str:conversation_id>/messages/', views.mock_messages, name='messages'),
    path('send/', views.mock_send_message, name='send_message'),
]
