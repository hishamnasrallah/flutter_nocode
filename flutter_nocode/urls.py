# ADD THESE TO YOUR flutter_nocode/urls.py file in the urlpatterns list

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # ============ COMPREHENSIVE NEWS APPLICATION ENDPOINTS ============

    # Main News Endpoints (Core)
    path('api/mock/news/articles', views.news_articles, name='mock_news_articles'),
    path('api/mock/news/sources', views.news_sources, name='mock_news_sources'),
    path('api/mock/news/categories', views.news_categories, name='mock_news_categories'),
    path('api/mock/news/breaking', views.news_breaking, name='mock_news_breaking'),
    path('api/mock/news/trending', views.news_trending, name='mock_news_trending'),

    # Comprehensive Feed Endpoints
    path('api/mock/comprehensive/news/feed', views.comprehensive_news_feed, name='comprehensive_news_feed'),
    path('api/mock/comprehensive/news/article/<str:article_id>/', views.comprehensive_article_detail,
         name='comprehensive_article_detail'),

    # Authors
    path('api/mock/news/authors', views.news_authors, name='news_authors'),
    path('api/mock/news/authors/<str:author_id>/articles', views.news_author_articles, name='news_author_articles'),

    # Multimedia
    path('api/mock/news/videos', views.news_videos, name='news_videos'),
    path('api/mock/news/podcasts', views.news_podcasts, name='news_podcasts'),
    path('api/mock/news/premium', views.news_premium, name='news_premium'),
    path('api/mock/news/local', views.news_local, name='news_local'),

    # User Features
    path('api/mock/news/recommendations', views.news_recommendations, name='news_recommendations'),
    path('api/mock/news/bookmarks', views.news_bookmarks, name='news_bookmarks'),
    path('api/mock/news/bookmarks/add', views.news_bookmark_add, name='news_bookmark_add'),
    path('api/mock/news/bookmarks/<str:article_id>/remove', views.news_bookmark_remove, name='news_bookmark_remove'),
    path('api/mock/news/history', views.news_history, name='news_history'),
    path('api/mock/news/notifications', views.news_notifications, name='news_notifications'),

    # Search
    path('api/mock/news/search/advanced', views.news_advanced_search, name='news_advanced_search'),

    # Comments and Interactions
    path('api/mock/news/articles/<str:article_id>/comments', views.news_article_comments, name='news_article_comments'),
    path('api/mock/news/comments/add', views.news_comment_add, name='news_comment_add'),
    path('api/mock/news/articles/like', views.news_article_like, name='news_article_like'),
    path('api/mock/news/articles/share', views.news_article_share, name='news_article_share'),

    # Platform Features
    path('api/mock/news/stats', views.news_platform_stats, name='news_platform_stats'),
    path('api/mock/news/trending-topics', views.news_trending_topics, name='news_trending_topics'),
    path('api/mock/news/weather', views.news_weather_widget, name='news_weather_widget'),
    path('api/mock/news/live-updates', views.news_live_updates, name='news_live_updates'),

    # Settings and Preferences
    path('api/mock/news/preferences', views.news_user_preferences, name='news_user_preferences'),
    path('api/mock/news/newsletter/subscribe', views.news_newsletter_subscribe, name='news_newsletter_subscribe'),

    # Related Content
    path('api/mock/news/articles/<str:article_id>/related', views.news_related_articles, name='news_related_articles'),

    # Sources Detail
    path('api/mock/news/sources/<str:source_id>/', views.news_source_detail, name='news_source_detail'),
    path('api/mock/news/sources/follow', views.news_follow_source, name='news_follow_source'),
    path('api/mock/news/authors/follow', views.news_follow_author, name='news_follow_author'),

    # ============ E-COMMERCE ENDPOINTS (Keep existing) ============
    path('api/mock/ecommerce/products', views.ecommerce_products, name='mock_ecommerce_products'),
    path('api/mock/ecommerce/categories', views.ecommerce_categories, name='mock_ecommerce_categories'),
    path('api/mock/ecommerce/cart', views.ecommerce_cart, name='mock_ecommerce_cart'),
    path('api/mock/ecommerce/orders', views.ecommerce_orders, name='mock_ecommerce_orders'),
    path('api/mock/ecommerce/reviews', views.ecommerce_reviews, name='mock_ecommerce_reviews'),

    # ============ RESTAURANT ENDPOINTS (Keep existing) ============
    path('api/mock/restaurant/menu', views.restaurant_menu, name='mock_restaurant_menu'),
    path('api/mock/restaurant/categories', views.restaurant_categories, name='mock_restaurant_categories'),
    path('api/mock/restaurant/offers', views.restaurant_offers, name='mock_restaurant_offers'),
    path('api/mock/restaurant/reviews', views.restaurant_reviews, name='mock_restaurant_reviews'),
    path('api/mock/restaurant/reservations', views.restaurant_reservations, name='mock_restaurant_reservations'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)