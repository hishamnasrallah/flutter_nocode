"""
Complete Marketplace Mock Data Provider
File: core/mock_data/marketplace_mock_data.py

Provides comprehensive mock data for all 40+ pages of the marketplace application
"""

from .base_mock_data import BaseMockData
import random
import uuid
from datetime import datetime, timedelta


class MarketplaceMockData(BaseMockData):
    """Complete mock data provider for marketplace application"""

    def __init__(self):
        self.products = self._generate_products()
        self.categories = self._generate_categories()
        self.sellers = self._generate_sellers()
        self.reviews = self._generate_reviews()
        self.orders = self._generate_orders()
        self.users = self._generate_users()
        self.cart_items = self._generate_cart_items()
        self.wishlist = self._generate_wishlist()
        self.addresses = self._generate_addresses()
        self.notifications = self._generate_notifications()

    def get_data_sources(self):
        """Return all data sources"""
        return {
            "Products": self.products,
            "Categories": self.categories,
            "Cart": self.cart_items,
            "Orders": self.orders,
            "Reviews": self.reviews,
            "Sellers": self.sellers,
            "Wishlist": self.wishlist,
            "UserProfile": self.users,
            "Addresses": self.addresses,
            "Notifications": self.notifications,
        }

    def get_sample_images(self):
        """Return sample images for all categories"""
        return {
            "products": [f"https://picsum.photos/300/300?random=prod{i}" for i in range(1, 101)],
            "categories": [f"https://picsum.photos/200/200?random=cat{i}" for i in range(1, 21)],
            "banners": [f"https://picsum.photos/800/400?random=banner{i}" for i in range(1, 11)],
            "sellers": [f"https://picsum.photos/100/100?random=seller{i}" for i in range(1, 51)],
            "avatars": [f"https://picsum.photos/150/150?random=avatar{i}" for i in range(1, 21)],
        }

    def _generate_products(self):
        """Generate 500+ products across all categories"""
        products = []

        categories_map = {
            "Electronics": ["Smartphones", "Laptops", "Tablets", "Headphones", "Cameras", "Gaming", "Smart Home"],
            "Fashion": ["Men's Clothing", "Women's Clothing", "Shoes", "Accessories", "Bags", "Watches", "Jewelry"],
            "Home & Garden": ["Furniture", "Kitchen", "Bedding", "Decor", "Garden Tools", "Lighting", "Storage"],
            "Sports": ["Fitness", "Outdoor", "Team Sports", "Water Sports", "Cycling", "Running", "Yoga"],
            "Books": ["Fiction", "Non-Fiction", "Educational", "Comics", "Magazines", "E-books", "Audiobooks"],
            "Toys": ["Action Figures", "Board Games", "Educational", "Dolls", "Building Sets", "Outdoor Toys",
                     "Puzzles"],
            "Beauty": ["Skincare", "Makeup", "Hair Care", "Fragrances", "Tools", "Men's Grooming", "Nail Care"],
            "Automotive": ["Parts", "Accessories", "Tools", "Cleaning", "Electronics", "Tires", "Oil & Fluids"],
            "Food": ["Snacks", "Beverages", "Organic", "International", "Frozen", "Dairy", "Bakery"],
            "Health": ["Vitamins", "Supplements", "Medical", "Fitness", "Personal Care", "First Aid", "Wellness"],
        }

        brands_map = {
            "Electronics": ["Apple", "Samsung", "Sony", "LG", "Dell", "HP", "Asus", "Lenovo", "Microsoft", "Google"],
            "Fashion": ["Nike", "Adidas", "Zara", "H&M", "Gucci", "Louis Vuitton", "Prada", "Versace", "Calvin Klein",
                        "Tommy Hilfiger"],
            "Home & Garden": ["IKEA", "Ashley", "Wayfair", "Home Depot", "Pottery Barn", "West Elm", "CB2",
                              "Crate & Barrel"],
            "Sports": ["Nike", "Adidas", "Under Armour", "Puma", "Reebok", "New Balance", "Asics", "Fila", "Wilson",
                       "Spalding"],
            "Books": ["Penguin", "HarperCollins", "Random House", "Simon & Schuster", "Macmillan", "Hachette",
                      "Scholastic"],
            "Toys": ["LEGO", "Mattel", "Hasbro", "Fisher-Price", "Nerf", "Barbie", "Hot Wheels", "Disney", "Marvel",
                     "Pokemon"],
        }

        product_names = {
            "Electronics": [
                "Pro Max Smartphone 256GB", "Gaming Laptop RTX 4080", "Wireless Noise-Cancelling Headphones",
                "4K OLED Smart TV 65\"", "Mirrorless Camera Full Frame", "Gaming Console Next Gen",
                "Smart Watch Series 8", "Tablet Pro 12.9\"", "Wireless Earbuds Pro", "Smart Speaker with Display",
                "Gaming Mouse RGB", "Mechanical Keyboard", "Webcam 4K", "External SSD 2TB", "Power Bank 20000mAh"
            ],
            "Fashion": [
                "Premium Cotton T-Shirt", "Slim Fit Jeans", "Running Shoes Pro", "Leather Jacket",
                "Summer Dress Floral", "Business Suit 3-Piece", "Sports Bra High Support", "Winter Coat Waterproof",
                "Sneakers Limited Edition", "Crossbody Bag Leather", "Sunglasses Polarized", "Watch Automatic",
                "Scarf Cashmere", "Belt Genuine Leather", "Wallet RFID Protection"
            ],
            "Home & Garden": [
                "Modular Sofa L-Shaped", "Standing Desk Electric", "Memory Foam Mattress Queen", "Air Purifier HEPA",
                "Coffee Machine Espresso", "Cookware Set 12-Piece", "Robot Vacuum Smart", "LED Smart Bulbs 4-Pack",
                "Throw Pillows Set", "Area Rug 8x10", "Wall Art Canvas Set", "Plant Pots Ceramic Set",
                "Garden Tools Set", "Outdoor Furniture Set", "Storage Ottoman"
            ],
        }

        # Generate products
        product_id = 1
        for category, subcategories in categories_map.items():
            brands = brands_map.get(category, ["Brand A", "Brand B", "Brand C"])
            names = product_names.get(category, ["Product"])

            for _ in range(50):  # 50 products per category
                name = random.choice(names)
                brand = random.choice(brands)
                subcategory = random.choice(subcategories)

                price = round(random.uniform(9.99, 2999.99), 2)
                discount = random.choice([0, 10, 15, 20, 25, 30, 40, 50])
                original_price = round(price / (1 - discount / 100), 2) if discount > 0 else price

                product = {
                    "id": str(product_id),
                    "name": f"{brand} {name}",
                    "description": f"High-quality {name.lower()} from {brand}. {self._generate_product_description(category)}",
                    "price": price,
                    "originalPrice": original_price,
                    "discount": discount,
                    "images": [
                        f"https://picsum.photos/600/600?random=prod{product_id}a",
                        f"https://picsum.photos/600/600?random=prod{product_id}b",
                        f"https://picsum.photos/600/600?random=prod{product_id}c",
                    ],
                    "category": category,
                    "subcategory": subcategory,
                    "brand": brand,
                    "rating": round(random.uniform(3.5, 5.0), 1),
                    "reviewCount": random.randint(10, 5000),
                    "stock": random.randint(0, 500),
                    "sku": f"SKU-{product_id:06d}",
                    "tags": self._generate_tags(category, subcategory),
                    "seller": random.choice(self.sellers)["name"] if hasattr(self,
                                                                             'sellers') else f"Seller {random.randint(1, 20)}",
                    "sellerId": str(random.randint(1, 50)),
                    "shippingCost": round(random.uniform(0, 19.99), 2) if random.random() > 0.3 else 0,
                    "deliveryDays": random.randint(1, 7),
                    "features": self._generate_features(category),
                    "specifications": self._generate_specifications(category),
                    "soldCount": random.randint(0, 10000),
                    "viewCount": random.randint(100, 50000),
                    "isNew": random.random() > 0.8,
                    "isBestSeller": random.random() > 0.9,
                    "isFeatured": random.random() > 0.85,
                    "isDeal": discount > 30,
                }

                products.append(product)
                product_id += 1

        return products

    def _generate_product_description(self, category):
        """Generate detailed product description"""
        descriptions = {
            "Electronics": "Features cutting-edge technology with premium build quality. Designed for professional use with advanced features and long-lasting battery life.",
            "Fashion": "Made from premium materials with attention to detail. Comfortable fit and stylish design suitable for any occasion.",
            "Home & Garden": "Transform your living space with this elegant and functional piece. Durable construction ensures years of reliable use.",
            "Sports": "Engineered for peak performance with professional-grade materials. Enhance your training and achieve your fitness goals.",
            "Books": "Engaging content that will captivate your imagination. Professionally edited and beautifully presented.",
            "Toys": "Safe, educational, and fun for children. Promotes creativity and learning through interactive play.",
        }
        return descriptions.get(category, "Premium quality product with excellent features and reliable performance.")

    def _generate_tags(self, category, subcategory):
        """Generate relevant tags"""
        base_tags = ["trending", "popular", "premium", "authentic", "warranty"]
        category_tags = {
            "Electronics": ["tech", "gadget", "smart", "wireless", "innovative"],
            "Fashion": ["style", "comfort", "designer", "trendy", "seasonal"],
            "Home & Garden": ["modern", "eco-friendly", "space-saving", "decorative", "functional"],
            "Sports": ["fitness", "athletic", "performance", "outdoor", "training"],
        }

        tags = base_tags[:random.randint(2, 4)]
        tags.extend(random.sample(category_tags.get(category, []), min(3, len(category_tags.get(category, [])))))
        tags.append(subcategory.lower().replace(" ", "-"))

        return tags

    def _generate_features(self, category):
        """Generate product features"""
        features_map = {
            "Electronics": [
                "High-resolution display",
                "Long battery life",
                "Fast charging support",
                "Wireless connectivity",
                "Water resistant",
                "Premium build quality",
                "Latest processor",
                "Expandable storage",
            ],
            "Fashion": [
                "Premium fabric",
                "Machine washable",
                "Breathable material",
                "UV protection",
                "Moisture-wicking",
                "Stretchable fabric",
                "Reinforced stitching",
                "Comfortable fit",
            ],
            "Home & Garden": [
                "Easy assembly",
                "Space-saving design",
                "Eco-friendly materials",
                "Multi-functional",
                "Weather resistant",
                "Easy maintenance",
                "Modern design",
                "Energy efficient",
            ],
        }

        features = features_map.get(category, ["High quality", "Durable", "Reliable", "Efficient"])
        return random.sample(features, min(5, len(features)))

    def _generate_specifications(self, category):
        """Generate technical specifications"""
        specs_map = {
            "Electronics": {
                "Processor": "Latest Generation",
                "RAM": "8GB/16GB/32GB",
                "Storage": "256GB/512GB/1TB",
                "Display": "OLED/LCD/AMOLED",
                "Battery": "4000-5000mAh",
                "Connectivity": "WiFi 6, Bluetooth 5.0",
            },
            "Fashion": {
                "Material": "Cotton/Polyester/Wool",
                "Sizes": "XS, S, M, L, XL, XXL",
                "Colors": "Multiple options",
                "Care": "Machine washable",
                "Fit": "Regular/Slim/Relaxed",
                "Season": "All season",
            },
            "Home & Garden": {
                "Dimensions": "Various sizes available",
                "Material": "Wood/Metal/Plastic",
                "Weight Capacity": "50-500 lbs",
                "Assembly": "Required/Not required",
                "Warranty": "1-5 years",
                "Color Options": "Multiple",
            },
        }

        return specs_map.get(category, {"General": "Standard specifications"})

    def _generate_categories(self):
        """Generate all marketplace categories"""
        categories = [
            {
                "id": "1",
                "name": "Electronics",
                "icon": "devices",
                "image": "https://picsum.photos/400/400?random=electronics",
                "productCount": 245,
                "subcategories": ["Smartphones", "Laptops", "Audio", "Gaming", "Smart Home"],
            },
            {
                "id": "2",
                "name": "Fashion",
                "icon": "checkroom",
                "image": "https://picsum.photos/400/400?random=fashion",
                "productCount": 532,
                "subcategories": ["Men", "Women", "Kids", "Shoes", "Accessories"],
            },
            {
                "id": "3",
                "name": "Home & Garden",
                "icon": "home",
                "image": "https://picsum.photos/400/400?random=home",
                "productCount": 178,
                "subcategories": ["Furniture", "Kitchen", "Decor", "Garden", "Storage"],
            },
            {
                "id": "4",
                "name": "Sports",
                "icon": "sports",
                "image": "https://picsum.photos/400/400?random=sports",
                "productCount": 156,
                "subcategories": ["Fitness", "Outdoor", "Team Sports", "Water Sports", "Cycling"],
            },
            {
                "id": "5",
                "name": "Books",
                "icon": "menu_book",
                "image": "https://picsum.photos/400/400?random=books",
                "productCount": 892,
                "subcategories": ["Fiction", "Non-Fiction", "Educational", "Comics", "E-books"],
            },
            {
                "id": "6",
                "name": "Toys",
                "icon": "toys",
                "image": "https://picsum.photos/400/400?random=toys",
                "productCount": 234,
                "subcategories": ["Action Figures", "Board Games", "Educational", "Outdoor", "Puzzles"],
            },
            {
                "id": "7",
                "name": "Beauty",
                "icon": "face",
                "image": "https://picsum.photos/400/400?random=beauty",
                "productCount": 412,
                "subcategories": ["Skincare", "Makeup", "Hair Care", "Fragrances", "Tools"],
            },
            {
                "id": "8",
                "name": "Automotive",
                "icon": "directions_car",
                "image": "https://picsum.photos/400/400?random=auto",
                "productCount": 198,
                "subcategories": ["Parts", "Accessories", "Tools", "Cleaning", "Electronics"],
            },
            {
                "id": "9",
                "name": "Food",
                "icon": "restaurant",
                "image": "https://picsum.photos/400/400?random=food",
                "productCount": 367,
                "subcategories": ["Snacks", "Beverages", "Organic", "International", "Frozen"],
            },
            {
                "id": "10",
                "name": "Health",
                "icon": "health_and_safety",
                "image": "https://picsum.photos/400/400?random=health",
                "productCount": 289,
                "subcategories": ["Vitamins", "Supplements", "Medical", "Fitness", "Personal Care"],
            },
        ]

        return categories

    def _generate_sellers(self):
        """Generate seller profiles"""
        sellers = []

        seller_names = [
            "TechHub Store", "Fashion Forward", "Home Essentials", "Sports Pro Shop", "Book Haven",
            "Toy Kingdom", "Beauty Boutique", "Auto Parts Plus", "Gourmet Foods", "Health & Wellness",
            "Gadget Galaxy", "Style Station", "Comfort Home", "Athlete's Choice", "Reading Corner",
            "Kids Paradise", "Glamour Shop", "Car Care Center", "Fresh Market", "Vita Store",
            "Digital Dreams", "Trendy Threads", "Living Spaces", "Fitness First", "Page Turner",
            "Play Time", "Beauty Bliss", "Motor Works", "Tasty Treats", "Wellness World",
            "Smart Tech", "Chic Boutique", "Cozy Corner", "Sport Zone", "Book World",
            "Fun Factory", "Glow Up", "Drive Smart", "Food Hub", "Health Plus",
            "Innovate Tech", "Fashion Hub", "Home Style", "Active Life", "Literary Lane",
            "Happy Kids", "Beauty Bar", "Auto Expert", "Delicious Deals", "Care Center",
        ]

        for i, name in enumerate(seller_names, 1):
            seller = {
                "id": str(i),
                "name": name,
                "logo": f"https://picsum.photos/200/200?random=seller{i}",
                "rating": round(random.uniform(4.0, 5.0), 1),
                "productCount": random.randint(50, 1000),
                "followers": random.randint(100, 50000),
                "description": f"{name} - Your trusted seller for quality products. Fast shipping and excellent customer service.",
                "joinedDate": (datetime.now() - timedelta(days=random.randint(30, 1825))).strftime("%Y-%m-%d"),
                "responseTime": f"{random.randint(1, 24)} hours",
                "shippingSpeed": random.choice(["Same Day", "Next Day", "2-3 Days", "3-5 Days"]),
                "returnPolicy": "30-day return policy",
                "verified": random.random() > 0.3,
                "totalSales": random.randint(100, 100000),
                "location": random.choice(["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia"]),
            }
            sellers.append(seller)

        return sellers

    def _generate_reviews(self):
        """Generate product reviews"""
        reviews = []

        review_titles = [
            "Excellent product!", "Great value for money", "Highly recommended", "Good quality",
            "As described", "Fast shipping", "Love it!", "Perfect!", "Amazing quality",
            "Worth every penny", "Exceeded expectations", "Very satisfied", "Great purchase",
            "Fantastic!", "Superb quality", "Exactly what I needed", "5 stars!", "Outstanding",
            "Best purchase ever", "Impressed with quality"
        ]

        review_comments = [
            "The product quality is excellent and exactly as described. Very happy with my purchase.",
            "Fast delivery and great packaging. Product works perfectly.",
            "Amazing value for money. Would definitely buy again.",
            "High quality materials and excellent craftsmanship. Highly recommended!",
            "Received the product quickly and it exceeded my expectations.",
            "Very satisfied with this purchase. Great seller and fast shipping.",
            "Product is exactly as shown in the pictures. Great quality!",
            "Excellent customer service and product quality. 5 stars!",
            "Love this product! Works perfectly and looks great.",
            "Best purchase I've made in a while. Highly recommend to everyone.",
        ]

        user_names = ["John D.", "Sarah M.", "Mike R.", "Emily K.", "David L.", "Lisa W.", "Tom B.", "Amy C.",
                      "Chris P.", "Jessica T."]

        for i in range(200):
            review = {
                "id": str(uuid.uuid4()),
                "productId": str(random.randint(1, 100)),
                "userId": str(uuid.uuid4()),
                "userName": random.choice(user_names),
                "rating": random.randint(3, 5),
                "title": random.choice(review_titles),
                "comment": random.choice(review_comments),
                "date": (datetime.now() - timedelta(days=random.randint(1, 365))).isoformat(),
                "helpful": random.randint(0, 500),
                "verified": random.random() > 0.2,
                "images": [f"https://picsum.photos/200/200?random=review{i}"] if random.random() > 0.7 else [],
            }
            reviews.append(review)

        return reviews

    def _generate_orders(self):
        """Generate order history"""
        orders = []

        for i in range(50):
            order_date = datetime.now() - timedelta(days=random.randint(1, 365))
            status = random.choice(["Delivered", "Shipped", "Processing", "Confirmed", "Cancelled"])

            order = {
                "id": str(uuid.uuid4()),
                "orderNumber": f"ORD-2024-{i + 1000:04d}",
                "date": order_date.isoformat(),
                "status": status,
                "total": round(random.uniform(29.99, 999.99), 2),
                "items": random.randint(1, 10),
                "trackingNumber": f"TRK{random.randint(100000, 999999)}" if status in ["Shipped",
                                                                                       "Delivered"] else None,
                "estimatedDelivery": (order_date + timedelta(days=random.randint(3, 7))).strftime("%Y-%m-%d"),
                "shippingAddress": "123 Main St, New York, NY 10001",
                "paymentMethod": random.choice(["Credit Card", "PayPal", "Apple Pay", "Google Pay"]),
                "products": self._generate_order_products(),
            }
            orders.append(order)

        return orders

    def _generate_order_products(self):
        """Generate products for an order"""
        num_products = random.randint(1, 5)
        products = []

        for _ in range(num_products):
            products.append({
                "name": f"Product {random.randint(1, 100)}",
                "quantity": random.randint(1, 3),
                "price": round(random.uniform(9.99, 299.99), 2),
                "image": f"https://picsum.photos/100/100?random=order{random.randint(1, 1000)}",
            })

        return products

    def _generate_users(self):
        """Generate user profiles"""
        users = []

        for i in range(10):
            user = {
                "id": str(uuid.uuid4()),
                "name": f"User {i + 1}",
                "email": f"user{i + 1}@example.com",
                "phone": f"+1-555-{random.randint(1000, 9999):04d}",
                "avatar": f"https://picsum.photos/150/150?random=user{i}",
                "memberSince": (datetime.now() - timedelta(days=random.randint(30, 730))).strftime("%Y-%m-%d"),
                "totalOrders": random.randint(5, 100),
                "totalSpent": round(random.uniform(100, 10000), 2),
                "loyaltyPoints": random.randint(100, 5000),
                "tier": random.choice(["Bronze", "Silver", "Gold", "Platinum"]),
            }
            users.append(user)

        return users

    def _generate_cart_items(self):
        """Generate shopping cart items"""
        cart_items = []

        for i in range(random.randint(1, 5)):
            product = random.choice(self.products)
            cart_item = {
                "id": str(uuid.uuid4()),
                "productId": product["id"],
                "productName": product["name"],
                "price": product["price"],
                "quantity": random.randint(1, 3),
                "image": product["images"][0],
                "subtotal": round(product["price"] * random.randint(1, 3), 2),
                "seller": product["seller"],
            }
            cart_items.append(cart_item)

        return cart_items

    def _generate_wishlist(self):
        """Generate wishlist items"""
        wishlist = []

        for i in range(random.randint(5, 20)):
            product = random.choice(self.products)
            wishlist_item = {
                "id": str(uuid.uuid4()),
                "productId": product["id"],
                "productName": product["name"],
                "price": product["price"],
                "image": product["images"][0],
                "addedDate": (datetime.now() - timedelta(days=random.randint(1, 60))).isoformat(),
                "inStock": product["stock"] > 0,
            }
            wishlist.append(wishlist_item)

        return wishlist

    def _generate_addresses(self):
        """Generate shipping addresses"""
        addresses = []

        address_data = [
            ("Home", "123 Main Street", "New York", "NY", "10001", "USA", True),
            ("Office", "456 Business Ave", "Los Angeles", "CA", "90001", "USA", False),
            ("Parents", "789 Family Road", "Chicago", "IL", "60601", "USA", False),
        ]

        for i, (name, street, city, state, zip_code, country, is_default) in enumerate(address_data, 1):
            address = {
                "id": str(i),
                "name": name,
                "street": street,
                "city": city,
                "state": state,
                "zipCode": zip_code,
                "country": country,
                "isDefault": is_default,
                "phone": f"+1-555-{random.randint(1000, 9999):04d}",
            }
            addresses.append(address)

        return addresses

    def _generate_notifications(self):
        """Generate user notifications"""
        notifications = []

        notification_templates = [
            ("Order Shipped", "Your order #ORDER123 has been shipped", "order"),
            ("Flash Sale", "50% off on selected items! Limited time only", "promotion"),
            ("New Message", "You have a new message from seller", "message"),
            ("Price Drop", "Item in your wishlist is now on sale", "price"),
            ("Review Request", "Please review your recent purchase", "review"),
            ("Loyalty Points", "You've earned 100 loyalty points", "reward"),
            ("New Arrival", "New products in your favorite category", "product"),
            ("Order Delivered", "Your order has been delivered", "order"),
        ]

        for i in range(20):
            title, message, type_str = random.choice(notification_templates)
            notification = {
                "id": str(uuid.uuid4()),
                "title": title,
                "message": message,
                "type": type_str,
                "date": (datetime.now() - timedelta(hours=random.randint(1, 168))).isoformat(),
                "read": random.random() > 0.5,
                "actionUrl": f"/{type_str}/{random.randint(1, 100)}",
            }
            notifications.append(notification)

        return notifications

    # API Methods

    def get_products_by_category(self, category):
        """Get products for a specific category"""
        return [p for p in self.products if p["category"] == category]

    def get_product_details(self, product_id):
        """Get detailed product information"""
        for product in self.products:
            if product["id"] == product_id:
                # Add additional details
                product["reviews"] = [r for r in self.reviews if r["productId"] == product_id]
                product["relatedProducts"] = random.sample(self.products, min(10, len(self.products)))
                return product
        return None

    def search_products(self, query):
        """Search products by name or description"""
        query_lower = query.lower()
        results = []

        for product in self.products:
            if (query_lower in product["name"].lower() or
                    query_lower in product["description"].lower() or
                    query_lower in product["category"].lower()):
                results.append(product)

        return results[:50]

    def get_deals(self):
        """Get products with high discounts"""
        return [p for p in self.products if p["discount"] >= 30]

    def get_new_arrivals(self):
        """Get new products"""
        return [p for p in self.products if p.get("isNew", False)]

    def get_best_sellers(self):
        """Get best selling products"""
        return [p for p in self.products if p.get("isBestSeller", False)]

    def get_flash_sale(self):
        """Get flash sale products"""
        flash_products = random.sample(self.products, min(20, len(self.products)))
        for product in flash_products:
            product["flashDiscount"] = random.randint(40, 70)
            product["flashEndTime"] = (datetime.now() + timedelta(hours=random.randint(1, 24))).isoformat()
        return flash_products