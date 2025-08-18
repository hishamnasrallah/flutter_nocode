# File: core/api/mock/marketplace/order_views.py
"""
Marketplace Order & Cart Mock API Views
Handles shopping cart, orders, and checkout
"""

import json
import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from core.mock_data import CompleteMarketplaceMockData

marketplace_mock = CompleteMarketplaceMockData()


@csrf_exempt
@require_http_methods(["GET"])
def marketplace_cart(request):
    """Get cart items"""
    all_data = marketplace_mock.get_data_sources()
    cart_items = all_data.get('Cart', [])
    return JsonResponse(cart_items, safe=False)


@csrf_exempt
@require_http_methods(["POST"])
def marketplace_add_to_cart(request):
    """Add item to cart"""
    data = json.loads(request.body)
    return JsonResponse({
        "success": True,
        "message": "Item added to cart",
        "cartCount": random.randint(1, 10)
    })


@csrf_exempt
@require_http_methods(["GET"])
def marketplace_orders(request):
    """Get user orders"""
    all_data = marketplace_mock.get_data_sources()
    orders = all_data.get('Orders', [])
    return JsonResponse(orders, safe=False)


@csrf_exempt
@require_http_methods(["GET"])
def marketplace_order_detail(request, order_id):
    """Get order details"""
    all_data = marketplace_mock.get_data_sources()
    orders = all_data.get('Order Details', all_data.get('Orders', []))

    order = next((o for o in orders if o.get('id') == order_id), None)
    if order:
        return JsonResponse(order)

    return JsonResponse({"error": "Order not found"}, status=404)


@csrf_exempt
@require_http_methods(["GET"])
def marketplace_order_tracking(request, order_id):
    """Get order tracking info"""
    all_data = marketplace_mock.get_data_sources()
    tracking_data = all_data.get('Order Tracking', [])

    if isinstance(tracking_data, list) and tracking_data:
        return JsonResponse(tracking_data[0])
    elif isinstance(tracking_data, dict):
        return JsonResponse(tracking_data)

    return JsonResponse({
        "orderId": order_id,
        "status": "processing",
        "updates": []
    })