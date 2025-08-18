
from django.urls import path
from . import views

app_name = 'mock_ecommerce'

urlpatterns = [
    path('products/', views.ecommerce_products, name='products'),
    path('categories/', views.ecommerce_categories, name='categories'),
    path('cart/', views.ecommerce_cart, name='cart'),
    path('orders/', views.ecommerce_orders, name='orders'),
    path('reviews/', views.ecommerce_reviews, name='reviews'),
]