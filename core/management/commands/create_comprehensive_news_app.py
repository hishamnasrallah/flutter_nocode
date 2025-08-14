"""
Management command to create a comprehensive news application
File: core/management/commands/create_comprehensive_news_app.py
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import (
    Application, Theme, Screen, Widget, WidgetProperty,
    Action, DataSource, DataSourceField
)


class Command(BaseCommand):
    help = 'Create a comprehensive news application with all features'

    def add_arguments(self, parser):
        parser.add_argument(
            '--name',
            type=str,
            default='NewsHub Pro',
            help='Custom name for the news application'
        )
        parser.add_argument(
            '--package',
            type=str,
            default='com.newshub.pro',
            help='Package identifier for the application'
        )

    def handle(self, *args, **options):
        app_name = options['name']
        package_name = options['package']

        try:
            with transaction.atomic():
                app = create_comprehensive_news_app(app_name, package_name)
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully created comprehensive news application: {app.name}'
                    )
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating news application: {str(e)}')
            )


def create_comprehensive_news_app(custom_name=None, package_name=None):
    """Create a comprehensive news application with all features"""

    # Create professional news theme
    theme = Theme.objects.create(
        name="NewsHub Professional Theme",
        primary_color="#D32F2F",  # News red
        accent_color="#FF5722",   # Deep orange accent
        background_color="#FAFAFA",  # Light grey background
        text_color="#212121",  # Dark grey text
        font_family="Roboto",
        is_dark_mode=False
    )

    # Create application
    app = Application.objects.create(
        name=custom_name or "NewsHub Pro - Intelligent News Platform",
        description="""A comprehensive news application featuring real-time updates, 25+ categories, 
        AI-powered recommendations, offline reading, multimedia content, social features, and personalized news feeds. 
        Complete with breaking news alerts, trending topics, bookmarks, and advanced search capabilities.""",
        package_name=package_name or "com.newshub.pro",
        version="1.0.0",
        theme=theme
    )

    # Base URL for mock APIs
    base_url = "http://localhost:8000"

    # Create comprehensive data sources
    data_sources = create_data_sources(app, base_url)

    # Create actions
    actions = create_actions(app, data_sources)

    # Create screens
    screens = create_screens(app)

    # Update actions with screen references
    update_action_targets(actions, screens)

    # Create widgets for each screen
    create_home_screen_widgets(screens['home'], data_sources, actions)
    create_categories_screen_widgets(screens['categories'], data_sources, actions)
    create_article_details_widgets(screens['article_details'], data_sources, actions)
    create_search_screen_widgets(screens['search'], data_sources, actions)
    create_bookmarks_screen_widgets(screens['bookmarks'], data_sources, actions)
    create_profile_screen_widgets(screens['profile'], data_sources, actions)
    create_trending_screen_widgets(screens['trending'], data_sources, actions)
    create_videos_screen_widgets(screens['videos'], data_sources, actions)
    create_sources_screen_widgets(screens['sources'], data_sources, actions)
    create_notifications_screen_widgets(screens['notifications'], data_sources, actions)
    create_settings_screen_widgets(screens['settings'], data_sources, actions)

    return app


def create_data_sources(app, base_url):
    """Create all data sources for the news app"""
    data_sources = {}

    # Comprehensive feed data source
    feed_ds = DataSource.objects.create(
        application=app,
        name="News Feed",
        data_source_type="REST_API",
        base_url=base_url,
        endpoint="/api/mock/comprehensive/news/feed",
        method="GET"
    )

    feed_fields = [
        ("id", "string", "Article ID", True),
        ("title", "string", "Headline", True),
        ("summary", "string", "Summary", True),
        ("featuredImage", "image_url", "Main Image", True),
        ("author", "string", "Author Name", False),
        ("source", "string", "News Source", True),
        ("publishedAt", "datetime", "Published Date", True),
        ("readingTime", "integer", "Reading Time", False),
        ("category", "string", "Category", True),
        ("viewsCount", "integer", "Views", False),
        ("likesCount", "integer", "Likes", False),
        ("commentsCount", "integer", "Comments", False)
    ]

    for field_name, field_type, display_name, is_required in feed_fields:
        DataSourceField.objects.create(
            data_source=feed_ds,
            field_name=field_name,
            field_type=field_type,
            display_name=display_name,
            is_required=is_required
        )

    data_sources['feed'] = feed_ds

    # Breaking news data source
    breaking_ds = DataSource.objects.create(
        application=app,
        name="Breaking News",
        data_source_type="REST_API",
        base_url=base_url,
        endpoint="/api/mock/news/breaking",
        method="GET"
    )

    for field_name, field_type, display_name, is_required in feed_fields:
        DataSourceField.objects.create(
            data_source=breaking_ds,
            field_name=field_name,
            field_type=field_type,
            display_name=display_name,
            is_required=is_required
        )

    data_sources['breaking'] = breaking_ds

    # Categories data source
    categories_ds = DataSource.objects.create(
        application=app,
        name="Categories",
        data_source_type="REST_API",
        base_url=base_url,
        endpoint="/api/mock/news/categories",
        method="GET"
    )

    category_fields = [
        ("id", "string", "Category ID", True),
        ("name", "string", "Category Name", True),
        ("icon", "string", "Category Icon", False),
        ("color", "color", "Category Color", False),
        ("priority", "integer", "Display Priority", False)
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

    # Add more data sources...

    return data_sources


def create_actions(app, data_sources):
    """Create all actions for the news app"""
    actions = {}

    # Navigation actions
    nav_actions = [
        ("Navigate to Article", "navigate"),
        ("Navigate to Category", "navigate"),
        ("Navigate to Search", "navigate"),
        ("Navigate to Bookmarks", "navigate"),
        ("Navigate to Profile", "navigate"),
        ("Navigate to Settings", "navigate"),
        ("Navigate to Notifications", "navigate"),
        ("Navigate to Videos", "navigate"),
        ("Navigate to Sources", "navigate"),
        ("Navigate to Trending", "navigate"),
        ("Go Back", "navigate_back"),
    ]

    for name, action_type in nav_actions:
        action = Action.objects.create(
            application=app,
            name=name,
            action_type=action_type
        )
        actions[name] = action

    # Data actions with API sources
    actions["Refresh Feed"] = Action.objects.create(
        application=app,
        name="Refresh Feed",
        action_type="refresh_data"
    )

    actions["Load More Articles"] = Action.objects.create(
        application=app,
        name="Load More Articles",
        action_type="api_call",
        api_data_source=data_sources['feed']
    )

    # User interaction actions
    actions["Like Article"] = Action.objects.create(
        application=app,
        name="Like Article",
        action_type="api_call"
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

    return actions


def create_screens(app):
    """Create all screens for the news app"""
    screens = {}

    screens['home'] = Screen.objects.create(
        application=app,
        name="Home",
        route_name="/",
        is_home_screen=True,
        app_bar_title="NewsHub Pro",
        show_app_bar=True,
        show_back_button=False
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

    screens['article_details'] = Screen.objects.create(
        application=app,
        name="Article Details",
        route_name="/article",
        is_home_screen=False,
        app_bar_title="Article",
        show_app_bar=True,
        show_back_button=True
    )

    screens['search'] = Screen.objects.create(
        application=app,
        name="Search",
        route_name="/search",
        is_home_screen=False,
        app_bar_title="Search News",
        show_app_bar=True,
        show_back_button=True
    )

    screens['bookmarks'] = Screen.objects.create(
        application=app,
        name="Bookmarks",
        route_name="/bookmarks",
        is_home_screen=False,
        app_bar_title="Saved Articles",
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

    screens['trending'] = Screen.objects.create(
        application=app,
        name="Trending",
        route_name="/trending",
        is_home_screen=False,
        app_bar_title="Trending Now",
        show_app_bar=True,
        show_back_button=True
    )

    screens['videos'] = Screen.objects.create(
        application=app,
        name="Videos",
        route_name="/videos",
        is_home_screen=False,
        app_bar_title="Video News",
        show_app_bar=True,
        show_back_button=True
    )

    screens['sources'] = Screen.objects.create(
        application=app,
        name="Sources",
        route_name="/sources",
        is_home_screen=False,
        app_bar_title="News Sources",
        show_app_bar=True,
        show_back_button=True
    )

    screens['notifications'] = Screen.objects.create(
        application=app,
        name="Notifications",
        route_name="/notifications",
        is_home_screen=False,
        app_bar_title="Notifications",
        show_app_bar=True,
        show_back_button=True
    )

    screens['settings'] = Screen.objects.create(
        application=app,
        name="Settings",
        route_name="/settings",
        is_home_screen=False,
        app_bar_title="Settings",
        show_app_bar=True,
        show_back_button=True
    )

    return screens


def update_action_targets(actions, screens):
    """Update navigation actions with their target screens"""
    action_screen_mapping = {
        "Navigate to Article": screens['article_details'],
        "Navigate to Category": screens['categories'],
        "Navigate to Search": screens['search'],
        "Navigate to Bookmarks": screens['bookmarks'],
        "Navigate to Profile": screens['profile'],
        "Navigate to Settings": screens['settings'],
        "Navigate to Notifications": screens['notifications'],
        "Navigate to Videos": screens['videos'],
        "Navigate to Sources": screens['sources'],
        "Navigate to Trending": screens['trending'],
    }

    for action_name, target_screen in action_screen_mapping.items():
        if action_name in actions:
            actions[action_name].target_screen = target_screen
            actions[action_name].save()


def create_home_screen_widgets(screen, data_sources, actions):
    """Create widgets for the home screen"""

    # Main container
    main_container = Widget.objects.create(
        screen=screen,
        widget_type="Column",
        order=0,
        widget_id="home_main_column"
    )

    # Breaking news banner
    breaking_banner = Widget.objects.create(
        screen=screen,
        widget_type="Container",
        parent_widget=main_container,
        order=0,
        widget_id="breaking_news_banner"
    )

    WidgetProperty.objects.create(
        widget=breaking_banner,
        property_name="color",
        property_type="color",
        color_value="#D32F2F"
    )

    WidgetProperty.objects.create(
        widget=breaking_banner,
        property_name="padding",
        property_type="integer",
        integer_value=12
    )

    breaking_text = Widget.objects.create(
        screen=screen,
        widget_type="Text",
        parent_widget=breaking_banner,
        order=0,
        widget_id="breaking_news_text"
    )

    WidgetProperty.objects.create(
        widget=breaking_text,
        property_name="text",
        property_type="string",
        string_value="BREAKING NEWS: Major developments unfolding..."
    )

    WidgetProperty.objects.create(
        widget=breaking_text,
        property_name="color",
        property_type="color",
        color_value="#FFFFFF"
    )

    # Categories horizontal scroll
    categories_container = Widget.objects.create(
        screen=screen,
        widget_type="Container",
        parent_widget=main_container,
        order=1,
        widget_id="categories_container"
    )

    WidgetProperty.objects.create(
        widget=categories_container,
        property_name="height",
        property_type="integer",
        integer_value=100
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

    # Main news feed
    news_feed = Widget.objects.create(
        screen=screen,
        widget_type="ListView",
        parent_widget=main_container,
        order=2,
        widget_id="main_news_feed"
    )

    WidgetProperty.objects.create(
        widget=news_feed,
        property_name="dataSource",
        property_type="data_source_field_reference",
        data_source_field_reference=DataSourceField.objects.get(
            data_source=data_sources['feed'],
            field_name="title"
        )
    )

    # Bottom navigation bar
    bottom_nav = Widget.objects.create(
        screen=screen,
        widget_type="Row",
        parent_widget=main_container,
        order=3,
        widget_id="bottom_navigation"
    )

    # Home button
    home_btn = Widget.objects.create(
        screen=screen,
        widget_type="IconButton",
        parent_widget=bottom_nav,
        order=0,
        widget_id="nav_home"
    )

    WidgetProperty.objects.create(
        widget=home_btn,
        property_name="icon",
        property_type="string",
        string_value="home"
    )

    # Search button
    search_btn = Widget.objects.create(
        screen=screen,
        widget_type="IconButton",
        parent_widget=bottom_nav,
        order=1,
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

    # Bookmarks button
    bookmarks_btn = Widget.objects.create(
        screen=screen,
        widget_type="IconButton",
        parent_widget=bottom_nav,
        order=2,
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

    # Profile button
    profile_btn = Widget.objects.create(
        screen=screen,
        widget_type="IconButton",
        parent_widget=bottom_nav,
        order=3,
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


def create_categories_screen_widgets(screen, data_sources, actions):
    """Create widgets for categories screen"""

    # Main grid for categories
    categories_grid = Widget.objects.create(
        screen=screen,
        widget_type="GridView",
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


def create_article_details_widgets(screen, data_sources, actions):
    """Create widgets for article details screen"""

    # Scrollable column
    scroll_view = Widget.objects.create(
        screen=screen,
        widget_type="SingleChildScrollView",
        order=0,
        widget_id="article_scroll"
    )

    article_column = Widget.objects.create(
        screen=screen,
        widget_type="Column",
        parent_widget=scroll_view,
        order=0,
        widget_id="article_column"
    )

    # Featured image
    article_image = Widget.objects.create(
        screen=screen,
        widget_type="Image",
        parent_widget=article_column,
        order=0,
        widget_id="article_featured_image"
    )

    # Article title
    article_title = Widget.objects.create(
        screen=screen,
        widget_type="Text",
        parent_widget=article_column,
        order=1,
        widget_id="article_title"
    )

    WidgetProperty.objects.create(
        widget=article_title,
        property_name="fontSize",
        property_type="integer",
        integer_value=24
    )

    # Article metadata row
    meta_row = Widget.objects.create(
        screen=screen,
        widget_type="Row",
        parent_widget=article_column,
        order=2,
        widget_id="article_meta"
    )

    # Author
    author_text = Widget.objects.create(
        screen=screen,
        widget_type="Text",
        parent_widget=meta_row,
        order=0,
        widget_id="article_author"
    )

    # Date
    date_text = Widget.objects.create(
        screen=screen,
        widget_type="Text",
        parent_widget=meta_row,
        order=1,
        widget_id="article_date"
    )

    # Article content
    article_content = Widget.objects.create(
        screen=screen,
        widget_type="Text",
        parent_widget=article_column,
        order=3,
        widget_id="article_content"
    )

    # Action buttons row
    action_row = Widget.objects.create(
        screen=screen,
        widget_type="Row",
        parent_widget=article_column,
        order=4,
        widget_id="article_actions"
    )

    # Like button
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
        string_value="favorite"
    )

    WidgetProperty.objects.create(
        widget=like_btn,
        property_name="onPressed",
        property_type="action_reference",
        action_reference=actions["Like Article"]
    )

    # Share button
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

    # Bookmark button
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


def create_search_screen_widgets(screen, data_sources, actions):
    """Create widgets for search screen"""

    # Main column
    search_column = Widget.objects.create(
        screen=screen,
        widget_type="Column",
        order=0,
        widget_id="search_column"
    )

    # Search bar
    search_field = Widget.objects.create(
        screen=screen,
        widget_type="TextField",
        parent_widget=search_column,
        order=0,
        widget_id="search_input"
    )

    WidgetProperty.objects.create(
        widget=search_field,
        property_name="hintText",
        property_type="string",
        string_value="Search for news, topics, or authors..."
    )

    # Search results list
    results_list = Widget.objects.create(
        screen=screen,
        widget_type="ListView",
        parent_widget=search_column,
        order=1,
        widget_id="search_results"
    )


def create_bookmarks_screen_widgets(screen, data_sources, actions):
    """Create widgets for bookmarks screen"""

    # Bookmarked articles list
    bookmarks_list = Widget.objects.create(
        screen=screen,
        widget_type="ListView",
        order=0,
        widget_id="bookmarks_list"
    )


def create_profile_screen_widgets(screen, data_sources, actions):
    """Create widgets for profile screen"""

    # Profile column
    profile_column = Widget.objects.create(
        screen=screen,
        widget_type="Column",
        order=0,
        widget_id="profile_column"
    )

    # Profile header
    profile_header = Widget.objects.create(
        screen=screen,
        widget_type="Container",
        parent_widget=profile_column,
        order=0,
        widget_id="profile_header"
    )

    # Avatar
    avatar = Widget.objects.create(
        screen=screen,
        widget_type="Image",
        parent_widget=profile_header,
        order=0,
        widget_id="profile_avatar"
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

    # Settings button
    settings_btn = Widget.objects.create(
        screen=screen,
        widget_type="ElevatedButton",
        parent_widget=profile_column,
        order=1,
        widget_id="settings_button"
    )

    WidgetProperty.objects.create(
        widget=settings_btn,
        property_name="text",
        property_type="string",
        string_value="Settings"
    )

    WidgetProperty.objects.create(
        widget=settings_btn,
        property_name="onPressed",
        property_type="action_reference",
        action_reference=actions["Navigate to Settings"]
    )


def create_trending_screen_widgets(screen, data_sources, actions):
    """Create widgets for trending screen"""

    # Trending articles list
    trending_list = Widget.objects.create(
        screen=screen,
        widget_type="ListView",
        order=0,
        widget_id="trending_list"
    )

    WidgetProperty.objects.create(
        widget=trending_list,
        property_name="dataSource",
        property_type="data_source_field_reference",
        data_source_field_reference=DataSourceField.objects.get(
            data_source=data_sources.get('feed'),
            field_name="title"
        )
    )


def create_videos_screen_widgets(screen, data_sources, actions):
    """Create widgets for videos screen"""

    # Video grid
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


def create_sources_screen_widgets(screen, data_sources, actions):
    """Create widgets for sources screen"""

    # Sources list
    sources_list = Widget.objects.create(
        screen=screen,
        widget_type="ListView",
        order=0,
        widget_id="sources_list"
    )


def create_notifications_screen_widgets(screen, data_sources, actions):
    """Create widgets for notifications screen"""

    # Notifications list
    notifications_list = Widget.objects.create(
        screen=screen,
        widget_type="ListView",
        order=0,
        widget_id="notifications_list"
    )


def create_settings_screen_widgets(screen, data_sources, actions):
    """Create widgets for settings screen"""

    # Settings column
    settings_column = Widget.objects.create(
        screen=screen,
        widget_type="Column",
        order=0,
        widget_id="settings_column"
    )

    # Dark mode toggle
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

    # Notifications setting
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

    # About section
    about_tile = Widget.objects.create(
        screen=screen,
        widget_type="ListTile",
        parent_widget=settings_column,
        order=2,
        widget_id="about_setting"
    )

    WidgetProperty.objects.create(
        widget=about_tile,
        property_name="title",
        property_type="string",
        string_value="About"
    )