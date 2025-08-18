# File: core/api/mock/marketplace/urls.py
"""
URL Configuration for Marketplace Mock APIs
"""

from django.urls import path
from . import product_views, user_views, order_views, seller_views, review_views, support_views

app_name = 'mock_marketplace'

urlpatterns = [
    # Product & Catalog
    path('products/', product_views.marketplace_products, name='products'),
    path('products/<str:product_id>/', product_views.marketplace_product_detail, name='product_detail'),
    path('products/search/', product_views.marketplace_search, name='search'),
    path('products/trending/', product_views.marketplace_trending, name='trending'),
    path('products/deals/', product_views.marketplace_deals, name='deals'),
    path('products/new-arrivals/', product_views.marketplace_new_arrivals, name='new_arrivals'),
    path('flash-sales/', product_views.marketplace_flash_sales, name='flash_sales'),
    path('best-sellers/', product_views.marketplace_best_sellers, name='best_sellers'),

    # Categories
    path('categories/', product_views.marketplace_categories, name='categories'),
    path('categories/<str:category_id>/products/', product_views.marketplace_category_products,
         name='category_products'),

    # User & Account
    path('user/profile/', user_views.marketplace_user_profile, name='user_profile'),
    path('user/addresses/', user_views.marketplace_user_addresses, name='user_addresses'),
    path('user/cards/', user_views.marketplace_user_cards, name='user_cards'),
    path('user/wishlist/', user_views.marketplace_wishlist, name='wishlist'),
    path('user/recently-viewed/', user_views.marketplace_recently_viewed, name='recently_viewed'),
    path('user/loyalty-points/', user_views.marketplace_loyalty_points, name='loyalty_points'),
    path('user/wallet/', user_views.marketplace_wallet, name='wallet'),
    path('user/referrals/', user_views.marketplace_referrals, name='referrals'),

    # Cart & Orders
    path('cart/', order_views.marketplace_cart, name='cart'),
    path('cart/add/', order_views.marketplace_add_to_cart, name='add_to_cart'),
    path('orders/', order_views.marketplace_orders, name='orders'),
    path('orders/<str:order_id>/', order_views.marketplace_order_detail, name='order_detail'),
    path('orders/<str:order_id>/tracking/', order_views.marketplace_order_tracking, name='order_tracking'),

    # Sellers
    path('sellers/', seller_views.marketplace_sellers, name='sellers'),
    path('sellers/<str:seller_id>/', seller_views.marketplace_seller_detail, name='seller_detail'),
    path('seller/dashboard/', seller_views.marketplace_seller_dashboard, name='seller_dashboard'),
    path('seller/products/', seller_views.mock_seller_products, name='seller_products'),
    path('seller/orders/', seller_views.mock_seller_orders, name='seller_orders'),
    path('seller/analytics/', seller_views.mock_seller_analytics, name='seller_analytics'),
    path('seller/products/create/', seller_views.mock_create_product, name='create_product'),
    path('seller/products/<str:product_id>/update/', seller_views.mock_update_product, name='update_product'),

    # Reviews
    path('reviews/', review_views.marketplace_reviews, name='reviews'),
    path('reviews/product/<str:product_id>/', review_views.marketplace_product_reviews, name='product_reviews'),
    path('reviews/add/', review_views.marketplace_add_review, name='add_review'),

    # Support
    path('faqs/', support_views.marketplace_faqs, name='faqs'),
    path('notifications/', support_views.marketplace_notifications, name='notifications'),
    path('coupons/', support_views.marketplace_coupons, name='coupons'),
]