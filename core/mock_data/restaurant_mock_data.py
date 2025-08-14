"""Mock data for restaurant applications"""

from .base_mock_data import BaseMockData


class RestaurantMockData(BaseMockData):
    """Mock data provider for restaurant applications"""

    def get_data_sources(self):
        return {
            "Menu Items": self.get_menu_items(),
            "Categories": self.get_categories(),
            "Special Offers": self.get_special_offers(),
            "Reviews": self.get_reviews(),
            "Reservations": self.get_reservations()
        }

    def get_menu_items(self):
        return [
            {
                "id": "1",
                "name": "Classic Burger",
                "description": "Juicy beef patty with lettuce, tomato, and our special sauce",
                "price": 12.99,
                "category": "Main Course",
                "image": "https://picsum.photos/300/300?random=food1",
                "calories": 650,
                "rating": 4.6,
                "isVegetarian": False,
                "isSpicy": False,
                "preparationTime": "15 min"
            },
            {
                "id": "2",
                "name": "Caesar Salad",
                "description": "Fresh romaine lettuce with parmesan and croutons",
                "price": 8.99,
                "category": "Starters",
                "image": "https://picsum.photos/300/300?random=food2",
                "calories": 320,
                "rating": 4.4,
                "isVegetarian": True,
                "isSpicy": False,
                "preparationTime": "10 min"
            },
            {
                "id": "3",
                "name": "Spicy Chicken Wings",
                "description": "Crispy wings with our signature hot sauce",
                "price": 10.99,
                "category": "Starters",
                "image": "https://picsum.photos/300/300?random=food3",
                "calories": 480,
                "rating": 4.8,
                "isVegetarian": False,
                "isSpicy": True,
                "preparationTime": "20 min"
            },
            # Add more menu items...
        ]

    def get_categories(self):
        return [
            {"id": "1", "name": "Starters", "icon": "restaurant_menu", "itemCount": 12},
            {"id": "2", "name": "Main Course", "icon": "dinner_dining", "itemCount": 20},
            {"id": "3", "name": "Desserts", "icon": "cake", "itemCount": 8},
            {"id": "4", "name": "Beverages", "icon": "local_cafe", "itemCount": 15},
            {"id": "5", "name": "Specials", "icon": "star", "itemCount": 5}
        ]

    def get_special_offers(self):
        return [
            {
                "id": "offer1",
                "title": "Happy Hour Special",
                "description": "50% off on all beverages",
                "validFrom": "16:00",
                "validTo": "18:00",
                "discount": 50,
                "image": "https://picsum.photos/400/200?random=offer1"
            },
            {
                "id": "offer2",
                "title": "Family Combo",
                "description": "Complete meal for 4 at special price",
                "price": 49.99,
                "originalPrice": 79.99,
                "image": "https://picsum.photos/400/200?random=offer2"
            }
        ]

    def get_reviews(self):
        return [
            {
                "id": "r1",
                "customer": "Alice B.",
                "rating": 5,
                "comment": "Amazing food and great service!",
                "date": "2024-01-14"
            },
            {
                "id": "r2",
                "customer": "Bob K.",
                "rating": 4,
                "comment": "Good food, but a bit crowded on weekends",
                "date": "2024-01-13"
            }
        ]

    def get_reservations(self):
        return [
            {
                "id": "res1",
                "customerName": "John Smith",
                "date": "2024-01-20",
                "time": "19:00",
                "guests": 4,
                "table": "T12",
                "status": "Confirmed"
            }
        ]

    def get_sample_images(self):
        return {
            "food": [f"https://picsum.photos/300/300?random=food{i}" for i in range(1, 21)],
            "restaurant": [f"https://picsum.photos/400/300?random=rest{i}" for i in range(1, 6)],
            "offers": [f"https://picsum.photos/600/300?random=offer{i}" for i in range(1, 4)]
        }