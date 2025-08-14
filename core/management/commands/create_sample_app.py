from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import (
    Application, Theme, Screen, Widget, WidgetProperty, 
    Action, DataSource, DataSourceField
)


class Command(BaseCommand):
    help = 'Create sample applications to demonstrate the platform capabilities'
    
    def add_arguments(self, parser):
        parser.add_argument(
            'app_type',
            choices=['ecommerce', 'social_media', 'news'],
            help='Type of sample application to create'
        )
        parser.add_argument(
            '--name',
            type=str,
            help='Custom name for the application'
        )
    
    def handle(self, *args, **options):
        app_type = options['app_type']
        custom_name = options.get('name')
        
        try:
            with transaction.atomic():
                if app_type == 'ecommerce':
                    app = create_ecommerce_app(custom_name)
                elif app_type == 'social_media':
                    app = create_social_media_app(custom_name)
                elif app_type == 'news':
                    app = create_news_app(custom_name)
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully created {app_type} sample application: {app.name}'
                    )
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating sample application: {str(e)}')
            )


def create_ecommerce_app(custom_name=None):
    """Create a comprehensive e-commerce application"""
    
    # Create theme
    theme = Theme.objects.create(
        name="E-commerce Theme",
        primary_color="#2196F3",
        accent_color="#FF4081",
        background_color="#FFFFFF",
        text_color="#000000",
        font_family="Roboto",
        is_dark_mode=False
    )
    
    # Create application
    app = Application.objects.create(
        name=custom_name or "Sample E-commerce Store",
        description="A complete e-commerce application with product catalog, shopping cart, user authentication, and order management",
        package_name="com.example.ecommerce_store",
        version="1.0.0",
        theme=theme
    )
    
    # Create data sources
    products_ds = DataSource.objects.create(
        application=app,
        name="Products",
        data_source_type="REST_API",
        base_url="https://fakestoreapi.com",
        endpoint="/products",
        method="GET"
    )
    
    # Create data source fields for products
    product_fields = [
        ("id", "integer", "Product ID"),
        ("title", "string", "Product Name"),
        ("price", "decimal", "Price"),
        ("description", "string", "Description"),
        ("category", "string", "Category"),
        ("image", "image_url", "Product Image"),
        ("rating", "string", "Rating")
    ]
    
    for field_name, field_type, display_name in product_fields:
        DataSourceField.objects.create(
            data_source=products_ds,
            field_name=field_name,
            field_type=field_type,
            display_name=display_name,
            is_required=field_name in ['id', 'title', 'price']
        )
    
    # Create categories data source
    categories_ds = DataSource.objects.create(
        application=app,
        name="Categories",
        data_source_type="REST_API",
        base_url="https://fakestoreapi.com",
        endpoint="/products/categories",
        method="GET"
    )
    
    DataSourceField.objects.create(
        data_source=categories_ds,
        field_name="category",
        field_type="string",
        display_name="Category Name",
        is_required=True
    )
    
    # Create user data source
    users_ds = DataSource.objects.create(
        application=app,
        name="Users",
        data_source_type="REST_API",
        base_url="https://fakestoreapi.com",
        endpoint="/users",
        method="GET"
    )
    
    user_fields = [
        ("id", "integer", "User ID"),
        ("email", "email", "Email"),
        ("username", "string", "Username"),
        ("name", "string", "Full Name"),
        ("phone", "string", "Phone Number"),
        ("address", "string", "Address")
    ]
    
    for field_name, field_type, display_name in user_fields:
        DataSourceField.objects.create(
            data_source=users_ds,
            field_name=field_name,
            field_type=field_type,
            display_name=display_name,
            is_required=field_name in ['id', 'email', 'username']
        )
    
    # Create actions
    actions = [
        ("Navigate to Product Details", "navigate", None, None),
        ("Add to Cart", "api_call", None, None),
        ("View Cart", "navigate", None, None),
        ("Checkout", "navigate", None, None),
        ("User Login", "navigate", None, None),
        ("User Register", "navigate", None, None),
        ("Search Products", "api_call", products_ds, None),
        ("Filter by Category", "api_call", products_ds, None),
        ("View Profile", "navigate", None, None),
        ("View Orders", "navigate", None, None),
    ]
    
    action_objects = {}
    for name, action_type, api_ds, target in actions:
        action = Action.objects.create(
            application=app,
            name=name,
            action_type=action_type,
            api_data_source=api_ds
        )
        action_objects[name] = action
    
    # Create screens
    screens_data = [
        ("Home", "/", True, "Store Home", True, True),
        ("Product List", "/products", False, "Products", True, True),
        ("Product Details", "/product-details", False, "Product Details", True, True),
        ("Shopping Cart", "/cart", False, "Shopping Cart", True, True),
        ("Checkout", "/checkout", False, "Checkout", True, True),
        ("User Login", "/login", False, "Login", True, False),
        ("User Register", "/register", False, "Register", True, False),
        ("User Profile", "/profile", False, "My Profile", True, True),
        ("Order History", "/orders", False, "My Orders", True, True),
        ("Search Results", "/search", False, "Search Results", True, True),
    ]
    
    screen_objects = {}
    for name, route, is_home, title, show_bar, show_back in screens_data:
        screen = Screen.objects.create(
            application=app,
            name=name,
            route_name=route,
            is_home_screen=is_home,
            app_bar_title=title,
            show_app_bar=show_bar,
            show_back_button=show_back
        )
        screen_objects[name] = screen
    
    # Update actions with target screens
    action_objects["Navigate to Product Details"].target_screen = screen_objects["Product Details"]
    action_objects["Navigate to Product Details"].save()
    
    action_objects["View Cart"].target_screen = screen_objects["Shopping Cart"]
    action_objects["View Cart"].save()
    
    action_objects["Checkout"].target_screen = screen_objects["Checkout"]
    action_objects["Checkout"].save()
    
    action_objects["User Login"].target_screen = screen_objects["User Login"]
    action_objects["User Login"].save()
    
    action_objects["User Register"].target_screen = screen_objects["User Register"]
    action_objects["User Register"].save()
    
    action_objects["View Profile"].target_screen = screen_objects["User Profile"]
    action_objects["View Profile"].save()
    
    action_objects["View Orders"].target_screen = screen_objects["Order History"]
    action_objects["View Orders"].save()
    
    # Create widgets for Home screen
    home_screen = screen_objects["Home"]
    
    # Main container
    main_container = Widget.objects.create(
        screen=home_screen,
        widget_type="Column",
        order=0,
        widget_id="home_main_column"
    )
    
    # Welcome text
    welcome_text = Widget.objects.create(
        screen=home_screen,
        widget_type="Text",
        parent_widget=main_container,
        order=0,
        widget_id="welcome_text"
    )
    
    WidgetProperty.objects.create(
        widget=welcome_text,
        property_name="text",
        property_type="string",
        string_value="Welcome to Our Store!"
    )
    
    # Categories section
    categories_title = Widget.objects.create(
        screen=home_screen,
        widget_type="Text",
        parent_widget=main_container,
        order=1,
        widget_id="categories_title"
    )
    
    WidgetProperty.objects.create(
        widget=categories_title,
        property_name="text",
        property_type="string",
        string_value="Shop by Category"
    )
    
    # Featured products section
    featured_title = Widget.objects.create(
        screen=home_screen,
        widget_type="Text",
        parent_widget=main_container,
        order=2,
        widget_id="featured_title"
    )
    
    WidgetProperty.objects.create(
        widget=featured_title,
        property_name="text",
        property_type="string",
        string_value="Featured Products"
    )
    
    # Products list
    products_list = Widget.objects.create(
        screen=home_screen,
        widget_type="ListView",
        parent_widget=main_container,
        order=3,
        widget_id="featured_products_list"
    )
    
    # Navigation buttons
    buttons_row = Widget.objects.create(
        screen=home_screen,
        widget_type="Row",
        parent_widget=main_container,
        order=4,
        widget_id="navigation_buttons"
    )
    
    # View All Products button
    all_products_btn = Widget.objects.create(
        screen=home_screen,
        widget_type="ElevatedButton",
        parent_widget=buttons_row,
        order=0,
        widget_id="all_products_button"
    )
    
    WidgetProperty.objects.create(
        widget=all_products_btn,
        property_name="text",
        property_type="string",
        string_value="View All Products"
    )
    
    WidgetProperty.objects.create(
        widget=all_products_btn,
        property_name="onPressed",
        property_type="screen_reference",
        screen_reference=screen_objects["Product List"]
    )
    
    # Cart button
    cart_btn = Widget.objects.create(
        screen=home_screen,
        widget_type="ElevatedButton",
        parent_widget=buttons_row,
        order=1,
        widget_id="cart_button"
    )
    
    WidgetProperty.objects.create(
        widget=cart_btn,
        property_name="text",
        property_type="string",
        string_value="View Cart"
    )
    
    WidgetProperty.objects.create(
        widget=cart_btn,
        property_name="onPressed",
        property_type="screen_reference",
        screen_reference=screen_objects["Shopping Cart"]
    )
    
    # Create widgets for Product List screen
    product_list_screen = screen_objects["Product List"]
    
    # Search bar
    search_container = Widget.objects.create(
        screen=product_list_screen,
        widget_type="Container",
        order=0,
        widget_id="search_container"
    )
    
    search_field = Widget.objects.create(
        screen=product_list_screen,
        widget_type="TextField",
        parent_widget=search_container,
        order=0,
        widget_id="search_field"
    )
    
    WidgetProperty.objects.create(
        widget=search_field,
        property_name="hintText",
        property_type="string",
        string_value="Search products..."
    )
    
    # Products grid
    products_grid = Widget.objects.create(
        screen=product_list_screen,
        widget_type="GridView",
        order=1,
        widget_id="products_grid"
    )
    
    WidgetProperty.objects.create(
        widget=products_grid,
        property_name="dataSource",
        property_type="data_source_field_reference",
        data_source_field_reference=DataSourceField.objects.get(
            data_source=products_ds,
            field_name="title"
        )
    )
    
    # Create widgets for Product Details screen
    product_details_screen = screen_objects["Product Details"]
    
    details_column = Widget.objects.create(
        screen=product_details_screen,
        widget_type="Column",
        order=0,
        widget_id="product_details_column"
    )
    
    # Product image
    product_image = Widget.objects.create(
        screen=product_details_screen,
        widget_type="Image",
        parent_widget=details_column,
        order=0,
        widget_id="product_image"
    )
    
    # Product title
    product_title = Widget.objects.create(
        screen=product_details_screen,
        widget_type="Text",
        parent_widget=details_column,
        order=1,
        widget_id="product_title"
    )
    
    # Product price
    product_price = Widget.objects.create(
        screen=product_details_screen,
        widget_type="Text",
        parent_widget=details_column,
        order=2,
        widget_id="product_price"
    )
    
    # Product description
    product_description = Widget.objects.create(
        screen=product_details_screen,
        widget_type="Text",
        parent_widget=details_column,
        order=3,
        widget_id="product_description"
    )
    
    # Add to cart button
    add_to_cart_btn = Widget.objects.create(
        screen=product_details_screen,
        widget_type="ElevatedButton",
        parent_widget=details_column,
        order=4,
        widget_id="add_to_cart_button"
    )
    
    WidgetProperty.objects.create(
        widget=add_to_cart_btn,
        property_name="text",
        property_type="string",
        string_value="Add to Cart"
    )
    
    WidgetProperty.objects.create(
        widget=add_to_cart_btn,
        property_name="onPressed",
        property_type="action_reference",
        action_reference=action_objects["Add to Cart"]
    )
    
    return app


def create_social_media_app(custom_name=None):
    """Create a comprehensive social media application"""
    
    # Create theme
    theme = Theme.objects.create(
        name="Social Media Theme",
        primary_color="#1976D2",
        accent_color="#E91E63",
        background_color="#FAFAFA",
        text_color="#212121",
        font_family="Roboto",
        is_dark_mode=False
    )
    
    # Create application
    app = Application.objects.create(
        name=custom_name or "Sample Social Media App",
        description="A complete social media application with user profiles, posts, comments, likes, messaging, and real-time updates",
        package_name="com.example.social_media",
        version="1.0.0",
        theme=theme
    )
    
    # Create data sources
    posts_ds = DataSource.objects.create(
        application=app,
        name="Posts",
        data_source_type="REST_API",
        base_url="https://jsonplaceholder.typicode.com",
        endpoint="/posts",
        method="GET"
    )
    
    # Create data source fields for posts
    post_fields = [
        ("id", "integer", "Post ID"),
        ("userId", "integer", "User ID"),
        ("title", "string", "Post Title"),
        ("body", "string", "Post Content"),
        ("likes", "integer", "Likes Count"),
        ("comments", "integer", "Comments Count"),
        ("timestamp", "datetime", "Posted At")
    ]
    
    for field_name, field_type, display_name in post_fields:
        DataSourceField.objects.create(
            data_source=posts_ds,
            field_name=field_name,
            field_type=field_type,
            display_name=display_name,
            is_required=field_name in ['id', 'userId', 'title', 'body']
        )
    
    # Create users data source
    users_ds = DataSource.objects.create(
        application=app,
        name="Users",
        data_source_type="REST_API",
        base_url="https://jsonplaceholder.typicode.com",
        endpoint="/users",
        method="GET"
    )
    
    user_fields = [
        ("id", "integer", "User ID"),
        ("name", "string", "Full Name"),
        ("username", "string", "Username"),
        ("email", "email", "Email"),
        ("phone", "string", "Phone"),
        ("website", "url", "Website"),
        ("bio", "string", "Bio"),
        ("avatar", "image_url", "Profile Picture"),
        ("followers", "integer", "Followers Count"),
        ("following", "integer", "Following Count")
    ]
    
    for field_name, field_type, display_name in user_fields:
        DataSourceField.objects.create(
            data_source=users_ds,
            field_name=field_name,
            field_type=field_type,
            display_name=display_name,
            is_required=field_name in ['id', 'name', 'username']
        )
    
    # Create comments data source
    comments_ds = DataSource.objects.create(
        application=app,
        name="Comments",
        data_source_type="REST_API",
        base_url="https://jsonplaceholder.typicode.com",
        endpoint="/comments",
        method="GET"
    )
    
    comment_fields = [
        ("id", "integer", "Comment ID"),
        ("postId", "integer", "Post ID"),
        ("name", "string", "Commenter Name"),
        ("email", "email", "Commenter Email"),
        ("body", "string", "Comment Text")
    ]
    
    for field_name, field_type, display_name in comment_fields:
        DataSourceField.objects.create(
            data_source=comments_ds,
            field_name=field_name,
            field_type=field_type,
            display_name=display_name,
            is_required=True
        )
    
    # Create actions
    actions = [
        ("Like Post", "api_call", posts_ds, None),
        ("Comment on Post", "navigate", None, None),
        ("Share Post", "share_content", None, None),
        ("View Profile", "navigate", None, None),
        ("Follow User", "api_call", users_ds, None),
        ("Unfollow User", "api_call", users_ds, None),
        ("Create Post", "navigate", None, None),
        ("Edit Profile", "navigate", None, None),
        ("Send Message", "navigate", None, None),
        ("View Messages", "navigate", None, None),
        ("Search Users", "api_call", users_ds, None),
        ("Refresh Feed", "refresh_data", None, None),
    ]
    
    action_objects = {}
    for name, action_type, api_ds, target in actions:
        action = Action.objects.create(
            application=app,
            name=name,
            action_type=action_type,
            api_data_source=api_ds
        )
        action_objects[name] = action
    
    # Create screens
    screens_data = [
        ("Feed", "/", True, "Social Feed", True, False),
        ("Profile", "/profile", False, "Profile", True, True),
        ("Create Post", "/create-post", False, "New Post", True, True),
        ("Post Details", "/post-details", False, "Post", True, True),
        ("User Profile", "/user-profile", False, "User Profile", True, True),
        ("Messages", "/messages", False, "Messages", True, True),
        ("Chat", "/chat", False, "Chat", True, True),
        ("Search", "/search", False, "Search", True, True),
        ("Notifications", "/notifications", False, "Notifications", True, True),
        ("Settings", "/settings", False, "Settings", True, True),
        ("Edit Profile", "/edit-profile", False, "Edit Profile", True, True),
        ("Followers", "/followers", False, "Followers", True, True),
        ("Following", "/following", False, "Following", True, True),
    ]
    
    screen_objects = {}
    for name, route, is_home, title, show_bar, show_back in screens_data:
        screen = Screen.objects.create(
            application=app,
            name=name,
            route_name=route,
            is_home_screen=is_home,
            app_bar_title=title,
            show_app_bar=show_bar,
            show_back_button=show_back
        )
        screen_objects[name] = screen
    
    # Update actions with target screens
    action_objects["Comment on Post"].target_screen = screen_objects["Post Details"]
    action_objects["Comment on Post"].save()
    
    action_objects["View Profile"].target_screen = screen_objects["User Profile"]
    action_objects["View Profile"].save()
    
    action_objects["Create Post"].target_screen = screen_objects["Create Post"]
    action_objects["Create Post"].save()
    
    action_objects["Edit Profile"].target_screen = screen_objects["Edit Profile"]
    action_objects["Edit Profile"].save()
    
    action_objects["Send Message"].target_screen = screen_objects["Chat"]
    action_objects["Send Message"].save()
    
    action_objects["View Messages"].target_screen = screen_objects["Messages"]
    action_objects["View Messages"].save()
    
    # Create widgets for Feed screen
    feed_screen = screen_objects["Feed"]
    
    # Main container
    feed_container = Widget.objects.create(
        screen=feed_screen,
        widget_type="Column",
        order=0,
        widget_id="feed_main_column"
    )
    
    # Stories section
    stories_container = Widget.objects.create(
        screen=feed_screen,
        widget_type="Container",
        parent_widget=feed_container,
        order=0,
        widget_id="stories_container"
    )
    
    stories_list = Widget.objects.create(
        screen=feed_screen,
        widget_type="ListView",
        parent_widget=stories_container,
        order=0,
        widget_id="stories_list"
    )
    
    # Posts feed
    posts_list = Widget.objects.create(
        screen=feed_screen,
        widget_type="ListView",
        parent_widget=feed_container,
        order=1,
        widget_id="posts_feed"
    )
    
    WidgetProperty.objects.create(
        widget=posts_list,
        property_name="dataSource",
        property_type="data_source_field_reference",
        data_source_field_reference=DataSourceField.objects.get(
            data_source=posts_ds,
            field_name="title"
        )
    )
    
    # Floating action button for creating posts
    create_post_fab = Widget.objects.create(
        screen=feed_screen,
        widget_type="FloatingActionButton",
        order=2,
        widget_id="create_post_fab"
    )
    
    WidgetProperty.objects.create(
        widget=create_post_fab,
        property_name="onPressed",
        property_type="action_reference",
        action_reference=action_objects["Create Post"]
    )
    
    # Create widgets for Profile screen
    profile_screen = screen_objects["Profile"]
    
    profile_column = Widget.objects.create(
        screen=profile_screen,
        widget_type="Column",
        order=0,
        widget_id="profile_main_column"
    )
    
    # Profile header
    profile_header = Widget.objects.create(
        screen=profile_screen,
        widget_type="Container",
        parent_widget=profile_column,
        order=0,
        widget_id="profile_header"
    )
    
    # Profile picture
    profile_avatar = Widget.objects.create(
        screen=profile_screen,
        widget_type="Image",
        parent_widget=profile_header,
        order=0,
        widget_id="profile_avatar"
    )
    
    # Profile info
    profile_info = Widget.objects.create(
        screen=profile_screen,
        widget_type="Column",
        parent_widget=profile_header,
        order=1,
        widget_id="profile_info"
    )
    
    # Username
    username_text = Widget.objects.create(
        screen=profile_screen,
        widget_type="Text",
        parent_widget=profile_info,
        order=0,
        widget_id="username_text"
    )
    
    # Bio
    bio_text = Widget.objects.create(
        screen=profile_screen,
        widget_type="Text",
        parent_widget=profile_info,
        order=1,
        widget_id="bio_text"
    )
    
    # Stats row (followers, following, posts)
    stats_row = Widget.objects.create(
        screen=profile_screen,
        widget_type="Row",
        parent_widget=profile_column,
        order=1,
        widget_id="stats_row"
    )
    
    # Posts count
    posts_count = Widget.objects.create(
        screen=profile_screen,
        widget_type="Text",
        parent_widget=stats_row,
        order=0,
        widget_id="posts_count"
    )
    
    # Followers count
    followers_count = Widget.objects.create(
        screen=profile_screen,
        widget_type="Text",
        parent_widget=stats_row,
        order=1,
        widget_id="followers_count"
    )
    
    # Following count
    following_count = Widget.objects.create(
        screen=profile_screen,
        widget_type="Text",
        parent_widget=stats_row,
        order=2,
        widget_id="following_count"
    )
    
    # Action buttons
    action_buttons = Widget.objects.create(
        screen=profile_screen,
        widget_type="Row",
        parent_widget=profile_column,
        order=2,
        widget_id="action_buttons"
    )
    
    # Edit profile button
    edit_profile_btn = Widget.objects.create(
        screen=profile_screen,
        widget_type="ElevatedButton",
        parent_widget=action_buttons,
        order=0,
        widget_id="edit_profile_button"
    )
    
    WidgetProperty.objects.create(
        widget=edit_profile_btn,
        property_name="text",
        property_type="string",
        string_value="Edit Profile"
    )
    
    WidgetProperty.objects.create(
        widget=edit_profile_btn,
        property_name="onPressed",
        property_type="action_reference",
        action_reference=action_objects["Edit Profile"]
    )
    
    # User posts grid
    user_posts_grid = Widget.objects.create(
        screen=profile_screen,
        widget_type="GridView",
        parent_widget=profile_column,
        order=3,
        widget_id="user_posts_grid"
    )
    
    return app


def create_news_app(custom_name=None):
    """Create a comprehensive news application"""
    
    # Create theme
    theme = Theme.objects.create(
        name="News Theme",
        primary_color="#D32F2F",
        accent_color="#FF5722",
        background_color="#FFFFFF",
        text_color="#212121",
        font_family="Roboto",
        is_dark_mode=False
    )
    
    # Create application
    app = Application.objects.create(
        name=custom_name or "Sample News App",
        description="A comprehensive news application with breaking news, categories, search, bookmarks, offline reading, and push notifications",
        package_name="com.example.news_app",
        version="1.0.0",
        theme=theme
    )
    
    # Create data sources with mock data
    news_ds = DataSource.objects.create(
        application=app,
        name="News Articles",
        data_source_type="STATIC_JSON",
        static_data='''[
    {
        "id": "1",
        "title": "Breaking: Major Technology Breakthrough Announced",
        "description": "Scientists reveal groundbreaking discovery that could revolutionize computing",
        "content": "In a stunning announcement today, researchers at leading universities have unveiled a new quantum computing breakthrough that promises to accelerate processing speeds by 1000x. The technology uses novel quantum entanglement techniques...",
        "author": "John Smith",
        "source": "Tech Daily",
        "publishedAt": "2024-01-15T10:30:00Z",
        "urlToImage": "https://picsum.photos/400/200?random=1",
        "url": "https://example.com/article1",
        "category": "technology"
    },
    {
        "id": "2",
        "title": "Global Climate Summit Reaches Historic Agreement",
        "description": "World leaders commit to ambitious new targets for carbon reduction",
        "content": "Representatives from 195 nations have signed a landmark agreement committing to net-zero emissions by 2040. The agreement includes specific milestones and funding mechanisms...",
        "author": "Sarah Johnson",
        "source": "World News Network",
        "publishedAt": "2024-01-15T08:45:00Z",
        "urlToImage": "https://picsum.photos/400/200?random=2",
        "url": "https://example.com/article2",
        "category": "general"
    },
    {
        "id": "3",
        "title": "Stock Markets Hit Record Highs Amid Economic Recovery",
        "description": "Major indices surge as investors show renewed confidence",
        "content": "The S&P 500 and NASDAQ both reached all-time highs today, driven by strong earnings reports and positive economic indicators. Analysts predict continued growth...",
        "author": "Michael Chen",
        "source": "Financial Times",
        "publishedAt": "2024-01-15T14:20:00Z",
        "urlToImage": "https://picsum.photos/400/200?random=3",
        "url": "https://example.com/article3",
        "category": "business"
    },
    {
        "id": "4",
        "title": "New Medical Treatment Shows Promise for Rare Disease",
        "description": "Clinical trials demonstrate 90% success rate in early testing",
        "content": "A revolutionary gene therapy treatment has shown remarkable results in treating a previously incurable genetic disorder. Patients in the trial showed significant improvement...",
        "author": "Dr. Emily Wilson",
        "source": "Medical Journal",
        "publishedAt": "2024-01-15T11:00:00Z",
        "urlToImage": "https://picsum.photos/400/200?random=4",
        "url": "https://example.com/article4",
        "category": "health"
    },
    {
        "id": "5",
        "title": "Championship Finals: Underdog Team Stuns Champions",
        "description": "Historic upset as rookie team claims victory in thrilling finale",
        "content": "In one of the greatest upsets in sports history, the underdog team defeated the three-time champions in a nail-biting finish. The game went into overtime...",
        "author": "Robert Martinez",
        "source": "Sports Weekly",
        "publishedAt": "2024-01-14T22:30:00Z",
        "urlToImage": "https://picsum.photos/400/200?random=5",
        "url": "https://example.com/article5",
        "category": "sports"
    },
    {
        "id": "6",
        "title": "Breakthrough in Artificial Intelligence Research",
        "description": "New AI model demonstrates human-level reasoning capabilities",
        "content": "Researchers have developed an AI system that can solve complex problems with unprecedented accuracy. The model uses a novel architecture that mimics human cognitive processes...",
        "author": "Alex Kumar",
        "source": "AI Research Lab",
        "publishedAt": "2024-01-15T09:15:00Z",
        "urlToImage": "https://picsum.photos/400/200?random=6",
        "url": "https://example.com/article6",
        "category": "science"
    },
    {
        "id": "7",
        "title": "Entertainment Industry Announces Major Merger",
        "description": "Two media giants join forces in billion-dollar deal",
        "content": "In a move that will reshape the entertainment landscape, two of the industry's biggest players have announced a merger valued at $50 billion. The combined company will...",
        "author": "Lisa Anderson",
        "source": "Entertainment Today",
        "publishedAt": "2024-01-15T13:45:00Z",
        "urlToImage": "https://picsum.photos/400/200?random=7",
        "url": "https://example.com/article7",
        "category": "entertainment"
    },
    {
        "id": "8",
        "title": "Space Mission Successfully Launches to Mars",
        "description": "Historic mission aims to establish first permanent base on Mars",
        "content": "The long-awaited Mars colonization mission successfully launched today, carrying supplies and equipment for establishing humanity's first permanent base on another planet...",
        "author": "Captain James Webb",
        "source": "Space News",
        "publishedAt": "2024-01-15T06:00:00Z",
        "urlToImage": "https://picsum.photos/400/200?random=8",
        "url": "https://example.com/article8",
        "category": "science"
    },
    {
        "id": "9",
        "title": "Local Community Rallies to Support Food Bank",
        "description": "Record donations help feed thousands of families in need",
        "content": "The community response has been overwhelming, with donations exceeding expectations by 300%. The food bank can now serve meals to over 10,000 families this month...",
        "author": "Maria Garcia",
        "source": "Local News",
        "publishedAt": "2024-01-15T16:30:00Z",
        "urlToImage": "https://picsum.photos/400/200?random=9",
        "url": "https://example.com/article9",
        "category": "general"
    },
    {
        "id": "10",
        "title": "Tech Giant Unveils Revolutionary Smartphone",
        "description": "Next-generation device features holographic display technology",
        "content": "The latest smartphone release features breakthrough holographic projection technology, allowing users to interact with 3D images in mid-air. Pre-orders have already exceeded...",
        "author": "David Park",
        "source": "Tech Review",
        "publishedAt": "2024-01-15T12:00:00Z",
        "urlToImage": "https://picsum.photos/400/200?random=10",
        "url": "https://example.com/article10",
        "category": "technology"
    }
]'''
    )
    
    # Create data source fields for news
    news_fields = [
        ("id", "string", "Article ID"),
        ("title", "string", "Headline"),
        ("description", "string", "Summary"),
        ("content", "string", "Full Article"),
        ("author", "string", "Author"),
        ("source", "string", "News Source"),
        ("publishedAt", "datetime", "Published Date"),
        ("urlToImage", "image_url", "Article Image"),
        ("url", "url", "Original URL"),
        ("category", "string", "Category")
    ]
    
    for field_name, field_type, display_name in news_fields:
        DataSourceField.objects.create(
            data_source=news_ds,
            field_name=field_name,
            field_type=field_type,
            display_name=display_name,
            is_required=field_name in ['id', 'title', 'publishedAt']
        )
    
    # Create categories data source
    categories_ds = DataSource.objects.create(
        application=app,
        name="News Categories",
        data_source_type="STATIC_JSON",
        static_data='''[
            {"id": "general", "name": "General", "icon": "public"},
            {"id": "business", "name": "Business", "icon": "business"},
            {"id": "entertainment", "name": "Entertainment", "icon": "movie"},
            {"id": "health", "name": "Health", "icon": "local_hospital"},
            {"id": "science", "name": "Science", "icon": "science"},
            {"id": "sports", "name": "Sports", "icon": "sports"},
            {"id": "technology", "name": "Technology", "icon": "computer"}
        ]'''
    )
    
    category_fields = [
        ("id", "string", "Category ID"),
        ("name", "string", "Category Name"),
        ("icon", "icon", "Category Icon")
    ]
    
    for field_name, field_type, display_name in category_fields:
        DataSourceField.objects.create(
            data_source=categories_ds,
            field_name=field_name,
            field_type=field_type,
            display_name=display_name,
            is_required=True
        )
    
    # Create sources data source with mock data
    sources_ds = DataSource.objects.create(
        application=app,
        name="News Sources",
        data_source_type="STATIC_JSON",
        static_data='''[
    {
        "id": "tech-daily",
        "name": "Tech Daily",
        "description": "Your source for the latest technology news and reviews",
        "url": "https://techdaily.example.com",
        "category": "technology",
        "language": "en",
        "country": "US"
    },
    {
        "id": "world-news-network",
        "name": "World News Network",
        "description": "Breaking news from around the globe",
        "url": "https://wnn.example.com",
        "category": "general",
        "language": "en",
        "country": "US"
    },
    {
        "id": "financial-times",
        "name": "Financial Times",
        "description": "Business and financial news",
        "url": "https://ft.example.com",
        "category": "business",
        "language": "en",
        "country": "UK"
    },
    {
        "id": "sports-weekly",
        "name": "Sports Weekly",
        "description": "Complete sports coverage and analysis",
        "url": "https://sportsweekly.example.com",
        "category": "sports",
        "language": "en",
        "country": "US"
    },
    {
        "id": "medical-journal",
        "name": "Medical Journal",
        "description": "Latest medical research and health news",
        "url": "https://medjournal.example.com",
        "category": "health",
        "language": "en",
        "country": "US"
    },
    {
        "id": "entertainment-today",
        "name": "Entertainment Today",
        "description": "Movies, music, and celebrity news",
        "url": "https://entertainment.example.com",
        "category": "entertainment",
        "language": "en",
        "country": "US"
    },
    {
        "id": "science-magazine",
        "name": "Science Magazine",
        "description": "Scientific discoveries and research",
        "url": "https://sciencemag.example.com",
        "category": "science",
        "language": "en",
        "country": "US"
    },
    {
        "id": "local-news",
        "name": "Local News",
        "description": "News from your community",
        "url": "https://localnews.example.com",
        "category": "general",
        "language": "en",
        "country": "US"
    }
]'''
    )
    
    source_fields = [
        ("id", "string", "Source ID"),
        ("name", "string", "Source Name"),
        ("description", "string", "Description"),
        ("url", "url", "Website URL"),
        ("category", "string", "Category"),
        ("language", "string", "Language"),
        ("country", "string", "Country")
    ]
    
    for field_name, field_type, display_name in source_fields:
        DataSourceField.objects.create(
            data_source=sources_ds,
            field_name=field_name,
            field_type=field_type,
            display_name=display_name,
            is_required=field_name in ['id', 'name']
        )
    
    # Create actions
    actions = [
        ("Read Article", "navigate", None, None),
        ("Share Article", "share_content", None, None),
        ("Bookmark Article", "save_data", None, None),
        ("Remove Bookmark", "save_data", None, None),
        ("Search News", "api_call", news_ds, None),
        ("Filter by Category", "api_call", news_ds, None),
        ("Filter by Source", "api_call", news_ds, None),
        ("Refresh News", "refresh_data", None, None),
        ("Open Original Article", "open_url", None, None),
        ("View Bookmarks", "navigate", None, None),
        ("View Sources", "navigate", None, None),
        ("Settings", "navigate", None, None),
    ]
    
    action_objects = {}
    for name, action_type, api_ds, target in actions:
        action = Action.objects.create(
            application=app,
            name=name,
            action_type=action_type,
            api_data_source=api_ds
        )
        action_objects[name] = action
    
    # Create screens
    screens_data = [
        ("Headlines", "/", True, "Breaking News", True, False),
        ("Categories", "/categories", False, "Categories", True, True),
        ("Category News", "/category-news", False, "Category News", True, True),
        ("Article Details", "/article", False, "Article", True, True),
        ("Search", "/search", False, "Search News", True, True),
        ("Search Results", "/search-results", False, "Search Results", True, True),
        ("Bookmarks", "/bookmarks", False, "Saved Articles", True, True),
        ("Sources", "/sources", False, "News Sources", True, True),
        ("Source Articles", "/source-articles", False, "Source Articles", True, True),
        ("Settings", "/settings", False, "Settings", True, True),
        ("About", "/about", False, "About", True, True),
    ]
    
    screen_objects = {}
    for name, route, is_home, title, show_bar, show_back in screens_data:
        screen = Screen.objects.create(
            application=app,
            name=name,
            route_name=route,
            is_home_screen=is_home,
            app_bar_title=title,
            show_app_bar=show_bar,
            show_back_button=show_back
        )
        screen_objects[name] = screen
    
    # Update actions with target screens
    action_objects["Read Article"].target_screen = screen_objects["Article Details"]
    action_objects["Read Article"].save()
    
    action_objects["View Bookmarks"].target_screen = screen_objects["Bookmarks"]
    action_objects["View Bookmarks"].save()
    
    action_objects["View Sources"].target_screen = screen_objects["Sources"]
    action_objects["View Sources"].save()
    
    action_objects["Settings"].target_screen = screen_objects["Settings"]
    action_objects["Settings"].save()
    
    # Create widgets for Headlines screen
    headlines_screen = screen_objects["Headlines"]
    
    # Main container
    main_container = Widget.objects.create(
        screen=headlines_screen,
        widget_type="Column",
        order=0,
        widget_id="headlines_main_column"
    )
    
    # Breaking news banner
    breaking_banner = Widget.objects.create(
        screen=headlines_screen,
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
    
    breaking_text = Widget.objects.create(
        screen=headlines_screen,
        widget_type="Text",
        parent_widget=breaking_banner,
        order=0,
        widget_id="breaking_news_text"
    )
    
    WidgetProperty.objects.create(
        widget=breaking_text,
        property_name="text",
        property_type="string",
        string_value="🔴 BREAKING NEWS"
    )
    
    WidgetProperty.objects.create(
        widget=breaking_text,
        property_name="color",
        property_type="color",
        color_value="#FFFFFF"
    )
    
    # Categories horizontal list
    categories_section = Widget.objects.create(
        screen=headlines_screen,
        widget_type="Container",
        parent_widget=main_container,
        order=1,
        widget_id="categories_section"
    )
    
    categories_title = Widget.objects.create(
        screen=headlines_screen,
        widget_type="Text",
        parent_widget=categories_section,
        order=0,
        widget_id="categories_title"
    )
    
    WidgetProperty.objects.create(
        widget=categories_title,
        property_name="text",
        property_type="string",
        string_value="Categories"
    )
    
    categories_list = Widget.objects.create(
        screen=headlines_screen,
        widget_type="ListView",
        parent_widget=categories_section,
        order=1,
        widget_id="categories_horizontal_list"
    )
    
    WidgetProperty.objects.create(
        widget=categories_list,
        property_name="dataSource",
        property_type="data_source_field_reference",
        data_source_field_reference=DataSourceField.objects.get(
            data_source=categories_ds,
            field_name="name"
        )
    )
    
    # Top headlines list
    headlines_list = Widget.objects.create(
        screen=headlines_screen,
        widget_type="ListView",
        parent_widget=main_container,
        order=2,
        widget_id="headlines_list"
    )
    
    WidgetProperty.objects.create(
        widget=headlines_list,
        property_name="dataSource",
        property_type="data_source_field_reference",
        data_source_field_reference=DataSourceField.objects.get(
            data_source=news_ds,
            field_name="title"
        )
    )
    
    # Bottom navigation buttons
    bottom_nav = Widget.objects.create(
        screen=headlines_screen,
        widget_type="Row",
        parent_widget=main_container,
        order=3,
        widget_id="bottom_navigation"
    )
    
    # Search button
    search_btn = Widget.objects.create(
        screen=headlines_screen,
        widget_type="IconButton",
        parent_widget=bottom_nav,
        order=0,
        widget_id="search_button"
    )
    
    WidgetProperty.objects.create(
        widget=search_btn,
        property_name="onPressed",
        property_type="screen_reference",
        screen_reference=screen_objects["Search"]
    )
    
    # Bookmarks button
    bookmarks_btn = Widget.objects.create(
        screen=headlines_screen,
        widget_type="IconButton",
        parent_widget=bottom_nav,
        order=1,
        widget_id="bookmarks_button"
    )
    
    WidgetProperty.objects.create(
        widget=bookmarks_btn,
        property_name="onPressed",
        property_type="action_reference",
        action_reference=action_objects["View Bookmarks"]
    )
    
    # Sources button
    sources_btn = Widget.objects.create(
        screen=headlines_screen,
        widget_type="IconButton",
        parent_widget=bottom_nav,
        order=2,
        widget_id="sources_button"
    )
    
    WidgetProperty.objects.create(
        widget=sources_btn,
        property_name="onPressed",
        property_type="action_reference",
        action_reference=action_objects["View Sources"]
    )
    
    # Create widgets for Article Details screen
    article_screen = screen_objects["Article Details"]
    
    article_column = Widget.objects.create(
        screen=article_screen,
        widget_type="Column",
        order=0,
        widget_id="article_main_column"
    )
    
    # Article image
    article_image = Widget.objects.create(
        screen=article_screen,
        widget_type="Image",
        parent_widget=article_column,
        order=0,
        widget_id="article_image"
    )
    
    # Article title
    article_title = Widget.objects.create(
        screen=article_screen,
        widget_type="Text",
        parent_widget=article_column,
        order=1,
        widget_id="article_title"
    )
    
    # Article metadata (author, date, source)
    article_meta = Widget.objects.create(
        screen=article_screen,
        widget_type="Row",
        parent_widget=article_column,
        order=2,
        widget_id="article_metadata"
    )
    
    # Author
    article_author = Widget.objects.create(
        screen=article_screen,
        widget_type="Text",
        parent_widget=article_meta,
        order=0,
        widget_id="article_author"
    )
    
    # Published date
    article_date = Widget.objects.create(
        screen=article_screen,
        widget_type="Text",
        parent_widget=article_meta,
        order=1,
        widget_id="article_date"
    )
    
    # Article content
    article_content = Widget.objects.create(
        screen=article_screen,
        widget_type="Text",
        parent_widget=article_column,
        order=3,
        widget_id="article_content"
    )
    
    # Action buttons
    article_actions = Widget.objects.create(
        screen=article_screen,
        widget_type="Row",
        parent_widget=article_column,
        order=4,
        widget_id="article_actions"
    )
    
    # Share button
    share_btn = Widget.objects.create(
        screen=article_screen,
        widget_type="IconButton",
        parent_widget=article_actions,
        order=0,
        widget_id="share_button"
    )
    
    WidgetProperty.objects.create(
        widget=share_btn,
        property_name="onPressed",
        property_type="action_reference",
        action_reference=action_objects["Share Article"]
    )
    
    # Bookmark button
    bookmark_btn = Widget.objects.create(
        screen=article_screen,
        widget_type="IconButton",
        parent_widget=article_actions,
        order=1,
        widget_id="bookmark_button"
    )
    
    WidgetProperty.objects.create(
        widget=bookmark_btn,
        property_name="onPressed",
        property_type="action_reference",
        action_reference=action_objects["Bookmark Article"]
    )
    
    # Open original button
    open_original_btn = Widget.objects.create(
        screen=article_screen,
        widget_type="ElevatedButton",
        parent_widget=article_actions,
        order=2,
        widget_id="open_original_button"
    )
    
    WidgetProperty.objects.create(
        widget=open_original_btn,
        property_name="text",
        property_type="string",
        string_value="Read Full Article"
    )
    
    WidgetProperty.objects.create(
        widget=open_original_btn,
        property_name="onPressed",
        property_type="action_reference",
        action_reference=action_objects["Open Original Article"]
    )
    
    return app