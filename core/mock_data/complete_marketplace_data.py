# File: core/mock_data/complete_marketplace_data.py
"""
Complete mock data provider for the MegaMart marketplace application
Provides 2000+ products and all related marketplace data
"""

import json
import random
import uuid
from datetime import datetime, timedelta
from .base_mock_data import BaseMockData


class CompleteMarketplaceMockData(BaseMockData):
    """Complete mock data provider for marketplace with 2000+ products"""

    def __init__(self):
        super().__init__()
        self.initialize_data()

    def initialize_data(self):
        """Initialize all mock data"""
        self.categories = self._generate_categories()
        self.sellers = self._generate_sellers()
        self.products = self._generate_products()
        self.users = self._generate_users()
        self.reviews = self._generate_reviews()
        self.orders = self._generate_orders()
        self.cart_items = self._generate_cart_items()
        self.flash_sales = self._generate_flash_sales()
        self.coupons = self._generate_coupons()
        self.notifications = self._generate_notifications()

    def get_data_sources(self):
        """Return all data sources for the marketplace"""
        return {
            'Products': self.products,
            'Product Details': self.products,
            'Categories': self.categories,
            'Trending Products': self._get_trending_products(),
            'Flash Sales': self.flash_sales,
            'New Arrivals': self._get_new_arrivals(),
            'Best Sellers': self._get_best_sellers(),
            'Deals': self._generate_deals(),
            'User Profile': self.users,
            'Addresses': self.users['addresses'],
            'Payment Cards': self._generate_payment_cards(),
            'Wishlist': self._generate_wishlist(),
            'Recently Viewed': self._generate_recently_viewed(),
            'Loyalty Points': self._generate_loyalty_data(),
            'Wallet': self._generate_wallet_data(),
            'Referrals': self._generate_referral_data(),
            'Cart': self.cart_items,
            'Orders': self.orders,
            'Order Details': self.orders,
            'Order Tracking': self._generate_tracking_data(),
            'Returns': self._generate_returns(),
            'Sellers': self.sellers,
            'Seller Details': self.sellers,
            'Seller Dashboard': self._generate_seller_dashboard(),
            'Seller Analytics': self._generate_seller_analytics(),
            'Reviews': self.reviews,
            'Questions': self._generate_questions(),
            'Notifications': self.notifications,
            'Messages': self._generate_messages(),
            'Chat': self._generate_chat_data(),
            'FAQs': self._generate_faqs(),
            'Help Articles': self._generate_help_articles(),
            'Support Tickets': self._generate_support_tickets(),
            'Coupons': self.coupons,
            'Gift Cards': self._generate_gift_cards(),
            'Subscriptions': self._generate_subscriptions(),
        }

    def get_sample_images(self):
        """Return sample image URLs"""
        return {
            'products': [f'https://picsum.photos/300/300?random={i}' for i in range(100)],
            'banners': [f'https://picsum.photos/800/400?random=banner{i}' for i in range(10)],
            'categories': [f'https://picsum.photos/200/200?random=cat{i}' for i in range(20)],
            'avatars': [f'https://picsum.photos/100/100?random=avatar{i}' for i in range(50)],
        }

    def _generate_categories(self):
        """Generate complete category hierarchy"""
        categories = [
            {
                'id': 'electronics',
                'name': 'Electronics',
                'icon': 'devices',
                'image': 'https://picsum.photos/400/200?random=electronics',
                'productCount': 345,
                'description': 'Latest gadgets and electronics',
                'subcategories': [
                    {'id': 'phones', 'name': 'Phones & Tablets', 'count': 120, 'icon': 'smartphone'},
                    {'id': 'computers', 'name': 'Computers & Laptops', 'count': 85, 'icon': 'computer'},
                    {'id': 'audio', 'name': 'Audio & Video', 'count': 140, 'icon': 'headphones'},
                    {'id': 'cameras', 'name': 'Cameras & Photography', 'count': 65, 'icon': 'camera_alt'},
                    {'id': 'gaming', 'name': 'Gaming', 'count': 95, 'icon': 'sports_esports'},
                ]
            },
            {
                'id': 'fashion',
                'name': 'Fashion',
                'icon': 'shopping_bag',
                'image': 'https://picsum.photos/400/200?random=fashion',
                'productCount': 567,
                'description': 'Trending fashion and accessories',
                'subcategories': [
                    {'id': 'mens', 'name': "Men's Fashion", 'count': 200, 'icon': 'person'},
                    {'id': 'womens', 'name': "Women's Fashion", 'count': 267, 'icon': 'person_outline'},
                    {'id': 'kids', 'name': 'Kids Fashion', 'count': 100, 'icon': 'child_care'},
                    {'id': 'shoes', 'name': 'Shoes', 'count': 150, 'icon': 'directions_walk'},
                    {'id': 'accessories', 'name': 'Accessories', 'count': 120, 'icon': 'watch'},
                ]
            },
            {
                'id': 'home_garden',
                'name': 'Home & Garden',
                'icon': 'home',
                'image': 'https://picsum.photos/400/200?random=home',
                'productCount': 432,
                'description': 'Everything for your home',
                'subcategories': [
                    {'id': 'furniture', 'name': 'Furniture', 'count': 150, 'icon': 'chair'},
                    {'id': 'decor', 'name': 'Home Decor', 'count': 120, 'icon': 'photo_frame'},
                    {'id': 'kitchen', 'name': 'Kitchen & Dining', 'count': 100, 'icon': 'kitchen'},
                    {'id': 'bedding', 'name': 'Bedding & Bath', 'count': 80, 'icon': 'bed'},
                    {'id': 'garden', 'name': 'Garden & Outdoor', 'count': 90, 'icon': 'local_florist'},
                ]
            },
            {
                'id': 'sports',
                'name': 'Sports & Outdoors',
                'icon': 'sports_soccer',
                'image': 'https://picsum.photos/400/200?random=sports',
                'productCount': 289,
                'description': 'Sports equipment and outdoor gear',
                'subcategories': [
                    {'id': 'fitness', 'name': 'Fitness Equipment', 'count': 100, 'icon': 'fitness_center'},
                    {'id': 'outdoor', 'name': 'Outdoor Recreation', 'count': 80, 'icon': 'terrain'},
                    {'id': 'team_sports', 'name': 'Team Sports', 'count': 60, 'icon': 'sports_basketball'},
                    {'id': 'water_sports', 'name': 'Water Sports', 'count': 49, 'icon': 'pool'},
                ]
            },
            {
                'id': 'books',
                'name': 'Books & Media',
                'icon': 'menu_book',
                'image': 'https://picsum.photos/400/200?random=books',
                'productCount': 876,
                'description': 'Books, movies, music and more',
                'subcategories': [
                    {'id': 'fiction', 'name': 'Fiction', 'count': 300, 'icon': 'auto_stories'},
                    {'id': 'non_fiction', 'name': 'Non-Fiction', 'count': 250, 'icon': 'library_books'},
                    {'id': 'textbooks', 'name': 'Textbooks', 'count': 150, 'icon': 'school'},
                    {'id': 'movies', 'name': 'Movies & TV', 'count': 100, 'icon': 'movie'},
                    {'id': 'music', 'name': 'Music', 'count': 76, 'icon': 'music_note'},
                ]
            },
            {
                'id': 'beauty',
                'name': 'Beauty & Personal Care',
                'icon': 'face',
                'image': 'https://picsum.photos/400/200?random=beauty',
                'productCount': 423,
                'description': 'Beauty and personal care products',
                'subcategories': [
                    {'id': 'skincare', 'name': 'Skincare', 'count': 150, 'icon': 'spa'},
                    {'id': 'makeup', 'name': 'Makeup', 'count': 120, 'icon': 'brush'},
                    {'id': 'haircare', 'name': 'Hair Care', 'count': 100, 'icon': 'content_cut'},
                    {'id': 'fragrance', 'name': 'Fragrance', 'count': 53, 'icon': 'local_florist'},
                ]
            },
            {
                'id': 'food',
                'name': 'Food & Groceries',
                'icon': 'restaurant',
                'image': 'https://picsum.photos/400/200?random=food',
                'productCount': 654,
                'description': 'Fresh food and groceries',
                'subcategories': [
                    {'id': 'fresh', 'name': 'Fresh Produce', 'count': 200, 'icon': 'eco'},
                    {'id': 'pantry', 'name': 'Pantry Staples', 'count': 180, 'icon': 'kitchen'},
                    {'id': 'snacks', 'name': 'Snacks & Beverages', 'count': 150, 'icon': 'local_drink'},
                    {'id': 'frozen', 'name': 'Frozen Foods', 'count': 124, 'icon': 'ac_unit'},
                ]
            },
            {
                'id': 'health',
                'name': 'Health & Wellness',
                'icon': 'favorite',
                'image': 'https://picsum.photos/400/200?random=health',
                'productCount': 345,
                'description': 'Health and wellness products',
                'subcategories': [
                    {'id': 'vitamins', 'name': 'Vitamins & Supplements', 'count': 150, 'icon': 'medication'},
                    {'id': 'personal_care', 'name': 'Personal Care', 'count': 100, 'icon': 'clean_hands'},
                    {'id': 'medical', 'name': 'Medical Supplies', 'count': 95, 'icon': 'medical_services'},
                ]
            },
            {
                'id': 'automotive',
                'name': 'Automotive',
                'icon': 'directions_car',
                'image': 'https://picsum.photos/400/200?random=auto',
                'productCount': 234,
                'description': 'Auto parts and accessories',
                'subcategories': [
                    {'id': 'parts', 'name': 'Auto Parts', 'count': 100, 'icon': 'build'},
                    {'id': 'accessories', 'name': 'Accessories', 'count': 80, 'icon': 'dashboard'},
                    {'id': 'tools', 'name': 'Tools & Equipment', 'count': 54, 'icon': 'handyman'},
                ]
            },
            {
                'id': 'toys',
                'name': 'Toys & Games',
                'icon': 'toys',
                'image': 'https://picsum.photos/400/200?random=toys',
                'productCount': 456,
                'description': 'Toys and games for all ages',
                'subcategories': [
                    {'id': 'action_figures', 'name': 'Action Figures', 'count': 150, 'icon': 'sports_martial_arts'},
                    {'id': 'board_games', 'name': 'Board Games', 'count': 100, 'icon': 'casino'},
                    {'id': 'educational', 'name': 'Educational Toys', 'count': 106, 'icon': 'psychology'},
                    {'id': 'outdoor_toys', 'name': 'Outdoor Toys', 'count': 100, 'icon': 'park'},
                ]
            },
            {
                'id': 'pets',
                'name': 'Pet Supplies',
                'icon': 'pets',
                'image': 'https://picsum.photos/400/200?random=pets',
                'productCount': 298,
                'description': 'Everything for your pets',
                'subcategories': [
                    {'id': 'dog', 'name': 'Dog Supplies', 'count': 120, 'icon': 'pets'},
                    {'id': 'cat', 'name': 'Cat Supplies', 'count': 100, 'icon': 'pets'},
                    {'id': 'fish', 'name': 'Fish & Aquatic', 'count': 40, 'icon': 'set_meal'},
                    {'id': 'bird', 'name': 'Bird Supplies', 'count': 38, 'icon': 'flutter_dash'},
                ]
            }
        ]

        return categories

    def _generate_products(self):
        """Generate 2000+ diverse products"""
        products = []

        # Product name templates by category
        product_templates = {
            'electronics': [
                'Smartphone', 'Laptop', 'Tablet', 'Smartwatch', 'Headphones',
                'Camera', 'TV', 'Speaker', 'Monitor', 'Keyboard', 'Mouse',
                'Drone', 'Power Bank', 'Charger', 'Cable', 'Router'
            ],
            'fashion': [
                'T-Shirt', 'Jeans', 'Dress', 'Jacket', 'Shoes', 'Sneakers',
                'Handbag', 'Wallet', 'Watch', 'Sunglasses', 'Belt', 'Scarf',
                'Shirt', 'Pants', 'Skirt', 'Coat', 'Sweater', 'Hoodie'
            ],
            'home_garden': [
                'Sofa', 'Chair', 'Table', 'Bed', 'Mattress', 'Lamp', 'Rug',
                'Curtains', 'Pillow', 'Blanket', 'Mirror', 'Vase', 'Plant',
                'Garden Tool', 'Planter', 'Outdoor Furniture'
            ],
            'sports': [
                'Running Shoes', 'Yoga Mat', 'Dumbbell', 'Treadmill', 'Bicycle',
                'Tennis Racket', 'Basketball', 'Football', 'Golf Club', 'Helmet',
                'Fitness Tracker', 'Water Bottle', 'Gym Bag', 'Resistance Band'
            ],
            'books': [
                'Novel', 'Textbook', 'Cookbook', 'Biography', 'Self-Help Book',
                'Children Book', 'Comic Book', 'Magazine', 'Dictionary', 'Guide'
            ],
            'beauty': [
                'Face Cream', 'Lipstick', 'Foundation', 'Mascara', 'Perfume',
                'Shampoo', 'Conditioner', 'Body Lotion', 'Face Mask', 'Serum',
                'Nail Polish', 'Hair Dryer', 'Makeup Brush', 'Cologne'
            ],
            'food': [
                'Organic Vegetables', 'Fresh Fruits', 'Bread', 'Milk', 'Cheese',
                'Coffee', 'Tea', 'Chocolate', 'Snacks', 'Juice', 'Pasta',
                'Rice', 'Oil', 'Spices', 'Honey', 'Cereal'
            ],
            'health': [
                'Vitamin C', 'Protein Powder', 'First Aid Kit', 'Thermometer',
                'Blood Pressure Monitor', 'Hand Sanitizer', 'Face Mask', 'Bandages',
                'Pain Relief', 'Allergy Medicine', 'Supplements'
            ],
            'automotive': [
                'Tire', 'Battery', 'Oil Filter', 'Brake Pads', 'Headlight',
                'Car Cover', 'Floor Mats', 'Phone Mount', 'Dash Cam', 'Air Freshener'
            ],
            'toys': [
                'LEGO Set', 'Action Figure', 'Doll', 'Board Game', 'Puzzle',
                'Remote Control Car', 'Building Blocks', 'Art Set', 'Science Kit',
                'Musical Toy', 'Stuffed Animal', 'Video Game'
            ],
            'pets': [
                'Dog Food', 'Cat Food', 'Pet Bed', 'Leash', 'Collar', 'Pet Toy',
                'Litter Box', 'Aquarium', 'Bird Cage', 'Pet Carrier', 'Grooming Kit'
            ]
        }

        # Brand names
        brands = [
            'TechPro', 'StyleMax', 'HomeComfort', 'SportElite', 'BookWorld',
            'BeautyGlow', 'FreshMart', 'HealthPlus', 'AutoParts', 'ToyLand',
            'PetCare', 'Premium', 'Elite', 'Pro', 'Max', 'Plus', 'Ultra',
            'Super', 'Mega', 'Prime', 'Express', 'Direct', 'Global'
        ]

        # Generate products
        product_id = 1
        for category in self.categories:
            category_id = category['id']
            templates = product_templates.get(category_id, ['Product'])

            # Generate products for this category
            num_products = category['productCount']
            for i in range(num_products):
                template = random.choice(templates)
                brand = random.choice(brands)

                # Generate price based on category
                if category_id == 'electronics':
                    price = round(random.uniform(49.99, 2999.99), 2)
                elif category_id == 'fashion':
                    price = round(random.uniform(19.99, 499.99), 2)
                elif category_id == 'home_garden':
                    price = round(random.uniform(29.99, 1999.99), 2)
                elif category_id == 'books':
                    price = round(random.uniform(9.99, 99.99), 2)
                elif category_id == 'food':
                    price = round(random.uniform(2.99, 49.99), 2)
                else:
                    price = round(random.uniform(9.99, 299.99), 2)

                # Calculate discount
                has_discount = random.random() > 0.7
                discount = random.choice([10, 15, 20, 25, 30, 40, 50]) if has_discount else 0

                product = {
                    'id': str(uuid.uuid4()),
                    'productId': product_id,
                    'name': f'{brand} {template} {random.choice(["Pro", "Plus", "Elite", "Max", ""])} {random.randint(100, 999)}'.strip(),
                    'brand': brand,
                    'price': price,
                    'originalPrice': round(price * (1 + discount / 100), 2) if discount else price,
                    'discount': discount,
                    'image': f'https://picsum.photos/300/300?random={product_id}',
                    'images': [
                        f'https://picsum.photos/600/600?random={product_id}1',
                        f'https://picsum.photos/600/600?random={product_id}2',
                        f'https://picsum.photos/600/600?random={product_id}3',
                        f'https://picsum.photos/600/600?random={product_id}4',
                    ],
                    'rating': round(random.uniform(3.5, 5.0), 1),
                    'reviews': random.randint(10, 2000),
                    'sold': random.randint(50, 5000),
                    'seller': f'Store {random.randint(1, 100)}',
                    'sellerId': str(uuid.uuid4()),
                    'category': category['name'],
                    'categoryId': category_id,
                    'subcategory': random.choice(category['subcategories'])['name'] if category[
                        'subcategories'] else '',
                    'inStock': random.choice([True, True, True, False]),
                    'stockQuantity': random.randint(0, 100),
                    'description': f'High-quality {template.lower()} from {brand}. {self._generate_product_description(template)}',
                    'features': self._generate_product_features(category_id),
                    'specifications': self._generate_specifications(category_id, template),
                    'tags': random.sample(
                        ['bestseller', 'new', 'trending', 'limited', 'exclusive', 'sale', 'premium', 'popular'],
                        random.randint(1, 4)),
                    'shipping': {
                        'free': price > 50,
                        'express': True,
                        'estimatedDays': random.randint(2, 7)
                    },
                    'warranty': f'{random.choice([6, 12, 24])} months',
                    'returnable': True,
                    'returnDays': 30,
                    'createdAt': (datetime.now() - timedelta(days=random.randint(1, 365))).isoformat()
                }

                products.append(product)
                product_id += 1

        return products

    def _generate_product_description(self, template):
        """Generate product description"""
        descriptions = [
            "Experience superior quality and performance with this amazing product.",
            "Designed with attention to detail and built to last.",
            "Perfect for everyday use with premium materials.",
            "Innovative design meets functionality in this exceptional product.",
            "Crafted with care to exceed your expectations.",
            "The ultimate solution for your needs.",
            "Combining style and practicality for modern living.",
            "Engineered for excellence and reliability."
        ]
        return random.choice(descriptions)

    def _generate_product_features(self, category):
        """Generate product features based on category"""
        features_map = {
            'electronics': [
                'Latest technology', 'Energy efficient', 'Long battery life',
                'High performance', 'Compact design', 'Easy to use'
            ],
            'fashion': [
                'Comfortable fit', 'Premium fabric', 'Machine washable',
                'Trendy design', 'Multiple colors', 'All seasons'
            ],
            'home_garden': [
                'Easy assembly', 'Space saving', 'Durable construction',
                'Modern design', 'Multi-functional', 'Eco-friendly'
            ],
            'sports': [
                'Professional grade', 'Lightweight', 'Durable',
                'Ergonomic design', 'Weather resistant', 'Portable'
            ]
        }

        features = features_map.get(category, [
            'High quality', 'Great value', 'Customer favorite',
            'Best seller', 'Premium materials', 'Satisfaction guaranteed'
        ])

        return random.sample(features, min(4, len(features)))

    def _generate_specifications(self, category, template):
        """Generate product specifications"""
        specs = {
            'Brand': f'Brand {random.randint(1, 50)}',
            'Model': f'Model-{random.randint(1000, 9999)}',
            'Weight': f'{round(random.uniform(0.1, 10), 1)} kg',
            'Dimensions': f'{random.randint(10, 50)}x{random.randint(10, 50)}x{random.randint(5, 20)} cm',
            'Material': random.choice(['Plastic', 'Metal', 'Wood', 'Fabric', 'Glass', 'Leather']),
            'Color': random.choice(['Black', 'White', 'Blue', 'Red', 'Gray', 'Green', 'Brown']),
            'Warranty': f'{random.choice([6, 12, 24])} months',
            'Country': random.choice(['USA', 'China', 'Germany', 'Japan', 'India'])
        }

        # Add category-specific specs
        if category == 'electronics':
            specs.update({
                'Battery': f'{random.randint(2000, 5000)} mAh',
                'Screen': f'{random.choice([5, 6, 7, 10, 13, 15])} inch',
                'Memory': f'{random.choice([4, 8, 16, 32, 64])} GB',
                'Processor': random.choice(['Snapdragon', 'Intel', 'AMD', 'Apple'])
            })
        elif category == 'fashion':
            specs.update({
                'Size': random.choice(['S', 'M', 'L', 'XL', 'XXL']),
                'Fabric': random.choice(['Cotton', 'Polyester', 'Wool', 'Silk', 'Denim']),
                'Care': 'Machine washable',
                'Season': random.choice(['Summer', 'Winter', 'All Season'])
            })

        return specs

    def _generate_sellers(self):
        """Generate 100 sellers"""
        sellers = []

        seller_names = [
            'Tech Store', 'Fashion Hub', 'Home Essentials', 'Sports World',
            'Book Paradise', 'Beauty Zone', 'Fresh Market', 'Health Store',
            'Auto Parts Pro', 'Toy Kingdom', 'Pet Paradise', 'Mega Store',
            'Elite Shop', 'Premium Mart', 'Express Store', 'Global Trade'
        ]

        for i in range(100):
            base_name = random.choice(seller_names)
            sellers.append({
                'id': str(uuid.uuid4()),
                'name': f'{base_name} {i + 1}',
                'logo': f'https://picsum.photos/100/100?random=seller{i}',
                'banner': f'https://picsum.photos/800/200?random=sellerbanner{i}',
                'rating': round(random.uniform(4.0, 5.0), 1),
                'reviews': random.randint(100, 5000),
                'products': random.randint(10, 500),
                'followers': random.randint(100, 50000),
                'description': f'Trusted seller with {random.randint(1, 10)} years of experience. Quality products and excellent service.',
                'joinDate': (datetime.now() - timedelta(days=random.randint(30, 1000))).isoformat(),
                'verified': random.choice([True, True, False]),
                'responseTime': f'{random.randint(1, 24)} hours',
                'responseRate': f'{random.randint(85, 100)}%',
                'shipOnTime': f'{random.randint(90, 100)}%',
                'positiveRating': f'{random.randint(85, 100)}%',
                'totalSales': random.randint(1000, 100000),
                'policies': {
                    'shipping': 'Free shipping on orders over $50',
                    'returns': '30-day return policy',
                    'warranty': '1-year warranty on all products',
                    'payment': 'All major cards accepted'
                },
                'categories': random.sample([c['name'] for c in self.categories], random.randint(1, 5)),
                'location': random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']),
                'businessType': random.choice(['Manufacturer', 'Distributor', 'Retailer', 'Wholesaler'])
            })

        return sellers

    def _generate_users(self):
        """Generate user profile data"""
        return {
            'id': str(uuid.uuid4()),
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'phone': '+1 234 567 8900',
            'avatar': 'https://picsum.photos/100/100?random=avatar',
            'memberSince': '2023-01-15',
            'tier': 'Gold',
            'tierProgress': 75,
            'nextTier': 'Platinum',
            'points': 2450,
            'wallet': 125.50,
            'totalOrders': 45,
            'totalSpent': 3456.78,
            'addresses': [
                {
                    'id': 'addr1',
                    'name': 'Home',
                    'fullName': 'John Doe',
                    'phone': '+1 234 567 8900',
                    'street': '123 Main Street',
                    'apartment': 'Apt 4B',
                    'city': 'New York',
                    'state': 'NY',
                    'zipCode': '10001',
                    'country': 'USA',
                    'isDefault': True
                },
                {
                    'id': 'addr2',
                    'name': 'Office',
                    'fullName': 'John Doe',
                    'phone': '+1 234 567 8901',
                    'street': '456 Business Ave',
                    'apartment': 'Suite 200',
                    'city': 'New York',
                    'state': 'NY',
                    'zipCode': '10002',
                    'country': 'USA',
                    'isDefault': False
                }
            ],
            'preferences': {
                'newsletter': True,
                'promotions': True,
                'orderUpdates': True,
                'priceAlerts': True,
                'newProducts': False,
                'language': 'en',
                'currency': 'USD',
                'darkMode': False
            }
        }

    def _generate_reviews(self):
        """Generate 500+ product reviews"""
        reviews = []

        review_titles = [
            'Excellent product!', 'Great value for money', 'Highly recommended',
            'Good quality', 'As described', 'Very satisfied', 'Amazing!',
            'Worth the price', 'Perfect!', 'Love it!', 'Best purchase ever',
            'Exceeded expectations', 'Fantastic quality', 'Would buy again'
        ]

        review_comments = [
            'This product exceeded my expectations. The quality is outstanding and delivery was fast.',
            'Great value for the price. Works exactly as described.',
            'Very happy with this purchase. Would definitely recommend to others.',
            'Excellent quality and fast shipping. Five stars!',
            'Product arrived quickly and was well packaged. Very satisfied.',
            'Amazing product! Looks even better than in the pictures.',
            'Perfect for my needs. Great seller and fast delivery.',
            'High quality product at a reasonable price. Very pleased.',
            'Exactly what I was looking for. Thank you!',
            'Superb quality and excellent customer service.'
        ]

        usernames = [f'User{i}' for i in range(1, 1001)]

        for i in range(500):
            product = random.choice(self.products) if self.products else None

            reviews.append({
                'id': str(uuid.uuid4()),
                'productId': product['id'] if product else str(uuid.uuid4()),
                'productName': product['name'] if product else 'Product',
                'userId': str(uuid.uuid4()),
                'userName': random.choice(usernames),
                'userAvatar': f'https://picsum.photos/50/50?random=user{i}',
                'rating': random.choices([3, 4, 5], weights=[1, 3, 6])[0],
                'title': random.choice(review_titles),
                'comment': random.choice(review_comments),
                'date': (datetime.now() - timedelta(days=random.randint(1, 180))).isoformat(),
                'helpful': random.randint(0, 100),
                'verified': random.choice([True, True, False]),
                'images': [f'https://picsum.photos/200/200?random=review{i}{j}' for j in range(random.randint(0, 3))],
                'sellerResponse': random.choice([
                    None, None, None,  # Most reviews don't have responses
                    'Thank you for your feedback! We appreciate your business.',
                    'We\'re glad you\'re happy with your purchase!',
                    'Thanks for the 5-star review!'
                ])
            })

        return reviews

    def _generate_orders(self):
        """Generate order history"""
        orders = []
        statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']

        for i in range(50):
            order_date = datetime.now() - timedelta(days=random.randint(1, 180))
            status = random.choice(statuses)

            # Select random products for order
            order_products = random.sample(self.products, min(random.randint(1, 5), len(self.products)))

            items = []
            subtotal = 0
            for product in order_products:
                quantity = random.randint(1, 3)
                item_total = product['price'] * quantity
                subtotal += item_total

                items.append({
                    'productId': product['id'],
                    'productName': product['name'],
                    'productImage': product['image'],
                    'price': product['price'],
                    'quantity': quantity,
                    'subtotal': item_total,
                    'seller': product['seller']
                })

            shipping = 5.99 if subtotal < 50 else 0
            tax = round(subtotal * 0.08, 2)
            total = round(subtotal + shipping + tax, 2)

            orders.append({
                'id': str(uuid.uuid4()),
                'orderNumber': f'ORD{100000 + i}',
                'date': order_date.isoformat(),
                'status': status,
                'items': items,
                'itemCount': len(items),
                'subtotal': subtotal,
                'shipping': shipping,
                'tax': tax,
                'total': total,
                'paymentMethod': random.choice(['Credit Card', 'PayPal', 'Apple Pay', 'Google Pay']),
                'shippingAddress': self.users['addresses'][0],
                'trackingNumber': f'TRK{random.randint(100000, 999999)}' if status in ['shipped',
                                                                                       'delivered'] else None,
                'estimatedDelivery': (order_date + timedelta(
                    days=random.randint(3, 7))).isoformat() if status != 'cancelled' else None,
                'deliveredDate': (order_date + timedelta(
                    days=random.randint(3, 7))).isoformat() if status == 'delivered' else None
            })

        return sorted(orders, key=lambda x: x['date'], reverse=True)

    def _generate_cart_items(self):
        """Generate cart items"""
        cart_items = []
        cart_products = random.sample(self.products, min(random.randint(1, 5), len(self.products)))

        for product in cart_products:
            quantity = random.randint(1, 3)
            cart_items.append({
                'id': str(uuid.uuid4()),
                'productId': product['id'],
                'productName': product['name'],
                'productImage': product['image'],
                'price': product['price'],
                'originalPrice': product.get('originalPrice', product['price']),
                'discount': product.get('discount', 0),
                'quantity': quantity,
                'subtotal': product['price'] * quantity,
                'seller': product['seller'],
                'sellerId': product['sellerId'],
                'inStock': product['inStock'],
                'selected': True
            })

        return cart_items

    def _generate_flash_sales(self):
        """Generate flash sale items"""
        flash_sales = []
        flash_products = random.sample(self.products, min(20, len(self.products)))

        for product in flash_products:
            flash_sales.append({
                'id': str(uuid.uuid4()),
                'productId': product['id'],
                'product': product,
                'discountPercent': random.choice([30, 40, 50, 60, 70]),
                'originalPrice': product['price'],
                'salePrice': round(product['price'] * random.uniform(0.3, 0.7), 2),
                'startTime': datetime.now().isoformat(),
                'endTime': (datetime.now() + timedelta(hours=random.randint(2, 24))).isoformat(),
                'stock': random.randint(5, 50),
                'sold': random.randint(0, 100)
            })

        return flash_sales

    def _get_trending_products(self):
        """Get trending products"""
        trending = random.sample(self.products, min(30, len(self.products)))
        for product in trending:
            product['trendScore'] = random.randint(80, 100)
            product['trendRank'] = random.randint(1, 100)
        return sorted(trending, key=lambda x: x['trendScore'], reverse=True)

    def _get_new_arrivals(self):
        """Get new arrival products"""
        new_arrivals = random.sample(self.products, min(40, len(self.products)))
        for product in new_arrivals:
            product['arrivalDate'] = (datetime.now() - timedelta(days=random.randint(1, 14))).isoformat()
            product['isNew'] = True
        return sorted(new_arrivals, key=lambda x: x['arrivalDate'], reverse=True)

    def _get_best_sellers(self):
        """Get best selling products"""
        best_sellers = random.sample(self.products, min(30, len(self.products)))
        for product in best_sellers:
            product['soldCount'] = random.randint(100, 5000)
            product['salesRank'] = random.randint(1, 100)
        return sorted(best_sellers, key=lambda x: x['soldCount'], reverse=True)

    def _generate_deals(self):
        """Generate special deals"""
        deals = []

        deal_types = [
            'Buy One Get One', 'Limited Time Offer', 'Clearance Sale',
            'Season End Sale', 'Flash Deal', 'Weekend Special',
            'Member Exclusive', 'Bundle Deal', 'New Customer Offer'
        ]

        for i in range(20):
            deal_products = random.sample(self.products, min(random.randint(3, 8), len(self.products)))

            deals.append({
                'id': str(uuid.uuid4()),
                'title': random.choice(deal_types),
                'description': 'Special offer for limited time only!',
                'discount': f'{random.choice([20, 30, 40, 50])}% OFF',
                'badge': random.choice(['HOT', 'NEW', 'LIMITED', 'EXCLUSIVE']),
                'validFrom': datetime.now().isoformat(),
                'validUntil': (datetime.now() + timedelta(days=random.randint(1, 30))).isoformat(),
                'products': deal_products,
                'minPurchase': random.choice([0, 50, 100, 150]),
                'maxDiscount': random.choice([50, 100, 200]),
                'termsConditions': 'Standard terms and conditions apply.'
            })

        return deals

    def _generate_payment_cards(self):
        """Generate payment cards"""
        return [
            {
                'id': 'card1',
                'lastFour': '4242',
                'brand': 'Visa',
                'holderName': 'John Doe',
                'expiryMonth': 12,
                'expiryYear': 2025,
                'isDefault': True,
                'billingAddress': self.users['addresses'][0]
            },
            {
                'id': 'card2',
                'lastFour': '5555',
                'brand': 'Mastercard',
                'holderName': 'John Doe',
                'expiryMonth': 6,
                'expiryYear': 2024,
                'isDefault': False,
                'billingAddress': self.users['addresses'][0]
            },
            {
                'id': 'card3',
                'lastFour': '3782',
                'brand': 'Amex',
                'holderName': 'John Doe',
                'expiryMonth': 9,
                'expiryYear': 2026,
                'isDefault': False,
                'billingAddress': self.users['addresses'][1]
            }
        ]

    def _generate_wishlist(self):
        """Generate wishlist items"""
        wishlist = []
        wishlist_products = random.sample(self.products, min(15, len(self.products)))

        for product in wishlist_products:
            wishlist.append({
                'id': str(uuid.uuid4()),
                'productId': product['id'],
                'productName': product['name'],
                'productImage': product['image'],
                'price': product['price'],
                'originalPrice': product.get('originalPrice', product['price']),
                'discount': product.get('discount', 0),
                'inStock': product['inStock'],
                'addedDate': (datetime.now() - timedelta(days=random.randint(1, 60))).isoformat(),
                'priceDropAlert': random.choice([True, False]),
                'seller': product['seller']
            })

        return wishlist

    def _generate_recently_viewed(self):
        """Generate recently viewed products"""
        viewed = []
        viewed_products = random.sample(self.products, min(20, len(self.products)))

        for product in viewed_products:
            viewed.append({
                'id': str(uuid.uuid4()),
                'productId': product['id'],
                'productName': product['name'],
                'productImage': product['image'],
                'price': product['price'],
                'category': product['category'],
                'viewedAt': (datetime.now() - timedelta(hours=random.randint(1, 168))).isoformat(),
                'viewCount': random.randint(1, 5)
            })

        return sorted(viewed, key=lambda x: x['viewedAt'], reverse=True)

    def _generate_loyalty_data(self):
        """Generate loyalty program data"""
        return {
            'totalPoints': 2450,
            'availablePoints': 2000,
            'pendingPoints': 450,
            'redeemedPoints': 1500,
            'tier': 'Gold',
            'tierProgress': 75,
            'nextTier': 'Platinum',
            'pointsToNextTier': 550,
            'tierBenefits': [
                'Free shipping on all orders',
                '10% birthday discount',
                'Early access to sales',
                'Exclusive member offers'
            ],
            'pointsHistory': [
                {
                    'id': str(uuid.uuid4()),
                    'date': (datetime.now() - timedelta(days=i)).isoformat(),
                    'description': random.choice([
                        f'Purchase order #ORD{100000 + i}',
                        'Referral bonus',
                        'Review bonus',
                        'Birthday bonus'
                    ]),
                    'points': random.choice([50, 100, 150, 200, -500]),
                    'type': 'earned' if random.random() > 0.2 else 'redeemed',
                    'balance': 2450 - (i * 50)
                }
                for i in range(20)
            ],
            'rewards': [
                {
                    'id': str(uuid.uuid4()),
                    'name': '$10 Voucher',
                    'pointsRequired': 1000,
                    'value': 10,
                    'available': True,
                    'category': 'voucher',
                    'expiryDays': 30
                },
                {
                    'id': str(uuid.uuid4()),
                    'name': '$25 Voucher',
                    'pointsRequired': 2000,
                    'value': 25,
                    'available': True,
                    'category': 'voucher',
                    'expiryDays': 30
                },
                {
                    'id': str(uuid.uuid4()),
                    'name': '$50 Voucher',
                    'pointsRequired': 4000,
                    'value': 50,
                    'available': False,
                    'category': 'voucher',
                    'expiryDays': 30
                },
                {
                    'id': str(uuid.uuid4()),
                    'name': 'Free Shipping (3 months)',
                    'pointsRequired': 1500,
                    'value': 0,
                    'available': True,
                    'category': 'shipping',
                    'expiryDays': 90
                },
                {
                    'id': str(uuid.uuid4()),
                    'name': '20% Off Coupon',
                    'pointsRequired': 800,
                    'value': 20,
                    'available': True,
                    'category': 'discount',
                    'expiryDays': 14
                }
            ]
        }

    def _generate_wallet_data(self):
        """Generate wallet data"""
        transactions = []

        for i in range(30):
            trans_type = random.choice(['credit', 'debit'])
            trans_category = random.choice([
                'Added money', 'Purchase refund', 'Cashback earned',
                'Order payment', 'Withdrawal', 'Reward redeemed',
                'Referral bonus', 'Promotional credit'
            ])

            amount = round(random.uniform(5, 200), 2)

            transactions.append({
                'id': str(uuid.uuid4()),
                'date': (datetime.now() - timedelta(days=i)).isoformat(),
                'type': trans_type,
                'category': trans_category,
                'amount': amount if trans_type == 'credit' else -amount,
                'description': trans_category,
                'status': random.choice(['completed', 'completed', 'pending']),
                'reference': f'TXN{random.randint(100000, 999999)}',
                'balance': 125.50 + (amount if trans_type == 'credit' else -amount)
            })

        return {
            'balance': 125.50,
            'pendingAmount': 25.00,
            'totalAdded': 500.00,
            'totalSpent': 374.50,
            'transactions': sorted(transactions, key=lambda x: x['date'], reverse=True),
            'bankAccounts': [
                {
                    'id': 'bank1',
                    'bankName': 'Chase Bank',
                    'accountLast4': '1234',
                    'accountType': 'Checking',
                    'isDefault': True
                }
            ],
            'autoRecharge': {
                'enabled': False,
                'threshold': 20,
                'rechargeAmount': 100
            }
        }

    def _generate_referral_data(self):
        """Generate referral program data"""
        referrals = []

        for i in range(10):
            referrals.append({
                'id': str(uuid.uuid4()),
                'userName': f'Friend {i + 1}',
                'email': f'friend{i + 1}@example.com',
                'joinedDate': (datetime.now() - timedelta(days=random.randint(1, 90))).isoformat(),
                'status': random.choice(['completed', 'pending', 'expired']),
                'earned': round(random.uniform(5, 25), 2) if random.choice(
                    ['completed', 'pending']) == 'completed' else 0,
                'ordersMade': random.randint(0, 10)
            })

        return {
            'referralCode': 'MEGA2024',
            'shareUrl': 'https://megamart.com/ref/MEGA2024',
            'referredUsers': len(referrals),
            'totalEarnings': round(sum(r['earned'] for r in referrals), 2),
            'pendingEarnings': round(sum(r['earned'] for r in referrals if r['status'] == 'pending'), 2),
            'availableEarnings': round(sum(r['earned'] for r in referrals if r['status'] == 'completed'), 2),
            'referralHistory': referrals,
            'referralTerms': {
                'newUserBonus': 10,
                'referrerBonus': 15,
                'minimumPurchase': 50,
                'validityDays': 30
            },
            'stats': {
                'totalShares': random.randint(50, 200),
                'totalClicks': random.randint(100, 500),
                'conversionRate': f'{random.randint(10, 30)}%'
            }
        }

    def _generate_tracking_data(self):
        """Generate order tracking data"""
        tracking_statuses = [
            {
                'status': 'Order Placed',
                'date': (datetime.now() - timedelta(days=3)).isoformat(),
                'location': 'Online',
                'description': 'Your order has been successfully placed',
                'completed': True
            },
            {
                'status': 'Order Confirmed',
                'date': (datetime.now() - timedelta(days=3, hours=2)).isoformat(),
                'location': 'System',
                'description': 'Your order has been confirmed and is being processed',
                'completed': True
            },
            {
                'status': 'Packed',
                'date': (datetime.now() - timedelta(days=2)).isoformat(),
                'location': 'Warehouse',
                'description': 'Your order has been packed and is ready for shipment',
                'completed': True
            },
            {
                'status': 'Shipped',
                'date': (datetime.now() - timedelta(days=1)).isoformat(),
                'location': 'Distribution Center',
                'description': 'Your order has been shipped',
                'completed': True
            },
            {
                'status': 'Out for Delivery',
                'date': datetime.now().isoformat(),
                'location': 'Local Facility',
                'description': 'Your order is out for delivery',
                'completed': True
            },
            {
                'status': 'Delivered',
                'date': None,
                'location': 'Delivery Address',
                'description': 'Package will be delivered soon',
                'completed': False
            }
        ]

        return tracking_statuses

    def _generate_returns(self):
        """Generate return/refund data"""
        returns = []

        for i in range(5):
            order = random.choice(self.orders) if self.orders else None

            returns.append({
                'id': str(uuid.uuid4()),
                'orderId': order['id'] if order else str(uuid.uuid4()),
                'orderNumber': order['orderNumber'] if order else f'ORD{100000 + i}',
                'requestDate': (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat(),
                'reason': random.choice([
                    'Product damaged',
                    'Wrong item received',
                    'Not as described',
                    'Changed mind',
                    'Size issue'
                ]),
                'status': random.choice(['pending', 'approved', 'rejected', 'completed']),
                'refundAmount': round(random.uniform(20, 200), 2),
                'refundMethod': random.choice(['Wallet', 'Original Payment Method']),
                'returnMethod': random.choice(['Pickup', 'Drop at store', 'Courier']),
                'returnLabel': f'RTN{random.randint(100000, 999999)}',
                'notes': 'Processing your return request.'
            })

        return returns

    def _generate_questions(self):
        """Generate product Q&A"""
        questions = []

        question_templates = [
            'Is this product genuine?',
            'What is the warranty period?',
            'Is installation service available?',
            'What are the dimensions?',
            'Is this suitable for daily use?',
            'How long does delivery take?',
            'Is COD available?',
            'Can this be returned?'
        ]

        for i in range(100):
            product = random.choice(self.products) if self.products else None

            questions.append({
                'id': str(uuid.uuid4()),
                'productId': product['id'] if product else str(uuid.uuid4()),
                'question': random.choice(question_templates),
                'answer': 'Yes, this product comes with manufacturer warranty and is 100% genuine.' if random.random() > 0.3 else None,
                'askedBy': f'User{random.randint(1, 1000)}',
                'askedDate': (datetime.now() - timedelta(days=random.randint(1, 60))).isoformat(),
                'answeredBy': 'Seller' if random.random() > 0.3 else None,
                'answeredDate': (datetime.now() - timedelta(
                    days=random.randint(1, 30))).isoformat() if random.random() > 0.3 else None,
                'helpful': random.randint(0, 50)
            })

        return questions

    def _generate_notifications(self):
        """Generate user notifications"""
        notifications = []

        notification_templates = [
            ('Order Update', 'Your order #ORD{} has been {}', 'order'),
            ('Price Drop', '{} is now available at {}% off', 'promotion'),
            ('New Message', 'You have a new message from {}', 'message'),
            ('Wishlist Alert', '{} from your wishlist is back in stock', 'wishlist'),
            ('Reward Points', 'You earned {} points from your recent purchase', 'reward'),
            ('Flash Sale', 'Flash sale starting in 1 hour! Up to {}% off', 'sale'),
            ('Delivery Update', 'Your package will be delivered today', 'delivery')
        ]

        for i in range(30):
            template = random.choice(notification_templates)

            notifications.append({
                'id': str(uuid.uuid4()),
                'title': template[0],
                'message': template[1].format(
                    random.randint(100000, 999999),
                    random.choice(['shipped', 'delivered', 'processing'])
                ) if 'Order' in template[0] else template[1].format(random.randint(10, 70)),
                'type': template[2],
                'date': (datetime.now() - timedelta(hours=random.randint(1, 168))).isoformat(),
                'read': random.choice([True, False, False]),
                'actionUrl': f'/orders/{uuid.uuid4()}' if 'order' in template[2] else None,
                'icon': random.choice(['notifications', 'local_offer', 'message', 'favorite', 'stars'])
            })

        return sorted(notifications, key=lambda x: x['date'], reverse=True)

    def _generate_messages(self):
        """Generate chat messages"""
        messages = []

        for i in range(20):
            messages.append({
                'id': str(uuid.uuid4()),
                'senderId': str(uuid.uuid4()),
                'senderName': random.choice(['Support Team', 'Seller', 'Customer Service']),
                'senderAvatar': f'https://picsum.photos/50/50?random=sender{i}',
                'message': random.choice([
                    'How can I help you today?',
                    'Your order has been processed.',
                    'Thank you for your purchase!',
                    'Is there anything else you need?',
                    'We have received your inquiry.'
                ]),
                'timestamp': (datetime.now() - timedelta(hours=random.randint(1, 72))).isoformat(),
                'read': random.choice([True, False]),
                'type': random.choice(['text', 'text', 'image', 'order'])
            })

        return messages

    def _generate_chat_data(self):
        """Generate live chat data"""
        return {
            'chatId': str(uuid.uuid4()),
            'sellerId': str(uuid.uuid4()),
            'sellerName': 'MegaMart Support',
            'sellerAvatar': 'https://picsum.photos/50/50?random=support',
            'online': True,
            'typing': False,
            'messages': [
                {
                    'id': str(uuid.uuid4()),
                    'text': 'Hello! How can I help you today?',
                    'sender': 'seller',
                    'timestamp': (datetime.now() - timedelta(minutes=5)).isoformat(),
                    'read': True
                },
                {
                    'id': str(uuid.uuid4()),
                    'text': 'I have a question about my order',
                    'sender': 'user',
                    'timestamp': (datetime.now() - timedelta(minutes=4)).isoformat(),
                    'read': True
                },
                {
                    'id': str(uuid.uuid4()),
                    'text': 'Sure! Please provide your order number.',
                    'sender': 'seller',
                    'timestamp': (datetime.now() - timedelta(minutes=3)).isoformat(),
                    'read': True
                }
            ]
        }

    def _generate_faqs(self):
        """Generate FAQs"""
        faqs = []

        faq_data = {
            'Orders': [
                'How do I track my order?',
                'Can I cancel my order?',
                'How do I change my delivery address?',
                'What payment methods are accepted?'
            ],
            'Shipping': [
                'How long does delivery take?',
                'Do you ship internationally?',
                'What are the shipping charges?',
                'How do I get free shipping?'
            ],
            'Returns': [
                'What is your return policy?',
                'How do I return an item?',
                'When will I get my refund?',
                'Who pays for return shipping?'
            ],
            'Account': [
                'How do I reset my password?',
                'How do I update my profile?',
                'How do I delete my account?',
                'How do I subscribe to newsletter?'
            ]
        }

        for category, questions in faq_data.items():
            for question in questions:
                faqs.append({
                    'id': str(uuid.uuid4()),
                    'category': category,
                    'question': question,
                    'answer': f'To {question.lower()[:-1]}, please follow these steps: 1) Go to your account, 2) Select the relevant option, 3) Follow the instructions provided.',
                    'helpful': random.randint(50, 500),
                    'notHelpful': random.randint(0, 50)
                })

        return faqs

    def _generate_help_articles(self):
        """Generate help articles"""
        articles = []

        article_titles = [
            'Getting Started with MegaMart',
            'How to Place Your First Order',
            'Understanding Shipping Options',
            'Payment Security Guide',
            'Return and Refund Process',
            'Loyalty Program Benefits',
            'Using Coupons and Promotions',
            'Seller Guidelines',
            'Product Authentication',
            'Mobile App Features'
        ]

        for title in article_titles:
            articles.append({
                'id': str(uuid.uuid4()),
                'title': title,
                'category': random.choice(['Getting Started', 'Orders', 'Payments', 'Account']),
                'content': f'Detailed guide about {title.lower()}. This article covers everything you need to know...',
                'author': 'MegaMart Support',
                'lastUpdated': (datetime.now() - timedelta(days=random.randint(1, 60))).isoformat(),
                'views': random.randint(100, 5000),
                'helpful': random.randint(80, 100),
                'tags': random.sample(['guide', 'tutorial', 'faq', 'tips', 'help'], 3)
            })

        return articles

    def _generate_support_tickets(self):
        """Generate support tickets"""
        tickets = []

        for i in range(10):
            tickets.append({
                'id': str(uuid.uuid4()),
                'ticketNumber': f'TKT{100000 + i}',
                'subject': random.choice([
                    'Order not received',
                    'Refund not processed',
                    'Account access issue',
                    'Product quality concern',
                    'Payment failed'
                ]),
                'status': random.choice(['open', 'in_progress', 'resolved', 'closed']),
                'priority': random.choice(['low', 'medium', 'high']),
                'createdAt': (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat(),
                'lastUpdated': (datetime.now() - timedelta(days=random.randint(0, 7))).isoformat(),
                'assignedTo': 'Support Agent',
                'messages': random.randint(1, 10)
            })

        return tickets

    def _generate_coupons(self):
        """Generate available coupons"""
        coupons = []

        coupon_codes = [
            'SAVE10', 'SAVE20', 'SAVE30', 'WELCOME20',
            'FIRSTORDER', 'FREESHIP', 'WEEKEND15',
            'FLASH50', 'MEGA25', 'SPECIAL40'
        ]

        for code in coupon_codes:
            coupons.append({
                'code': code,
                'discount': f'{random.choice([10, 15, 20, 25, 30])}%',
                'discountType': random.choice(['percentage', 'fixed']),
                'discountValue': random.choice([10, 15, 20, 25, 30]),
                'minPurchase': random.choice([0, 50, 100, 150, 200]),
                'maxDiscount': random.choice([50, 100, 200]),
                'validFrom': datetime.now().isoformat(),
                'validUntil': (datetime.now() + timedelta(days=random.randint(7, 30))).isoformat(),
                'used': random.choice([True, False, False]),
                'usageLimit': random.choice([1, 3, 5]),
                'description': 'Special discount on selected items',
                'terms': 'Cannot be combined with other offers',
                'applicableCategories': random.sample([c['id'] for c in self.categories], random.randint(1, 5))
            })

        return coupons

    def _generate_gift_cards(self):
        """Generate gift cards"""
        gift_cards = []

        for i in range(5):
            gift_cards.append({
                'id': str(uuid.uuid4()),
                'code': f'GIFT{random.randint(100000, 999999)}',
                'balance': random.choice([25, 50, 100, 200]),
                'originalValue': random.choice([25, 50, 100, 200]),
                'expiryDate': (datetime.now() + timedelta(days=365)).isoformat(),
                'status': random.choice(['active', 'partially_used', 'expired']),
                'purchasedDate': (datetime.now() - timedelta(days=random.randint(1, 90))).isoformat(),
                'from': 'John Doe',
                'to': 'Jane Smith',
                'message': 'Happy Birthday!'
            })

        return gift_cards

    def _generate_subscriptions(self):
        """Generate subscription plans"""
        return [
            {
                'id': str(uuid.uuid4()),
                'name': 'MegaMart Plus',
                'price': 9.99,
                'duration': 'monthly',
                'benefits': [
                    'Free shipping on all orders',
                    'Exclusive member deals',
                    '2x loyalty points',
                    'Early access to sales',
                    'Priority customer support'
                ],
                'savings': 'Save up to $200/year',
                'popular': False,
                'trial': 30
            },
            {
                'id': str(uuid.uuid4()),
                'name': 'MegaMart Premium',
                'price': 79.99,
                'duration': 'yearly',
                'benefits': [
                    'All Plus benefits',
                    'Same-day delivery',
                    '5% cashback on all purchases',
                    'Extended return period (60 days)',
                    'Exclusive premium products',
                    'Personal shopping assistant'
                ],
                'savings': 'Save up to $500/year',
                'popular': True,
                'trial': 30
            }
        ]

    def _generate_seller_dashboard(self):
        """Generate seller dashboard data"""
        return {
            'sales': round(random.uniform(5000, 50000), 2),
            'orders': random.randint(50, 500),
            'revenue': round(random.uniform(10000, 100000), 2),
            'products': random.randint(20, 200),
            'metrics': {
                'views': random.randint(1000, 50000),
                'conversion': round(random.uniform(1, 10), 2),
                'rating': round(random.uniform(4.0, 5.0), 1),
                'responseTime': f'{random.randint(1, 12)} hours',
                'fulfillmentRate': f'{random.randint(90, 100)}%'
            },
            'todayStats': {
                'sales': round(random.uniform(100, 1000), 2),
                'orders': random.randint(5, 50),
                'views': random.randint(100, 1000)
            },
            'chartData': {
                'salesTrend': [random.randint(100, 1000) for _ in range(7)],
                'ordersTrend': [random.randint(10, 100) for _ in range(7)],
                'dates': [(datetime.now() - timedelta(days=i)).strftime('%b %d') for i in range(6, -1, -1)]
            }
        }

    def _generate_seller_analytics(self):
        """Generate seller analytics data"""
        return {
            'performance': {
                'salesGrowth': f'{random.choice(["+", "-"])}{random.randint(5, 50)}%',
                'orderGrowth': f'{random.choice(["+", "-"])}{random.randint(5, 30)}%',
                'conversionRate': f'{round(random.uniform(1, 10), 2)}%',
                'averageOrderValue': round(random.uniform(50, 200), 2)
            },
            'topProducts': random.sample(self.products, min(10, len(self.products))),
            'customerStats': {
                'totalCustomers': random.randint(100, 5000),
                'newCustomers': random.randint(10, 100),
                'repeatCustomers': random.randint(50, 500),
                'satisfaction': f'{random.randint(85, 100)}%'
            },
            'geographicData': {
                'topCities': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'],
                'topStates': ['CA', 'TX', 'NY', 'FL', 'IL']
            }
        }


# Create singleton instance
marketplace_data = CompleteMarketplaceMockData()