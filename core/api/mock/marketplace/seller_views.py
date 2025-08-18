# =====================================
# File: core/api/mock/marketplace/seller_views.py
"""
Marketplace Seller Dashboard Mock API Views
Handles seller-specific endpoints and analytics
"""

import json
import random
import uuid
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from core.mock_data import CompleteMarketplaceMockData

marketplace_mock = CompleteMarketplaceMockData()


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
        seller['products'] = [p for p in products if p.get('sellerId') == seller_id][:20]
        return JsonResponse(seller)

    return JsonResponse({"error": "Seller not found"}, status=404)


@csrf_exempt
@require_http_methods(["GET"])
def marketplace_seller_dashboard(request):
    """Get seller dashboard data"""
    dashboard_data = marketplace_mock._generate_seller_dashboard()
    recent_orders = marketplace_mock.orders[:5] if hasattr(marketplace_mock, 'orders') else []
    dashboard_data['recentOrders'] = recent_orders
    return JsonResponse(dashboard_data)


@csrf_exempt
@require_http_methods(["GET"])
def mock_seller_products(request):
    """Mock seller products list"""
    products = []

    for i in range(20):
        products.append({
            "id": f"prod_{i}",
            "name": f"Product {i + 1}",
            "price": round(random.uniform(10, 500), 2),
            "stock": random.randint(0, 100),
            "sales": random.randint(0, 500),
            "rating": round(random.uniform(3.5, 5.0), 1),
            "status": random.choice(["active", "inactive", "out_of_stock"]),
            "image": f"https://picsum.photos/200/200?random=prod{i}"
        })

    return JsonResponse(products, safe=False)


@csrf_exempt
@require_http_methods(["GET"])
def mock_seller_orders(request):
    """Mock seller orders"""
    orders = []

    for i in range(15):
        orders.append({
            "id": f"ord_{i}",
            "order_number": f"ORD{100000 + i}",
            "customer": {
                "name": f"Customer {i + 1}",
                "email": f"customer{i + 1}@example.com"
            },
            "items": random.randint(1, 5),
            "total": round(random.uniform(50, 500), 2),
            "status": random.choice(["pending", "processing", "shipped", "delivered", "cancelled"]),
            "payment_status": random.choice(["paid", "pending", "failed"]),
            "date": (datetime.now() - timedelta(days=i)).isoformat()
        })

    return JsonResponse(orders, safe=False)


@csrf_exempt
@require_http_methods(["GET"])
def mock_seller_analytics(request):
    """Mock seller analytics data"""
    return JsonResponse({
        "revenue": {
            "daily": round(random.uniform(100, 500), 2),
            "weekly": round(random.uniform(1000, 3000), 2),
            "monthly": round(random.uniform(5000, 15000), 2),
            "yearly": round(random.uniform(50000, 150000), 2)
        },
        "conversion_rate": round(random.uniform(1.5, 5.5), 2),
        "average_order_value": round(random.uniform(50, 150), 2),
        "customer_retention": round(random.uniform(20, 60), 1),
        "top_categories": [
            {
                "name": cat,
                "sales": random.randint(100, 1000),
                "percentage": random.randint(10, 30)
            } for cat in ["Electronics", "Fashion", "Home", "Sports", "Books"]
        ],
        "traffic_sources": {
            "direct": random.randint(20, 40),
            "search": random.randint(30, 50),
            "social": random.randint(10, 30),
            "referral": random.randint(5, 20)
        }
    })


@csrf_exempt
@require_http_methods(["POST"])
def mock_create_product(request):
    """Mock create product endpoint"""
    data = json.loads(request.body)

    return JsonResponse({
        "success": True,
        "product": {
            "id": f"prod_{uuid.uuid4().hex[:8]}",
            "name": data.get("name"),
            "price": data.get("price"),
            "stock": data.get("stock", 0),
            "status": "active"
        }
    })


@csrf_exempt
@require_http_methods(["PUT"])
def mock_update_product(request, product_id):
    """Mock update product endpoint"""
    return JsonResponse({
        "success": True,
        "message": f"Product {product_id} updated successfully"
    })
