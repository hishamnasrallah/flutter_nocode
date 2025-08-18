# File: core/api/mock/recipe/views.py
"""
Recipe & Meal Planner Mock API Views
Provides endpoints for recipe and meal planning applications
"""

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from core.mock_data import RecipeMockData

# Initialize mock data provider
recipe_mock = RecipeMockData()


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
    favorites = recipe_mock._generate_favorite_recipes()
    return JsonResponse(favorites, safe=False)


@csrf_exempt
@require_http_methods(["GET"])
def recipe_shopping_list(request):
    """Mock API endpoint for shopping list"""
    shopping_list = recipe_mock._generate_shopping_list()
    return JsonResponse(shopping_list, safe=False)


@csrf_exempt
@require_http_methods(["GET"])
def recipe_nutritional_info(request):
    """Mock API endpoint for nutritional info"""
    nutritional_info = recipe_mock._generate_nutritional_info()
    return JsonResponse(nutritional_info, safe=False)