"""Mock data for e-commerce applications"""

from .base_mock_data import BaseMockData


class EcommerceMockData(BaseMockData):
    """Mock data provider for e-commerce applications"""

    def get_data_sources(self):
        return {
            "Products": self.get_products(),
            "Categories": self.get_categories(),
            "Cart": self.get_cart_items(),
            "Orders": self.get_orders(),
            "Reviews": self.get_reviews()
        }

    def get_products(self):
        return [
            {
                "id": "1",
                "title": "Wireless Bluetooth Headphones",
                "description": "Premium noise-cancelling headphones with 30-hour battery life",
                "price": 199.99,
                "originalPrice": 299.99,
                "discount": 33,
                "category": "Electronics",
                "image": "https://picsum.photos/300/300?random=prod1",
                "rating": 4.5,
                "reviews": 234,
                "inStock": True,
                "brand": "TechSound"
            },
            {
                "id": "2",
                "title": "Smart Watch Pro",
                "description": "Fitness tracker with heart rate monitor and GPS",
                "price": 349.00,
                "originalPrice": 399.00,
                "discount": 12,
                "category": "Electronics",
                "image": "https://picsum.photos/300/300?random=prod2",
                "rating": 4.7,
                "reviews": 567,
                "inStock": True,
                "brand": "FitTech"
            },
            {
                "id": "3",
                "title": "Organic Cotton T-Shirt",
                "description": "Comfortable and sustainable fashion",
                "price": 29.99,
                "category": "Clothing",
                "image": "https://picsum.photos/300/300?random=prod3",
                "rating": 4.3,
                "reviews": 89,
                "inStock": True,
                "sizes": ["S", "M", "L", "XL"],
                "colors": ["White", "Black", "Navy", "Grey"]
            },
            # Add more products...
        ]

    def get_categories(self):
        return [
            {
                "id": "1",
                "name": "Electronics",
                "icon": "devices",
                "image": "https://picsum.photos/200/200?random=cat1",
                "productCount": 245
            },
            {
                "id": "2",
                "name": "Clothing",
                "icon": "checkroom",
                "image": "https://picsum.photos/200/200?random=cat2",
                "productCount": 532
            },
            {
                "id": "3",
                "name": "Home & Garden",
                "icon": "home",
                "image": "https://picsum.photos/200/200?random=cat3",
                "productCount": 178
            },
            # Add more categories...
        ]

    def get_cart_items(self):
        return [
            {
                "id": "cart1",
                "productId": "1",
                "productName": "Wireless Bluetooth Headphones",
                "price": 199.99,
                "quantity": 1,
                "image": "https://picsum.photos/100/100?random=cart1"
            },
            {
                "id": "cart2",
                "productId": "3",
                "productName": "Organic Cotton T-Shirt",
                "price": 29.99,
                "quantity": 2,
                "size": "M",
                "color": "Navy",
                "image": "https://picsum.photos/100/100?random=cart2"
            }
        ]

    def get_orders(self):
        return [
            {
                "id": "order1",
                "orderNumber": "ORD-2024-001",
                "date": "2024-01-10",
                "status": "Delivered",
                "total": 229.98,
                "items": 2
            },
            {
                "id": "order2",
                "orderNumber": "ORD-2024-002",
                "date": "2024-01-14",
                "status": "Shipped",
                "total": 349.00,
                "items": 1
            }
        ]

    def get_reviews(self):
        return [
            {
                "id": "rev1",
                "productId": "1",
                "user": "John D.",
                "rating": 5,
                "comment": "Excellent sound quality and battery life!",
                "date": "2024-01-12",
                "helpful": 45
            },
            {
                "id": "rev2",
                "productId": "1",
                "user": "Sarah M.",
                "rating": 4,
                "comment": "Great product, but wish it had more color options",
                "date": "2024-01-10",
                "helpful": 23
            }
        ]

    def get_sample_images(self):
        return {
            "products": [f"https://picsum.photos/300/300?random=p{i}" for i in range(1, 11)],
            "banners": [f"https://picsum.photos/800/400?random=b{i}" for i in range(1, 4)],
            "categories": [f"https://picsum.photos/200/200?random=c{i}" for i in range(1, 7)]
        }