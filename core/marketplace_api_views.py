# File: core/marketplace_api_views.py
# Complete Marketplace Mock API Views

import json
import random
import uuid
from datetime import datetime, timedelta
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


# ============= USER ENDPOINTS =============

@csrf_exempt
@require_http_methods(["GET"])
def marketplace_user_profile(request):
    """Get user profile"""
    all_data = marketplace_mock.get_data_sources()
    profile = all_data.get('User Profile', {})
    # Ensure it's always returned as a list for consistency
    if isinstance(profile, dict):
        return JsonResponse([profile], safe=False)
    return JsonResponse(profile, safe=False)


@csrf_exempt
@require_http_methods(["GET"])
def marketplace_user_addresses(request):
    """Get user addresses"""
    all_data = marketplace_mock.get_data_sources()
    addresses = all_data.get('Addresses', [])
    return JsonResponse(addresses, safe=False)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def marketplace_user_cards(request):
    """Get or add payment cards"""
    if request.method == "GET":
        all_data = marketplace_mock.get_data_sources()
        cards = all_data.get('Payment Cards', [])
        return JsonResponse(cards, safe=False)

    return JsonResponse({"success": True, "message": "Card added successfully"})


@csrf_exempt
@require_http_methods(["GET"])
def marketplace_wishlist(request):
    """Get user wishlist"""
    all_data = marketplace_mock.get_data_sources()
    wishlist = all_data.get('Wishlist', [])
    return JsonResponse(wishlist, safe=False)


@csrf_exempt
@require_http_methods(["GET"])
def marketplace_recently_viewed(request):
    """Get recently viewed products"""
    all_data = marketplace_mock.get_data_sources()
    recently_viewed = all_data.get('Recently Viewed', [])
    return JsonResponse(recently_viewed, safe=False)


@csrf_exempt
@require_http_methods(["GET"])
def marketplace_loyalty_points(request):
    """Get loyalty points info"""
    all_data = marketplace_mock.get_data_sources()
    loyalty_data = all_data.get('Loyalty Points', {})
    # Ensure it's always returned as a list for consistency
    if isinstance(loyalty_data, dict):
        return JsonResponse([loyalty_data], safe=False)
    return JsonResponse(loyalty_data, safe=False)


@csrf_exempt
@require_http_methods(["GET"])
def marketplace_wallet(request):
    """Get wallet information"""
    all_data = marketplace_mock.get_data_sources()
    wallet_data = all_data.get('Wallet', {})
    # Ensure it's always returned as a list for consistency
    if isinstance(wallet_data, dict):
        return JsonResponse([wallet_data], safe=False)
    return JsonResponse(wallet_data, safe=False)


@csrf_exempt
@require_http_methods(["GET"])
def marketplace_referrals(request):
    """Get referral program info"""
    all_data = marketplace_mock.get_data_sources()
    referral_data = all_data.get('Referrals', {})
    # Ensure it's always returned as a list for consistency
    if isinstance(referral_data, dict):
        return JsonResponse([referral_data], safe=False)
    return JsonResponse(referral_data, safe=False)


# ============= CART & CHECKOUT ENDPOINTS =============

@csrf_exempt
@require_http_methods(["GET"])
def marketplace_cart(request):
    """Get cart items"""
    all_data = marketplace_mock.get_data_sources()
    cart_items = all_data.get('Cart', [])
    return JsonResponse(cart_items, safe=False)


@csrf_exempt
@require_http_methods(["POST"])
def marketplace_add_to_cart(request):
    """Add item to cart"""
    data = json.loads(request.body)
    return JsonResponse({
        "success": True,
        "message": "Item added to cart",
        "cartCount": random.randint(1, 10)
    })


# ============= ORDERS ENDPOINTS =============

@csrf_exempt
@require_http_methods(["GET"])
def marketplace_orders(request):
    """Get user orders"""
    all_data = marketplace_mock.get_data_sources()
    orders = all_data.get('Orders', [])
    return JsonResponse(orders, safe=False)


@csrf_exempt
@require_http_methods(["GET"])
def marketplace_order_detail(request, order_id):
    """Get order details"""
    all_data = marketplace_mock.get_data_sources()
    orders = all_data.get('Order Details', all_data.get('Orders', []))

    order = next((o for o in orders if o.get('id') == order_id), None)
    if order:
        return JsonResponse(order)

    return JsonResponse({"error": "Order not found"}, status=404)


@csrf_exempt
@require_http_methods(["GET"])
def marketplace_order_tracking(request, order_id):
    """Get order tracking info"""
    all_data = marketplace_mock.get_data_sources()
    tracking_data = all_data.get('Order Tracking', [])

    # Find tracking for specific order or return first available
    if isinstance(tracking_data, list) and tracking_data:
        return JsonResponse(tracking_data[0])
    elif isinstance(tracking_data, dict):
        return JsonResponse(tracking_data)

    # Default tracking if not found
    return JsonResponse({
        "orderId": order_id,
        "status": "processing",
        "updates": []
    })


# ============= SELLER ENDPOINTS =============

@csrf_exempt
@require_http_methods(["GET"])
def marketplace_sellers(request):
    """Get all sellers"""
    all_data = marketplace_mock.get_data_sources()
    sellers = all_data.get('Sellers', [])
    return JsonResponse(sellers, safe=False)


@csrf_exempt
@require_http_methods(["GET"])
def marketplace_seller_detail(request, seller_id):
    """Get seller details"""
    all_data = marketplace_mock.get_data_sources()
    sellers = all_data.get('Seller Details', all_data.get('Sellers', []))
    products = all_data.get('Products', [])

    seller = next((s for s in sellers if s.get('id') == seller_id), None)

    if seller:
        # Add products from this seller
        seller['products'] = [p for p in products if p.get('sellerId') == seller_id][:20]
        return JsonResponse(seller)

    return JsonResponse({"error": "Seller not found"}, status=404)


@csrf_exempt
@require_http_methods(["GET"])
def marketplace_seller_dashboard(request):
    """Get seller dashboard data"""
    # Get dashboard data from comprehensive mock
    dashboard_data = marketplace_mock._generate_seller_dashboard()

    # Add recent orders (first 5)
    recent_orders = marketplace_mock.orders[:5] if hasattr(marketplace_mock, 'orders') else []
    dashboard_data['recentOrders'] = recent_orders

    return JsonResponse(dashboard_data)


# ============= REVIEWS ENDPOINTS =============

@csrf_exempt
@require_http_methods(["GET"])
def marketplace_reviews(request):
    """Get all reviews"""
    all_data = marketplace_mock.get_data_sources()
    reviews = all_data.get('Reviews', [])
    return JsonResponse(reviews, safe=False)


@csrf_exempt
@require_http_methods(["GET"])
def marketplace_product_reviews(request, product_id):
    """Get reviews for a specific product"""
    all_data = marketplace_mock.get_data_sources()
    reviews = all_data.get('Reviews', [])

    product_reviews = [r for r in reviews if r.get('productId') == product_id]
    return JsonResponse(product_reviews, safe=False)


@csrf_exempt
@require_http_methods(["POST"])
def marketplace_add_review(request):
    """Add a product review"""
    data = json.loads(request.body)

    review = {
        "id": str(uuid.uuid4()),
        "productId": data.get('productId'),
        "rating": data.get('rating', 5),
        "title": data.get('title', ''),
        "comment": data.get('comment', ''),
        "userName": data.get('userName', 'Anonymous'),
        "date": datetime.now().isoformat(),
        "helpful": 0,
        "verified": True
    }

    return JsonResponse({"success": True, "review": review})


# ============= SUPPORT ENDPOINTS =============

@csrf_exempt
@require_http_methods(["GET"])
def marketplace_faqs(request):
    """Get FAQs"""
    all_data = marketplace_mock.get_data_sources()
    faqs = all_data.get('FAQs', [])
    return JsonResponse(faqs, safe=False)


@csrf_exempt
@require_http_methods(["GET"])
def marketplace_notifications(request):
    """Get user notifications"""
    all_data = marketplace_mock.get_data_sources()
    notifications = all_data.get('Notifications', [])
    return JsonResponse(notifications, safe=False)


# ============= SPECIAL FEATURES =============

@csrf_exempt
@require_http_methods(["GET"])
def marketplace_coupons(request):
    """Get available coupons"""
    all_data = marketplace_mock.get_data_sources()
    coupons = all_data.get('Coupons', [])
    return JsonResponse(coupons, safe=False)