# File: core/marketplace_api_views.py
# Complete Marketplace Mock API Views

import json
import random
import uuid
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


class MarketplaceMockData:
    """Mock data provider for marketplace application"""

    def __init__(self):
        self.products = self._generate_products()
        self.categories = self._generate_categories()
        self.sellers = self._generate_sellers()
        self.reviews = self._generate_reviews()
        self.users = self._generate_users()

    def _generate_products(self):
        """Generate 2000+ products across all categories"""
        products = []
        categories = [
            "Electronics", "Fashion", "Home & Garden", "Sports & Outdoors",
            "Books & Media", "Beauty & Personal Care", "Food & Groceries",
            "Health & Wellness", "Automotive", "Toys & Games", "Pet Supplies"
        ]

        for i in range(2000):
            products.append({
                "id": str(uuid.uuid4()),
                "name": f"Product {i + 1}",
                "price": round(random.uniform(9.99, 999.99), 2),
                "image": f"https://picsum.photos/300/300?random={i}",
                "rating": round(random.uniform(3.5, 5.0), 1),
                "reviews": random.randint(10, 500),
                "seller": f"Seller {random.randint(1, 100)}",
                "category": random.choice(categories),
                "discount": random.choice([0, 10, 20, 30, 50]) if random.random() > 0.7 else 0,
                "inStock": random.choice([True, True, True, False]),
                "description": f"High quality product with excellent features and great value for money.",
                "specifications": {
                    "Brand": f"Brand {random.randint(1, 50)}",
                    "Model": f"Model-{i}",
                    "Weight": f"{round(random.uniform(0.1, 10), 1)} kg",
                    "Dimensions": f"{random.randint(10, 50)}x{random.randint(10, 50)}x{random.randint(5, 20)} cm"
                },
                "tags": random.sample(["bestseller", "new", "trending", "limited", "exclusive", "sale"],
                                      random.randint(1, 3))
            })

        return products

    def _generate_categories(self):
        """Generate category hierarchy"""
        main_categories = [
            {
                "id": "electronics",
                "name": "Electronics",
                "icon": "devices",
                "image": "https://picsum.photos/400/200?random=electronics",
                "productCount": 345,
                "subcategories": [
                    {"id": "phones", "name": "Phones & Tablets", "count": 120},
                    {"id": "computers", "name": "Computers", "count": 85},
                    {"id": "audio", "name": "Audio & Video", "count": 140},
                ]
            },
            {
                "id": "fashion",
                "name": "Fashion",
                "icon": "shopping_bag",
                "image": "https://picsum.photos/400/200?random=fashion",
                "productCount": 567,
                "subcategories": [
                    {"id": "mens", "name": "Men's Fashion", "count": 200},
                    {"id": "womens", "name": "Women's Fashion", "count": 267},
                    {"id": "kids", "name": "Kids Fashion", "count": 100},
                ]
            },
            # Add more categories...
        ]
        return main_categories

    def _generate_sellers(self):
        """Generate seller data"""
        sellers = []
        for i in range(100):
            sellers.append({
                "id": str(uuid.uuid4()),
                "name": f"Store {i + 1}",
                "logo": f"https://picsum.photos/100/100?random=seller{i}",
                "rating": round(random.uniform(4.0, 5.0), 1),
                "productCount": random.randint(10, 500),
                "followers": random.randint(100, 10000),
                "description": "Trusted seller with quality products",
                "joinDate": (datetime.now() - timedelta(days=random.randint(30, 1000))).isoformat(),
                "verified": random.choice([True, False]),
                "responseTime": f"{random.randint(1, 24)} hours",
                "policies": {
                    "shipping": "Free shipping on orders over $50",
                    "returns": "30-day return policy",
                    "warranty": "1-year warranty on all products"
                }
            })
        return sellers

    def _generate_reviews(self):
        """Generate product reviews"""
        reviews = []
        for i in range(500):
            reviews.append({
                "id": str(uuid.uuid4()),
                "productId": random.choice(self.products)["id"] if self.products else str(uuid.uuid4()),
                "rating": random.randint(3, 5),
                "title": random.choice([
                    "Great product!", "Good value", "Excellent quality",
                    "Highly recommend", "Worth the price", "Amazing!"
                ]),
                "comment": "This product exceeded my expectations. Great quality and fast delivery.",
                "userName": f"User{random.randint(1, 1000)}",
                "date": (datetime.now() - timedelta(days=random.randint(1, 90))).isoformat(),
                "helpful": random.randint(0, 50),
                "verified": random.choice([True, False]),
                "images": [f"https://picsum.photos/200/200?random=review{i}"] if random.random() > 0.7 else []
            })
        return reviews

    def _generate_users(self):
        """Generate user profiles"""
        return {
            "id": str(uuid.uuid4()),
            "name": "John Doe",
            "email": "john.doe@example.com",
            "avatar": "https://picsum.photos/100/100?random=avatar",
            "memberSince": "2023-01-15",
            "tier": "Gold",
            "points": 2450,
            "wallet": 125.50,
            "addresses": [
                {
                    "id": "addr1",
                    "name": "Home",
                    "street": "123 Main St",
                    "city": "New York",
                    "state": "NY",
                    "zipCode": "10001",
                    "isDefault": True
                }
            ]
        }


# Initialize mock data
marketplace_mock = MarketplaceMockData()


# ============= PRODUCTS ENDPOINTS =============

@csrf_exempt
@require_http_methods(["GET"])
def marketplace_products(request):
    """Get all products with optional filters"""
    category = request.GET.get('category')
    sort = request.GET.get('sort', 'relevance')
    page = int(request.GET.get('page', 1))
    limit = int(request.GET.get('limit', 20))

    products = marketplace_mock.products

    # Apply filters
    if category:
        products = [p for p in products if p['category'].lower() == category.lower()]

    # Apply sorting
    if sort == 'price_low':
        products = sorted(products, key=lambda x: x['price'])
    elif sort == 'price_high':
        products = sorted(products, key=lambda x: x['price'], reverse=True)
    elif sort == 'rating':
        products = sorted(products, key=lambda x: x['rating'], reverse=True)

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
    product = next((p for p in marketplace_mock.products if p['id'] == product_id), None)

    if product:
        # Add extra details
        product['images'] = [
            f"https://picsum.photos/600/600?random={product_id}1",
            f"https://picsum.photos/600/600?random={product_id}2",
            f"https://picsum.photos/600/600?random={product_id}3",
            f"https://picsum.photos/600/600?random={product_id}4",
        ]
        product['reviews'] = [r for r in marketplace_mock.reviews if r['productId'] == product_id][:5]
        product['relatedProducts'] = random.sample(marketplace_mock.products, min(8, len(marketplace_mock.products)))

        return JsonResponse(product)

    return JsonResponse({"error": "Product not found"}, status=404)


@csrf_exempt
@require_http_methods(["GET"])
def marketplace_search(request):
    """Search products"""
    query = request.GET.get('q', '').lower()
    products = [p for p in marketplace_mock.products if query in p['name'].lower()]
    return JsonResponse(products[:50], safe=False)


@csrf_exempt
@require_http_methods(["GET"])
def marketplace_trending(request):
    """Get trending products"""
    trending = random.sample(marketplace_mock.products, min(20, len(marketplace_mock.products)))
    for product in trending:
        product['trendScore'] = random.randint(80, 100)
    return JsonResponse(trending, safe=False)


@csrf_exempt
@require_http_methods(["GET"])
def marketplace_flash_sales(request):
    """Get flash sale items"""
    flash_sales = []
    products = random.sample(marketplace_mock.products, min(10, len(marketplace_mock.products)))

    for product in products:
        flash_sales.append({
            "id": str(uuid.uuid4()),
            "productId": product['id'],
            "product": product,
            "discountPercent": random.choice([30, 40, 50, 60, 70]),
            "endTime": (datetime.now() + timedelta(hours=random.randint(1, 24))).isoformat(),
            "stock": random.randint(5, 50)
        })

    return JsonResponse(flash_sales, safe=False)


@csrf_exempt
@require_http_methods(["GET"])
def marketplace_new_arrivals(request):
    """Get new arrival products"""
    new_arrivals = random.sample(marketplace_mock.products, min(20, len(marketplace_mock.products)))
    for product in new_arrivals:
        product['arrivalDate'] = (datetime.now() - timedelta(days=random.randint(1, 7))).isoformat()
    return JsonResponse(new_arrivals, safe=False)


@csrf_exempt
@require_http_methods(["GET"])
def marketplace_best_sellers(request):
    """Get best selling products"""
    best_sellers = random.sample(marketplace_mock.products, min(20, len(marketplace_mock.products)))
    for product in best_sellers:
        product['soldCount'] = random.randint(100, 1000)
    return JsonResponse(sorted(best_sellers, key=lambda x: x['soldCount'], reverse=True), safe=False)


@csrf_exempt
@require_http_methods(["GET"])
def marketplace_deals(request):
    """Get special deals"""
    deals = []
    for i in range(10):
        deals.append({
            "id": str(uuid.uuid4()),
            "title": f"Special Deal {i + 1}",
            "discount": f"{random.choice([20, 30, 40, 50])}% OFF",
            "validUntil": (datetime.now() + timedelta(days=random.randint(1, 30))).isoformat(),
            "products": random.sample(marketplace_mock.products, min(4, len(marketplace_mock.products)))
        })
    return JsonResponse(deals, safe=False)


# ============= CATEGORIES ENDPOINTS =============

@csrf_exempt
@require_http_methods(["GET"])
def marketplace_categories(request):
    """Get all categories"""
    return JsonResponse(marketplace_mock.categories, safe=False)


@csrf_exempt
@require_http_methods(["GET"])
def marketplace_category_products(request, category_id):
    """Get products in a specific category"""
    products = [p for p in marketplace_mock.products if p['category'].lower() == category_id.lower()]
    return JsonResponse(products[:50], safe=False)


# ============= USER ENDPOINTS =============

@csrf_exempt
@require_http_methods(["GET"])
def marketplace_user_profile(request):
    """Get user profile"""
    return JsonResponse(marketplace_mock.users)


@csrf_exempt
@require_http_methods(["GET"])
def marketplace_user_addresses(request):
    """Get user addresses"""
    return JsonResponse(marketplace_mock.users['addresses'], safe=False)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def marketplace_user_cards(request):
    """Get or add payment cards"""
    if request.method == "GET":
        cards = [
            {
                "id": "card1",
                "lastFour": "4242",
                "brand": "Visa",
                "expiryMonth": 12,
                "expiryYear": 2025,
                "isDefault": True
            },
            {
                "id": "card2",
                "lastFour": "5555",
                "brand": "Mastercard",
                "expiryMonth": 6,
                "expiryYear": 2024,
                "isDefault": False
            }
        ]
        return JsonResponse(cards, safe=False)

    return JsonResponse({"success": True, "message": "Card added successfully"})


@csrf_exempt
@require_http_methods(["GET"])
def marketplace_wishlist(request):
    """Get user wishlist"""
    wishlist = []
    products = random.sample(marketplace_mock.products, min(12, len(marketplace_mock.products)))

    for product in products:
        wishlist.append({
            "id": str(uuid.uuid4()),
            "productId": product['id'],
            "productName": product['name'],
            "price": product['price'],
            "image": product['image'],
            "addedDate": (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat()
        })

    return JsonResponse(wishlist, safe=False)


@csrf_exempt
@require_http_methods(["GET"])
def marketplace_recently_viewed(request):
    """Get recently viewed products"""
    viewed = []
    products = random.sample(marketplace_mock.products, min(10, len(marketplace_mock.products)))

    for product in products:
        viewed.append({
            "id": str(uuid.uuid4()),
            "productId": product['id'],
            "productName": product['name'],
            "price": product['price'],
            "image": product['image'],
            "viewedAt": (datetime.now() - timedelta(hours=random.randint(1, 72))).isoformat()
        })

    return JsonResponse(viewed, safe=False)


@csrf_exempt
@require_http_methods(["GET"])
def marketplace_loyalty_points(request):
    """Get loyalty points info"""
    return JsonResponse({
        "totalPoints": 2450,
        "availablePoints": 2000,
        "pendingPoints": 450,
        "tier": "Gold",
        "nextTier": "Platinum",
        "pointsToNextTier": 550,
        "history": [
            {
                "id": str(uuid.uuid4()),
                "date": (datetime.now() - timedelta(days=i)).isoformat(),
                "description": f"Purchase order #{1000 + i}",
                "points": random.choice([50, 100, 150, 200]),
                "type": "earned"
            }
            for i in range(10)
        ],
        "rewards": [
            {
                "id": str(uuid.uuid4()),
                "name": "$10 Voucher",
                "pointsRequired": 1000,
                "available": True
            },
            {
                "id": str(uuid.uuid4()),
                "name": "$25 Voucher",
                "pointsRequired": 2000,
                "available": True
            },
            {
                "id": str(uuid.uuid4()),
                "name": "$50 Voucher",
                "pointsRequired": 4000,
                "available": False
            }
        ]
    })


@csrf_exempt
@require_http_methods(["GET"])
def marketplace_wallet(request):
    """Get wallet information"""
    return JsonResponse({
        "balance": 125.50,
        "pendingAmount": 0,
        "transactions": [
            {
                "id": str(uuid.uuid4()),
                "date": (datetime.now() - timedelta(days=i)).isoformat(),
                "type": random.choice(["credit", "debit"]),
                "amount": round(random.uniform(10, 100), 2),
                "description": random.choice([
                    "Added money", "Purchase refund", "Cashback earned",
                    "Order payment", "Withdrawal"
                ]),
                "status": "completed"
            }
            for i in range(15)
        ]
    })


@csrf_exempt
@require_http_methods(["GET"])
def marketplace_referrals(request):
    """Get referral program info"""
    return JsonResponse({
        "referralCode": "MEGA2024",
        "shareUrl": "https://megamart.com/ref/MEGA2024",
        "referredUsers": random.randint(5, 20),
        "earnings": round(random.uniform(50, 500), 2),
        "pendingEarnings": round(random.uniform(10, 100), 2),
        "referralHistory": [
            {
                "id": str(uuid.uuid4()),
                "userName": f"Friend {i + 1}",
                "joinedDate": (datetime.now() - timedelta(days=random.randint(1, 60))).isoformat(),
                "earned": round(random.uniform(5, 25), 2),
                "status": random.choice(["completed", "pending"])
            }
            for i in range(10)
        ]
    })


# ============= CART & CHECKOUT ENDPOINTS =============

@csrf_exempt
@require_http_methods(["GET"])
def marketplace_cart(request):
    """Get cart items"""
    cart_items = []
    products = random.sample(marketplace_mock.products, min(3, len(marketplace_mock.products)))

    for product in products:
        quantity = random.randint(1, 3)
        cart_items.append({
            "id": str(uuid.uuid4()),
            "productId": product['id'],
            "productName": product['name'],
            "price": product['price'],
            "quantity": quantity,
            "image": product['image'],
            "subtotal": product['price'] * quantity,
            "seller": product['seller']
        })

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
    orders = []
    statuses = ["pending", "processing", "shipped", "delivered", "cancelled"]

    for i in range(20):
        order_date = datetime.now() - timedelta(days=random.randint(1, 90))
        orders.append({
            "id": str(uuid.uuid4()),
            "orderNumber": f"ORD{100000 + i}",
            "date": order_date.isoformat(),
            "status": random.choice(statuses),
            "total": round(random.uniform(50, 500), 2),
            "items": random.randint(1, 5),
            "trackingNumber": f"TRK{random.randint(100000, 999999)}" if random.random() > 0.3 else None,
            "estimatedDelivery": (order_date + timedelta(days=random.randint(3, 7))).isoformat()
        })

    return JsonResponse(sorted(orders, key=lambda x: x['date'], reverse=True), safe=False)


@csrf_exempt
@require_http_methods(["GET"])
def marketplace_order_detail(request, order_id):
    """Get order details"""
    products = random.sample(marketplace_mock.products, min(3, len(marketplace_mock.products)))

    order = {
        "id": order_id,
        "orderNumber": f"ORD{random.randint(100000, 999999)}",
        "date": (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat(),
        "status": random.choice(["processing", "shipped", "delivered"]),
        "products": [
            {
                **product,
                "quantity": random.randint(1, 3),
                "subtotal": product['price'] * random.randint(1, 3)
            }
            for product in products
        ],
        "shipping": {
            "method": "Standard Delivery",
            "cost": 5.99,
            "address": marketplace_mock.users['addresses'][0]
        },
        "payment": {
            "method": "Credit Card",
            "lastFour": "4242"
        },
        "timeline": [
            {"status": "Order Placed", "date": datetime.now().isoformat(), "completed": True},
            {"status": "Payment Confirmed", "date": datetime.now().isoformat(), "completed": True},
            {"status": "Processing", "date": datetime.now().isoformat(), "completed": True},
            {"status": "Shipped", "date": None, "completed": False},
            {"status": "Delivered", "date": None, "completed": False}
        ],
        "total": round(sum(p['price'] * random.randint(1, 3) for p in products) + 5.99, 2)
    }

    return JsonResponse(order)


@csrf_exempt
@require_http_methods(["GET"])
def marketplace_order_tracking(request, order_id):
    """Get order tracking info"""
    tracking = {
        "orderId": order_id,
        "trackingNumber": f"TRK{random.randint(100000, 999999)}",
        "status": "in_transit",
        "currentLocation": "Distribution Center, New York",
        "estimatedDelivery": (datetime.now() + timedelta(days=random.randint(1, 3))).isoformat(),
        "updates": [
            {
                "date": (datetime.now() - timedelta(days=2)).isoformat(),
                "location": "Warehouse, California",
                "status": "Package received",
                "description": "Package has been received at our warehouse"
            },
            {
                "date": (datetime.now() - timedelta(days=1)).isoformat(),
                "location": "In Transit",
                "status": "Shipped",
                "description": "Package has been shipped"
            },
            {
                "date": datetime.now().isoformat(),
                "location": "Distribution Center, New York",
                "status": "In Transit",
                "description": "Package is in transit to delivery location"
            }
        ]
    }

    return JsonResponse(tracking)


# ============= SELLER ENDPOINTS =============

@csrf_exempt
@require_http_methods(["GET"])
def marketplace_sellers(request):
    """Get all sellers"""
    return JsonResponse(marketplace_mock.sellers, safe=False)


@csrf_exempt
@require_http_methods(["GET"])
def marketplace_seller_detail(request, seller_id):
    """Get seller details"""
    seller = next((s for s in marketplace_mock.sellers if s['id'] == seller_id), None)

    if seller:
        seller['products'] = random.sample(marketplace_mock.products, min(20, len(marketplace_mock.products)))
        return JsonResponse(seller)

    return JsonResponse({"error": "Seller not found"}, status=404)


@csrf_exempt
@require_http_methods(["GET"])
def marketplace_seller_dashboard(request):
    """Get seller dashboard data"""
    return JsonResponse({
        "sales": round(random.uniform(1000, 10000), 2),
        "orders": random.randint(50, 200),
        "revenue": round(random.uniform(5000, 50000), 2),
        "products": random.randint(20, 100),
        "metrics": {
            "views": random.randint(1000, 10000),
            "conversion": round(random.uniform(1, 5), 2),
            "rating": round(random.uniform(4.0, 5.0), 1),
            "responseTime": f"{random.randint(1, 12)} hours"
        },
        "recentOrders": marketplace_orders(request).content.decode('utf-8')[:5],
        "topProducts": random.sample(marketplace_mock.products, min(5, len(marketplace_mock.products)))
    })


# ============= REVIEWS ENDPOINTS =============

@csrf_exempt
@require_http_methods(["GET"])
def marketplace_reviews(request):
    """Get all reviews"""
    return JsonResponse(marketplace_mock.reviews, safe=False)


@csrf_exempt
@require_http_methods(["GET"])
def marketplace_product_reviews(request, product_id):
    """Get reviews for a specific product"""
    reviews = [r for r in marketplace_mock.reviews if r['productId'] == product_id]
    return JsonResponse(reviews, safe=False)


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
    faqs = [
        {
            "id": str(uuid.uuid4()),
            "category": category,
            "question": f"How do I {action}?",
            "answer": f"To {action}, follow these steps..."
        }
        for category in ["Orders", "Shipping", "Returns", "Payment", "Account"]
        for action in ["track my order", "return an item", "change payment method", "update address"]
    ]

    return JsonResponse(faqs[:20], safe=False)


@csrf_exempt
@require_http_methods(["GET"])
def marketplace_notifications(request):
    """Get user notifications"""
    notifications = []
    types = ["order", "promotion", "system", "message"]

    for i in range(20):
        notifications.append({
            "id": str(uuid.uuid4()),
            "title": f"Notification {i + 1}",
            "message": "You have a new update",
            "type": random.choice(types),
            "date": (datetime.now() - timedelta(hours=random.randint(1, 72))).isoformat(),
            "read": random.choice([True, False])
        })

    return JsonResponse(notifications, safe=False)


# ============= SPECIAL FEATURES =============

@csrf_exempt
@require_http_methods(["GET"])
def marketplace_coupons(request):
    """Get available coupons"""
    coupons = []

    for i in range(10):
        coupons.append({
            "code": f"SAVE{random.randint(10, 50)}",
            "discount": f"{random.choice([10, 15, 20, 25, 30])}%",
            "minPurchase": random.choice([50, 100, 150, 200]),
            "validUntil": (datetime.now() + timedelta(days=random.randint(7, 30))).isoformat(),
            "used": random.choice([True, False]),
            "description": "Special discount on selected items"
        })

    return JsonResponse(coupons, safe=False)