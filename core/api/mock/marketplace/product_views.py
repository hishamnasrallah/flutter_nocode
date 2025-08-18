# File: core/api/mock/marketplace/product_views.py
"""
Marketplace Product-related Mock API Views
Handles all product catalog, search, and category endpoints
"""

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from core.mock_data import CompleteMarketplaceMockData

# Initialize mock data
marketplace_mock = CompleteMarketplaceMockData()


# ============= PRODUCTS ENDPOINTS =============

@csrf_exempt
@require_http_methods(["GET"])
def marketplace_products(request):
    """Get all products with optional filters"""
    category = request.GET.get('category')
    sort = request.GET.get('sort', 'relevance')
    page = int(request.GET.get('page', 1))
    limit = int(request.GET.get('limit', 20))

    # Get products from comprehensive mock data
    all_data = marketplace_mock.get_data_sources()
    products = all_data.get('Products', [])

    # Apply filters
    if category:
        products = [p for p in products if p.get('category', '').lower() == category.lower()]

    # Apply sorting
    if sort == 'price_low':
        products = sorted(products, key=lambda x: x.get('price', 0))
    elif sort == 'price_high':
        products = sorted(products, key=lambda x: x.get('price', 0), reverse=True)
    elif sort == 'rating':
        products = sorted(products, key=lambda x: x.get('rating', 0), reverse=True)

    # Pagination
    start = (page - 1) * limit
    end = start + limit

    return JsonResponse({
        "products": products[start:end],
        "total": len(products),
        "page": page,
        "totalPages": (len(products) + limit - 1) // limit
    })


@csrf_exempt
@require_http_methods(["GET"])
def marketplace_product_detail(request, product_id):
    """Get detailed product information"""
    all_data = marketplace_mock.get_data_sources()
    products = all_data.get('Product Details', all_data.get('Products', []))
    reviews = all_data.get('Reviews', [])

    product = next((p for p in products if p.get('id') == product_id), None)

    if product:
        # Add reviews for this product
        product['reviews'] = [r for r in reviews if r.get('productId') == product_id][:5]
        # Add related products
        product['relatedProducts'] = random.sample(products, min(8, len(products)))
        return JsonResponse(product)

    return JsonResponse({"error": "Product not found"}, status=404)


@csrf_exempt
@require_http_methods(["GET"])
def marketplace_search(request):
    """Search products"""
    query = request.GET.get('q', '').lower()
    all_data = marketplace_mock.get_data_sources()
    products = all_data.get('Products', [])

    results = [p for p in products if query in p.get('name', '').lower() or query in p.get('description', '').lower()]
    return JsonResponse(results[:50], safe=False)


@csrf_exempt
@require_http_methods(["GET"])
def marketplace_trending(request):
    """Get trending products"""
    all_data = marketplace_mock.get_data_sources()
    trending = all_data.get('Trending Products', [])
    return JsonResponse(trending[:20], safe=False)


@csrf_exempt
@require_http_methods(["GET"])
def marketplace_flash_sales(request):
    """Get flash sale items"""
    all_data = marketplace_mock.get_data_sources()
    flash_sales = all_data.get('Flash Sales', [])
    return JsonResponse(flash_sales, safe=False)


@csrf_exempt
@require_http_methods(["GET"])
def marketplace_new_arrivals(request):
    """Get new arrival products"""
    all_data = marketplace_mock.get_data_sources()
    new_arrivals = all_data.get('New Arrivals', [])
    return JsonResponse(new_arrivals[:20], safe=False)


@csrf_exempt
@require_http_methods(["GET"])
def marketplace_best_sellers(request):
    """Get best selling products"""
    all_data = marketplace_mock.get_data_sources()
    best_sellers = all_data.get('Best Sellers', [])
    return JsonResponse(best_sellers[:20], safe=False)


@csrf_exempt
@require_http_methods(["GET"])
def marketplace_deals(request):
    """Get special deals"""
    all_data = marketplace_mock.get_data_sources()
    deals = all_data.get('Deals', [])
    return JsonResponse(deals, safe=False)


# ============= CATEGORIES ENDPOINTS =============

@csrf_exempt
@require_http_methods(["GET"])
def marketplace_categories(request):
    """Get all categories"""
    all_data = marketplace_mock.get_data_sources()
    categories = all_data.get('Categories', [])
    return JsonResponse(categories, safe=False)


@csrf_exempt
@require_http_methods(["GET"])
def marketplace_category_products(request, category_id):
    """Get products in a specific category"""
    all_data = marketplace_mock.get_data_sources()
    products = all_data.get('Products', [])

    filtered = [p for p in products if p.get('categoryId', '').lower() == category_id.lower() or
                p.get('category', '').lower() == category_id.lower()]
    return JsonResponse(filtered[:50], safe=False)


# Add missing import
import random