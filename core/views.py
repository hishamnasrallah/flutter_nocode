# File: core/views.py
import random
import uuid
from datetime import datetime, timedelta

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .mock_data import NewsMockData, EcommerceMockData, RestaurantMockData, ComprehensiveNewsMockData, RecipeMockData # NEW

# Initialize mock data providers
news_mock = NewsMockData()
comprehensive_news_mock = ComprehensiveNewsMockData()
ecommerce_mock = EcommerceMockData()
restaurant_mock = RestaurantMockData()
recipe_mock = RecipeMockData() # NEW

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


# ============ ADD THESE NEW VIEWS FOR COMPREHENSIVE NEWS APP ============

# Comprehensive News Feed endpoint
@csrf_exempt
@require_http_methods(["GET"])
def comprehensive_news_feed(request):
    """Get comprehensive personalized news feed with pagination"""
    page = int(request.GET.get('page', 1))
    limit = int(request.GET.get('limit', 20))
    user_id = request.GET.get('user_id')

    feed_data = comprehensive_news_mock.get_feed(user_id, page, limit)
    return JsonResponse(feed_data, safe=False)


# Article detail endpoint
@csrf_exempt
@require_http_methods(["GET"])
def comprehensive_article_detail(request, article_id):
    """Get detailed article information"""
    article = comprehensive_news_mock.get_article_details(article_id)
    if article:
        return JsonResponse(article, safe=False)
    return JsonResponse({"error": "Article not found"}, status=404)


# Authors endpoint
@csrf_exempt
@require_http_methods(["GET"])
def news_authors(request):
    """Get all authors/journalists"""
    authors = comprehensive_news_mock.get_authors()
    return JsonResponse(authors, safe=False)


# Author's articles
@csrf_exempt
@require_http_methods(["GET"])
def news_author_articles(request, author_id):
    """Get articles by specific author"""
    articles = [a for a in comprehensive_news_mock.articles if a["author"]["id"] == author_id]
    return JsonResponse(articles, safe=False)


# Video news content
@csrf_exempt
@require_http_methods(["GET"])
def news_videos(request):
    """Get video news content"""
    videos = comprehensive_news_mock.get_videos()
    return JsonResponse(videos, safe=False)


# Podcast episodes
@csrf_exempt
@require_http_methods(["GET"])
def news_podcasts(request):
    """Get podcast episodes"""
    podcasts = comprehensive_news_mock.get_podcasts()
    return JsonResponse(podcasts, safe=False)


# Premium content
@csrf_exempt
@require_http_methods(["GET"])
def news_premium(request):
    """Get premium content"""
    premium = comprehensive_news_mock.get_premium()
    return JsonResponse(premium, safe=False)


# Local news
@csrf_exempt
@require_http_methods(["GET"])
def news_local(request):
    """Get local news based on location"""
    location = request.GET.get('location')
    local_news = comprehensive_news_mock.get_local_news(location)
    return JsonResponse(local_news, safe=False)


# AI-powered recommendations
@csrf_exempt
@require_http_methods(["GET"])
def news_recommendations(request):
    """Get AI-powered article recommendations"""
    user_id = request.GET.get('user_id')
    recommendations = comprehensive_news_mock.get_recommendations(user_id)
    return JsonResponse(recommendations, safe=False)


# User bookmarks
@csrf_exempt
@require_http_methods(["GET"])
def news_bookmarks(request):
    """Get user bookmarks"""
    user_id = request.GET.get('user_id')
    bookmarks = comprehensive_news_mock.get_bookmarks(user_id)
    return JsonResponse(bookmarks, safe=False)


# Add bookmark
@csrf_exempt
@require_http_methods(["POST"])
def news_bookmark_add(request):
    """Add article to bookmarks"""
    data = json.loads(request.body)
    article_id = data.get('article_id')
    user_id = data.get('user_id')
    return JsonResponse({"success": True, "message": "Bookmark added", "article_id": article_id})


# Remove bookmark
@csrf_exempt
@require_http_methods(["DELETE"])
def news_bookmark_remove(request, article_id):
    """Remove article from bookmarks"""
    return JsonResponse({"success": True, "message": "Bookmark removed", "article_id": article_id})


# Reading history
@csrf_exempt
@require_http_methods(["GET"])
def news_history(request):
    """Get user's reading history"""
    user_id = request.GET.get('user_id')
    history = comprehensive_news_mock.get_history(user_id)
    return JsonResponse(history, safe=False)


# User notifications
@csrf_exempt
@require_http_methods(["GET"])
def news_notifications(request):
    """Get user notifications"""
    user_id = request.GET.get('user_id')
    notifications = comprehensive_news_mock.get_notifications(user_id)
    return JsonResponse(notifications, safe=False)


# Advanced search
@csrf_exempt
@require_http_methods(["GET"])
def news_advanced_search(request):
    """Advanced search with multiple filters"""
    query = request.GET.get('q', '')
    category = request.GET.get('category')
    author = request.GET.get('author')
    source = request.GET.get('source')
    date_from = request.GET.get('from')
    date_to = request.GET.get('to')

    results = comprehensive_news_mock.search(query)

    # Apply filters
    if category:
        results = [r for r in results if r["category"]["id"] == category]
    if author:
        results = [r for r in results if r["author"]["id"] == author]
    if source:
        results = [r for r in results if r["source"]["id"] == source]

    return JsonResponse(results, safe=False)


# Article comments
@csrf_exempt
@require_http_methods(["GET"])
def news_article_comments(request, article_id):
    """Get comments for specific article"""
    article = comprehensive_news_mock.get_article_details(article_id)
    if article:
        return JsonResponse(article.get("comments", []), safe=False)
    return JsonResponse([], safe=False)


# Add comment
@csrf_exempt
@require_http_methods(["POST"])
def news_comment_add(request):
    """Add comment to article"""
    data = json.loads(request.body)
    return JsonResponse({
        "success": True,
        "comment": {
            "id": str(uuid.uuid4()),
            "content": data.get("content"),
            "userName": data.get("userName", "Anonymous"),
            "timestamp": datetime.now().isoformat(),
            "likes": 0
        }
    })


# Like article
@csrf_exempt
@require_http_methods(["POST"])
def news_article_like(request):
    """Like/unlike an article"""
    data = json.loads(request.body)
    article_id = data.get('article_id')
    user_id = data.get('user_id')
    action = data.get('action', 'like')  # 'like' or 'unlike'

    return JsonResponse({
        "success": True,
        "action": action,
        "article_id": article_id
    })


# Share article
@csrf_exempt
@require_http_methods(["POST"])
def news_article_share(request):
    """Share article on social media"""
    data = json.loads(request.body)
    article_id = data.get('article_id')
    platform = data.get('platform')  # 'twitter', 'facebook', 'whatsapp', etc

    return JsonResponse({
        "success": True,
        "platform": platform,
        "article_id": article_id,
        "share_url": f"https://newshub.com/article/{article_id}"
    })


# Platform statistics
@csrf_exempt
@require_http_methods(["GET"])
def news_platform_stats(request):
    """Get platform-wide statistics"""
    stats = comprehensive_news_mock.get_stats()
    return JsonResponse(stats, safe=False)


# Trending topics
@csrf_exempt
@require_http_methods(["GET"])
def news_trending_topics(request):
    """Get current trending topics"""
    topics = comprehensive_news_mock._get_trending_topics()
    topics_with_count = [{"topic": topic, "count": random.randint(100, 10000)} for topic in topics]
    return JsonResponse(topics_with_count, safe=False)


# Weather widget
@csrf_exempt
@require_http_methods(["GET"])
def news_weather_widget(request):
    """Get weather data for news app widget"""
    location = request.GET.get('location', 'New York')
    weather_data = {
        "location": location,
        "temperature": random.randint(60, 85),
        "condition": random.choice(["Sunny", "Partly Cloudy", "Cloudy", "Rainy"]),
        "humidity": random.randint(40, 80),
        "wind": f"{random.randint(5, 20)} mph",
        "icon": "wb_sunny",
        "forecast": [
            {"day": "Mon", "high": 75, "low": 60, "condition": "Sunny", "icon": "wb_sunny"},
            {"day": "Tue", "high": 73, "low": 58, "condition": "Cloudy", "icon": "cloud"},
            {"day": "Wed", "high": 70, "low": 55, "condition": "Rainy", "icon": "rain"},
            {"day": "Thu", "high": 72, "low": 57, "condition": "Partly Cloudy", "icon": "cloud_queue"},
            {"day": "Fri", "high": 76, "low": 62, "condition": "Sunny", "icon": "wb_sunny"}
        ]
    }
    return JsonResponse(weather_data, safe=False)


# Live updates
@csrf_exempt
@require_http_methods(["GET"])
def news_live_updates(request):
    """Get live updates for breaking stories"""
    story_id = request.GET.get('story_id')
    updates = []

    for i in range(5):
        updates.append({
            "id": str(uuid.uuid4()),
            "story_id": story_id,
            "timestamp": (datetime.now() - timedelta(minutes=i * 15)).isoformat(),
            "title": f"Update {i + 1}",
            "content": f"Latest development in the ongoing story...",
            "priority": random.choice(["high", "medium", "low"]),
            "author": "News Desk"
        })

    return JsonResponse(updates, safe=False)


# User preferences
@csrf_exempt
@require_http_methods(["GET", "POST"])
def news_user_preferences(request):
    """Get or update user news preferences"""
    if request.method == "GET":
        preferences = {
            "categories": ["technology", "business", "sports", "health", "science"],
            "sources": ["Global News Network", "Tech Today", "Business Weekly"],
            "authors": ["John Smith", "Sarah Johnson"],
            "notifications": {
                "breaking_news": True,
                "trending": True,
                "daily_digest": True,
                "weekly_summary": False
            },
            "reading_preferences": {
                "font_size": "medium",
                "dark_mode": False,
                "compact_view": False,
                "auto_play_videos": True
            },
            "language": "en",
            "region": "US"
        }
        return JsonResponse(preferences, safe=False)

    elif request.method == "POST":
        data = json.loads(request.body)
        return JsonResponse({"success": True, "message": "Preferences updated successfully"})


# Newsletter subscription
@csrf_exempt
@require_http_methods(["POST"])
def news_newsletter_subscribe(request):
    """Subscribe to newsletter"""
    data = json.loads(request.body)
    email = data.get('email')
    categories = data.get('categories', [])
    frequency = data.get('frequency', 'daily')  # 'daily', 'weekly', 'monthly'

    return JsonResponse({
        "success": True,
        "message": "Successfully subscribed to newsletter",
        "subscription": {
            "email": email,
            "categories": categories,
            "frequency": frequency,
            "subscription_id": str(uuid.uuid4())
        }
    })


# Related articles
@csrf_exempt
@require_http_methods(["GET"])
def news_related_articles(request, article_id):
    """Get related articles for a specific article"""
    article = comprehensive_news_mock.get_article_details(article_id)
    if article:
        related_ids = article.get("relatedArticles", [])
        related = [a for a in comprehensive_news_mock.articles if a["id"] in related_ids]
        return JsonResponse(related[:5], safe=False)
    return JsonResponse([], safe=False)


# Source details
@csrf_exempt
@require_http_methods(["GET"])
def news_source_detail(request, source_id):
    """Get detailed information about a news source"""
    source = next((s for s in comprehensive_news_mock.sources if s["id"] == source_id), None)
    if source:
        # Add recent articles from this source
        source["recent_articles"] = [
                                        a for a in comprehensive_news_mock.articles
                                        if a["source"]["id"] == source_id
                                    ][:10]
        return JsonResponse(source, safe=False)
    return JsonResponse({"error": "Source not found"}, status=404)


# Follow/unfollow source
@csrf_exempt
@require_http_methods(["POST"])
def news_follow_source(request):
    """Follow or unfollow a news source"""
    data = json.loads(request.body)
    source_id = data.get('source_id')
    action = data.get('action', 'follow')  # 'follow' or 'unfollow'
    user_id = data.get('user_id')

    return JsonResponse({
        "success": True,
        "action": action,
        "source_id": source_id,
        "message": f"Successfully {action}ed source"
    })


# Follow/unfollow author
@csrf_exempt
@require_http_methods(["POST"])
def news_follow_author(request):
    """Follow or unfollow an author"""
    data = json.loads(request.body)
    author_id = data.get('author_id')
    action = data.get('action', 'follow')  # 'follow' or 'unfollow'
    user_id = data.get('user_id')

    return JsonResponse({
        "success": True,
        "action": action,
        "author_id": author_id,
        "message": f"Successfully {action}ed author"
    })

# ============ NEW RECIPE APP ENDPOINTS ============ # NEW
@csrf_exempt
@require_http_methods(["GET"])
def recipe_all_recipes(request):
    """Mock API endpoint for all recipes"""
    recipes = recipe_mock.get_all_recipes()
    return JsonResponse(recipes, safe=False)

@csrf_exempt
@require_http_methods(["GET"])
def recipe_detail(request, recipe_id):
    """Mock API endpoint for a single recipe detail"""
    recipe = recipe_mock.get_recipe_detail(recipe_id)
    if recipe:
        return JsonResponse(recipe, safe=False)
    return JsonResponse({"error": "Recipe not found"}, status=404)

@csrf_exempt
@require_http_methods(["GET"])
def recipe_categories(request):
    """Mock API endpoint for recipe categories"""
    categories = recipe_mock.get_categories()
    return JsonResponse(categories, safe=False)

@csrf_exempt
@require_http_methods(["GET"])
def recipe_search(request):
    """Mock API endpoint for searching recipes"""
    query = request.GET.get('q', '')
    results = recipe_mock.search_recipes(query)
    return JsonResponse(results, safe=False)

@csrf_exempt
@require_http_methods(["GET"])
def recipe_favorites(request):
    """Mock API endpoint for favorite recipes"""
    favorites = recipe_mock._generate_favorite_recipes() # Re-generate for mock
    return JsonResponse(favorites, safe=False)

@csrf_exempt
@require_http_methods(["GET"])
def recipe_shopping_list(request):
    """Mock API endpoint for shopping list"""
    shopping_list = recipe_mock._generate_shopping_list() # Re-generate for mock
    return JsonResponse(shopping_list, safe=False)

@csrf_exempt
@require_http_methods(["GET"])
def recipe_nutritional_info(request):
    """Mock API endpoint for nutritional info"""
    nutritional_info = recipe_mock._generate_nutritional_info() # Re-generate for mock
    return JsonResponse(nutritional_info, safe=False)
