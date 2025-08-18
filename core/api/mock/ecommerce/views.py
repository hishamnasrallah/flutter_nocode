# File: core/api/mock/ecommerce/views.py
"""
E-commerce Mock API Views
Provides endpoints for e-commerce applications
"""

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from core.mock_data import EcommerceMockData

# Initialize mock data provider
ecommerce_mock = EcommerceMockData()


@csrf_exempt
@require_http_methods(["GET"])
def ecommerce_products(request):
    """Mock API endpoint for products"""
    products = ecommerce_mock.get_products()
    return JsonResponse(products, safe=False)


@csrf_exempt
@require_http_methods(["GET"])
def ecommerce_categories(request):
    """Mock API endpoint for e-commerce categories"""
    categories = ecommerce_mock.get_categories()
    return JsonResponse(categories, safe=False)


@csrf_exempt
@require_http_methods(["GET"])
def ecommerce_cart(request):
    """Mock API endpoint for cart items"""
    cart = ecommerce_mock.get_cart_items()
    return JsonResponse(cart, safe=False)


@csrf_exempt
@require_http_methods(["GET"])
def ecommerce_orders(request):
    """Mock API endpoint for orders"""
    orders = ecommerce_mock.get_orders()
    return JsonResponse(orders, safe=False)


@csrf_exempt
@require_http_methods(["GET"])
def ecommerce_reviews(request):
    """Mock API endpoint for reviews"""
    reviews = ecommerce_mock.get_reviews()
    return JsonResponse(reviews, safe=False)