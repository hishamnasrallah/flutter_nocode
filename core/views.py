from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .mock_data import NewsMockData, EcommerceMockData, RestaurantMockData

# Initialize mock data providers
news_mock = NewsMockData()
ecommerce_mock = EcommerceMockData()
restaurant_mock = RestaurantMockData()

# News API endpoints
@csrf_exempt
@require_http_methods(["GET"])
def news_articles(request):
    """Mock API endpoint for news articles"""
    articles = news_mock.get_news_articles()
    return JsonResponse(articles, safe=False)

@csrf_exempt
@require_http_methods(["GET"])
def news_sources(request):
    """Mock API endpoint for news sources"""
    sources = news_mock.get_news_sources()
    return JsonResponse(sources, safe=False)

@csrf_exempt
@require_http_methods(["GET"])
def news_categories(request):
    """Mock API endpoint for news categories"""
    categories = news_mock.get_categories()
    return JsonResponse(categories, safe=False)

@csrf_exempt
@require_http_methods(["GET"])
def news_breaking(request):
    """Mock API endpoint for breaking news"""
    breaking = news_mock.get_breaking_news()
    return JsonResponse(breaking, safe=False)

@csrf_exempt
@require_http_methods(["GET"])
def news_trending(request):
    """Mock API endpoint for trending stories"""
    trending = news_mock.get_trending_stories()
    return JsonResponse(trending, safe=False)

# E-commerce API endpoints
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

# Restaurant API endpoints
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