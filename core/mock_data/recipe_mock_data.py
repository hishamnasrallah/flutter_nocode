# File: core/mock_data/recipe_mock_data.py
"""
Mock data for a Recipe & Meal Planner application.
"""

import random
import uuid
from datetime import datetime, timedelta
from .base_mock_data import BaseMockData


class RecipeMockData(BaseMockData):
    """Mock data provider for a Recipe & Meal Planner application."""

    def __init__(self):
        self.categories = self._generate_categories()
        self.recipes = self._generate_recipes()

    def get_data_sources(self):
        """Return dictionary of data source names and their mock data."""
        return {
            "Recipes": self.recipes,
            "Categories": self.categories,
            "Favorite Recipes": self._generate_favorite_recipes(),
            "Shopping List": self._generate_shopping_list(),
            "Nutritional Info": self._generate_nutritional_info(),
        }

    def get_sample_images(self):
        """Return dictionary of image categories and URLs."""
        return {
            "recipes": [f"https://picsum.photos/600/400?random=recipe{i}" for i in range(1, 51)],
            "categories": [f"https://picsum.photos/400/300?random=cat{i}" for i in range(1, 11)],
            "avatars": [f"https://picsum.photos/100/100?random=user{i}" for i in range(1, 6)],
        }

    def _generate_categories(self):
        """Generate mock recipe categories."""
        categories = [
            {"id": "1", "name": "Breakfast", "icon": "free_breakfast",
             "image": "https://picsum.photos/400/300?random=breakfast"},
            {"id": "2", "name": "Lunch", "icon": "lunch_dining", "image": "https://picsum.photos/400/300?random=lunch"},
            {"id": "3", "name": "Dinner", "icon": "dinner_dining",
             "image": "https://picsum.photos/400/300?random=dinner"},
            {"id": "4", "name": "Desserts", "icon": "cake", "image": "https://picsum.photos/400/300?random=dessert"},
            {"id": "5", "name": "Appetizers", "icon": "tapas",
             "image": "https://picsum.photos/400/300?random=appetizer"},
            {"id": "6", "name": "Italian", "icon": "local_pizza",
             "image": "https://picsum.photos/400/300?random=italian"},
            {"id": "7", "name": "Mexican", "icon": "local_dining",
             "image": "https://picsum.photos/400/300?random=mexican"},
            {"id": "8", "name": "Asian", "icon": "ramen_dining", "image": "https://picsum.photos/400/300?random=asian"},
            {"id": "9", "name": "Vegetarian", "icon": "eco",
             "image": "https://picsum.photos/400/300?random=vegetarian"},
            {"id": "10", "name": "Healthy", "icon": "fitness_center",
             "image": "https://picsum.photos/400/300?random=healthy"},
        ]
        return categories

    def _generate_recipes(self):
        """Generate mock recipe data."""
        recipes = []
        recipe_names = [
            "Spicy Chicken Tacos", "Classic Beef Lasagna", "Vegetable Stir-fry", "Homemade Pizza",
            "Creamy Tomato Pasta", "Lemon Herb Salmon", "Quinoa Salad with Avocado", "Chocolate Lava Cake",
            "Blueberry Pancakes", "Avocado Toast with Egg", "Chicken Noodle Soup", "Beef and Broccoli",
            "Shrimp Scampi", "Mushroom Risotto", "Apple Pie", "Banana Bread", "French Toast",
            "Grilled Cheese Sandwich", "Tomato Soup", "Caesar Salad", "Chicken Curry", "Pad Thai",
            "Sushi Rolls", "Fish and Chips", "Shepherd's Pie", "Tiramisu", "Cheesecake", "Brownies",
            "Oatmeal Cookies", "Smoothie Bowl", "Breakfast Burrito", "Eggs Benedict", "Waffles",
            "Chicken Caesar Wrap", "Turkey Club Sandwich", "Minestrone Soup", "Lentil Soup",
            "Chicken Pot Pie", "Beef Stew", "Pork Chops with Apples", "Roasted Chicken", "Baked Ziti",
            "Gnocchi with Pesto", "Tuna Melt", "Eggplant Parmesan", "Spinach and Artichoke Dip",
            "Guacamole", "Hummus", "Bruschetta", "Spring Rolls"
        ]

        ingredients_list = [
            ["chicken breast", "taco shells", "lettuce", "tomato", "cheddar cheese", "salsa", "sour cream"],
            ["ground beef", "lasagna noodles", "ricotta cheese", "mozzarella", "marinara sauce", "onion", "garlic"],
            ["broccoli", "carrots", "bell peppers", "soy sauce", "ginger", "garlic", "rice noodles"],
            ["pizza dough", "tomato sauce", "mozzarella", "pepperoni", "mushrooms", "bell peppers"],
            ["pasta", "canned tomatoes", "heavy cream", "garlic", "basil", "parmesan cheese"],
            ["salmon fillets", "lemon", "fresh dill", "garlic", "olive oil", "asparagus"],
            ["quinoa", "avocado", "cherry tomatoes", "cucumber", "red onion", "lime juice", "cilantro"],
            ["dark chocolate", "butter", "eggs", "sugar", "flour", "vanilla extract"],
            ["flour", "milk", "eggs", "baking powder", "sugar", "blueberries"],
            ["avocado", "bread", "egg", "chili flakes", "salt", "pepper"],
        ]

        instructions_list = [
            ["Cook chicken, season. Warm taco shells. Assemble with toppings."],
            ["Brown beef. Layer noodles, sauce, cheese. Bake until bubbly."],
            ["Sauté vegetables. Add sauce. Toss with noodles."],
            ["Roll out dough. Add sauce, cheese, toppings. Bake until golden."],
            ["Cook pasta. Sauté garlic. Add tomatoes, cream. Combine with pasta."],
            ["Season salmon. Bake with lemon and dill. Roast asparagus."],
            ["Cook quinoa. Chop vegetables. Mix with dressing."],
            ["Melt chocolate and butter. Mix with eggs, sugar, flour. Bake until edges are set."],
            ["Mix dry ingredients. Add wet. Fold in blueberries. Cook on griddle."],
            ["Toast bread. Mash avocado. Fry egg. Top toast with avocado and egg."],
        ]

        cooking_times = ["15-20 min", "45-60 min", "30-40 min", "25-35 min", "20-30 min", "30-45 min"]
        difficulties = ["Easy", "Medium", "Hard"]

        for i, name in enumerate(recipe_names):
            category = random.choice(self.categories)
            recipe_id = str(uuid.uuid4())
            recipes.append({
                "id": recipe_id,
                "name": name,
                "description": f"A delicious and easy-to-make {name.lower()} recipe, perfect for any occasion.",
                "imageUrl": self.get_sample_images()["recipes"][i % len(self.get_sample_images()["recipes"])],
                "ingredients": random.choice(ingredients_list),
                "instructions": random.choice(instructions_list),
                "cookingTime": random.choice(cooking_times),
                "servingSize": random.randint(2, 6),
                "difficulty": random.choice(difficulties),
                "category": category["name"],
                "categoryId": category["id"],
                "prepTime": f"{random.randint(5, 15)} min",
                "calories": random.randint(300, 800),
                "rating": round(random.uniform(3.5, 5.0), 1),
                "reviewCount": random.randint(10, 200),
                "isFavorite": random.choice([True, False]),
                "author": f"Chef {random.choice(['John', 'Jane', 'Mike', 'Sarah'])}",
                "publishedDate": (datetime.now() - timedelta(days=random.randint(1, 365))).isoformat(),
            })
        return recipes

    def _generate_favorite_recipes(self):
        """Generate mock favorite recipes."""
        return random.sample(self.recipes, min(5, len(self.recipes)))

    def _generate_shopping_list(self):
        """Generate mock shopping list."""
        selected_recipes = random.sample(self.recipes, min(3, len(self.recipes)))
        shopping_list_items = {}
        for recipe in selected_recipes:
            for ingredient in recipe["ingredients"]:
                item = ingredient.lower()
                shopping_list_items[item] = shopping_list_items.get(item, 0) + 1  # Simple count for now

        # Convert to a list of dicts for easier consumption
        return [{"item": k, "quantity": v, "unit": "unit(s)"} for k, v in shopping_list_items.items()]

    def _generate_nutritional_info(self):
        """Generate mock nutritional information."""
        return {
            "calories": random.randint(300, 800),
            "protein": f"{random.randint(10, 50)}g",
            "carbs": f"{random.randint(20, 100)}g",
            "fat": f"{random.randint(5, 40)}g",
        }

    # API methods for specific endpoints
    def get_all_recipes(self):
        return self.recipes

    def get_recipe_detail(self, recipe_id):
        for recipe in self.recipes:
            if recipe["id"] == recipe_id:
                return recipe
        return None

    def get_recipes_by_category(self, category_id):
        return [r for r in self.recipes if r["categoryId"] == category_id]

    def search_recipes(self, query):
        query_lower = query.lower()
        return [
            r for r in self.recipes
            if query_lower in r["name"].lower() or
               any(query_lower in ing.lower() for ing in r["ingredients"])
        ]
