# File: core/management/commands/create_recipe_app.py
"""
Management command to create a comprehensive Recipe & Meal Planner application.
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import (
    Application, Theme, Screen, Widget, WidgetProperty,
    Action, DataSource, DataSourceField
)


class Command(BaseCommand):
    help = 'Create a comprehensive Recipe & Meal Planner application'

    def add_arguments(self, parser):
        parser.add_argument(
            '--name',
            type=str,
            default='RecipeHub',
            help='Custom name for the recipe application'
        )
        parser.add_argument(
            '--package',
            type=str,
            default='com.recipehub.app',
            help='Package identifier for the application'
        )

    def handle(self, *args, **options):
        app_name = options['name']
        package_name = options['package']

        try:
            with transaction.atomic():
                app = create_recipe_app(app_name, package_name)
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully created Recipe & Meal Planner application: {app.name}'
                    )
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating recipe application: {str(e)}')
            )


def create_recipe_app(custom_name=None, package_name=None):
    """Create a comprehensive Recipe & Meal Planner application."""

    # Create a vibrant food-themed theme
    theme = Theme.objects.create(
        name="RecipeHub Theme",
        primary_color="#FF5722",  # Deep Orange
        accent_color="#FFC107",   # Amber
        background_color="#FFF3E0",  # Light Orange Background
        text_color="#3E2723",  # Dark Brown Text
        font_family="Roboto",
        is_dark_mode=False
    )

    # Create application
    app = Application.objects.create(
        name=custom_name or "Recipe & Meal Planner",
        description="""A comprehensive recipe and meal planning application. Browse thousands of recipes, 
        create shopping lists, save favorites, and plan your meals with ease.""",
        package_name=package_name or "com.recipehub.app",
        version="1.0.0",
        theme=theme
    )

    # Base URL for mock APIs
    base_url = "http://localhost:8000"

    # Create data sources
    data_sources = create_data_sources(app, base_url)

    # Create actions
    actions = create_actions(app, data_sources)

    # Create screens
    screens = create_screens(app)

    # Update actions with screen references
    update_action_targets(actions, screens)

    # Create widgets for each screen
    create_home_screen_widgets(screens['home'], data_sources, actions)
    create_recipe_list_screen_widgets(screens['recipe_list'], data_sources, actions)
    create_recipe_details_screen_widgets(screens['recipe_details'], data_sources, actions)
    create_categories_screen_widgets(screens['categories'], data_sources, actions)
    create_favorites_screen_widgets(screens['favorites'], data_sources, actions)
    create_shopping_list_screen_widgets(screens['shopping_list'], data_sources, actions)
    create_search_screen_widgets(screens['search'], data_sources, actions)
    create_profile_screen_widgets(screens['profile'], data_sources, actions)

    return app


def create_data_sources(app, base_url):
    """Create all data sources for the recipe app."""
    data_sources = {}

    # Recipes data source
    recipes_ds = DataSource.objects.create(
        application=app,
        name="Recipes",
        data_source_type="REST_API",
        base_url=base_url,
        endpoint="/api/mock/recipes/all",
        method="GET"
    )
    recipe_fields = [
        ("id", "string", "Recipe ID", True),
        ("name", "string", "Recipe Name", True),
        ("description", "string", "Description", False),
        ("imageUrl", "image_url", "Image URL", True),
        ("ingredients", "string", "Ingredients (JSON)", True), # Will be parsed as list in Flutter
        ("instructions", "string", "Instructions (JSON)", True), # Will be parsed as list in Flutter
        ("cookingTime", "string", "Cooking Time", False),
        ("servingSize", "integer", "Serving Size", False),
        ("difficulty", "string", "Difficulty", False),
        ("category", "string", "Category Name", True),
        ("categoryId", "string", "Category ID", True),
        ("prepTime", "string", "Preparation Time", False),
        ("calories", "integer", "Calories", False),
        ("rating", "decimal", "Rating", False),
        ("reviewCount", "integer", "Review Count", False),
        ("isFavorite", "boolean", "Is Favorite", False),
        ("author", "string", "Author", False),
        ("publishedDate", "datetime", "Published Date", False),
    ]
    for field_name, field_type, display_name, is_required in recipe_fields:
        DataSourceField.objects.create(
            data_source=recipes_ds,
            field_name=field_name,
            field_type=field_type,
            display_name=display_name,
            is_required=is_required
        )
    data_sources['recipes'] = recipes_ds

    # Categories data source
    categories_ds = DataSource.objects.create(
        application=app,
        name="Categories",
        data_source_type="REST_API",
        base_url=base_url,
        endpoint="/api/mock/recipes/categories",
        method="GET"
    )
    category_fields = [
        ("id", "string", "Category ID", True),
        ("name", "string", "Category Name", True),
        ("icon", "string", "Category Icon", False),
        ("image", "image_url", "Category Image", False),
    ]
    for field_name, field_type, display_name, is_required in category_fields:
        DataSourceField.objects.create(
            data_source=categories_ds,
            field_name=field_name,
            field_type=field_type,
            display_name=display_name,
            is_required=is_required
        )
    data_sources['categories'] = categories_ds

    # Favorites data source (mocked for now)
    favorites_ds = DataSource.objects.create(
        application=app,
        name="Favorite Recipes",
        data_source_type="REST_API",
        base_url=base_url,
        endpoint="/api/mock/recipes/favorites",
        method="GET"
    )
    # Fields for favorites will be similar to recipes, or just a list of IDs
    DataSourceField.objects.create(data_source=favorites_ds, field_name="id", field_type="string", display_name="Recipe ID", is_required=True)
    DataSourceField.objects.create(data_source=favorites_ds, field_name="name", field_type="string", display_name="Recipe Name", is_required=True)
    DataSourceField.objects.create(data_source=favorites_ds, field_name="imageUrl", field_type="image_url", display_name="Image URL", is_required=False)
    data_sources['favorites'] = favorites_ds

    # Shopping List data source (mocked for now)
    shopping_list_ds = DataSource.objects.create(
        application=app,
        name="Shopping List",
        data_source_type="REST_API",
        base_url=base_url,
        endpoint="/api/mock/recipes/shopping-list",
        method="GET"
    )
    DataSourceField.objects.create(data_source=shopping_list_ds, field_name="item", field_type="string", display_name="Item Name", is_required=True)
    DataSourceField.objects.create(data_source=shopping_list_ds, field_name="quantity", field_type="integer", display_name="Quantity", is_required=True)
    DataSourceField.objects.create(data_source=shopping_list_ds, field_name="unit", field_type="string", display_name="Unit", is_required=False)
    data_sources['shopping_list'] = shopping_list_ds

    return data_sources


def create_actions(app, data_sources):
    """Create all actions for the recipe app."""
    actions = {}

    # Navigation actions
    nav_actions = [
        ("Navigate to Recipe Details", "navigate"),
        ("Navigate to Categories", "navigate"),
        ("Navigate to Favorites", "navigate"),
        ("Navigate to Shopping List", "navigate"),
        ("Navigate to Search", "navigate"),
        ("Navigate to Profile", "navigate"),
        ("Go Back", "navigate_back"),
    ]
    for name, action_type in nav_actions:
        action = Action.objects.create(
            application=app,
            name=name,
            action_type=action_type
        )
        actions[name] = action

    # Recipe specific actions
    actions["Add to Favorites"] = Action.objects.create(
        application=app,
        name="Add to Favorites",
        action_type="save_data", # Mock save
        dialog_title="Favorite Added",
        dialog_message="Recipe added to your favorites!"
    )
    actions["Remove from Favorites"] = Action.objects.create(
        application=app,
        name="Remove from Favorites",
        action_type="save_data", # Mock save
        dialog_title="Favorite Removed",
        dialog_message="Recipe removed from your favorites."
    )
    actions["Generate Shopping List"] = Action.objects.create(
        application=app,
        name="Generate Shopping List",
        action_type="api_call", # Mock API call
        api_data_source=data_sources['shopping_list'],
        dialog_title="Shopping List Generated",
        dialog_message="Your shopping list has been updated!"
    )
    actions["Share Recipe"] = Action.objects.create(
        application=app,
        name="Share Recipe",
        action_type="share_content",
        dialog_title="Share Recipe",
        dialog_message="Share this delicious recipe!"
    )
    actions["Search Recipes"] = Action.objects.create(
        application=app,
        name="Search Recipes",
        action_type="api_call",
        api_data_source=data_sources['recipes'] # This will be used for search
    )

    return actions


def create_screens(app):
    """Create all screens for the recipe app."""
    screens = {}

    screens['home'] = Screen.objects.create(
        application=app,
        name="Home",
        route_name="/",
        is_home_screen=True,
        app_bar_title="RecipeHub",
        show_app_bar=True,
        show_back_button=False
    )
    screens['recipe_list'] = Screen.objects.create(
        application=app,
        name="Recipe List",
        route_name="/recipes",
        is_home_screen=False,
        app_bar_title="All Recipes",
        show_app_bar=True,
        show_back_button=True
    )
    screens['recipe_details'] = Screen.objects.create(
        application=app,
        name="Recipe Details",
        route_name="/recipe-details",
        is_home_screen=False,
        app_bar_title="Recipe",
        show_app_bar=True,
        show_back_button=True
    )
    screens['categories'] = Screen.objects.create(
        application=app,
        name="Categories",
        route_name="/categories",
        is_home_screen=False,
        app_bar_title="Categories",
        show_app_bar=True,
        show_back_button=True
    )
    screens['favorites'] = Screen.objects.create(
        application=app,
        name="Favorites",
        route_name="/favorites",
        is_home_screen=False,
        app_bar_title="My Favorites",
        show_app_bar=True,
        show_back_button=True
    )
    screens['shopping_list'] = Screen.objects.create(
        application=app,
        name="Shopping List",
        route_name="/shopping-list",
        is_home_screen=False,
        app_bar_title="Shopping List",
        show_app_bar=True,
        show_back_button=True
    )
    screens['search'] = Screen.objects.create(
        application=app,
        name="Search",
        route_name="/search",
        is_home_screen=False,
        app_bar_title="Search Recipes",
        show_app_bar=True,
        show_back_button=True
    )
    screens['profile'] = Screen.objects.create(
        application=app,
        name="Profile",
        route_name="/profile",
        is_home_screen=False,
        app_bar_title="My Profile",
        show_app_bar=True,
        show_back_button=True
    )

    return screens


def update_action_targets(actions, screens):
    """Update navigation actions with their target screens."""
    action_screen_mapping = {
        "Navigate to Recipe Details": screens['recipe_details'],
        "Navigate to Categories": screens['categories'],
        "Navigate to Favorites": screens['favorites'],
        "Navigate to Shopping List": screens['shopping_list'],
        "Navigate to Search": screens['search'],
        "Navigate to Profile": screens['profile'],
    }
    for action_name, target_screen in action_screen_mapping.items():
        if action_name in actions:
            actions[action_name].target_screen = target_screen
            actions[action_name].save()


def create_home_screen_widgets(screen, data_sources, actions):
    """Create widgets for the home screen."""

    # Main Column for the screen content
    main_column = Widget.objects.create(
        screen=screen,
        widget_type="Column",
        order=0,
        widget_id="home_main_column"
    )

    # Welcome Text
    welcome_text = Widget.objects.create(
        screen=screen,
        widget_type="Text",
        parent_widget=main_column,
        order=0,
        widget_id="welcome_text"
    )
    WidgetProperty.objects.create(
        widget=welcome_text, property_name="text", property_type="string", string_value="Welcome to RecipeHub!"
    )
    WidgetProperty.objects.create(
        widget=welcome_text, property_name="fontSize", property_type="integer", integer_value=24
    )
    WidgetProperty.objects.create(
        widget=welcome_text, property_name="fontWeight", property_type="string", string_value="bold"
    )

    # Search Bar (TextField with search icon)
    search_row = Widget.objects.create(
        screen=screen,
        widget_type="Row",
        parent_widget=main_column,
        order=1,
        widget_id="home_search_row"
    )
    search_field = Widget.objects.create(
        screen=screen,
        widget_type="TextField",
        parent_widget=search_row,
        order=0,
        widget_id="home_search_field"
    )
    WidgetProperty.objects.create(
        widget=search_field, property_name="hintText", property_type="string", string_value="Search recipes..."
    )
    WidgetProperty.objects.create(
        widget=search_field, property_name="prefixIcon", property_type="icon", string_value="search"
    )
    search_button = Widget.objects.create(
        screen=screen,
        widget_type="IconButton",
        parent_widget=search_row,
        order=1,
        widget_id="home_search_button"
    )
    WidgetProperty.objects.create(
        widget=search_button, property_name="icon", property_type="icon", string_value="arrow_forward"
    )
    WidgetProperty.objects.create(
        widget=search_button, property_name="onPressed", property_type="action_reference", action_reference=actions["Navigate to Search"]
    )

    # Featured Recipes Section
    featured_title = Widget.objects.create(
        screen=screen,
        widget_type="Text",
        parent_widget=main_column,
        order=2,
        widget_id="featured_recipes_title"
    )
    WidgetProperty.objects.create(
        widget=featured_title, property_name="text", property_type="string", string_value="Featured Recipes"
    )
    WidgetProperty.objects.create(
        widget=featured_title, property_name="fontSize", property_type="integer", integer_value=20
    )
    WidgetProperty.objects.create(
        widget=featured_title, property_name="fontWeight", property_type="string", string_value="medium"
    )

    # Horizontal ListView for Featured Recipes
    featured_recipes_list = Widget.objects.create(
        screen=screen,
        widget_type="ListView",
        parent_widget=main_column,
        order=3,
        widget_id="featured_recipes_list"
    )
    WidgetProperty.objects.create(
        widget=featured_recipes_list, property_name="scrollDirection", property_type="string", string_value="horizontal"
    )
    WidgetProperty.objects.create(
        widget=featured_recipes_list, property_name="height", property_type="integer", integer_value=200
    )
    WidgetProperty.objects.create(
        widget=featured_recipes_list, property_name="dataSource", property_type="data_source_field_reference",
        data_source_field_reference=DataSourceField.objects.get(data_source=data_sources['recipes'], field_name="name")
    )

    # Quick Links/Navigation Buttons (Bottom Navigation Bar)
    bottom_nav = Widget.objects.create(
        screen=screen,
        widget_type="BottomNavigationBar",
        order=4,
        widget_id="main_bottom_nav"
    )
    # Home Button
    home_nav_item = Widget.objects.create(
        screen=screen,
        widget_type="IconButton", # Representing a nav item
        parent_widget=bottom_nav,
        order=0,
        widget_id="nav_home_item"
    )
    WidgetProperty.objects.create(widget=home_nav_item, property_name="icon", property_type="icon", string_value="home")
    WidgetProperty.objects.create(widget=home_nav_item, property_name="label", property_type="string", string_value="Home")
    # Recipes Button
    recipes_nav_item = Widget.objects.create(
        screen=screen,
        widget_type="IconButton",
        parent_widget=bottom_nav,
        order=1,
        widget_id="nav_recipes_item"
    )
    WidgetProperty.objects.create(widget=recipes_nav_item, property_name="icon", property_type="icon", string_value="menu_book")
    WidgetProperty.objects.create(widget=recipes_nav_item, property_name="label", property_type="string", string_value="Recipes")
    WidgetProperty.objects.create(widget=recipes_nav_item, property_name="onTap", property_type="action_reference", action_reference=actions["Navigate to Recipe Details"])
    # Categories Button
    categories_nav_item = Widget.objects.create(
        screen=screen,
        widget_type="IconButton",
        parent_widget=bottom_nav,
        order=2,
        widget_id="nav_categories_item"
    )
    WidgetProperty.objects.create(widget=categories_nav_item, property_name="icon", property_type="icon", string_value="category")
    WidgetProperty.objects.create(widget=categories_nav_item, property_name="label", property_type="string", string_value="Categories")
    WidgetProperty.objects.create(widget=categories_nav_item, property_name="onTap", property_type="action_reference", action_reference=actions["Navigate to Categories"])
    # Favorites Button
    favorites_nav_item = Widget.objects.create(
        screen=screen,
        widget_type="IconButton",
        parent_widget=bottom_nav,
        order=3,
        widget_id="nav_favorites_item"
    )
    WidgetProperty.objects.create(widget=favorites_nav_item, property_name="icon", property_type="icon", string_value="favorite")
    WidgetProperty.objects.create(widget=favorites_nav_item, property_name="label", property_type="string", string_value="Favorites")
    WidgetProperty.objects.create(widget=favorites_nav_item, property_name="onTap", property_type="action_reference", action_reference=actions["Navigate to Favorites"])
    # Shopping List Button
    shopping_nav_item = Widget.objects.create(
        screen=screen,
        widget_type="IconButton",
        parent_widget=bottom_nav,
        order=4,
        widget_id="nav_shopping_item"
    )
    WidgetProperty.objects.create(widget=shopping_nav_item, property_name="icon", property_type="icon", string_value="shopping_cart")
    WidgetProperty.objects.create(widget=shopping_nav_item, property_name="label", property_type="string", string_value="Shopping")
    WidgetProperty.objects.create(widget=shopping_nav_item, property_name="onTap", property_type="action_reference", action_reference=actions["Navigate to Shopping List"])


def create_recipe_list_screen_widgets(screen, data_sources, actions):
    """Create widgets for the Recipe List screen."""

    main_column = Widget.objects.create(
        screen=screen,
        widget_type="Column",
        order=0,
        widget_id="recipe_list_main_column"
    )

    # Search Bar (TextField with search icon)
    search_row = Widget.objects.create(
        screen=screen,
        widget_type="Row",
        parent_widget=main_column,
        order=0,
        widget_id="recipe_list_search_row"
    )
    search_field = Widget.objects.create(
        screen=screen,
        widget_type="TextField",
        parent_widget=search_row,
        order=0,
        widget_id="recipe_list_search_field"
    )
    WidgetProperty.objects.create(
        widget=search_field, property_name="hintText", property_type="string", string_value="Search all recipes..."
    )
    WidgetProperty.objects.create(
        widget=search_field, property_name="prefixIcon", property_type="icon", string_value="search"
    )
    search_button = Widget.objects.create(
        screen=screen,
        widget_type="IconButton",
        parent_widget=search_row,
        order=1,
        widget_id="recipe_list_search_button"
    )
    WidgetProperty.objects.create(
        widget=search_button, property_name="icon", property_type="icon", string_value="arrow_forward"
    )
    WidgetProperty.objects.create(
        widget=search_button, property_name="onPressed", property_type="action_reference", action_reference=actions["Search Recipes"]
    )

    # List of all recipes
    all_recipes_list = Widget.objects.create(
        screen=screen,
        widget_type="ListView",
        parent_widget=main_column,
        order=1,
        widget_id="all_recipes_list"
    )
    WidgetProperty.objects.create(
        widget=all_recipes_list, property_name="dataSource", property_type="data_source_field_reference",
        data_source_field_reference=DataSourceField.objects.get(data_source=data_sources['recipes'], field_name="name")
    )


def create_recipe_details_screen_widgets(screen, data_sources, actions):
    """Create widgets for the Recipe Details screen."""

    # SingleChildScrollView to make the content scrollable
    scroll_view = Widget.objects.create(
        screen=screen,
        widget_type="SingleChildScrollView",
        order=0,
        widget_id="recipe_details_scroll_view"
    )

    # Main Column for recipe details
    main_column = Widget.objects.create(
        screen=screen,
        widget_type="Column",
        parent_widget=scroll_view,
        order=0,
        widget_id="recipe_details_main_column"
    )

    # Recipe Image
    recipe_image = Widget.objects.create(
        screen=screen,
        widget_type="Image",
        parent_widget=main_column,
        order=0,
        widget_id="recipe_image"
    )
    WidgetProperty.objects.create(
        widget=recipe_image, property_name="imageUrl", property_type="data_source_field_reference",
        data_source_field_reference=DataSourceField.objects.get(data_source=data_sources['recipes'], field_name="imageUrl")
    )
    WidgetProperty.objects.create(
        widget=recipe_image, property_name="height", property_type="integer", integer_value=250
    )
    WidgetProperty.objects.create(
        widget=recipe_image, property_name="fit", property_type="string", string_value="cover"
    )

    # Recipe Name
    recipe_name = Widget.objects.create(
        screen=screen,
        widget_type="Text",
        parent_widget=main_column,
        order=1,
        widget_id="recipe_name"
    )
    WidgetProperty.objects.create(
        widget=recipe_name, property_name="text", property_type="data_source_field_reference",
        data_source_field_reference=DataSourceField.objects.get(data_source=data_sources['recipes'], field_name="name")
    )
    WidgetProperty.objects.create(
        widget=recipe_name, property_name="fontSize", property_type="integer", integer_value=28
    )
    WidgetProperty.objects.create(
        widget=recipe_name, property_name="fontWeight", property_type="string", string_value="bold"
    )
    WidgetProperty.objects.create(
        widget=recipe_name, property_name="padding", property_type="integer", integer_value=16
    )

    # Action Buttons Row (Favorite, Share)
    action_buttons_row = Widget.objects.create(
        screen=screen,
        widget_type="Row",
        parent_widget=main_column,
        order=2,
        widget_id="recipe_action_buttons"
    )
    favorite_button = Widget.objects.create(
        screen=screen,
        widget_type="IconButton",
        parent_widget=action_buttons_row,
        order=0,
        widget_id="favorite_button"
    )
    WidgetProperty.objects.create(
        widget=favorite_button, property_name="icon", property_type="icon", string_value="favorite_border"
    )
    WidgetProperty.objects.create(
        widget=favorite_button, property_name="onPressed", property_type="action_reference", action_reference=actions["Add to Favorites"]
    )
    share_button = Widget.objects.create(
        screen=screen,
        widget_type="IconButton",
        parent_widget=action_buttons_row,
        order=1,
        widget_id="share_button"
    )
    WidgetProperty.objects.create(
        widget=share_button, property_name="icon", property_type="icon", string_value="share"
    )
    WidgetProperty.objects.create(
        widget=share_button, property_name="onPressed", property_type="action_reference", action_reference=actions["Share Recipe"]
    )

    # Ingredients Section
    ingredients_title = Widget.objects.create(
        screen=screen,
        widget_type="Text",
        parent_widget=main_column,
        order=3,
        widget_id="ingredients_title"
    )
    WidgetProperty.objects.create(
        widget=ingredients_title, property_name="text", property_type="string", string_value="Ingredients"
    )
    WidgetProperty.objects.create(
        widget=ingredients_title, property_name="fontSize", property_type="integer", integer_value=20
    )
    WidgetProperty.objects.create(
        widget=ingredients_title, property_name="fontWeight", property_type="string", string_value="medium"
    )
    WidgetProperty.objects.create(
        widget=ingredients_title, property_name="padding", property_type="integer", integer_value=16
    )

    ingredients_list = Widget.objects.create(
        screen=screen,
        widget_type="ListView",
        parent_widget=main_column,
        order=4,
        widget_id="ingredients_list"
    )
    WidgetProperty.objects.create(
        widget=ingredients_list, property_name="dataSource", property_type="data_source_field_reference",
        data_source_field_reference=DataSourceField.objects.get(data_source=data_sources['recipes'], field_name="ingredients")
    )
    WidgetProperty.objects.create(
        widget=ingredients_list, property_name="shrinkWrap", property_type="boolean", boolean_value=True
    )
    WidgetProperty.objects.create(
        widget=ingredients_list, property_name="physics", property_type="string", string_value="NeverScrollableScrollPhysics"
    )

    # Instructions Section
    instructions_title = Widget.objects.create(
        screen=screen,
        widget_type="Text",
        parent_widget=main_column,
        order=5,
        widget_id="instructions_title"
    )
    WidgetProperty.objects.create(
        widget=instructions_title, property_name="text", property_type="string", string_value="Instructions"
    )
    WidgetProperty.objects.create(
        widget=instructions_title, property_name="fontSize", property_type="integer", integer_value=20
    )
    WidgetProperty.objects.create(
        widget=instructions_title, property_name="fontWeight", property_type="string", string_value="medium"
    )
    WidgetProperty.objects.create(
        widget=instructions_title, property_name="padding", property_type="integer", integer_value=16
    )

    instructions_list = Widget.objects.create(
        screen=screen,
        widget_type="ListView",
        parent_widget=main_column,
        order=6,
        widget_id="instructions_list"
    )
    WidgetProperty.objects.create(
        widget=instructions_list, property_name="dataSource", property_type="data_source_field_reference",
        data_source_field_reference=DataSourceField.objects.get(data_source=data_sources['recipes'], field_name="instructions")
    )
    WidgetProperty.objects.create(
        widget=instructions_list, property_name="shrinkWrap", property_type="boolean", boolean_value=True
    )
    WidgetProperty.objects.create(
        widget=instructions_list, property_name="physics", property_type="string", string_value="NeverScrollableScrollPhysics"
    )


def create_categories_screen_widgets(screen, data_sources, actions):
    """Create widgets for the Categories screen."""

    # GridView for categories
    categories_grid = Widget.objects.create(
        screen=screen,
        widget_type="GridView",
        order=0,
        widget_id="categories_grid"
    )
    WidgetProperty.objects.create(
        widget=categories_grid, property_name="crossAxisCount", property_type="integer", integer_value=2
    )
    WidgetProperty.objects.create(
        widget=categories_grid, property_name="childAspectRatio", property_type="decimal", decimal_value=1.2
    )
    WidgetProperty.objects.create(
        widget=categories_grid, property_name="dataSource", property_type="data_source_field_reference",
        data_source_field_reference=DataSourceField.objects.get(data_source=data_sources['categories'], field_name="name")
    )


def create_favorites_screen_widgets(screen, data_sources, actions):
    """Create widgets for the Favorites screen."""

    # ListView for favorite recipes
    favorites_list = Widget.objects.create(
        screen=screen,
        widget_type="ListView",
        order=0,
        widget_id="favorites_list"
    )
    WidgetProperty.objects.create(
        widget=favorites_list, property_name="dataSource", property_type="data_source_field_reference",
        data_source_field_reference=DataSourceField.objects.get(data_source=data_sources['favorites'], field_name="name")
    )


def create_shopping_list_screen_widgets(screen, data_sources, actions):
    """Create widgets for the Shopping List screen."""

    main_column = Widget.objects.create(
        screen=screen,
        widget_type="Column",
        order=0,
        widget_id="shopping_list_main_column"
    )

    # Generate Shopping List Button
    generate_button = Widget.objects.create(
        screen=screen,
        widget_type="ElevatedButton",
        parent_widget=main_column,
        order=0,
        widget_id="generate_shopping_list_button"
    )
    WidgetProperty.objects.create(
        widget=generate_button, property_name="text", property_type="string", string_value="Generate Shopping List"
    )
    WidgetProperty.objects.create(
        widget=generate_button, property_name="onPressed", property_type="action_reference", action_reference=actions["Generate Shopping List"]
    )

    # ListView for shopping list items
    shopping_items_list = Widget.objects.create(
        screen=screen,
        widget_type="ListView",
        parent_widget=main_column,
        order=1,
        widget_id="shopping_items_list"
    )
    WidgetProperty.objects.create(
        widget=shopping_items_list, property_name="dataSource", property_type="data_source_field_reference",
        data_source_field_reference=DataSourceField.objects.get(data_source=data_sources['shopping_list'], field_name="item")
    )


def create_search_screen_widgets(screen, data_sources, actions):
    """Create widgets for the Search screen."""

    main_column = Widget.objects.create(
        screen=screen,
        widget_type="Column",
        order=0,
        widget_id="search_main_column"
    )

    # Search Input Field
    search_input = Widget.objects.create(
        screen=screen,
        widget_type="TextField",
        parent_widget=main_column,
        order=0,
        widget_id="search_input_field"
    )
    WidgetProperty.objects.create(
        widget=search_input, property_name="hintText", property_type="string", string_value="Type to search recipes..."
    )
    WidgetProperty.objects.create(
        widget=search_input, property_name="prefixIcon", property_type="icon", string_value="search"
    )

    # Search Results List
    search_results_list = Widget.objects.create(
        screen=screen,
        widget_type="ListView",
        parent_widget=main_column,
        order=1,
        widget_id="search_results_list"
    )
    WidgetProperty.objects.create(
        widget=search_results_list, property_name="dataSource", property_type="data_source_field_reference",
        data_source_field_reference=DataSourceField.objects.get(data_source=data_sources['recipes'], field_name="name")
    )


def create_profile_screen_widgets(screen, data_sources, actions):
    """Create widgets for the Profile screen."""

    main_column = Widget.objects.create(
        screen=screen,
        widget_type="Column",
        order=0,
        widget_id="profile_main_column"
    )

    # Profile Picture
    profile_image = Widget.objects.create(
        screen=screen,
        widget_type="Image",
        parent_widget=main_column,
        order=0,
        widget_id="profile_picture"
    )
    WidgetProperty.objects.create(
        widget=profile_image, property_name="imageUrl", property_type="url", string_value="https://picsum.photos/200/200?random=profile"
    )
    WidgetProperty.objects.create(
        widget=profile_image, property_name="width", property_type="integer", integer_value=100
    )
    WidgetProperty.objects.create(
        widget=profile_image, property_name="height", property_type="integer", integer_value=100
    )
    WidgetProperty.objects.create(
        widget=profile_image, property_name="borderRadius", property_type="integer", integer_value=50 # Circular
    )

    # User Name
    user_name = Widget.objects.create(
        screen=screen,
        widget_type="Text",
        parent_widget=main_column,
        order=1,
        widget_id="user_name"
    )
    WidgetProperty.objects.create(
        widget=user_name, property_name="text", property_type="string", string_value="John Doe"
    )
    WidgetProperty.objects.create(
        widget=user_name, property_name="fontSize", property_type="integer", integer_value=24
    )
    WidgetProperty.objects.create(
        widget=user_name, property_name="fontWeight", property_type="string", string_value="bold"
    )

    # User Email
    user_email = Widget.objects.create(
        screen=screen,
        widget_type="Text",
        parent_widget=main_column,
        order=2,
        widget_id="user_email"
    )
    WidgetProperty.objects.create(
        widget=user_email, property_name="text", property_type="string", string_value="john.doe@example.com"
    )
    WidgetProperty.objects.create(
        widget=user_email, property_name="fontSize", property_type="integer", integer_value=16
    )
    WidgetProperty.objects.create(
        widget=user_email, property_name="color", property_type="color", color_value="#757575"
    )

    # Favorites Button
    favorites_button = Widget.objects.create(
        screen=screen,
        widget_type="ElevatedButton",
        parent_widget=main_column,
        order=3,
        widget_id="profile_favorites_button"
    )
    WidgetProperty.objects.create(
        widget=favorites_button, property_name="text", property_type="string", string_value="View Favorites"
    )
    WidgetProperty.objects.create(
        widget=favorites_button, property_name="onPressed", property_type="action_reference", action_reference=actions["Navigate to Favorites"]
    )

    # Shopping List Button
    shopping_list_button = Widget.objects.create(
        screen=screen,
        widget_type="ElevatedButton",
        parent_widget=main_column,
        order=4,
        widget_id="profile_shopping_list_button"
    )
    WidgetProperty.objects.create(
        widget=shopping_list_button, property_name="text", property_type="string", string_value="View Shopping List"
    )
    WidgetProperty.objects.create(
        widget=shopping_list_button, property_name="onPressed", property_type="action_reference", action_reference=actions["Navigate to Shopping List"]
    )
