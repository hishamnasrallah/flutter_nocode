# File: core/views.py
"""
Main application views for the Flutter No-Code project.
This file contains only the main application views.
All mock API views are organized in the api/mock/ directory.
"""

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


# ============ MAIN APPLICATION VIEWS ============

@csrf_exempt
@require_http_methods(["GET"])
def health_check(request):
    """Health check endpoint for the application"""
    return JsonResponse({
        "status": "healthy",
        "message": "Flutter No-Code Backend is running",
        "version": "1.0.0"
    })


@csrf_exempt
@require_http_methods(["GET"])
def api_info(request):
    """Provides information about available APIs"""
    return JsonResponse({
        "name": "Flutter No-Code Mock API Server",
        "version": "1.0.0",
        "description": "Mock API endpoints for Flutter application development",
        "available_apis": {
            "news": "/api/mock/news/",
            "ecommerce": "/api/mock/ecommerce/",
            "restaurant": "/api/mock/restaurant/",
            "recipe": "/api/mock/recipe/",
            "marketplace": "/api/mock/marketplace/",
            "auth": "/api/mock/auth/",
            "chat": "/api/mock/chat/",
            "payment": "/api/mock/payment/",
            "media": "/api/mock/media/"
        },
        "documentation": "/api/docs/"
    })


# Add any other main application views here
# Keep this file clean - only non-mock API views should be here