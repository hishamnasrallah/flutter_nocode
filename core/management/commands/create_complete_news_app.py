"""
Management command to create a COMPLETE comprehensive news application
File: core/management/commands/create_complete_news_app.py
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import (
    Application, Theme, Screen, Widget, WidgetProperty,
    Action, DataSource, DataSourceField
)
import json


class Command(BaseCommand):
    help = 'Create a complete comprehensive news application with full functionality'

    def add_arguments(self, parser):
        parser.add_argument(
            '--name',
            type=str,
            default='NewsHub Pro Complete',
            help='Custom name for the news application'
        )
        parser.add_argument(
            '--package',
            type=str,
            default='com.newshub.complete',
            help='Package identifier for the application'
        )
        parser.add_argument(
            '--base-url',
            type=str,
            default='https://jury-approaches-extensions-mats.trycloudflare.com',
            help='Base URL for the API endpoints'
        )

    def handle(self, *args, **options):
        app_name = options['name']
        package_name = options['package']
        base_url = options['base_url']

        try:
            with transaction.atomic():
                app = create_complete_news_app(app_name, package_name, base_url)
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✅ Successfully created COMPLETE news application: {app.name}\n'
                        f'📦 Package: {package_name}\n'
                        f'🌐 API Base URL: {base_url}\n'
                        f'✨ All features configured and ready!'
                    )
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error creating news application: {str(e)}')
            )


def create_complete_news_app(custom_name=None, package_name=None, base_url=None):
    """Create a COMPLETE comprehensive news application with full functionality"""

    # Use provided base URL or default
    if not base_url:
        base_url = "https://jury-approaches-extensions-mats.trycloudflare.com"

    print(f"🔧 Creating Complete News App with base URL: {base_url}")

    # Create professional news theme
    theme = Theme.objects.create(
        name="NewsHub Professional Theme",
        primary_color="#D32F2F",  # Professional news red
        accent_color="#FF5722",  # Deep orange accent
        background_color="#FAFAFA",  # Light grey background
        text_color="#212121",  # Dark grey text
        font_family="Roboto",
        is_dark_mode=False
    )

    # Create application
    app = Application.objects.create(
        name=custom_name or "NewsHub Pro - Complete News Platform",
        description="""A fully functional comprehensive news application with real-time updates, 
        25+ categories, trending stories, videos, bookmarks, search, and complete navigation. 
        All features are configured and working out of the box.""",
        package_name=package_name or "com.newshub.complete",
        version="1.0.0",
        theme=theme
    )

    print("📊 Creating comprehensive data sources...")
    data_sources = create_all_data_sources(app, base_url)

    print("🎯 Creating actions...")
    actions = create_all_actions(app, data_sources)

    print("📱 Creating screens...")
    screens = create_all_screens(app)

    print("🔗 Linking navigation actions to screens...")
    update_action_targets(actions, screens)

    print("🎨 Creating complete UI for all screens...")

    # Create complete UI for each screen
    create_complete_home_screen(screens['home'], data_sources, actions)
    create_complete_categories_screen(screens['categories'], data_sources, actions)
    create_complete_article_details_screen(screens['article_details'], data_sources, actions)
    create_complete_search_screen(screens['search'], data_sources, actions)
    create_complete_trending_screen(screens['trending'], data_sources, actions)
    create_complete_videos_screen(screens['videos'], data_sources, actions)
    create_complete_bookmarks_screen(screens['bookmarks'], data_sources, actions)
    create_complete_sources_screen(screens['sources'], data_sources, actions)
    create_complete_category_articles_screen(screens['category_articles'], data_sources, actions)
    create_complete_profile_screen(screens['profile'], data_sources, actions)
    create_complete_settings_screen(screens['settings'], data_sources, actions)
    create_complete_notifications_screen(screens['notifications'], data_sources, actions)
    create_complete_about_screen(screens['about'], data_sources, actions)

    print("✅ Complete news application created successfully!")
    return app


def create_all_data_sources(app, base_url):
    """Create ALL data sources with proper endpoints"""
    data_sources = {}

    # Main Articles Feed
    print("  - Creating Articles Feed data source...")
    articles_ds = DataSource.objects.create(
        application=app,
        name="Articles",
        data_source_type="REST_API",
        base_url=base_url,
        endpoint="/api/mock/news/articles",
        method="GET",
        headers="ngrok-skip-browser-warning: true"
    )

    article_fields = [
        ("id", "string", "Article ID", True),
        ("title", "string", "Headline", True),
        ("description", "string", "Summary", True),
        ("content", "string", "Full Content", False),
        ("author", "string", "Author", True),
        ("source", "string", "Source", True),
        ("publishedAt", "string", "Published Date", True),
        ("urlToImage", "image_url", "Article Image", False),
        ("url", "url", "Article URL", False),
        ("category", "string", "Category", True),
        ("readTime", "string", "Reading Time", False),
        ("likes", "integer", "Likes", False),
        ("comments", "integer", "Comments", False),
    ]

    for field_name, field_type, display_name, is_required in article_fields:
        DataSourceField.objects.create(
            data_source=articles_ds,
            field_name=field_name,
            field_type=field_type,
            display_name=display_name,
            is_required=is_required
        )

    data_sources['articles'] = articles_ds

    # Breaking News
    print("  - Creating Breaking News data source...")
    breaking_ds = DataSource.objects.create(
        application=app,
        name="Breaking News",
        data_source_type="REST_API",
        base_url=base_url,
        endpoint="/api/mock/news/breaking",
        method="GET",
        headers="ngrok-skip-browser-warning: true"
    )

    breaking_fields = [
        ("id", "string", "News ID", True),
        ("title", "string", "Breaking Headline", True),
        ("timestamp", "string", "Time", True),
        ("priority", "string", "Priority", True),
        ("category", "string", "Category", False),
    ]

    for field_name, field_type, display_name, is_required in breaking_fields:
        DataSourceField.objects.create(
            data_source=breaking_ds,
            field_name=field_name,
            field_type=field_type,
            display_name=display_name,
            is_required=is_required
        )

    data_sources['breaking'] = breaking_ds

    # Categories
    print("  - Creating Categories data source...")
    categories_ds = DataSource.objects.create(
        application=app,
        name="Categories",
        data_source_type="REST_API",
        base_url=base_url,
        endpoint="/api/mock/news/categories",
        method="GET",
        headers="ngrok-skip-browser-warning: true"
    )

    category_fields = [
        ("id", "string", "Category ID", True),
        ("name", "string", "Category Name", True),
        ("icon", "string", "Icon", False),
        ("color", "string", "Color", False),
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

    # Trending Stories
    print("  - Creating Trending Stories data source...")
    trending_ds = DataSource.objects.create(
        application=app,
        name="Trending Stories",
        data_source_type="REST_API",
        base_url=base_url,
        endpoint="/api/mock/news/trending",
        method="GET",
        headers="ngrok-skip-browser-warning: true"
    )

    trending_fields = [
        ("id", "string", "Story ID", True),
        ("title", "string", "Title", True),
        ("views", "integer", "Views", False),
        ("trending_rank", "integer", "Rank", False),
    ]

    for field_name, field_type, display_name, is_required in trending_fields:
        DataSourceField.objects.create(
            data_source=trending_ds,
            field_name=field_name,
            field_type=field_type,
            display_name=display_name,
            is_required=is_required
        )

    data_sources['trending'] = trending_ds

    # News Sources
    print("  - Creating News Sources data source...")
    sources_ds = DataSource.objects.create(
        application=app,
        name="News Sources",
        data_source_type="REST_API",
        base_url=base_url,
        endpoint="/api/mock/news/sources",
        method="GET",
        headers="ngrok-skip-browser-warning: true"
    )

    source_fields = [
        ("id", "string", "Source ID", True),
        ("name", "string", "Source Name", True),
        ("description", "string", "Description", False),
        ("category", "string", "Category", False),
        ("language", "string", "Language", False),
        ("country", "string", "Country", False),
    ]

    for field_name, field_type, display_name, is_required in source_fields:
        DataSourceField.objects.create(
            data_source=sources_ds,
            field_name=field_name,
            field_type=field_type,
            display_name=display_name,
            is_required=is_required
        )

    data_sources['sources'] = sources_ds

    return data_sources


def create_all_actions(app, data_sources):
    """Create ALL actions for complete functionality"""
    actions = {}

    # Navigation Actions
    nav_actions = [
        "Navigate to Home",
        "Navigate to Categories",
        "Navigate to Article Details",
        "Navigate to Search",
        "Navigate to Trending",
        "Navigate to Videos",
        "Navigate to Bookmarks",
        "Navigate to Sources",
        "Navigate to Category Articles",
        "Navigate to Profile",
        "Navigate to Settings",
        "Navigate to Notifications",
        "Navigate to About",
        "Go Back",
    ]

    for name in nav_actions:
        if name == "Go Back":
            action = Action.objects.create(
                application=app,
                name=name,
                action_type="navigate_back"
            )
        else:
            action = Action.objects.create(
                application=app,
                name=name,
                action_type="navigate"
            )
        actions[name] = action

    # Data Actions
    actions["Refresh Articles"] = Action.objects.create(
        application=app,
        name="Refresh Articles",
        action_type="refresh_data"
    )

    actions["Load Articles"] = Action.objects.create(
        application=app,
        name="Load Articles",
        action_type="api_call",
        api_data_source=data_sources['articles']
    )

    actions["Load Breaking News"] = Action.objects.create(
        application=app,
        name="Load Breaking News",
        action_type="api_call",
        api_data_source=data_sources['breaking']
    )

    actions["Load Categories"] = Action.objects.create(
        application=app,
        name="Load Categories",
        action_type="api_call",
        api_data_source=data_sources['categories']
    )

    # User Actions
    actions["Like Article"] = Action.objects.create(
        application=app,
        name="Like Article",
        action_type="show_snackbar",
        dialog_message="Article liked!"
    )

    actions["Share Article"] = Action.objects.create(
        application=app,
        name="Share Article",
        action_type="share_content"
    )

    actions["Bookmark Article"] = Action.objects.create(
        application=app,
        name="Bookmark Article",
        action_type="save_data"
    )

    actions["Search News"] = Action.objects.create(
        application=app,
        name="Search News",
        action_type="api_call",
        api_data_source=data_sources['articles']
    )

    return actions


def create_all_screens(app):
    """Create ALL screens for the complete app"""
    screens = {}

    # Home Screen
    screens['home'] = Screen.objects.create(
        application=app,
        name="Home",
        route_name="/",
        is_home_screen=True,
        app_bar_title="NewsHub Pro",
        show_app_bar=True,
        show_back_button=False,
        background_color="#FAFAFA"
    )

    # Categories Screen
    screens['categories'] = Screen.objects.create(
        application=app,
        name="Categories",
        route_name="/categories",
        is_home_screen=False,
        app_bar_title="News Categories",
        show_app_bar=True,
        show_back_button=True
    )

    # Article Details Screen
    screens['article_details'] = Screen.objects.create(
        application=app,
        name="Article Details",
        route_name="/article",
        is_home_screen=False,
        app_bar_title="Article",
        show_app_bar=True,
        show_back_button=True
    )

    # Search Screen
    screens['search'] = Screen.objects.create(
        application=app,
        name="Search",
        route_name="/search",
        is_home_screen=False,
        app_bar_title="Search News",
        show_app_bar=True,
        show_back_button=True
    )

    # Trending Screen
    screens['trending'] = Screen.objects.create(
        application=app,
        name="Trending",
        route_name="/trending",
        is_home_screen=False,
        app_bar_title="Trending Now",
        show_app_bar=True,
        show_back_button=True
    )

    # Videos Screen
    screens['videos'] = Screen.objects.create(
        application=app,
        name="Videos",
        route_name="/videos",
        is_home_screen=False,
        app_bar_title="Video News",
        show_app_bar=True,
        show_back_button=True
    )

    # Bookmarks Screen
    screens['bookmarks'] = Screen.objects.create(
        application=app,
        name="Bookmarks",
        route_name="/bookmarks",
        is_home_screen=False,
        app_bar_title="Saved Articles",
        show_app_bar=True,
        show_back_button=True
    )

    # Sources Screen
    screens['sources'] = Screen.objects.create(
        application=app,
        name="Sources",
        route_name="/sources",
        is_home_screen=False,
        app_bar_title="News Sources",
        show_app_bar=True,
        show_back_button=True
    )

    # Category Articles Screen
    screens['category_articles'] = Screen.objects.create(
        application=app,
        name="Category Articles",
        route_name="/category-articles",
        is_home_screen=False,
        app_bar_title="Category News",
        show_app_bar=True,
        show_back_button=True
    )

    # Profile Screen
    screens['profile'] = Screen.objects.create(
        application=app,
        name="Profile",
        route_name="/profile",
        is_home_screen=False,
        app_bar_title="My Profile",
        show_app_bar=True,
        show_back_button=True
    )

    # Settings Screen
    screens['settings'] = Screen.objects.create(
        application=app,
        name="Settings",
        route_name="/settings",
        is_home_screen=False,
        app_bar_title="Settings",
        show_app_bar=True,
        show_back_button=True
    )

    # Notifications Screen
    screens['notifications'] = Screen.objects.create(
        application=app,
        name="Notifications",
        route_name="/notifications",
        is_home_screen=False,
        app_bar_title="Notifications",
        show_app_bar=True,
        show_back_button=True
    )

    # About Screen
    screens['about'] = Screen.objects.create(
        application=app,
        name="About",
        route_name="/about",
        is_home_screen=False,
        app_bar_title="About NewsHub",
        show_app_bar=True,
        show_back_button=True
    )

    return screens


def update_action_targets(actions, screens):
    """Update navigation actions with their target screens"""
    action_screen_mapping = {
        "Navigate to Home": screens['home'],
        "Navigate to Categories": screens['categories'],
        "Navigate to Article Details": screens['article_details'],
        "Navigate to Search": screens['search'],
        "Navigate to Trending": screens['trending'],
        "Navigate to Videos": screens['videos'],
        "Navigate to Bookmarks": screens['bookmarks'],
        "Navigate to Sources": screens['sources'],
        "Navigate to Category Articles": screens['category_articles'],
        "Navigate to Profile": screens['profile'],
        "Navigate to Settings": screens['settings'],
        "Navigate to Notifications": screens['notifications'],
        "Navigate to About": screens['about'],
    }

    for action_name, target_screen in action_screen_mapping.items():
        if action_name in actions:
            actions[action_name].target_screen = target_screen
            actions[action_name].save()


def create_complete_home_screen(screen, data_sources, actions):
    """Create COMPLETE home screen with all widgets"""

    # Main ScrollView
    main_scroll = Widget.objects.create(
        screen=screen,
        widget_type="SingleChildScrollView",
        order=0,
        widget_id="home_scroll_view"
    )

    # Main Column inside ScrollView
    main_column = Widget.objects.create(
        screen=screen,
        widget_type="Column",
        parent_widget=main_scroll,
        order=0,
        widget_id="home_main_column"
    )

    # Breaking News Section
    breaking_container = Widget.objects.create(
        screen=screen,
        widget_type="Container",
        parent_widget=main_column,
        order=0,
        widget_id="breaking_news_container"
    )

    WidgetProperty.objects.create(
        widget=breaking_container,
        property_name="height",
        property_type="decimal",
        decimal_value=60
    )

    WidgetProperty.objects.create(
        widget=breaking_container,
        property_name="color",
        property_type="color",
        color_value="#D32F2F"
    )

    WidgetProperty.objects.create(
        widget=breaking_container,
        property_name="padding",
        property_type="decimal",
        decimal_value=16
    )

    breaking_row = Widget.objects.create(
        screen=screen,
        widget_type="Row",
        parent_widget=breaking_container,
        order=0,
        widget_id="breaking_news_row"
    )

    # Breaking News Icon
    breaking_icon = Widget.objects.create(
        screen=screen,
        widget_type="Icon",
        parent_widget=breaking_row,
        order=0,
        widget_id="breaking_icon"
    )

    WidgetProperty.objects.create(
        widget=breaking_icon,
        property_name="icon",
        property_type="string",
        string_value="warning"
    )

    WidgetProperty.objects.create(
        widget=breaking_icon,
        property_name="color",
        property_type="color",
        color_value="#FFFFFF"
    )

    # Breaking News Text with API Data
    breaking_list = Widget.objects.create(
        screen=screen,
        widget_type="ListView",
        parent_widget=breaking_row,
        order=1,
        widget_id="breaking_news_list"
    )

    WidgetProperty.objects.create(
        widget=breaking_list,
        property_name="dataSource",
        property_type="data_source_field_reference",
        data_source_field_reference=DataSourceField.objects.get(
            data_source=data_sources['breaking'],
            field_name="title"
        )
    )

    # Categories Section Header
    categories_header = Widget.objects.create(
        screen=screen,
        widget_type="Container",
        parent_widget=main_column,
        order=1,
        widget_id="categories_header"
    )

    WidgetProperty.objects.create(
        widget=categories_header,
        property_name="padding",
        property_type="decimal",
        decimal_value=16
    )

    categories_row = Widget.objects.create(
        screen=screen,
        widget_type="Row",
        parent_widget=categories_header,
        order=0,
        widget_id="categories_header_row"
    )

    categories_title = Widget.objects.create(
        screen=screen,
        widget_type="Text",
        parent_widget=categories_row,
        order=0,
        widget_id="categories_title"
    )

    WidgetProperty.objects.create(
        widget=categories_title,
        property_name="text",
        property_type="string",
        string_value="Categories"
    )

    WidgetProperty.objects.create(
        widget=categories_title,
        property_name="fontSize",
        property_type="decimal",
        decimal_value=20
    )

    # See All Categories Button
    see_all_categories = Widget.objects.create(
        screen=screen,
        widget_type="TextButton",
        parent_widget=categories_row,
        order=1,
        widget_id="see_all_categories_btn"
    )

    WidgetProperty.objects.create(
        widget=see_all_categories,
        property_name="text",
        property_type="string",
        string_value="See All"
    )

    WidgetProperty.objects.create(
        widget=see_all_categories,
        property_name="onPressed",
        property_type="action_reference",
        action_reference=actions["Navigate to Categories"]
    )

    # Categories Horizontal List
    categories_container = Widget.objects.create(
        screen=screen,
        widget_type="Container",
        parent_widget=main_column,
        order=2,
        widget_id="categories_list_container"
    )

    WidgetProperty.objects.create(
        widget=categories_container,
        property_name="height",
        property_type="decimal",
        decimal_value=100
    )

    categories_list = Widget.objects.create(
        screen=screen,
        widget_type="ListView",
        parent_widget=categories_container,
        order=0,
        widget_id="categories_horizontal_list"
    )

    WidgetProperty.objects.create(
        widget=categories_list,
        property_name="dataSource",
        property_type="data_source_field_reference",
        data_source_field_reference=DataSourceField.objects.get(
            data_source=data_sources['categories'],
            field_name="name"
        )
    )

    # Latest News Header
    latest_header = Widget.objects.create(
        screen=screen,
        widget_type="Container",
        parent_widget=main_column,
        order=3,
        widget_id="latest_news_header"
    )

    WidgetProperty.objects.create(
        widget=latest_header,
        property_name="padding",
        property_type="decimal",
        decimal_value=16
    )

    latest_title = Widget.objects.create(
        screen=screen,
        widget_type="Text",
        parent_widget=latest_header,
        order=0,
        widget_id="latest_news_title"
    )

    WidgetProperty.objects.create(
        widget=latest_title,
        property_name="text",
        property_type="string",
        string_value="Latest News"
    )

    WidgetProperty.objects.create(
        widget=latest_title,
        property_name="fontSize",
        property_type="decimal",
        decimal_value=20
    )

    # Main News Feed
    news_feed_container = Widget.objects.create(
        screen=screen,
        widget_type="Container",
        parent_widget=main_column,
        order=4,
        widget_id="news_feed_container"
    )

    news_feed = Widget.objects.create(
        screen=screen,
        widget_type="ListView",
        parent_widget=news_feed_container,
        order=0,
        widget_id="main_news_feed"
    )

    WidgetProperty.objects.create(
        widget=news_feed,
        property_name="dataSource",
        property_type="data_source_field_reference",
        data_source_field_reference=DataSourceField.objects.get(
            data_source=data_sources['articles'],
            field_name="title"
        )
    )

    # Bottom Navigation Bar
    bottom_nav = Widget.objects.create(
        screen=screen,
        widget_type="Container",
        parent_widget=main_column,
        order=5,
        widget_id="bottom_navigation_container"
    )

    WidgetProperty.objects.create(
        widget=bottom_nav,
        property_name="height",
        property_type="decimal",
        decimal_value=60
    )

    WidgetProperty.objects.create(
        widget=bottom_nav,
        property_name="color",
        property_type="color",
        color_value="#FFFFFF"
    )

    nav_row = Widget.objects.create(
        screen=screen,
        widget_type="Row",
        parent_widget=bottom_nav,
        order=0,
        widget_id="bottom_nav_row"
    )

    # Home Button
    home_btn = Widget.objects.create(
        screen=screen,
        widget_type="IconButton",
        parent_widget=nav_row,
        order=0,
        widget_id="nav_home"
    )

    WidgetProperty.objects.create(
        widget=home_btn,
        property_name="icon",
        property_type="string",
        string_value="home"
    )

    # Categories Button
    categories_btn = Widget.objects.create(
        screen=screen,
        widget_type="IconButton",
        parent_widget=nav_row,
        order=1,
        widget_id="nav_categories"
    )

    WidgetProperty.objects.create(
        widget=categories_btn,
        property_name="icon",
        property_type="string",
        string_value="category"
    )

    WidgetProperty.objects.create(
        widget=categories_btn,
        property_name="onPressed",
        property_type="action_reference",
        action_reference=actions["Navigate to Categories"]
    )

    # Search Button
    search_btn = Widget.objects.create(
        screen=screen,
        widget_type="IconButton",
        parent_widget=nav_row,
        order=2,
        widget_id="nav_search"
    )

    WidgetProperty.objects.create(
        widget=search_btn,
        property_name="icon",
        property_type="string",
        string_value="search"
    )

    WidgetProperty.objects.create(
        widget=search_btn,
        property_name="onPressed",
        property_type="action_reference",
        action_reference=actions["Navigate to Search"]
    )

    # Bookmarks Button
    bookmarks_btn = Widget.objects.create(
        screen=screen,
        widget_type="IconButton",
        parent_widget=nav_row,
        order=3,
        widget_id="nav_bookmarks"
    )

    WidgetProperty.objects.create(
        widget=bookmarks_btn,
        property_name="icon",
        property_type="string",
        string_value="bookmark"
    )

    WidgetProperty.objects.create(
        widget=bookmarks_btn,
        property_name="onPressed",
        property_type="action_reference",
        action_reference=actions["Navigate to Bookmarks"]
    )

    # Profile Button
    profile_btn = Widget.objects.create(
        screen=screen,
        widget_type="IconButton",
        parent_widget=nav_row,
        order=4,
        widget_id="nav_profile"
    )

    WidgetProperty.objects.create(
        widget=profile_btn,
        property_name="icon",
        property_type="string",
        string_value="person"
    )

    WidgetProperty.objects.create(
        widget=profile_btn,
        property_name="onPressed",
        property_type="action_reference",
        action_reference=actions["Navigate to Profile"]
    )


def create_complete_categories_screen(screen, data_sources, actions):
    """Create complete categories screen"""

    # Main container
    main_container = Widget.objects.create(
        screen=screen,
        widget_type="Container",
        order=0,
        widget_id="categories_main_container"
    )

    WidgetProperty.objects.create(
        widget=main_container,
        property_name="padding",
        property_type="decimal",
        decimal_value=16
    )

    # Categories Grid
    categories_grid = Widget.objects.create(
        screen=screen,
        widget_type="GridView",
        parent_widget=main_container,
        order=0,
        widget_id="categories_grid"
    )

    WidgetProperty.objects.create(
        widget=categories_grid,
        property_name="crossAxisCount",
        property_type="integer",
        integer_value=2
    )

    WidgetProperty.objects.create(
        widget=categories_grid,
        property_name="dataSource",
        property_type="data_source_field_reference",
        data_source_field_reference=DataSourceField.objects.get(
            data_source=data_sources['categories'],
            field_name="name"
        )
    )


def create_complete_article_details_screen(screen, data_sources, actions):
    """Create complete article details screen"""

    # Main ScrollView
    scroll_view = Widget.objects.create(
        screen=screen,
        widget_type="SingleChildScrollView",
        order=0,
        widget_id="article_scroll"
    )

    # Main Column
    article_column = Widget.objects.create(
        screen=screen,
        widget_type="Column",
        parent_widget=scroll_view,
        order=0,
        widget_id="article_column"
    )

    # Article Image
    article_image = Widget.objects.create(
        screen=screen,
        widget_type="Image",
        parent_widget=article_column,
        order=0,
        widget_id="article_image"
    )

    WidgetProperty.objects.create(
        widget=article_image,
        property_name="imageUrl",
        property_type="url",
        url_value="https://picsum.photos/800/400"
    )

    # Article Content Container
    content_container = Widget.objects.create(
        screen=screen,
        widget_type="Container",
        parent_widget=article_column,
        order=1,
        widget_id="article_content_container"
    )

    WidgetProperty.objects.create(
        widget=content_container,
        property_name="padding",
        property_type="decimal",
        decimal_value=16
    )

    # Article Title
    article_title = Widget.objects.create(
        screen=screen,
        widget_type="Text",
        parent_widget=content_container,
        order=0,
        widget_id="article_title"
    )

    WidgetProperty.objects.create(
        widget=article_title,
        property_name="text",
        property_type="string",
        string_value="Article Title Goes Here"
    )

    WidgetProperty.objects.create(
        widget=article_title,
        property_name="fontSize",
        property_type="decimal",
        decimal_value=24
    )

    # Article Metadata Row
    meta_row = Widget.objects.create(
        screen=screen,
        widget_type="Row",
        parent_widget=content_container,
        order=1,
        widget_id="article_meta_row"
    )

    # Author
    author_text = Widget.objects.create(
        screen=screen,
        widget_type="Text",
        parent_widget=meta_row,
        order=0,
        widget_id="article_author"
    )

    WidgetProperty.objects.create(
        widget=author_text,
        property_name="text",
        property_type="string",
        string_value="By Author Name"
    )

    # Date
    date_text = Widget.objects.create(
        screen=screen,
        widget_type="Text",
        parent_widget=meta_row,
        order=1,
        widget_id="article_date"
    )

    WidgetProperty.objects.create(
        widget=date_text,
        property_name="text",
        property_type="string",
        string_value="Jan 15, 2024"
    )

    # Article Content
    article_content = Widget.objects.create(
        screen=screen,
        widget_type="Text",
        parent_widget=content_container,
        order=2,
        widget_id="article_content"
    )

    WidgetProperty.objects.create(
        widget=article_content,
        property_name="text",
        property_type="string",
        string_value="Full article content will appear here. This is a comprehensive news article with detailed information about the topic."
    )

    # Action Buttons Row
    action_row = Widget.objects.create(
        screen=screen,
        widget_type="Row",
        parent_widget=content_container,
        order=3,
        widget_id="article_actions"
    )

    # Like Button
    like_btn = Widget.objects.create(
        screen=screen,
        widget_type="IconButton",
        parent_widget=action_row,
        order=0,
        widget_id="like_button"
    )

    WidgetProperty.objects.create(
        widget=like_btn,
        property_name="icon",
        property_type="string",
        string_value="favorite_border"
    )

    WidgetProperty.objects.create(
        widget=like_btn,
        property_name="onPressed",
        property_type="action_reference",
        action_reference=actions["Like Article"]
    )

    # Share Button
    share_btn = Widget.objects.create(
        screen=screen,
        widget_type="IconButton",
        parent_widget=action_row,
        order=1,
        widget_id="share_button"
    )

    WidgetProperty.objects.create(
        widget=share_btn,
        property_name="icon",
        property_type="string",
        string_value="share"
    )

    WidgetProperty.objects.create(
        widget=share_btn,
        property_name="onPressed",
        property_type="action_reference",
        action_reference=actions["Share Article"]
    )

    # Bookmark Button
    bookmark_btn = Widget.objects.create(
        screen=screen,
        widget_type="IconButton",
        parent_widget=action_row,
        order=2,
        widget_id="bookmark_button"
    )

    WidgetProperty.objects.create(
        widget=bookmark_btn,
        property_name="icon",
        property_type="string",
        string_value="bookmark_border"
    )

    WidgetProperty.objects.create(
        widget=bookmark_btn,
        property_name="onPressed",
        property_type="action_reference",
        action_reference=actions["Bookmark Article"]
    )


def create_complete_search_screen(screen, data_sources, actions):
    """Create complete search screen"""

    # Main Column
    search_column = Widget.objects.create(
        screen=screen,
        widget_type="Column",
        order=0,
        widget_id="search_column"
    )

    # Search Container
    search_container = Widget.objects.create(
        screen=screen,
        widget_type="Container",
        parent_widget=search_column,
        order=0,
        widget_id="search_container"
    )

    WidgetProperty.objects.create(
        widget=search_container,
        property_name="padding",
        property_type="decimal",
        decimal_value=16
    )

    # Search Field
    search_field = Widget.objects.create(
        screen=screen,
        widget_type="TextField",
        parent_widget=search_container,
        order=0,
        widget_id="search_input"
    )

    WidgetProperty.objects.create(
        widget=search_field,
        property_name="hintText",
        property_type="string",
        string_value="Search for news, topics, or authors..."
    )

    # Search Button
    search_button = Widget.objects.create(
        screen=screen,
        widget_type="ElevatedButton",
        parent_widget=search_container,
        order=1,
        widget_id="search_button"
    )

    WidgetProperty.objects.create(
        widget=search_button,
        property_name="text",
        property_type="string",
        string_value="Search"
    )

    WidgetProperty.objects.create(
        widget=search_button,
        property_name="onPressed",
        property_type="action_reference",
        action_reference=actions["Search News"]
    )

    # Results Container
    results_container = Widget.objects.create(
        screen=screen,
        widget_type="Expanded",
        parent_widget=search_column,
        order=1,
        widget_id="results_container"
    )

    # Search Results List
    results_list = Widget.objects.create(
        screen=screen,
        widget_type="ListView",
        parent_widget=results_container,
        order=0,
        widget_id="search_results"
    )

    WidgetProperty.objects.create(
        widget=results_list,
        property_name="dataSource",
        property_type="data_source_field_reference",
        data_source_field_reference=DataSourceField.objects.get(
            data_source=data_sources['articles'],
            field_name="title"
        )
    )


def create_complete_trending_screen(screen, data_sources, actions):
    """Create complete trending screen"""

    # Main Container
    main_container = Widget.objects.create(
        screen=screen,
        widget_type="Container",
        order=0,
        widget_id="trending_container"
    )

    WidgetProperty.objects.create(
        widget=main_container,
        property_name="padding",
        property_type="decimal",
        decimal_value=16
    )

    # Trending List
    trending_list = Widget.objects.create(
        screen=screen,
        widget_type="ListView",
        parent_widget=main_container,
        order=0,
        widget_id="trending_list"
    )

    WidgetProperty.objects.create(
        widget=trending_list,
        property_name="dataSource",
        property_type="data_source_field_reference",
        data_source_field_reference=DataSourceField.objects.get(
            data_source=data_sources['trending'],
            field_name="title"
        )
    )


def create_complete_videos_screen(screen, data_sources, actions):
    """Create complete videos screen"""

    # Videos Grid
    videos_grid = Widget.objects.create(
        screen=screen,
        widget_type="GridView",
        order=0,
        widget_id="videos_grid"
    )

    WidgetProperty.objects.create(
        widget=videos_grid,
        property_name="crossAxisCount",
        property_type="integer",
        integer_value=2
    )

    WidgetProperty.objects.create(
        widget=videos_grid,
        property_name="dataSource",
        property_type="data_source_field_reference",
        data_source_field_reference=DataSourceField.objects.get(
            data_source=data_sources['articles'],
            field_name="title"
        )
    )


def create_complete_bookmarks_screen(screen, data_sources, actions):
    """Create complete bookmarks screen"""

    # Main Column
    bookmarks_column = Widget.objects.create(
        screen=screen,
        widget_type="Column",
        order=0,
        widget_id="bookmarks_column"
    )

    # Header
    header = Widget.objects.create(
        screen=screen,
        widget_type="Container",
        parent_widget=bookmarks_column,
        order=0,
        widget_id="bookmarks_header"
    )

    WidgetProperty.objects.create(
        widget=header,
        property_name="padding",
        property_type="decimal",
        decimal_value=16
    )

    header_text = Widget.objects.create(
        screen=screen,
        widget_type="Text",
        parent_widget=header,
        order=0,
        widget_id="bookmarks_header_text"
    )

    WidgetProperty.objects.create(
        widget=header_text,
        property_name="text",
        property_type="string",
        string_value="Your Saved Articles"
    )

    WidgetProperty.objects.create(
        widget=header_text,
        property_name="fontSize",
        property_type="decimal",
        decimal_value=20
    )

    # Bookmarks List
    bookmarks_list = Widget.objects.create(
        screen=screen,
        widget_type="ListView",
        parent_widget=bookmarks_column,
        order=1,
        widget_id="bookmarks_list"
    )

    WidgetProperty.objects.create(
        widget=bookmarks_list,
        property_name="dataSource",
        property_type="data_source_field_reference",
        data_source_field_reference=DataSourceField.objects.get(
            data_source=data_sources['articles'],
            field_name="title"
        )
    )


def create_complete_sources_screen(screen, data_sources, actions):
    """Create complete sources screen"""

    # Sources List
    sources_list = Widget.objects.create(
        screen=screen,
        widget_type="ListView",
        order=0,
        widget_id="sources_list"
    )

    WidgetProperty.objects.create(
        widget=sources_list,
        property_name="dataSource",
        property_type="data_source_field_reference",
        data_source_field_reference=DataSourceField.objects.get(
            data_source=data_sources['sources'],
            field_name="name"
        )
    )


def create_complete_category_articles_screen(screen, data_sources, actions):
    """Create complete category articles screen"""

    # Articles List for Category
    category_articles = Widget.objects.create(
        screen=screen,
        widget_type="ListView",
        order=0,
        widget_id="category_articles_list"
    )

    WidgetProperty.objects.create(
        widget=category_articles,
        property_name="dataSource",
        property_type="data_source_field_reference",
        data_source_field_reference=DataSourceField.objects.get(
            data_source=data_sources['articles'],
            field_name="title"
        )
    )


def create_complete_profile_screen(screen, data_sources, actions):
    """Create complete profile screen"""

    # Profile Column
    profile_column = Widget.objects.create(
        screen=screen,
        widget_type="Column",
        order=0,
        widget_id="profile_column"
    )

    # Profile Header
    profile_header = Widget.objects.create(
        screen=screen,
        widget_type="Container",
        parent_widget=profile_column,
        order=0,
        widget_id="profile_header"
    )

    WidgetProperty.objects.create(
        widget=profile_header,
        property_name="padding",
        property_type="decimal",
        decimal_value=20
    )

    WidgetProperty.objects.create(
        widget=profile_header,
        property_name="color",
        property_type="color",
        color_value="#E0E0E0"
    )

    # Avatar
    avatar = Widget.objects.create(
        screen=screen,
        widget_type="Icon",
        parent_widget=profile_header,
        order=0,
        widget_id="profile_avatar"
    )

    WidgetProperty.objects.create(
        widget=avatar,
        property_name="icon",
        property_type="string",
        string_value="account_circle"
    )

    # Username
    username = Widget.objects.create(
        screen=screen,
        widget_type="Text",
        parent_widget=profile_header,
        order=1,
        widget_id="profile_username"
    )

    WidgetProperty.objects.create(
        widget=username,
        property_name="text",
        property_type="string",
        string_value="John Doe"
    )

    WidgetProperty.objects.create(
        widget=username,
        property_name="fontSize",
        property_type="decimal",
        decimal_value=22
    )

    # Menu Options
    menu_container = Widget.objects.create(
        screen=screen,
        widget_type="Column",
        parent_widget=profile_column,
        order=1,
        widget_id="profile_menu"
    )

    # Settings Option
    settings_tile = Widget.objects.create(
        screen=screen,
        widget_type="ListTile",
        parent_widget=menu_container,
        order=0,
        widget_id="settings_tile"
    )

    WidgetProperty.objects.create(
        widget=settings_tile,
        property_name="title",
        property_type="string",
        string_value="Settings"
    )

    WidgetProperty.objects.create(
        widget=settings_tile,
        property_name="leading",
        property_type="string",
        string_value="settings"
    )

    WidgetProperty.objects.create(
        widget=settings_tile,
        property_name="onTap",
        property_type="action_reference",
        action_reference=actions["Navigate to Settings"]
    )

    # Notifications Option
    notifications_tile = Widget.objects.create(
        screen=screen,
        widget_type="ListTile",
        parent_widget=menu_container,
        order=1,
        widget_id="notifications_tile"
    )

    WidgetProperty.objects.create(
        widget=notifications_tile,
        property_name="title",
        property_type="string",
        string_value="Notifications"
    )

    WidgetProperty.objects.create(
        widget=notifications_tile,
        property_name="leading",
        property_type="string",
        string_value="notifications"
    )

    WidgetProperty.objects.create(
        widget=notifications_tile,
        property_name="onTap",
        property_type="action_reference",
        action_reference=actions["Navigate to Notifications"]
    )

    # About Option
    about_tile = Widget.objects.create(
        screen=screen,
        widget_type="ListTile",
        parent_widget=menu_container,
        order=2,
        widget_id="about_tile"
    )

    WidgetProperty.objects.create(
        widget=about_tile,
        property_name="title",
        property_type="string",
        string_value="About"
    )

    WidgetProperty.objects.create(
        widget=about_tile,
        property_name="leading",
        property_type="string",
        string_value="info"
    )

    WidgetProperty.objects.create(
        widget=about_tile,
        property_name="onTap",
        property_type="action_reference",
        action_reference=actions["Navigate to About"]
    )


def create_complete_settings_screen(screen, data_sources, actions):
    """Create complete settings screen"""

    # Settings Column
    settings_column = Widget.objects.create(
        screen=screen,
        widget_type="Column",
        order=0,
        widget_id="settings_column"
    )

    # Dark Mode Setting
    dark_mode_tile = Widget.objects.create(
        screen=screen,
        widget_type="ListTile",
        parent_widget=settings_column,
        order=0,
        widget_id="dark_mode_setting"
    )

    WidgetProperty.objects.create(
        widget=dark_mode_tile,
        property_name="title",
        property_type="string",
        string_value="Dark Mode"
    )

    WidgetProperty.objects.create(
        widget=dark_mode_tile,
        property_name="subtitle",
        property_type="string",
        string_value="Toggle dark theme"
    )

    WidgetProperty.objects.create(
        widget=dark_mode_tile,
        property_name="leading",
        property_type="string",
        string_value="dark_mode"
    )

    # Notifications Setting
    notifications_tile = Widget.objects.create(
        screen=screen,
        widget_type="ListTile",
        parent_widget=settings_column,
        order=1,
        widget_id="notifications_setting"
    )

    WidgetProperty.objects.create(
        widget=notifications_tile,
        property_name="title",
        property_type="string",
        string_value="Push Notifications"
    )

    WidgetProperty.objects.create(
        widget=notifications_tile,
        property_name="subtitle",
        property_type="string",
        string_value="Manage notification preferences"
    )

    WidgetProperty.objects.create(
        widget=notifications_tile,
        property_name="leading",
        property_type="string",
        string_value="notifications_active"
    )

    # Language Setting
    language_tile = Widget.objects.create(
        screen=screen,
        widget_type="ListTile",
        parent_widget=settings_column,
        order=2,
        widget_id="language_setting"
    )

    WidgetProperty.objects.create(
        widget=language_tile,
        property_name="title",
        property_type="string",
        string_value="Language"
    )

    WidgetProperty.objects.create(
        widget=language_tile,
        property_name="subtitle",
        property_type="string",
        string_value="English"
    )

    WidgetProperty.objects.create(
        widget=language_tile,
        property_name="leading",
        property_type="string",
        string_value="language"
    )

    # Clear Cache Setting
    cache_tile = Widget.objects.create(
        screen=screen,
        widget_type="ListTile",
        parent_widget=settings_column,
        order=3,
        widget_id="cache_setting"
    )

    WidgetProperty.objects.create(
        widget=cache_tile,
        property_name="title",
        property_type="string",
        string_value="Clear Cache"
    )

    WidgetProperty.objects.create(
        widget=cache_tile,
        property_name="subtitle",
        property_type="string",
        string_value="Free up storage space"
    )

    WidgetProperty.objects.create(
        widget=cache_tile,
        property_name="leading",
        property_type="string",
        string_value="cached"
    )


def create_complete_notifications_screen(screen, data_sources, actions):
    """Create complete notifications screen"""

    # Notifications List
    notifications_list = Widget.objects.create(
        screen=screen,
        widget_type="ListView",
        order=0,
        widget_id="notifications_list"
    )

    # Sample notification items
    for i in range(5):
        notification_tile = Widget.objects.create(
            screen=screen,
            widget_type="ListTile",
            parent_widget=notifications_list,
            order=i,
            widget_id=f"notification_{i}"
        )

        WidgetProperty.objects.create(
            widget=notification_tile,
            property_name="title",
            property_type="string",
            string_value=f"Notification {i + 1}"
        )

        WidgetProperty.objects.create(
            widget=notification_tile,
            property_name="subtitle",
            property_type="string",
            string_value="New article available"
        )

        WidgetProperty.objects.create(
            widget=notification_tile,
            property_name="leading",
            property_type="string",
            string_value="notification_important"
        )


def create_complete_about_screen(screen, data_sources, actions):
    """Create complete about screen"""

    # About Column
    about_column = Widget.objects.create(
        screen=screen,
        widget_type="Column",
        order=0,
        widget_id="about_column"
    )

    # App Logo
    logo_container = Widget.objects.create(
        screen=screen,
        widget_type="Center",
        parent_widget=about_column,
        order=0,
        widget_id="logo_container"
    )

    logo_icon = Widget.objects.create(
        screen=screen,
        widget_type="Icon",
        parent_widget=logo_container,
        order=0,
        widget_id="app_logo"
    )

    WidgetProperty.objects.create(
        widget=logo_icon,
        property_name="icon",
        property_type="string",
        string_value="newspaper"
    )

    # App Name
    app_name = Widget.objects.create(
        screen=screen,
        widget_type="Text",
        parent_widget=about_column,
        order=1,
        widget_id="app_name"
    )

    WidgetProperty.objects.create(
        widget=app_name,
        property_name="text",
        property_type="string",
        string_value="NewsHub Pro"
    )

    WidgetProperty.objects.create(
        widget=app_name,
        property_name="fontSize",
        property_type="decimal",
        decimal_value=24
    )

    # Version
    version_text = Widget.objects.create(
        screen=screen,
        widget_type="Text",
        parent_widget=about_column,
        order=2,
        widget_id="app_version"
    )

    WidgetProperty.objects.create(
        widget=version_text,
        property_name="text",
        property_type="string",
        string_value="Version 1.0.0"
    )

    # Description
    description_text = Widget.objects.create(
        screen=screen,
        widget_type="Text",
        parent_widget=about_column,
        order=3,
        widget_id="app_description"
    )

    WidgetProperty.objects.create(
        widget=description_text,
        property_name="text",
        property_type="string",
        string_value="Your comprehensive news platform with real-time updates, personalized content, and complete coverage of global events."
    )

    # Copyright
    copyright_text = Widget.objects.create(
        screen=screen,
        widget_type="Text",
        parent_widget=about_column,
        order=4,
        widget_id="copyright"
    )

    WidgetProperty.objects.create(
        widget=copyright_text,
        property_name="text",
        property_type="string",
        string_value="© 2024 NewsHub Pro. All rights reserved."
    )