# File: core/api/mock/auth/views.py
"""
Authentication Mock API Views
Provides mock authentication endpoints for user registration, login, and profile management
"""

import json
import uuid
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


@csrf_exempt
@require_http_methods(["POST"])
def mock_register(request):
    """Mock user registration endpoint"""
    data = json.loads(request.body)

    return JsonResponse({
        "success": True,
        "token": f"mock_token_{uuid.uuid4().hex}",
        "user": {
            "id": str(uuid.uuid4()),
            "username": data.get("username", "user123"),
            "email": data.get("email", "user@example.com"),
            "first_name": data.get("first_name", "John"),
            "last_name": data.get("last_name", "Doe"),
            "profile_picture": "https://picsum.photos/100/100?random=user"
        }
    })


@csrf_exempt
@require_http_methods(["POST"])
def mock_login(request):
    """Mock user login endpoint"""
    data = json.loads(request.body)

    return JsonResponse({
        "success": True,
        "token": f"mock_token_{uuid.uuid4().hex}",
        "user": {
            "id": "user_123",
            "username": data.get("username", "user123"),
            "email": "user@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "is_seller": False,
            "member_since": "2023-01-15"
        }
    })


@csrf_exempt
@require_http_methods(["POST"])
def mock_logout(request):
    """Mock logout endpoint"""
    return JsonResponse({"success": True, "message": "Logged out successfully"})


@csrf_exempt
@require_http_methods(["POST"])
def mock_forgot_password(request):
    """Mock forgot password endpoint"""
    data = json.loads(request.body)
    email = data.get("email")

    return JsonResponse({
        "success": True,
        "message": f"Password reset link sent to {email}"
    })


@csrf_exempt
@require_http_methods(["POST"])
def mock_reset_password(request):
    """Mock reset password endpoint"""
    data = json.loads(request.body)

    return JsonResponse({
        "success": True,
        "message": "Password reset successfully"
    })


@csrf_exempt
@require_http_methods(["GET", "PUT"])
def mock_user_profile(request):
    """Mock user profile endpoint"""
    if request.method == "GET":
        return JsonResponse({
            "id": "user_123",
            "username": "john_doe",
            "email": "john@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "phone": "+1234567890",
            "bio": "Love shopping and finding great deals!",
            "profile_picture": "https://picsum.photos/200/200?random=profile",
            "is_seller": False,
            "seller_rating": 0,
            "member_since": "2023-01-15",
            "total_orders": 25,
            "total_spent": 1250.50,
            "loyalty_points": 500,
            "addresses": [
                {
                    "id": "addr_1",
                    "name": "Home",
                    "street": "123 Main St",
                    "city": "New York",
                    "state": "NY",
                    "zip": "10001",
                    "country": "USA",
                    "is_default": True
                }
            ]
        })

    elif request.method == "PUT":
        return JsonResponse({
            "success": True,
            "message": "Profile updated successfully"
        })


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