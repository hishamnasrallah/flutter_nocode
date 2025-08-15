# ADD THESE TO YOUR flutter_nocode/urls.py file in the urlpatterns list

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views
from core.marketplace_api_views import marketplace_products, marketplace_product_detail, marketplace_search, \
    marketplace_trending, marketplace_deals, marketplace_new_arrivals, marketplace_flash_sales, \
    marketplace_best_sellers, marketplace_categories, marketplace_category_products, marketplace_user_profile, \
    marketplace_user_addresses, marketplace_user_cards, marketplace_wishlist, marketplace_recently_viewed, \
    marketplace_loyalty_points, marketplace_wallet, marketplace_referrals, marketplace_cart, marketplace_add_to_cart, \
    marketplace_orders, marketplace_order_detail, marketplace_order_tracking, marketplace_sellers, \
    marketplace_seller_detail, marketplace_seller_dashboard, marketplace_reviews, marketplace_product_reviews, \
    marketplace_add_review, marketplace_faqs, marketplace_notifications, marketplace_coupons
from core import auth_mock_views, chat_mock_views, stripe_mock_views, media_mock_views, seller_mock_views

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

urlpatterns += [
    # Products & Catalog
    path('api/marketplace/products', marketplace_products, name='marketplace_products'),
    path('api/marketplace/products/<str:product_id>/', marketplace_product_detail, name='marketplace_product_detail'),
    path('api/marketplace/products/search', marketplace_search, name='marketplace_search'),
    path('api/marketplace/products/trending', marketplace_trending, name='marketplace_trending'),
    path('api/marketplace/products/deals', marketplace_deals, name='marketplace_deals'),
    path('api/marketplace/products/new-arrivals', marketplace_new_arrivals, name='marketplace_new_arrivals'),
    path('api/marketplace/flash-sales', marketplace_flash_sales, name='marketplace_flash_sales'),
    path('api/marketplace/best-sellers', marketplace_best_sellers, name='marketplace_best_sellers'),

    # Categories
    path('api/marketplace/categories', marketplace_categories, name='marketplace_categories'),
    path('api/marketplace/categories/<str:category_id>/products', marketplace_category_products,
         name='marketplace_category_products'),

    # User & Account
    path('api/marketplace/user/profile', marketplace_user_profile, name='marketplace_user_profile'),
    path('api/marketplace/user/addresses', marketplace_user_addresses, name='marketplace_user_addresses'),
    path('api/marketplace/user/cards', marketplace_user_cards, name='marketplace_user_cards'),
    path('api/marketplace/user/wishlist', marketplace_wishlist, name='marketplace_wishlist'),
    path('api/marketplace/user/recently-viewed', marketplace_recently_viewed, name='marketplace_recently_viewed'),
    path('api/marketplace/user/loyalty-points', marketplace_loyalty_points, name='marketplace_loyalty_points'),
    path('api/marketplace/user/wallet', marketplace_wallet, name='marketplace_wallet'),
    path('api/marketplace/user/referrals', marketplace_referrals, name='marketplace_referrals'),

    # Cart & Checkout
    path('api/marketplace/cart', marketplace_cart, name='marketplace_cart'),
    path('api/marketplace/cart/add', marketplace_add_to_cart, name='marketplace_add_to_cart'),

    # Orders
    path('api/marketplace/orders', marketplace_orders, name='marketplace_orders'),
    path('api/marketplace/orders/<str:order_id>/', marketplace_order_detail, name='marketplace_order_detail'),
    path('api/marketplace/orders/<str:order_id>/tracking', marketplace_order_tracking,
         name='marketplace_order_tracking'),

    # Sellers
    path('api/marketplace/sellers', marketplace_sellers, name='marketplace_sellers'),
    path('api/marketplace/sellers/<str:seller_id>/', marketplace_seller_detail, name='marketplace_seller_detail'),
    path('api/marketplace/seller/dashboard', marketplace_seller_dashboard, name='marketplace_seller_dashboard'),

    # Reviews & Ratings
    path('api/marketplace/reviews', marketplace_reviews, name='marketplace_reviews'),
    path('api/marketplace/reviews/product/<str:product_id>/', marketplace_product_reviews,
         name='marketplace_product_reviews'),
    path('api/marketplace/reviews/add', marketplace_add_review, name='marketplace_add_review'),

    # Support & Help
    path('api/marketplace/faqs', marketplace_faqs, name='marketplace_faqs'),
    path('api/marketplace/notifications', marketplace_notifications, name='marketplace_notifications'),

    # Offers & Promotions
    path('api/marketplace/coupons', marketplace_coupons, name='marketplace_coupons'),
]
urlpatterns += [
    # Authentication Mock Endpoints
    path('api/mock/auth/register', auth_mock_views.mock_register, name='mock_register'),
    path('api/mock/auth/login', auth_mock_views.mock_login, name='mock_login'),
    path('api/mock/auth/logout', auth_mock_views.mock_logout, name='mock_logout'),
    path('api/mock/auth/forgot-password', auth_mock_views.mock_forgot_password, name='mock_forgot_password'),
    path('api/mock/auth/reset-password', auth_mock_views.mock_reset_password, name='mock_reset_password'),
    path('api/mock/auth/profile', auth_mock_views.mock_user_profile, name='mock_user_profile'),

    # Chat Mock Endpoints
    path('api/mock/chat/conversations', chat_mock_views.mock_conversations, name='mock_conversations'),
    path('api/mock/chat/conversations/<str:conversation_id>/messages', chat_mock_views.mock_messages,
         name='mock_messages'),
    path('api/mock/chat/send', chat_mock_views.mock_send_message, name='mock_send_message'),

    # Payment Mock Endpoints
    path('api/mock/stripe/payment-intent', stripe_mock_views.mock_create_payment_intent, name='mock_payment_intent'),
    path('api/mock/stripe/confirm', stripe_mock_views.mock_confirm_payment, name='mock_confirm_payment'),
    path('api/mock/stripe/webhook', stripe_mock_views.mock_stripe_webhook, name='mock_stripe_webhook'),
    path('api/mock/stripe/payment-methods', stripe_mock_views.mock_payment_methods, name='mock_payment_methods'),
    path('api/mock/stripe/payment-methods/add', stripe_mock_views.mock_add_payment_method,
         name='mock_add_payment_method'),

    # Media Upload Mock Endpoints
    path('api/mock/media/upload', media_mock_views.mock_upload_file, name='mock_upload_file'),
    path('api/mock/media/upload-multiple', media_mock_views.mock_upload_multiple, name='mock_upload_multiple'),
    path('api/mock/media/delete/<str:file_id>', media_mock_views.mock_delete_file, name='mock_delete_file'),

    # Seller Mock Endpoints
    path('api/mock/seller/dashboard', seller_mock_views.mock_seller_dashboard, name='mock_seller_dashboard'),
    path('api/mock/seller/products', seller_mock_views.mock_seller_products, name='mock_seller_products'),
    path('api/mock/seller/orders', seller_mock_views.mock_seller_orders, name='mock_seller_orders'),
    path('api/mock/seller/analytics', seller_mock_views.mock_seller_analytics, name='mock_seller_analytics'),
    path('api/mock/seller/products/create', seller_mock_views.mock_create_product, name='mock_create_product'),
    path('api/mock/seller/products/<str:product_id>/update', seller_mock_views.mock_update_product,
         name='mock_update_product'),
]
# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)