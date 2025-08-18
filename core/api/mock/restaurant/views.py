# File: core/api/mock/restaurant/views.py
"""
Restaurant Mock API Views
Provides endpoints for restaurant applications
"""

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from core.mock_data import RestaurantMockData

# Initialize mock data provider
restaurant_mock = RestaurantMockData()


@csrf_exempt
@require_http_methods(["GET"])
def restaurant_menu(request):
    """Mock API endpoint for menu items"""
    menu = restaurant_mock.get_menu_items()
    return JsonResponse(menu, safe=False)


@csrf_exempt
@require_http_methods(["GET"])
def restaurant_categories(request):
    """Mock API endpoint for restaurant categories"""
    categories = restaurant_mock.get_categories()
    return JsonResponse(categories, safe=False)


@csrf_exempt
@require_http_methods(["GET"])
def restaurant_offers(request):
    """Mock API endpoint for special offers"""
    offers = restaurant_mock.get_special_offers()
    return JsonResponse(offers, safe=False)


@csrf_exempt
@require_http_methods(["GET"])
def restaurant_reviews(request):
    """Mock API endpoint for restaurant reviews"""
    reviews = restaurant_mock.get_reviews()
    return JsonResponse(reviews, safe=False)


@csrf_exempt
@require_http_methods(["GET"])
def restaurant_reservations(request):
    """Mock API endpoint for reservations"""
    reservations = restaurant_mock.get_reservations()
    return JsonResponse(reservations, safe=False)