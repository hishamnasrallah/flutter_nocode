from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Mock API endpoints for development
    # News APIs
    path('api/mock/news/articles', views.news_articles, name='mock_news_articles'),
    path('api/mock/news/sources', views.news_sources, name='mock_news_sources'),
    path('api/mock/news/categories', views.news_categories, name='mock_news_categories'),
    path('api/mock/news/breaking', views.news_breaking, name='mock_news_breaking'),
    path('api/mock/news/trending', views.news_trending, name='mock_news_trending'),

    # E-commerce APIs
    path('api/mock/ecommerce/products', views.ecommerce_products, name='mock_ecommerce_products'),
    path('api/mock/ecommerce/categories', views.ecommerce_categories, name='mock_ecommerce_categories'),
    path('api/mock/ecommerce/cart', views.ecommerce_cart, name='mock_ecommerce_cart'),
    path('api/mock/ecommerce/orders', views.ecommerce_orders, name='mock_ecommerce_orders'),
    path('api/mock/ecommerce/reviews', views.ecommerce_reviews, name='mock_ecommerce_reviews'),

    # Restaurant APIs
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