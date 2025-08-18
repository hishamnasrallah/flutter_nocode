# File: core/api/mock/news/basic_views.py
"""
Basic News API Mock Views
Provides simple news endpoints for basic news applications
"""

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from core.mock_data import NewsMockData

# Initialize mock data provider
news_mock = NewsMockData()


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