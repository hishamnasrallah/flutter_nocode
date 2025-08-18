# File: core/api/mock/recipe/urls.py
"""
URL Configuration for Recipe Mock APIs
"""

from django.urls import path
from . import views

app_name = 'mock_recipe'

urlpatterns = [
    path('all/', views.recipe_all_recipes, name='all_recipes'),
    path('<str:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('categories/', views.recipe_categories, name='categories'),
    path('search/', views.recipe_search, name='search'),
    path('favorites/', views.recipe_favorites, name='favorites'),
    path('shopping-list/', views.recipe_shopping_list, name='shopping_list'),
    path('nutritional-info/', views.recipe_nutritional_info, name='nutritional_info'),
]