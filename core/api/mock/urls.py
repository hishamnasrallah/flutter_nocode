# File: core/api/mock/urls.py
"""
Master URL Configuration for all Mock APIs
This file includes all mock API modules
"""

from django.urls import path, include

app_name = 'mock'

urlpatterns = [
    # News Application APIs
    path('news/', include('core.api.mock.news.urls')),

    # E-commerce Application APIs
    path('ecommerce/', include('core.api.mock.ecommerce.urls')),

    # Restaurant Application APIs
    path('restaurant/', include('core.api.mock.restaurant.urls')),

    # Recipe Application APIs
    path('recipe/', include('core.api.mock.recipe.urls')),

    # Marketplace Application APIs (Most comprehensive)
    path('marketplace/', include('core.api.mock.marketplace.urls')),

    # Authentication System APIs
    path('auth/', include('core.api.mock.auth.urls')),

    # Chat System APIs
    path('chat/', include('core.api.mock.chat.urls')),

    # Payment System APIs
    path('payment/', include('core.api.mock.payment.urls')),
    path('stripe/', include('core.api.mock.payment.urls')),  # Alias for stripe

    # Media Upload System APIs
    path('media/', include('core.api.mock.media.urls')),
]