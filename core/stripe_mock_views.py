"""
Mock Stripe Payment API Views
File: core/stripe_mock_views.py
"""

import json
import uuid
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


@csrf_exempt
@require_http_methods(["POST"])
def mock_create_payment_intent(request):
    """Mock create payment intent endpoint"""
    data = json.loads(request.body)
    amount = data.get("amount", 100)

    return JsonResponse({
        "success": True,
        "client_secret": f"pi_{uuid.uuid4().hex}_secret_{uuid.uuid4().hex}",
        "payment_intent_id": f"pi_{uuid.uuid4().hex}",
        "amount": amount,
        "currency": "usd",
        "status": "requires_payment_method"
    })


@csrf_exempt
@require_http_methods(["POST"])
def mock_confirm_payment(request):
    """Mock confirm payment endpoint"""
    data = json.loads(request.body)

    return JsonResponse({
        "success": True,
        "payment_id": f"pay_{uuid.uuid4().hex}",
        "status": "succeeded",
        "message": "Payment successful",
        "order_id": f"ord_{uuid.uuid4().hex}"
    })


@csrf_exempt
@require_http_methods(["POST"])
def mock_stripe_webhook(request):
    """Mock Stripe webhook endpoint"""
    return JsonResponse({
        "success": True,
        "message": "Webhook processed"
    })


@csrf_exempt
@require_http_methods(["GET"])
def mock_payment_methods(request):
    """Mock get payment methods"""
    methods = [
        {
            "id": "pm_1",
            "type": "card",
            "last4": "4242",
            "brand": "Visa",
            "exp_month": 12,
            "exp_year": 2025,
            "is_default": True
        },
        {
            "id": "pm_2",
            "type": "card",
            "last4": "5555",
            "brand": "Mastercard",
            "exp_month": 6,
            "exp_year": 2024,
            "is_default": False
        }
    ]

    return JsonResponse(methods, safe=False)


@csrf_exempt
@require_http_methods(["POST"])
def mock_add_payment_method(request):
    """Mock add payment method"""
    data = json.loads(request.body)

    return JsonResponse({
        "success": True,
        "payment_method": {
            "id": f"pm_{uuid.uuid4().hex}",
            "type": "card",
            "last4": data.get("card_number", "0000")[-4:],
            "brand": "Visa",
            "exp_month": data.get("exp_month", 12),
            "exp_year": data.get("exp_year", 2025)
        }
    })