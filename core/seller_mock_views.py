"""
Mock Seller Dashboard API Views
File: core/seller_mock_views.py
"""

import json
import random
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


@csrf_exempt
@require_http_methods(["GET"])
def mock_seller_dashboard(request):
    """Mock seller dashboard data"""
    return JsonResponse({
        "stats": {
            "total_sales": 45678.90,
            "monthly_sales": 5432.10,
            "total_orders": 234,
            "pending_orders": 12,
            "total_products": 56,
            "out_of_stock": 3,
            "rating": 4.7,
            "reviews": 189
        },
        "recent_orders": [
            {
                "id": f"ord_{i}",
                "customer": f"Customer {i + 1}",
                "total": round(random.uniform(50, 500), 2),
                "status": random.choice(["pending", "processing", "shipped", "delivered"]),
                "date": (datetime.now() - timedelta(days=i)).isoformat()
            } for i in range(5)
        ],
        "top_products": [
            {
                "id": f"prod_{i}",
                "name": f"Product {i + 1}",
                "sales": random.randint(10, 100),
                "revenue": round(random.uniform(1000, 5000), 2),
                "stock": random.randint(0, 50)
            } for i in range(5)
        ],
        "sales_chart": {
            "labels": [(datetime.now() - timedelta(days=i)).strftime("%b %d") for i in range(6, -1, -1)],
            "data": [random.randint(100, 1000) for _ in range(7)]
        }
    })


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