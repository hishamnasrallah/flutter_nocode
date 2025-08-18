# File: core/api/mock/news/urls.py
"""
URL Configuration for News Mock APIs
"""

from django.urls import path
from . import basic_views, comprehensive_views

app_name = 'mock_news'

urlpatterns = [
    # ============ BASIC NEWS ENDPOINTS ============
    path('articles/', basic_views.news_articles, name='articles'),
    path('sources/', basic_views.news_sources, name='sources'),
    path('categories/', basic_views.news_categories, name='categories'),
    path('breaking/', basic_views.news_breaking, name='breaking'),
    path('trending/', basic_views.news_trending, name='trending'),

    # ============ COMPREHENSIVE NEWS ENDPOINTS ============
    # Feed & Articles
    path('comprehensive/feed/', comprehensive_views.comprehensive_news_feed, name='comprehensive_feed'),
    path('comprehensive/article/<str:article_id>/', comprehensive_views.comprehensive_article_detail,
         name='article_detail'),
    path('articles/<str:article_id>/related/', comprehensive_views.news_related_articles, name='related_articles'),

    # Authors & Sources
    path('authors/', comprehensive_views.news_authors, name='authors'),
    path('authors/<str:author_id>/articles/', comprehensive_views.news_author_articles, name='author_articles'),
    path('authors/follow/', comprehensive_views.news_follow_author, name='follow_author'),
    path('sources/<str:source_id>/', comprehensive_views.news_source_detail, name='source_detail'),
    path('sources/follow/', comprehensive_views.news_follow_source, name='follow_source'),

    # Multimedia
    path('videos/', comprehensive_views.news_videos, name='videos'),
    path('podcasts/', comprehensive_views.news_podcasts, name='podcasts'),
    path('premium/', comprehensive_views.news_premium, name='premium'),
    path('local/', comprehensive_views.news_local, name='local'),

    # User Features
    path('recommendations/', comprehensive_views.news_recommendations, name='recommendations'),
    path('bookmarks/', comprehensive_views.news_bookmarks, name='bookmarks'),
    path('bookmarks/add/', comprehensive_views.news_bookmark_add, name='bookmark_add'),
    path('bookmarks/<str:article_id>/remove/', comprehensive_views.news_bookmark_remove, name='bookmark_remove'),
    path('history/', comprehensive_views.news_history, name='history'),
    path('notifications/', comprehensive_views.news_notifications, name='notifications'),

    # Search
    path('search/advanced/', comprehensive_views.news_advanced_search, name='advanced_search'),

    # Interactions
    path('articles/<str:article_id>/comments/', comprehensive_views.news_article_comments, name='article_comments'),
    path('comments/add/', comprehensive_views.news_comment_add, name='comment_add'),
    path('articles/like/', comprehensive_views.news_article_like, name='article_like'),
    path('articles/share/', comprehensive_views.news_article_share, name='article_share'),

    # Platform Features
    path('stats/', comprehensive_views.news_platform_stats, name='platform_stats'),
    path('trending-topics/', comprehensive_views.news_trending_topics, name='trending_topics'),
    path('weather/', comprehensive_views.news_weather_widget, name='weather_widget'),
    path('live-updates/', comprehensive_views.news_live_updates, name='live_updates'),

    # User Settings
    path('preferences/', comprehensive_views.news_user_preferences, name='user_preferences'),
    path('newsletter/subscribe/', comprehensive_views.news_newsletter_subscribe, name='newsletter_subscribe'),
]