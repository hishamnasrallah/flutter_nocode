from django.urls import path
from . import views

app_name = 'mock_restaurant'

urlpatterns = [
    path('menu/', views.restaurant_menu, name='menu'),
    path('categories/', views.restaurant_categories, name='categories'),
    path('offers/', views.restaurant_offers, name='offers'),
    path('reviews/', views.restaurant_reviews, name='reviews'),
    path('reservations/', views.restaurant_reservations, name='reservations'),
]