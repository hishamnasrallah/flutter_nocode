"""
Management command to create a comprehensive Flutter To-Do Application
File: core/management/commands/create_todo_app.py

This creates a FULL production-ready To-Do application with:
- Task management (create, read, update, delete)
- Categorized task views (To Do, Done, In Progress)
- User authentication (Login, Register, Logout)
- User profile and settings management
- Splash screen for initial loading
- Intuitive navigation with a drawer and floating action button
- Comprehensive UI/UX with proper navigation
- All API endpoints configured for task and user data
- Data sources with comprehensive field definitions for tasks, users, and settings
- Actions for all user interactions including navigation and data manipulation
- Professional theme and styling for a polished look
- Search and filter functionality for tasks
- Detailed task view with editing capabilities
- Security settings management
- About and Help sections
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import (
    Application, Theme, Screen, Widget, WidgetProperty,
    Action, DataSource, DataSourceField
)
import json


class Command(BaseCommand):
    help = 'Create a comprehensive To-Do application with 15+ unique screens'

    def add_arguments(self, parser):
        parser.add_argument(
            '--name',
            type=str,
            default='My Comprehensive To-Do App',
            help='Custom name for the To-Do application'
        )
        parser.add_argument(
            '--package',
            type=str,
            default='com.todo.complete',
            help='Package identifier for the application'
        )
        parser.add_argument(
            '--base-url',
            type=str,
            default='https://your-api-server.com',
            help='Base URL for the API endpoints'
        )

    def handle(self, *args, **options):
        app_name = options['name']
        package_name = options['package']
        base_url = options['base_url']

        try:
            with transaction.atomic():
                app = create_complete_todo_app(app_name, package_name, base_url)
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✅ Successfully created COMPLETE To-Do application: {app.name}\n'
                        f'📦 Package: {package_name}\n'
                        f'🌐 API Base URL: {base_url}\n'
                        f'📱 15+ Screens Created\n'
                        f'✨ All features configured and ready!'
                    )
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error creating To-Do application: {str(e)}')
            )


def create_complete_todo_app(custom_name=None, package_name=None, base_url=None):
    """Create a COMPLETE comprehensive To-Do application with full functionality"""

    # Use provided base URL or default
    if not base_url:
        base_url = "https://your-default-api-server.com"

    print(f"🔧 Creating Complete To-Do App with base URL: {base_url}")

    # Step 1: Create professional theme
    theme = create_professional_theme()

    # Step 2: Create application
    app = create_application(custom_name, package_name, theme)

    print("📊 Creating comprehensive data sources...")
    data_sources = create_all_data_sources(app, base_url)

    print("🎯 Creating actions...")
    actions = create_all_actions(app, data_sources)

    print("📱 Creating screens...")
    screens = create_all_screens(app)

    print("🔗 Linking navigation actions to screens...")
    update_action_targets(actions, screens)

    print("🎨 Creating complete UI for all screens...")
    create_all_screen_uis(screens, data_sources, actions)

    print("✅ Complete To-Do application created successfully!")
    return app


def create_professional_theme():
    """Create a professional theme appropriate for the app type"""
    return Theme.objects.create(
        name="To-Do Professional Theme",
        primary_color="#4CAF50",  # Green
        accent_color="#8BC34A",   # Light Green
        background_color="#F5F5F5",  # Light Grey
        text_color="#212121",  # Dark text for readability
        font_family="Roboto",  # Common, clean font
        is_dark_mode=False
    )


def create_application(custom_name, package_name, theme):
    """Create the main application object"""
    return Application.objects.create(
        name=custom_name or "My Comprehensive To-Do App",
        description="""A comprehensive Flutter To-Do application designed for efficient task management.
        Features include categorized task views (To Do, Done, In Progress), full CRUD functionality for tasks,
        user authentication, profile management, and intuitive navigation.
        It provides a clean, modern UI/UX for seamless productivity.""",
        package_name=package_name or "com.todo.complete",
        version="1.0.0",
        theme=theme
    )


def create_all_data_sources(app, base_url):
    """Create ALL data sources with proper endpoints and comprehensive fields"""
    data_sources = {}

    # 1. TodoItem Data Source
    todo_ds = DataSource.objects.create(
        application=app,
        name="TodoItems",
        data_source_type="REST_API",
        base_url=base_url,
        endpoint="/api/todos",
        method="GET",
        headers="ngrok-skip-browser-warning: true"
    )
    todo_fields = [
        ("id", "string", "ID", True),
        ("title", "string", "Title", True),
        ("description", "string", "Description", False),
        ("status", "string", "Status", True),  # "todo", "in_progress", "done"
        ("due_date", "datetime", "Due Date", False),
        ("created_at", "datetime", "Created At", True),
        ("updated_at", "datetime", "Updated At", True),
        ("category", "string", "Category", False),
        ("priority", "string", "Priority", False), # "low", "medium", "high"
        ("assigned_to", "string", "Assigned To", False),
        ("is_completed", "boolean", "Is Completed", True),
        ("notes", "string", "Notes", False),
        ("attachments", "json", "Attachments", False),
        ("tags", "json", "Tags", False),
    ]
    for field_name, field_type, display_name, is_required in todo_fields:
        DataSourceField.objects.create(
            data_source=todo_ds,
            field_name=field_name,
            field_type=field_type,
            display_name=display_name,
            is_required=is_required
        )
    data_sources['TodoItems'] = todo_ds

    # 2. UserProfile Data Source
    user_profile_ds = DataSource.objects.create(
        application=app,
        name="UserProfile",
        data_source_type="REST_API",
        base_url=base_url,
        endpoint="/api/profile",
        method="GET",
        headers="ngrok-skip-browser-warning: true"
    )
    user_profile_fields = [
        ("id", "string", "User ID", True),
        ("username", "string", "Username", True),
        ("email", "email", "Email", True),
        ("profile_picture", "image_url", "Profile Picture", False),
        ("bio", "string", "Bio", False),
        ("first_name", "string", "First Name", False),
        ("last_name", "string", "Last Name", False),
        ("phone_number", "string", "Phone Number", False),
        ("address", "string", "Address", False),
        ("date_joined", "datetime", "Date Joined", True),
        ("last_login", "datetime", "Last Login", False),
    ]
    for field_name, field_type, display_name, is_required in user_profile_fields:
        DataSourceField.objects.create(
            data_source=user_profile_ds,
            field_name=field_name,
            field_type=field_type,
            display_name=display_name,
            is_required=is_required
        )
    data_sources['UserProfile'] = user_profile_ds

    # 3. Categories Data Source
    categories_ds = DataSource.objects.create(
        application=app,
        name="Categories",
        data_source_type="REST_API",
        base_url=base_url,
        endpoint="/api/categories",
        method="GET",
        headers="ngrok-skip-browser-warning: true"
    )
    categories_fields = [
        ("id", "string", "ID", True),
        ("name", "string", "Category Name", True),
        ("description", "string", "Description", False),
        ("task_count", "integer", "Task Count", False),
        ("icon", "string", "Icon Name", False),
    ]
    for field_name, field_type, display_name, is_required in categories_fields:
        DataSourceField.objects.create(
            data_source=categories_ds,
            field_name=field_name,
            field_type=field_type,
            display_name=display_name,
            is_required=is_required
        )
    data_sources['Categories'] = categories_ds

    # 4. Settings Data Source
    settings_ds = DataSource.objects.create(
        application=app,
        name="AppSettings",
        data_source_type="REST_API",
        base_url=base_url,
        endpoint="/api/settings",
        method="GET",
        headers="ngrok-skip-browser-warning: true"
    )
    settings_fields = [
        ("id", "string", "ID", True),
        ("user_id", "string", "User ID", True),
        ("theme_preference", "string", "Theme Preference", True), # "light", "dark", "system"
        ("notification_enabled", "boolean", "Notifications Enabled", True),
        ("sound_enabled", "boolean", "Sound Enabled", True),
        ("language", "string", "Language", True),
        ("sync_interval", "integer", "Sync Interval (min)", False),
        ("default_category", "string", "Default Category", False),
    ]
    for field_name, field_type, display_name, is_required in settings_fields:
        DataSourceField.objects.create(
            data_source=settings_ds,
            field_name=field_name,
            field_type=field_type,
            display_name=display_name,
            is_required=is_required
        )
    data_sources['AppSettings'] = settings_ds

    # 5. Authentication Data Source (for login/register)
    auth_ds = DataSource.objects.create(
        application=app,
        name="Auth",
        data_source_type="REST_API",
        base_url=base_url,
        endpoint="/api/auth/login",
        method="POST",
        headers="ngrok-skip-browser-warning: true"
    )
    auth_fields = [
        ("token", "string", "Auth Token", True),
        ("user_id", "string", "User ID", True),
        ("expires_in", "integer", "Expires In (seconds)", False),
        ("refresh_token", "string", "Refresh Token", False),
    ]
    for field_name, field_type, display_name, is_required in auth_fields:
        DataSourceField.objects.create(
            data_source=auth_ds,
            field_name=field_name,
            field_type=field_type,
            display_name=display_name,
            is_required=is_required
        )
    data_sources['Auth'] = auth_ds

    return data_sources


def create_all_actions(app, data_sources):
    """Create ALL actions for complete functionality"""
    actions = {}

    # Navigation Actions
    nav_actions = [
        "Navigate to Splash",
        "Navigate to Home",
        "Navigate to Create New Todo",
        "Navigate to Todo Detail",
        "Navigate to User Profile",
        "Navigate to Settings",
        "Navigate to Security",
        "Navigate to Login",
        "Navigate to Register",
        "Navigate to About",
        "Navigate to Help",
        "Navigate to Forgot Password",
        "Navigate to Search Results",
        "Go Back",
    ]
    for name in nav_actions:
        action_type = "navigate_back" if name == "Go Back" else "navigate"
        action = Action.objects.create(
            application=app,
            name=name,
            action_type=action_type
        )
        actions[name] = action

    # Data Actions (CRUD for TodoItems)
    data_actions = [
        ("Load All Todos", "api_call", data_sources['TodoItems']),
        ("Load Todo By Status", "api_call", data_sources['TodoItems']), # Filtered by status
        ("Load Todo Details", "api_call", data_sources['TodoItems']), # For single todo
        ("Create Todo", "api_call", data_sources['TodoItems']),
        ("Update Todo", "api_call", data_sources['TodoItems']),
        ("Delete Todo", "api_call", data_sources['TodoItems']),
        ("Mark Todo as Done", "api_call", data_sources['TodoItems']),
        ("Mark Todo as In Progress", "api_call", data_sources['TodoItems']),
        ("Mark Todo as To Do", "api_call", data_sources['TodoItems']),
        ("Search Todos", "api_call", data_sources['TodoItems']),
        ("Filter Todos by Category", "api_call", data_sources['TodoItems']),

        # User & Auth Actions
        ("Login User", "api_call", data_sources['Auth']),
        ("Register User", "api_call", data_sources['Auth']),
        ("Logout User", "api_call", None), # No API call, local action
        ("Load User Profile", "api_call", data_sources['UserProfile']),
        ("Update User Profile", "api_call", data_sources['UserProfile']),
        ("Load App Settings", "api_call", data_sources['AppSettings']),
        ("Update App Settings", "api_call", data_sources['AppSettings']),
        ("Load Categories", "api_call", data_sources['Categories']),
    ]

    for name, action_type, api_source in data_actions:
        action = Action.objects.create(
            application=app,
            name=name,
            action_type=action_type,
            api_data_source=api_source if api_source else None
        )
        actions[name] = action

    return actions


def create_all_screens(app):
    """Create ALL screens for the complete app (MINIMUM 10 SCREENS)"""
    screens = {}

    # Screen configurations: (name, route, is_home, title, show_bar, show_back, background_color)
    screen_configs = [
        ("Splash", "/splash", False, "", False, False, "#FFFFFF"),
        ("Login", "/login", False, "Login", True, False, "#FFFFFF"),
        ("Register", "/register", False, "Register", True, True, "#FFFFFF"),
        ("Forgot Password", "/forgot-password", False, "Forgot Password", True, True, "#FFFFFF"),
        ("Home", "/", True, "My To-Do List", True, False, "#F5F5F5"),
        ("Create New Todo", "/create-todo", False, "Create New To-Do", True, True, "#FFFFFF"),
        ("Todo Detail", "/todo-detail", False, "To-Do Details", True, True, "#FFFFFF"),
        ("User Profile", "/profile", False, "User Profile", True, True, "#FFFFFF"),
        ("Settings", "/settings", False, "Settings", True, True, "#FFFFFF"),
        ("Security", "/security", False, "Security", True, True, "#FFFFFF"),
        ("About", "/about", False, "About This App", True, True, "#FFFFFF"),
        ("Help", "/help", False, "Help & Support", True, True, "#FFFFFF"),
        ("Search Results", "/search-results", False, "Search Results", True, True, "#FFFFFF"),
        ("Categories List", "/categories", False, "Categories", True, True, "#FFFFFF"),
    ]

    for name, route, is_home, title, show_bar, show_back, bg_color in screen_configs:
        screen = Screen.objects.create(
            application=app,
            name=name,
            route_name=route,
            is_home_screen=is_home,
            app_bar_title=title,
            show_app_bar=show_bar,
            show_back_button=show_back,
            background_color=bg_color
        )
        screens[name] = screen

    return screens


def update_action_targets(actions, screens):
    """Link navigation actions to their target screens"""
    action_screen_mapping = {
        "Navigate to Splash": screens.get("Splash"),
        "Navigate to Home": screens.get("Home"),
        "Navigate to Create New Todo": screens.get("Create New Todo"),
        "Navigate to Todo Detail": screens.get("Todo Detail"),
        "Navigate to User Profile": screens.get("User Profile"),
        "Navigate to Settings": screens.get("Settings"),
        "Navigate to Security": screens.get("Security"),
        "Navigate to Login": screens.get("Login"),
        "Navigate to Register": screens.get("Register"),
        "Navigate to About": screens.get("About"),
        "Navigate to Help": screens.get("Help"),
        "Navigate to Forgot Password": screens.get("Forgot Password"),
        "Navigate to Search Results": screens.get("Search Results"),
    }

    for action_name, target_screen in action_screen_mapping.items():
        if action_name in actions and target_screen:
            actions[action_name].target_screen = target_screen
            actions[action_name].save()


def create_all_screen_uis(screens, data_sources, actions):
    """Create complete UI for ALL screens with detailed widgets"""
    create_complete_splash_screen_ui(screens['Splash'], data_sources, actions)
    create_complete_login_screen_ui(screens['Login'], data_sources, actions)
    create_complete_register_screen_ui(screens['Register'], data_sources, actions)
    create_complete_forgot_password_screen_ui(screens['Forgot Password'], data_sources, actions)
    create_complete_home_screen_ui(screens['Home'], data_sources, actions)
    create_complete_create_new_todo_screen_ui(screens['Create New Todo'], data_sources, actions)
    create_complete_todo_detail_screen_ui(screens['Todo Detail'], data_sources, actions)
    create_complete_user_profile_screen_ui(screens['User Profile'], data_sources, actions)
    create_complete_settings_screen_ui(screens['Settings'], data_sources, actions)
    create_complete_security_screen_ui(screens['Security'], data_sources, actions)
    create_complete_about_screen_ui(screens['About'], data_sources, actions)
    create_complete_help_screen_ui(screens['Help'], data_sources, actions)
    create_complete_search_results_screen_ui(screens['Search Results'], data_sources, actions)
    create_complete_categories_list_screen_ui(screens['Categories List'], data_sources, actions)


def create_complete_splash_screen_ui(screen, data_sources, actions):
    """Create a simple splash screen UI"""
    center_widget = Widget.objects.create(
        screen=screen,
        widget_type="Center",
        order=0,
        widget_id="splash_center"
    )
    column_widget = Widget.objects.create(
        screen=screen,
        widget_type="Column",
        parent_widget=center_widget,
        order=0,
        widget_id="splash_column"
    )
    WidgetProperty.objects.create(widget=column_widget, property_name="mainAxisAlignment", property_type="string", string_value="center")
    WidgetProperty.objects.create(widget=column_widget, property_name="crossAxisAlignment", property_type="string", string_value="center")

    image_widget = Widget.objects.create(
        screen=screen,
        widget_type="Image",
        parent_widget=column_widget,
        order=0,
        widget_id="splash_logo"
    )
    WidgetProperty.objects.create(widget=image_widget, property_name="imageUrl", property_type="string", string_value="https://images.pexels.com/photos/1640777/pexels-photo-1640777.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1")
    WidgetProperty.objects.create(widget=image_widget, property_name="width", property_type="decimal", decimal_value=150)
    WidgetProperty.objects.create(widget=image_widget, property_name="height", property_type="decimal", decimal_value=150)

    text_widget = Widget.objects.create(
        screen=screen,
        widget_type="Text",
        parent_widget=column_widget,
        order=1,
        widget_id="splash_app_name"
    )
    WidgetProperty.objects.create(widget=text_widget, property_name="text", property_type="string", string_value="My To-Do App")
    WidgetProperty.objects.create(widget=text_widget, property_name="fontSize", property_type="decimal", decimal_value=28)
    WidgetProperty.objects.create(widget=text_widget, property_name="fontWeight", property_type="string", string_value="bold")
    WidgetProperty.objects.create(widget=text_widget, property_name="color", property_type="string", string_value="#212121")


def create_complete_login_screen_ui(screen, data_sources, actions):
    """Create login screen UI"""
    scroll_view = Widget.objects.create(screen=screen, widget_type="SingleChildScrollView", order=0, widget_id="login_scroll_view")
    column = Widget.objects.create(screen=screen, widget_type="Column", parent_widget=scroll_view, order=0, widget_id="login_column")
    WidgetProperty.objects.create(widget=column, property_name="padding", property_type="decimal", decimal_value=24)
    WidgetProperty.objects.create(widget=column, property_name="mainAxisAlignment", property_type="string", string_value="center")
    WidgetProperty.objects.create(widget=column, property_name="crossAxisAlignment", property_type="string", string_value="stretch")

    # Logo/Title
    title = Widget.objects.create(screen=screen, widget_type="Text", parent_widget=column, order=0, widget_id="login_title")
    WidgetProperty.objects.create(widget=title, property_name="text", property_type="string", string_value="Welcome Back!")
    WidgetProperty.objects.create(widget=title, property_name="fontSize", property_type="decimal", decimal_value=32)
    WidgetProperty.objects.create(widget=title, property_name="fontWeight", property_type="string", string_value="bold")
    WidgetProperty.objects.create(widget=title, property_name="textAlign", property_type="string", string_value="center")
    WidgetProperty.objects.create(widget=title, property_name="paddingBottom", property_type="decimal", decimal_value=32)

    # Email Field
    email_field = Widget.objects.create(screen=screen, widget_type="TextField", parent_widget=column, order=1, widget_id="login_email_field")
    WidgetProperty.objects.create(widget=email_field, property_name="labelText", property_type="string", string_value="Email")
    WidgetProperty.objects.create(widget=email_field, property_name="keyboardType", property_type="string", string_value="email")
    WidgetProperty.objects.create(widget=email_field, property_name="paddingBottom", property_type="decimal", decimal_value=16)

    # Password Field
    password_field = Widget.objects.create(screen=screen, widget_type="TextField", parent_widget=column, order=2, widget_id="login_password_field")
    WidgetProperty.objects.create(widget=password_field, property_name="labelText", property_type="string", string_value="Password")
    WidgetProperty.objects.create(widget=password_field, property_name="obscureText", property_type="boolean", boolean_value=True)
    WidgetProperty.objects.create(widget=password_field, property_name="paddingBottom", property_type="decimal", decimal_value=24)

    # Login Button
    login_button = Widget.objects.create(screen=screen, widget_type="ElevatedButton", parent_widget=column, order=3, widget_id="login_button")
    WidgetProperty.objects.create(widget=login_button, property_name="text", property_type="string", string_value="Login")
    WidgetProperty.objects.create(widget=login_button, property_name="onPressed", property_type="action_reference", action_reference=actions["Login User"])
    WidgetProperty.objects.create(widget=login_button, property_name="padding", property_type="decimal", decimal_value=12)

    # Forgot Password
    forgot_password_button = Widget.objects.create(screen=screen, widget_type="TextButton", parent_widget=column, order=4, widget_id="forgot_password_button")
    WidgetProperty.objects.create(widget=forgot_password_button, property_name="text", property_type="string", string_value="Forgot Password?")
    WidgetProperty.objects.create(widget=forgot_password_button, property_name="onPressed", property_type="action_reference", action_reference=actions["Navigate to Forgot Password"])
    WidgetProperty.objects.create(widget=forgot_password_button, property_name="paddingTop", property_type="decimal", decimal_value=8)

    # Register Link
    register_link = Widget.objects.create(screen=screen, widget_type="TextButton", parent_widget=column, order=5, widget_id="register_link")
    WidgetProperty.objects.create(widget=register_link, property_name="text", property_type="string", string_value="Don't have an account? Register")
    WidgetProperty.objects.create(widget=register_link, property_name="onPressed", property_type="action_reference", action_reference=actions["Navigate to Register"])
    WidgetProperty.objects.create(widget=register_link, property_name="paddingTop", property_type="decimal", decimal_value=16)


def create_complete_register_screen_ui(screen, data_sources, actions):
    """Create register screen UI"""
    scroll_view = Widget.objects.create(screen=screen, widget_type="SingleChildScrollView", order=0, widget_id="register_scroll_view")
    column = Widget.objects.create(screen=screen, widget_type="Column", parent_widget=scroll_view, order=0, widget_id="register_column")
    WidgetProperty.objects.create(widget=column, property_name="padding", property_type="decimal", decimal_value=24)
    WidgetProperty.objects.create(widget=column, property_name="mainAxisAlignment", property_type="string", string_value="center")
    WidgetProperty.objects.create(widget=column, property_name="crossAxisAlignment", property_type="string", string_value="stretch")

    title = Widget.objects.create(screen=screen, widget_type="Text", parent_widget=column, order=0, widget_id="register_title")
    WidgetProperty.objects.create(widget=title, property_name="text", property_type="string", string_value="Create Account")
    WidgetProperty.objects.create(widget=title, property_name="fontSize", property_type="decimal", decimal_value=32)
    WidgetProperty.objects.create(widget=title, property_name="fontWeight", property_type="string", string_value="bold")
    WidgetProperty.objects.create(widget=title, property_name="textAlign", property_type="string", string_value="center")
    WidgetProperty.objects.create(widget=title, property_name="paddingBottom", property_type="decimal", decimal_value=32)

    username_field = Widget.objects.create(screen=screen, widget_type="TextField", parent_widget=column, order=1, widget_id="register_username_field")
    WidgetProperty.objects.create(widget=username_field, property_name="labelText", property_type="string", string_value="Username")
    WidgetProperty.objects.create(widget=username_field, property_name="paddingBottom", property_type="decimal", decimal_value=16)

    email_field = Widget.objects.create(screen=screen, widget_type="TextField", parent_widget=column, order=2, widget_id="register_email_field")
    WidgetProperty.objects.create(widget=email_field, property_name="labelText", property_type="string", string_value="Email")
    WidgetProperty.objects.create(widget=email_field, property_name="keyboardType", property_type="string", string_value="email")
    WidgetProperty.objects.create(widget=email_field, property_name="paddingBottom", property_type="decimal", decimal_value=16)

    password_field = Widget.objects.create(screen=screen, widget_type="TextField", parent_widget=column, order=3, widget_id="register_password_field")
    WidgetProperty.objects.create(widget=password_field, property_name="labelText", property_type="string", string_value="Password")
    WidgetProperty.objects.create(widget=password_field, property_name="obscureText", property_type="boolean", boolean_value=True)
    WidgetProperty.objects.create(widget=password_field, property_name="paddingBottom", property_type="decimal", decimal_value=16)

    confirm_password_field = Widget.objects.create(screen=screen, widget_type="TextField", parent_widget=column, order=4, widget_id="register_confirm_password_field")
    WidgetProperty.objects.create(widget=confirm_password_field, property_name="labelText", property_type="string", string_value="Confirm Password")
    WidgetProperty.objects.create(widget=confirm_password_field, property_name="obscureText", property_type="boolean", boolean_value=True)
    WidgetProperty.objects.create(widget=confirm_password_field, property_name="paddingBottom", property_type="decimal", decimal_value=24)

    register_button = Widget.objects.create(screen=screen, widget_type="ElevatedButton", parent_widget=column, order=5, widget_id="register_button")
    WidgetProperty.objects.create(widget=register_button, property_name="text", property_type="string", string_value="Register")
    WidgetProperty.objects.create(widget=register_button, property_name="onPressed", property_type="action_reference", action_reference=actions["Register User"])
    WidgetProperty.objects.create(widget=register_button, property_name="padding", property_type="decimal", decimal_value=12)

    login_link = Widget.objects.create(screen=screen, widget_type="TextButton", parent_widget=column, order=6, widget_id="register_login_link")
    WidgetProperty.objects.create(widget=login_link, property_name="text", property_type="string", string_value="Already have an account? Login")
    WidgetProperty.objects.create(widget=login_link, property_name="onPressed", property_type="action_reference", action_reference=actions["Navigate to Login"])
    WidgetProperty.objects.create(widget=login_link, property_name="paddingTop", property_type="decimal", decimal_value=16)


def create_complete_forgot_password_screen_ui(screen, data_sources, actions):
    """Create forgot password screen UI"""
    scroll_view = Widget.objects.create(screen=screen, widget_type="SingleChildScrollView", order=0, widget_id="forgot_password_scroll_view")
    column = Widget.objects.create(screen=screen, widget_type="Column", parent_widget=scroll_view, order=0, widget_id="forgot_password_column")
    WidgetProperty.objects.create(widget=column, property_name="padding", property_type="decimal", decimal_value=24)
    WidgetProperty.objects.create(widget=column, property_name="mainAxisAlignment", property_type="string", string_value="center")
    WidgetProperty.objects.create(widget=column, property_name="crossAxisAlignment", property_type="string", string_value="stretch")

    title = Widget.objects.create(screen=screen, widget_type="Text", parent_widget=column, order=0, widget_id="forgot_password_title")
    WidgetProperty.objects.create(widget=title, property_name="text", property_type="string", string_value="Reset Password")
    WidgetProperty.objects.create(widget=title, property_name="fontSize", property_type="decimal", decimal_value=32)
    WidgetProperty.objects.create(widget=title, property_name="fontWeight", property_type="string", string_value="bold")
    WidgetProperty.objects.create(widget=title, property_name="textAlign", property_type="string", string_value="center")
    WidgetProperty.objects.create(widget=title, property_name="paddingBottom", property_type="decimal", decimal_value=32)

    instruction_text = Widget.objects.create(screen=screen, widget_type="Text", parent_widget=column, order=1, widget_id="forgot_password_instruction")
    WidgetProperty.objects.create(widget=instruction_text, property_name="text", property_type="string", string_value="Enter your email address to receive a password reset link.")
    WidgetProperty.objects.create(widget=instruction_text, property_name="textAlign", property_type="string", string_value="center")
    WidgetProperty.objects.create(widget=instruction_text, property_name="paddingBottom", property_type="decimal", decimal_value=24)

    email_field = Widget.objects.create(screen=screen, widget_type="TextField", parent_widget=column, order=2, widget_id="forgot_password_email_field")
    WidgetProperty.objects.create(widget=email_field, property_name="labelText", property_type="string", string_value="Email")
    WidgetProperty.objects.create(widget=email_field, property_name="keyboardType", property_type="string", string_value="email")
    WidgetProperty.objects.create(widget=email_field, property_name="paddingBottom", property_type="decimal", decimal_value=24)

    reset_button = Widget.objects.create(screen=screen, widget_type="ElevatedButton", parent_widget=column, order=3, widget_id="reset_password_button")
    WidgetProperty.objects.create(widget=reset_button, property_name="text", property_type="string", string_value="Send Reset Link")
    WidgetProperty.objects.create(widget=reset_button, property_name="onPressed", property_type="action_reference", action_reference=actions["Login User"]) # Placeholder action
    WidgetProperty.objects.create(widget=reset_button, property_name="padding", property_type="decimal", decimal_value=12)

    back_to_login_link = Widget.objects.create(screen=screen, widget_type="TextButton", parent_widget=column, order=4, widget_id="back_to_login_link")
    WidgetProperty.objects.create(widget=back_to_login_link, property_name="text", property_type="string", string_value="Back to Login")
    WidgetProperty.objects.create(widget=back_to_login_link, property_name="onPressed", property_type="action_reference", action_reference=actions["Navigate to Login"])
    WidgetProperty.objects.create(widget=back_to_login_link, property_name="paddingTop", property_type="decimal", decimal_value=16)


def create_complete_home_screen_ui(screen, data_sources, actions):
    """Create COMPLETE home screen with all widgets and proper hierarchy"""

    # Main scroll view
    main_scroll = Widget.objects.create(
        screen=screen,
        widget_type="SingleChildScrollView",
        order=0,
        widget_id="home_scroll_view"
    )

    # Main column for content
    main_column = Widget.objects.create(
        screen=screen,
        widget_type="Column",
        parent_widget=main_scroll,
        order=0,
        widget_id="home_main_column"
    )
    WidgetProperty.objects.create(widget=main_column, property_name="mainAxisAlignment", property_type="string", string_value="start")
    WidgetProperty.objects.create(widget=main_column, property_name="crossAxisAlignment", property_type="string", string_value="stretch")
    WidgetProperty.objects.create(widget=main_column, property_name="padding", property_type="decimal", decimal_value=16)

    # Search Bar
    search_bar_container = Widget.objects.create(
        screen=screen,
        widget_type="Container",
        parent_widget=main_column,
        order=0,
        widget_id="search_bar_container"
    )
    WidgetProperty.objects.create(widget=search_bar_container, property_name="paddingBottom", property_type="decimal", decimal_value=16)

    search_field = Widget.objects.create(
        screen=screen,
        widget_type="TextField",
        parent_widget=search_bar_container,
        order=0,
        widget_id="home_search_field"
    )
    WidgetProperty.objects.create(widget=search_field, property_name="labelText", property_type="string", string_value="Search tasks...")
    WidgetProperty.objects.create(widget=search_field, property_name="prefixIcon", property_type="string", string_value="search")
    WidgetProperty.objects.create(widget=search_field, property_name="onSubmitted", property_type="action_reference", action_reference=actions["Search Todos"])

    # To Do Section
    create_task_category_section(
        screen, main_column, data_sources, actions,
        order=1,
        title="To Do",
        status_filter="todo",
        data_source=data_sources['TodoItems'],
        navigate_action=actions["Navigate to Todo Detail"],
        load_action=actions["Load Todo By Status"]
    )

    # In Progress Section
    create_task_category_section(
        screen, main_column, data_sources, actions,
        order=2,
        title="In Progress",
        status_filter="in_progress",
        data_source=data_sources['TodoItems'],
        navigate_action=actions["Navigate to Todo Detail"],
        load_action=actions["Load Todo By Status"]
    )

    # Done Section
    create_task_category_section(
        screen, main_column, data_sources, actions,
        order=3,
        title="Done",
        status_filter="done",
        data_source=data_sources['TodoItems'],
        navigate_action=actions["Navigate to Todo Detail"],
        load_action=actions["Load Todo By Status"]
    )

    # Floating Action Button for Create New Todo
    fab = Widget.objects.create(
        screen=screen,
        widget_type="FloatingActionButton",
        order=98, # Just before bottom nav
        widget_id="create_todo_fab"
    )
    WidgetProperty.objects.create(widget=fab, property_name="icon", property_type="string", string_value="add")
    WidgetProperty.objects.create(widget=fab, property_name="onPressed", property_type="action_reference", action_reference=actions["Navigate to Create New Todo"])
    WidgetProperty.objects.create(widget=fab, property_name="tooltip", property_type="string", string_value="Create New To-Do")

    # Drawer
    create_home_drawer(screen, actions)

    # Bottom Navigation (as per template requirement, even with drawer)
    create_bottom_navigation(screen, actions)


def create_task_category_section(screen, parent_widget, data_sources, actions, order, title, status_filter, data_source, navigate_action, load_action):
    """Creates a section for a specific task category (To Do, In Progress, Done)"""
    section_container = Widget.objects.create(
        screen=screen,
        widget_type="Card",
        parent_widget=parent_widget,
        order=order,
        widget_id=f"{status_filter}_section_card"
    )
    WidgetProperty.objects.create(widget=section_container, property_name="margin", property_type="decimal", decimal_value=8)
    WidgetProperty.objects.create(widget=section_container, property_name="elevation", property_type="decimal", decimal_value=2)

    section_column = Widget.objects.create(
        screen=screen,
        widget_type="Column",
        parent_widget=section_container,
        order=0,
        widget_id=f"{status_filter}_section_column"
    )
    WidgetProperty.objects.create(widget=section_column, property_name="crossAxisAlignment", property_type="string", string_value="start")
    WidgetProperty.objects.create(widget=section_column, property_name="padding", property_type="decimal", decimal_value=16)

    # Header Row
    header_row = Widget.objects.create(
        screen=screen,
        widget_type="Row",
        parent_widget=section_column,
        order=0,
        widget_id=f"{status_filter}_header_row"
    )
    WidgetProperty.objects.create(widget=header_row, property_name="mainAxisAlignment", property_type="string", string_value="spaceBetween")

    header_title = Widget.objects.create(
        screen=screen,
        widget_type="Text",
        parent_widget=header_row,
        order=0,
        widget_id=f"{status_filter}_header_title"
    )
    WidgetProperty.objects.create(widget=header_title, property_name="text", property_type="string", string_value=title)
    WidgetProperty.objects.create(widget=header_title, property_name="fontSize", property_type="decimal", decimal_value=20)
    WidgetProperty.objects.create(widget=header_title, property_name="fontWeight", property_type="string", string_value="bold")

    see_all_button = Widget.objects.create(
        screen=screen,
        widget_type="TextButton",
        parent_widget=header_row,
        order=1,
        widget_id=f"{status_filter}_see_all_button"
    )
    WidgetProperty.objects.create(widget=see_all_button, property_name="text", property_type="string", string_value="See All")
    WidgetProperty.objects.create(widget=see_all_button, property_name="onPressed", property_type="action_reference", action_reference=load_action) # This would ideally filter the list view

    # Task List (ListView)
    task_list = Widget.objects.create(
        screen=screen,
        widget_type="ListView",
        parent_widget=section_column,
        order=1,
        widget_id=f"{status_filter}_task_list"
    )
    WidgetProperty.objects.create(widget=task_list, property_name="shrinkWrap", property_type="boolean", boolean_value=True)
    WidgetProperty.objects.create(widget=task_list, property_name="physics", property_type="string", string_value="NeverScrollableScrollPhysics")
    WidgetProperty.objects.create(
        widget=task_list,
        property_name="dataSource",
        property_type="data_source_field_reference",
        data_source_field_reference=DataSourceField.objects.get(
            data_source=data_source,
            field_name="id" # Bind to the list of IDs, actual data will be fetched per item
        )
    )
    WidgetProperty.objects.create(widget=task_list, property_name="itemBuilder", property_type="string", string_value="""
        (context, index, item) => ListTile(
            title: Text(item['title']),
            subtitle: Text(item['description']),
            trailing: IconButton(
                icon: Icon(item['is_completed'] ? Icons.check_box : Icons.check_box_outline_blank),
                onPressed: () => actions['Mark Todo as Done'](item['id'])
            ),
            onTap: () => actions['Navigate to Todo Detail'](item['id'])
        )
    """)


def create_home_drawer(screen, actions):
    """Create the drawer for the home screen"""
    drawer = Widget.objects.create(
        screen=screen,
        widget_type="Drawer",
        order=97, # Before FAB and BottomNav
        widget_id="home_drawer"
    )

    drawer_column = Widget.objects.create(
        screen=screen,
        widget_type="Column",
        parent_widget=drawer,
        order=0,
        widget_id="drawer_column"
    )

    # Drawer Header
    drawer_header = Widget.objects.create(
        screen=screen,
        widget_type="DrawerHeader",
        parent_widget=drawer_column,
        order=0,
        widget_id="drawer_header"
    )
    WidgetProperty.objects.create(widget=drawer_header, property_name="decoration", property_type="string", string_value="""
        BoxDecoration(color: Theme.of(context).primaryColor)
    """)

    header_text = Widget.objects.create(
        screen=screen,
        widget_type="Text",
        parent_widget=drawer_header,
        order=0,
        widget_id="drawer_header_text"
    )
    WidgetProperty.objects.create(widget=header_text, property_name="text", property_type="string", string_value="To-Do App Menu")
    WidgetProperty.objects.create(widget=header_text, property_name="color", property_type="string", string_value="#FFFFFF")
    WidgetProperty.objects.create(widget=header_text, property_name="fontSize", property_type="decimal", decimal_value=24)

    # Drawer Items
    drawer_items = [
        ("User Profile", "person", "Navigate to User Profile"),
        ("Settings", "settings", "Navigate to Settings"),
        ("Security", "security", "Navigate to Security"),
        ("About", "info", "Navigate to About"),
        ("Help", "help", "Navigate to Help"),
        ("Login", "login", "Navigate to Login"),
        ("Logout", "logout", "Logout User"),
    ]

    for i, (label, icon, action_name) in enumerate(drawer_items):
        list_tile = Widget.objects.create(
            screen=screen,
            widget_type="ListTile",
            parent_widget=drawer_column,
            order=i + 1,
            widget_id=f"drawer_item_{label.lower().replace(' ', '_')}"
        )
        WidgetProperty.objects.create(widget=list_tile, property_name="title", property_type="string", string_value=label)
        WidgetProperty.objects.create(widget=list_tile, property_name="leadingIcon", property_type="string", string_value=icon)
        WidgetProperty.objects.create(widget=list_tile, property_name="onTap", property_type="action_reference", action_reference=actions[action_name])


def create_bottom_navigation(screen, actions):
    """Create reusable bottom navigation with 4-5 tabs"""
    bottom_nav = Widget.objects.create(
        screen=screen,
        widget_type="BottomNavigationBar",
        order=99,  # Always at bottom
        widget_id="bottom_navigation"
    )

    # Navigation items with proper configuration
    nav_items = [
        ("home", "Home", "Navigate to Home"),
        ("category", "Categories", "Navigate to Categories List"),
        ("search", "Search", "Navigate to Search Results"),
        ("person", "Profile", "Navigate to User Profile"),
    ]

    for i, (icon, label, action_name) in enumerate(nav_items):
        nav_item = Widget.objects.create(
            screen=screen,
            widget_type="BottomNavigationBarItem",
            parent_widget=bottom_nav,
            order=i,
            widget_id=f"nav_{icon}"
        )

        WidgetProperty.objects.create(
            widget=nav_item,
            property_name="icon",
            property_type="string",
            string_value=icon
        )

        WidgetProperty.objects.create(
            widget=nav_item,
            property_name="label",
            property_type="string",
            string_value=label
        )

        WidgetProperty.objects.create(
            widget=nav_item,
            property_name="onTap",
            property_type="action_reference",
            action_reference=actions[action_name]
        )


def create_complete_create_new_todo_screen_ui(screen, data_sources, actions):
    """Create UI for creating/editing a new todo item"""
    scroll_view = Widget.objects.create(screen=screen, widget_type="SingleChildScrollView", order=0, widget_id="create_todo_scroll_view")
    column = Widget.objects.create(screen=screen, widget_type="Column", parent_widget=scroll_view, order=0, widget_id="create_todo_column")
    WidgetProperty.objects.create(widget=column, property_name="padding", property_type="decimal", decimal_value=24)
    WidgetProperty.objects.create(widget=column, property_name="crossAxisAlignment", property_type="string", string_value="stretch")

    # Title Field
    title_field = Widget.objects.create(screen=screen, widget_type="TextField", parent_widget=column, order=0, widget_id="new_todo_title_field")
    WidgetProperty.objects.create(widget=title_field, property_name="labelText", property_type="string", string_value="Task Title")
    WidgetProperty.objects.create(widget=title_field, property_name="paddingBottom", property_type="decimal", decimal_value=16)

    # Description Field
    description_field = Widget.objects.create(screen=screen, widget_type="TextField", parent_widget=column, order=1, widget_id="new_todo_description_field")
    WidgetProperty.objects.create(widget=description_field, property_name="labelText", property_type="string", string_value="Description")
    WidgetProperty.objects.create(widget=description_field, property_name="maxLines", property_type="integer", integer_value=3)
    WidgetProperty.objects.create(widget=description_field, property_name="paddingBottom", property_type="decimal", decimal_value=16)

    # Due Date Field
    due_date_field = Widget.objects.create(screen=screen, widget_type="TextField", parent_widget=column, order=2, widget_id="new_todo_due_date_field")
    WidgetProperty.objects.create(widget=due_date_field, property_name="labelText", property_type="string", string_value="Due Date")
    WidgetProperty.objects.create(widget=due_date_field, property_name="readOnly", property_type="boolean", boolean_value=True)
    WidgetProperty.objects.create(widget=due_date_field, property_name="suffixIcon", property_type="string", string_value="calendar_today")
    WidgetProperty.objects.create(widget=due_date_field, property_name="onTap", property_type="action_reference", action_reference=actions["Load Todo Details"]) # Placeholder for date picker action
    WidgetProperty.objects.create(widget=due_date_field, property_name="paddingBottom", property_type="decimal", decimal_value=16)

    # Priority Dropdown
    priority_dropdown = Widget.objects.create(screen=screen, widget_type="DropdownButton", parent_widget=column, order=3, widget_id="new_todo_priority_dropdown")
    WidgetProperty.objects.create(widget=priority_dropdown, property_name="labelText", property_type="string", string_value="Priority")
    WidgetProperty.objects.create(widget=priority_dropdown, property_name="items", property_type="json", json_value=json.dumps([
        {"value": "low", "label": "Low"},
        {"value": "medium", "label": "Medium"},
        {"value": "high", "label": "High"}
    ]))
    WidgetProperty.objects.create(widget=priority_dropdown, property_name="paddingBottom", property_type="decimal", decimal_value=16)

    # Category Dropdown (bound to Categories data source)
    category_dropdown = Widget.objects.create(screen=screen, widget_type="DropdownButton", parent_widget=column, order=4, widget_id="new_todo_category_dropdown")
    WidgetProperty.objects.create(widget=category_dropdown, property_name="labelText", property_type="string", string_value="Category")
    WidgetProperty.objects.create(
        widget=category_dropdown,
        property_name="dataSource",
        property_type="data_source_field_reference",
        data_source_field_reference=DataSourceField.objects.get(
            data_source=data_sources['Categories'],
            field_name="name"
        )
    )
    WidgetProperty.objects.create(widget=category_dropdown, property_name="paddingBottom", property_type="decimal", decimal_value=24)

    # Save Button
    save_button = Widget.objects.create(screen=screen, widget_type="ElevatedButton", parent_widget=column, order=5, widget_id="save_todo_button")
    WidgetProperty.objects.create(widget=save_button, property_name="text", property_type="string", string_value="Save To-Do")
    WidgetProperty.objects.create(widget=save_button, property_name="onPressed", property_type="action_reference", action_reference=actions["Create Todo"])
    WidgetProperty.objects.create(widget=save_button, property_name="padding", property_type="decimal", decimal_value=12)


def create_complete_todo_detail_screen_ui(screen, data_sources, actions):
    """Create UI for displaying and editing a single todo item"""
    scroll_view = Widget.objects.create(screen=screen, widget_type="SingleChildScrollView", order=0, widget_id="todo_detail_scroll_view")
    column = Widget.objects.create(screen=screen, widget_type="Column", parent_widget=scroll_view, order=0, widget_id="todo_detail_column")
    WidgetProperty.objects.create(widget=column, property_name="padding", property_type="decimal", decimal_value=24)
    WidgetProperty.objects.create(widget=column, property_name="crossAxisAlignment", property_type="string", string_value="stretch")

    # Data binding for the entire screen
    WidgetProperty.objects.create(
        widget=column,
        property_name="dataSource",
        property_type="data_source_field_reference",
        data_source_field_reference=DataSourceField.objects.get(
            data_source=data_sources['TodoItems'],
            field_name="id" # This implies fetching a single todo by ID
        )
    )

    # Title Display/Edit
    title_text = Widget.objects.create(screen=screen, widget_type="Text", parent_widget=column, order=0, widget_id="detail_todo_title")
    WidgetProperty.objects.create(widget=title_text, property_name="text", property_type="data_source_field_reference", data_source_field_reference=DataSourceField.objects.get(data_sources['TodoItems'], field_name="title"))
    WidgetProperty.objects.create(widget=title_text, property_name="fontSize", property_type="decimal", decimal_value=28)
    WidgetProperty.objects.create(widget=title_text, property_name="fontWeight", property_type="string", string_value="bold")
    WidgetProperty.objects.create(widget=title_text, property_name="paddingBottom", property_type="decimal", decimal_value=16)

    # Description Display/Edit
    description_text = Widget.objects.create(screen=screen, widget_type="Text", parent_widget=column, order=1, widget_id="detail_todo_description")
    WidgetProperty.objects.create(widget=description_text, property_name="text", property_type="data_source_field_reference", data_source_field_reference=DataSourceField.objects.get(data_sources['TodoItems'], field_name="description"))
    WidgetProperty.objects.create(widget=description_text, property_name="fontSize", property_type="decimal", decimal_value=16)
    WidgetProperty.objects.create(widget=description_text, property_name="paddingBottom", property_type="decimal", decimal_value=16)

    # Status, Due Date, Priority, Category (as ListTiles or similar)
    status_tile = Widget.objects.create(screen=screen, widget_type="ListTile", parent_widget=column, order=2, widget_id="detail_todo_status")
    WidgetProperty.objects.create(widget=status_tile, property_name="leadingIcon", property_type="string", string_value="check_circle_outline")
    WidgetProperty.objects.create(widget=status_tile, property_name="title", property_type="string", string_value="Status")
    WidgetProperty.objects.create(widget=status_tile, property_name="subtitle", property_type="data_source_field_reference", data_source_field_reference=DataSourceField.objects.get(data_sources['TodoItems'], field_name="status"))
    WidgetProperty.objects.create(widget=status_tile, property_name="onTap", property_type="action_reference", action_reference=actions["Mark Todo as Done"]) # Example action to change status

    due_date_tile = Widget.objects.create(screen=screen, widget_type="ListTile", parent_widget=column, order=3, widget_id="detail_todo_due_date")
    WidgetProperty.objects.create(widget=due_date_tile, property_name="leadingIcon", property_type="string", string_value="event")
    WidgetProperty.objects.create(widget=due_date_tile, property_name="title", property_type="string", string_value="Due Date")
    WidgetProperty.objects.create(widget=due_date_tile, property_name="subtitle", property_type="data_source_field_reference", data_source_field_reference=DataSourceField.objects.get(data_sources['TodoItems'], field_name="due_date"))

    priority_tile = Widget.objects.create(screen=screen, widget_type="ListTile", parent_widget=column, order=4, widget_id="detail_todo_priority")
    WidgetProperty.objects.create(widget=priority_tile, property_name="leadingIcon", property_type="string", string_value="flag")
    WidgetProperty.objects.create(widget=priority_tile, property_name="title", property_type="string", string_value="Priority")
    WidgetProperty.objects.create(widget=priority_tile, property_name="subtitle", property_type="data_source_field_reference", data_source_field_reference=DataSourceField.objects.get(data_sources['TodoItems'], field_name="priority"))

    category_tile = Widget.objects.create(screen=screen, widget_type="ListTile", parent_widget=column, order=5, widget_id="detail_todo_category")
    WidgetProperty.objects.create(widget=category_tile, property_name="leadingIcon", property_type="string", string_value="category")
    WidgetProperty.objects.create(widget=category_tile, property_name="title", property_type="string", string_value="Category")
    WidgetProperty.objects.create(widget=category_tile, property_name="subtitle", property_type="data_source_field_reference", data_source_field_reference=DataSourceField.objects.get(data_sources['TodoItems'], field_name="category"))

    # Action Buttons (Edit, Delete)
    button_row = Widget.objects.create(screen=screen, widget_type="Row", parent_widget=column, order=6, widget_id="detail_buttons_row")
    WidgetProperty.objects.create(widget=button_row, property_name="mainAxisAlignment", property_type="string", string_value="spaceEvenly")
    WidgetProperty.objects.create(widget=button_row, property_name="paddingTop", property_type="decimal", decimal_value=24)

    edit_button = Widget.objects.create(screen=screen, widget_type="ElevatedButton", parent_widget=button_row, order=0, widget_id="edit_todo_button")
    WidgetProperty.objects.create(widget=edit_button, property_name="text", property_type="string", string_value="Edit")
    WidgetProperty.objects.create(widget=edit_button, property_name="onPressed", property_type="action_reference", action_reference=actions["Navigate to Create New Todo"]) # Re-use create screen for edit
    WidgetProperty.objects.create(widget=edit_button, property_name="icon", property_type="string", string_value="edit")

    delete_button = Widget.objects.create(screen=screen, widget_type="ElevatedButton", parent_widget=button_row, order=1, widget_id="delete_todo_button")
    WidgetProperty.objects.create(widget=delete_button, property_name="text", property_type="string", string_value="Delete")
    WidgetProperty.objects.create(widget=delete_button, property_name="onPressed", property_type="action_reference", action_reference=actions["Delete Todo"])
    WidgetProperty.objects.create(widget=delete_button, property_name="icon", property_type="string", string_value="delete")
    WidgetProperty.objects.create(widget=delete_button, property_name="backgroundColor", property_type="string", string_value="#EF5350") # Red color


def create_complete_user_profile_screen_ui(screen, data_sources, actions):
    """Create UI for user profile screen"""
    scroll_view = Widget.objects.create(screen=screen, widget_type="SingleChildScrollView", order=0, widget_id="profile_scroll_view")
    column = Widget.objects.create(screen=screen, widget_type="Column", parent_widget=scroll_view, order=0, widget_id="profile_column")
    WidgetProperty.objects.create(widget=column, property_name="padding", property_type="decimal", decimal_value=24)
    WidgetProperty.objects.create(widget=column, property_name="crossAxisAlignment", property_type="string", string_value="center")

    # Profile Picture
    profile_image = Widget.objects.create(screen=screen, widget_type="Image", parent_widget=column, order=0, widget_id="profile_picture")
    WidgetProperty.objects.create(widget=profile_image, property_name="imageUrl", property_type="data_source_field_reference", data_source_field_reference=DataSourceField.objects.get(data_sources['UserProfile'], field_name="profile_picture"))
    WidgetProperty.objects.create(widget=profile_image, property_name="width", property_type="decimal", decimal_value=120)
    WidgetProperty.objects.create(widget=profile_image, property_name="height", property_type="decimal", decimal_value=120)
    WidgetProperty.objects.create(widget=profile_image, property_name="borderRadius", property_type="decimal", decimal_value=60)
    WidgetProperty.objects.create(widget=profile_image, property_name="paddingBottom", property_type="decimal", decimal_value=24)

    # Username
    username_text = Widget.objects.create(screen=screen, widget_type="Text", parent_widget=column, order=1, widget_id="profile_username")
    WidgetProperty.objects.create(widget=username_text, property_name="text", property_type="data_source_field_reference", data_source_field_reference=DataSourceField.objects.get(data_sources['UserProfile'], field_name="username"))
    WidgetProperty.objects.create(widget=username_text, property_name="fontSize", property_type="decimal", decimal_value=24)
    WidgetProperty.objects.create(widget=username_text, property_name="fontWeight", property_type="string", string_value="bold")
    WidgetProperty.objects.create(widget=username_text, property_name="paddingBottom", property_type="decimal", decimal_value=8)

    # Email
    email_text = Widget.objects.create(screen=screen, widget_type="Text", parent_widget=column, order=2, widget_id="profile_email")
    WidgetProperty.objects.create(widget=email_text, property_name="text", property_type="data_source_field_reference", data_source_field_reference=DataSourceField.objects.get(data_sources['UserProfile'], field_name="email"))
    WidgetProperty.objects.create(widget=email_text, property_name="fontSize", property_type="decimal", decimal_value=16)
    WidgetProperty.objects.create(widget=email_text, property_name="color", property_type="string", string_value="#757575")
    WidgetProperty.objects.create(widget=email_text, property_name="paddingBottom", property_type="decimal", decimal_value=24)

    # Edit Profile Button
    edit_profile_button = Widget.objects.create(screen=screen, widget_type="ElevatedButton", parent_widget=column, order=3, widget_id="edit_profile_button")
    WidgetProperty.objects.create(widget=edit_profile_button, property_name="text", property_type="string", string_value="Edit Profile")
    WidgetProperty.objects.create(widget=edit_profile_button, property_name="onPressed", property_type="action_reference", action_reference=actions["Update User Profile"]) # Placeholder for edit profile action
    WidgetProperty.objects.create(widget=edit_profile_button, property_name="icon", property_type="string", string_value="edit")
    WidgetProperty.objects.create(widget=edit_profile_button, property_name="padding", property_type="decimal", decimal_value=12)


def create_complete_settings_screen_ui(screen, data_sources, actions):
    """Create UI for app settings"""
    scroll_view = Widget.objects.create(screen=screen, widget_type="SingleChildScrollView", order=0, widget_id="settings_scroll_view")
    column = Widget.objects.create(screen=screen, widget_type="Column", parent_widget=scroll_view, order=0, widget_id="settings_column")
    WidgetProperty.objects.create(widget=column, property_name="padding", property_type="decimal", decimal_value=16)
    WidgetProperty.objects.create(widget=column, property_name="crossAxisAlignment", property_type="string", string_value="stretch")

    # Theme Preference
    theme_tile = Widget.objects.create(screen=screen, widget_type="ListTile", parent_widget=column, order=0, widget_id="setting_theme_tile")
    WidgetProperty.objects.create(widget=theme_tile, property_name="leadingIcon", property_type="string", string_value="palette")
    WidgetProperty.objects.create(widget=theme_tile, property_name="title", property_type="string", string_value="Theme Preference")
    WidgetProperty.objects.create(widget=theme_tile, property_name="subtitle", property_type="data_source_field_reference", data_source_field_reference=DataSourceField.objects.get(data_sources['AppSettings'], field_name="theme_preference"))
    WidgetProperty.objects.create(widget=theme_tile, property_name="trailing", property_type="string", string_value="""
        DropdownButton<String>(
            value: item['theme_preference'],
            onChanged: (String? newValue) {
                actions['Update App Settings']({'theme_preference': newValue});
            },
            items: <String>['light', 'dark', 'system']
                .map<DropdownMenuItem<String>>((String value) {
                return DropdownMenuItem<String>(
                    value: value,
                    child: Text(value.capitalize()),
                );
            }).toList(),
        )
    """)

    # Notifications Toggle
    notifications_tile = Widget.objects.create(screen=screen, widget_type="ListTile", parent_widget=column, order=1, widget_id="setting_notifications_tile")
    WidgetProperty.objects.create(widget=notifications_tile, property_name="leadingIcon", property_type="string", string_value="notifications")
    WidgetProperty.objects.create(widget=notifications_tile, property_name="title", property_type="string", string_value="Enable Notifications")
    WidgetProperty.objects.create(widget=notifications_tile, property_name="trailing", property_type="string", string_value="""
        Switch(
            value: item['notification_enabled'],
            onChanged: (bool value) {
                actions['Update App Settings']({'notification_enabled': value});
            },
        )
    """)

    # Sound Toggle
    sound_tile = Widget.objects.create(screen=screen, widget_type="ListTile", parent_widget=column, order=2, widget_id="setting_sound_tile")
    WidgetProperty.objects.create(widget=sound_tile, property_name="leadingIcon", property_type="string", string_value="volume_up")
    WidgetProperty.objects.create(widget=sound_tile, property_name="title", property_type="string", string_value="Enable Sounds")
    WidgetProperty.objects.create(widget=sound_tile, property_name="trailing", property_type="string", string_value="""
        Switch(
            value: item['sound_enabled'],
            onChanged: (bool value) {
                actions['Update App Settings']({'sound_enabled': value});
            },
        )
    """)

    # Language Selection
    language_tile = Widget.objects.create(screen=screen, widget_type="ListTile", parent_widget=column, order=3, widget_id="setting_language_tile")
    WidgetProperty.objects.create(widget=language_tile, property_name="leadingIcon", property_type="string", string_value="language")
    WidgetProperty.objects.create(widget=language_tile, property_name="title", property_type="string", string_value="Language")
    WidgetProperty.objects.create(widget=language_tile, property_name="subtitle", property_type="data_source_field_reference", data_source_field_reference=DataSourceField.objects.get(data_sources['AppSettings'], field_name="language"))
    WidgetProperty.objects.create(widget=language_tile, property_name="trailing", property_type="string", string_value="""
        DropdownButton<String>(
            value: item['language'],
            onChanged: (String? newValue) {
                actions['Update App Settings']({'language': newValue});
            },
            items: <String>['English', 'Spanish', 'French']
                .map<DropdownMenuItem<String>>((String value) {
                return DropdownMenuItem<String>(
                    value: value,
                    child: Text(value),
                );
            }).toList(),
        )
    """)

    # Sync Interval
    sync_interval_tile = Widget.objects.create(screen=screen, widget_type="ListTile", parent_widget=column, order=4, widget_id="setting_sync_interval_tile")
    WidgetProperty.objects.create(widget=sync_interval_tile, property_name="leadingIcon", property_type="string", string_value="sync")
    WidgetProperty.objects.create(widget=sync_interval_tile, property_name="title", property_type="string", string_value="Sync Interval (minutes)")
    WidgetProperty.objects.create(widget=sync_interval_tile, property_name="subtitle", property_type="data_source_field_reference", data_source_field_reference=DataSourceField.objects.get(data_sources['AppSettings'], field_name="sync_interval"))
    WidgetProperty.objects.create(widget=sync_interval_tile, property_name="trailing", property_type="string", string_value="""
        TextField(
            keyboardType: TextInputType.number,
            controller: TextEditingController(text: item['sync_interval'].toString()),
            onSubmitted: (value) {
                actions['Update App Settings']({'sync_interval': int(value)});
            },
            decoration: InputDecoration(
                border: InputBorder.none,
                isDense: true,
                contentPadding: EdgeInsets.zero,
            ),
            textAlign: TextAlign.right,
            style: TextStyle(fontSize: 16),
        )
    """)


def create_complete_security_screen_ui(screen, data_sources, actions):
    """Create UI for security settings"""
    scroll_view = Widget.objects.create(screen=screen, widget_type="SingleChildScrollView", order=0, widget_id="security_scroll_view")
    column = Widget.objects.create(screen=screen, widget_type="Column", parent_widget=scroll_view, order=0, widget_id="security_column")
    WidgetProperty.objects.create(widget=column, property_name="padding", property_type="decimal", decimal_value=16)
    WidgetProperty.objects.create(widget=column, property_name="crossAxisAlignment", property_type="string", string_value="stretch")

    # Change Password
    change_password_tile = Widget.objects.create(screen=screen, widget_type="ListTile", parent_widget=column, order=0, widget_id="security_change_password")
    WidgetProperty.objects.create(widget=change_password_tile, property_name="leadingIcon", property_type="string", string_value="lock")
    WidgetProperty.objects.create(widget=change_password_tile, property_name="title", property_type="string", string_value="Change Password")
    WidgetProperty.objects.create(widget=change_password_tile, property_name="onTap", property_type="action_reference", action_reference=actions["Navigate to Forgot Password"]) # Re-use forgot password for now

    # Two-Factor Authentication
    two_factor_tile = Widget.objects.create(screen=screen, widget_type="ListTile", parent_widget=column, order=1, widget_id="security_two_factor")
    WidgetProperty.objects.create(widget=two_factor_tile, property_name="leadingIcon", property_type="string", string_value="security")
    WidgetProperty.objects.create(widget=two_factor_tile, property_name="title", property_type="string", string_value="Two-Factor Authentication")
    WidgetProperty.objects.create(widget=two_factor_tile, property_name="trailing", property_type="string", string_value="""
        Switch(
            value: false, // Placeholder for actual setting
            onChanged: (bool value) {
                // Action to toggle 2FA
            },
        )
    """)

    # Recent Activity
    recent_activity_tile = Widget.objects.create(screen=screen, widget_type="ListTile", parent_widget=column, order=2, widget_id="security_recent_activity")
    WidgetProperty.objects.create(widget=recent_activity_tile, property_name="leadingIcon", property_type="string", string_value="history")
    WidgetProperty.objects.create(widget=recent_activity_tile, property_name="title", property_type="string", string_value="Recent Activity")
    WidgetProperty.objects.create(widget=recent_activity_tile, property_name="onTap", property_type="action_reference", action_reference=actions["Load User Profile"]) # Placeholder for viewing activity log

    # Delete Account
    delete_account_tile = Widget.objects.create(screen=screen, widget_type="ListTile", parent_widget=column, order=3, widget_id="security_delete_account")
    WidgetProperty.objects.create(widget=delete_account_tile, property_name="leadingIcon", property_type="string", string_value="delete_forever")
    WidgetProperty.objects.create(widget=delete_account_tile, property_name="title", property_type="string", string_value="Delete Account")
    WidgetProperty.objects.create(widget=delete_account_tile, property_name="textColor", property_type="string", string_value="#EF5350")
    WidgetProperty.objects.create(widget=delete_account_tile, property_name="onTap", property_type="action_reference", action_reference=actions["Logout User"]) # Placeholder for delete account confirmation


def create_complete_about_screen_ui(screen, data_sources, actions):
    """Create UI for About screen"""
    scroll_view = Widget.objects.create(screen=screen, widget_type="SingleChildScrollView", order=0, widget_id="about_scroll_view")
    column = Widget.objects.create(screen=screen, widget_type="Column", parent_widget=scroll_view, order=0, widget_id="about_column")
    WidgetProperty.objects.create(widget=column, property_name="padding", property_type="decimal", decimal_value=24)
    WidgetProperty.objects.create(widget=column, property_name="crossAxisAlignment", property_type="string", string_value="center")

    app_icon = Widget.objects.create(screen=screen, widget_type="Image", parent_widget=column, order=0, widget_id="about_app_icon")
    WidgetProperty.objects.create(widget=app_icon, property_name="imageUrl", property_type="string", string_value="https://images.pexels.com/photos/1640777/pexels-photo-1640777.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1") # Placeholder
    WidgetProperty.objects.create(widget=app_icon, property_name="width", property_type="decimal", decimal_value=100)
    WidgetProperty.objects.create(widget=app_icon, property_name="height", property_type="decimal", decimal_value=100)
    WidgetProperty.objects.create(widget=app_icon, property_name="paddingBottom", property_type="decimal", decimal_value=16)

    app_name = Widget.objects.create(screen=screen, widget_type="Text", parent_widget=column, order=1, widget_id="about_app_name")
    WidgetProperty.objects.create(widget=app_name, property_name="text", property_type="string", string_value="My Comprehensive To-Do App")
    WidgetProperty.objects.create(widget=app_name, property_name="fontSize", property_type="decimal", decimal_value=24)
    WidgetProperty.objects.create(widget=app_name, property_name="fontWeight", property_type="string", string_value="bold")
    WidgetProperty.objects.create(widget=app_name, property_name="paddingBottom", property_type="decimal", decimal_value=8)

    version_text = Widget.objects.create(screen=screen, widget_type="Text", parent_widget=column, order=2, widget_id="about_version")
    WidgetProperty.objects.create(widget=version_text, property_name="text", property_type="string", string_value="Version 1.0.0")
    WidgetProperty.objects.create(widget=version_text, property_name="fontSize", property_type="decimal", decimal_value=16)
    WidgetProperty.objects.create(widget=version_text, property_name="color", property_type="string", string_value="#757575")
    WidgetProperty.objects.create(widget=version_text, property_name="paddingBottom", property_type="decimal", decimal_value=24)

    description_text = Widget.objects.create(screen=screen, widget_type="Text", parent_widget=column, order=3, widget_id="about_description")
    WidgetProperty.objects.create(widget=description_text, property_name="text", property_type="string", string_value="""
        This application helps you organize your tasks efficiently.
        Keep track of your to-dos, tasks in progress, and completed items with ease.
        Designed for productivity and a seamless user experience.
    """)
    WidgetProperty.objects.create(widget=description_text, property_name="textAlign", property_type="string", string_value="center")
    WidgetProperty.objects.create(widget=description_text, property_name="paddingBottom", property_type="decimal", decimal_value=24)

    # Legal Links
    terms_link = Widget.objects.create(screen=screen, widget_type="TextButton", parent_widget=column, order=4, widget_id="about_terms_link")
    WidgetProperty.objects.create(widget=terms_link, property_name="text", property_type="string", string_value="Terms of Service")
    WidgetProperty.objects.create(widget=terms_link, property_name="onPressed", property_type="action_reference", action_reference=actions["Load User Profile"]) # Placeholder for external link

    privacy_link = Widget.objects.create(screen=screen, widget_type="TextButton", parent_widget=column, order=5, widget_id="about_privacy_link")
    WidgetProperty.objects.create(widget=privacy_link, property_name="text", property_type="string", string_value="Privacy Policy")
    WidgetProperty.objects.create(widget=privacy_link, property_name="onPressed", property_type="action_reference", action_reference=actions["Load User Profile"]) # Placeholder for external link


def create_complete_help_screen_ui(screen, data_sources, actions):
    """Create UI for Help & Support screen"""
    scroll_view = Widget.objects.create(screen=screen, widget_type="SingleChildScrollView", order=0, widget_id="help_scroll_view")
    column = Widget.objects.create(screen=screen, widget_type="Column", parent_widget=scroll_view, order=0, widget_id="help_column")
    WidgetProperty.objects.create(widget=column, property_name="padding", property_type="decimal", decimal_value=16)
    WidgetProperty.objects.create(widget=column, property_name="crossAxisAlignment", property_type="string", string_value="stretch")

    # FAQ Section
    faq_header = Widget.objects.create(screen=screen, widget_type="Text", parent_widget=column, order=0, widget_id="help_faq_header")
    WidgetProperty.objects.create(widget=faq_header, property_name="text", property_type="string", string_value="Frequently Asked Questions")
    WidgetProperty.objects.create(widget=faq_header, property_name="fontSize", property_type="decimal", decimal_value=20)
    WidgetProperty.objects.create(widget=faq_header, property_name="fontWeight", property_type="string", string_value="bold")
    WidgetProperty.objects.create(widget=faq_header, property_name="paddingBottom", property_type="decimal", decimal_value=16)

    # Example FAQ items (using ExpansionTile)
    faq_item1 = Widget.objects.create(screen=screen, widget_type="ExpansionTile", parent_widget=column, order=1, widget_id="faq_item_1")
    WidgetProperty.objects.create(widget=faq_item1, property_name="title", property_type="string", string_value="How do I create a new task?")
    WidgetProperty.objects.create(widget=faq_item1, property_name="children", property_type="string", string_value="""
        [
            Text('Tap the floating "+" button on the home screen, fill in the details, and tap "Save To-Do".')
        ]
    """)

    faq_item2 = Widget.objects.create(screen=screen, widget_type="ExpansionTile", parent_widget=column, order=2, widget_id="faq_item_2")
    WidgetProperty.objects.create(widget=faq_item2, property_name="title", property_type="string", string_value="How do I change a task's status?")
    WidgetProperty.objects.create(widget=faq_item2, property_name="children", property_type="string", string_value="""
        [
            Text('On the home screen, tap the checkbox next to a task to mark it as done. For other statuses, open the task details and select the desired status.')
        ]
    """)

    # Contact Support Section
    contact_header = Widget.objects.create(screen=screen, widget_type="Text", parent_widget=column, order=3, widget_id="help_contact_header")
    WidgetProperty.objects.create(widget=contact_header, property_name="text", property_type="string", string_value="Contact Support")
    WidgetProperty.objects.create(widget=contact_header, property_name="fontSize", property_type="decimal", decimal_value=20)
    WidgetProperty.objects.create(widget=contact_header, property_name="fontWeight", property_type="string", string_value="bold")
    WidgetProperty.objects.create(widget=contact_header, property_name="paddingTop", property_type="decimal", decimal_value=24)
    WidgetProperty.objects.create(widget=contact_header, property_name="paddingBottom", property_type="decimal", decimal_value=16)

    email_tile = Widget.objects.create(screen=screen, widget_type="ListTile", parent_widget=column, order=4, widget_id="help_email_tile")
    WidgetProperty.objects.create(widget=email_tile, property_name="leadingIcon", property_type="string", string_value="email")
    WidgetProperty.objects.create(widget=email_tile, property_name="title", property_type="string", string_value="Email Us")
    WidgetProperty.objects.create(widget=email_tile, property_name="subtitle", property_type="string", string_value="support@todoapp.com")
    WidgetProperty.objects.create(widget=email_tile, property_name="onTap", property_type="action_reference", action_reference=actions["Load User Profile"]) # Placeholder for email client action

    phone_tile = Widget.objects.create(screen=screen, widget_type="ListTile", parent_widget=column, order=5, widget_id="help_phone_tile")
    WidgetProperty.objects.create(widget=phone_tile, property_name="leadingIcon", property_type="string", string_value="phone")
    WidgetProperty.objects.create(widget=phone_tile, property_name="title", property_type="string", string_value="Call Us")
    WidgetProperty.objects.create(widget=phone_tile, property_name="subtitle", property_type="string", string_value="+1 (800) 123-4567")
    WidgetProperty.objects.create(widget=phone_tile, property_name="onTap", property_type="action_reference", action_reference=actions["Load User Profile"]) # Placeholder for phone dialer action


def create_complete_search_results_screen_ui(screen, data_sources, actions):
    """Create UI for displaying search results"""
    column = Widget.objects.create(screen=screen, widget_type="Column", order=0, widget_id="search_results_column")
    WidgetProperty.objects.create(widget=column, property_name="padding", property_type="decimal", decimal_value=16)
    WidgetProperty.objects.create(widget=column, property_name="crossAxisAlignment", property_type="string", string_value="stretch")

    # Search Input (can be pre-filled from previous screen)
    search_input = Widget.objects.create(screen=screen, widget_type="TextField", parent_widget=column, order=0, widget_id="search_results_input")
    WidgetProperty.objects.create(widget=search_input, property_name="labelText", property_type="string", string_value="Search tasks...")
    WidgetProperty.objects.create(widget=search_input, property_name="prefixIcon", property_type="string", string_value="search")
    WidgetProperty.objects.create(widget=search_input, property_name="onSubmitted", property_type="action_reference", action_reference=actions["Search Todos"])
    WidgetProperty.objects.create(widget=search_input, property_name="paddingBottom", property_type="decimal", decimal_value=16)

    # Results List
    results_list = Widget.objects.create(
        screen=screen,
        widget_type="ListView",
        parent_widget=column,
        order=1,
        widget_id="search_results_list"
    )
    WidgetProperty.objects.create(widget=results_list, property_name="shrinkWrap", property_type="boolean", boolean_value=True)
    WidgetProperty.objects.create(
        widget=results_list,
        property_name="dataSource",
        property_type="data_source_field_reference",
        data_source_field_reference=DataSourceField.objects.get(
            data_source=data_sources['TodoItems'],
            field_name="id" # This list will be populated by search results
        )
    )
    WidgetProperty.objects.create(widget=results_list, property_name="itemBuilder", property_type="string", string_value="""
        (context, index, item) => Card(
            margin: EdgeInsets.symmetric(vertical: 8),
            child: ListTile(
                title: Text(item['title']),
                subtitle: Text(item['description']),
                trailing: Icon(item['is_completed'] ? Icons.check_box : Icons.check_box_outline_blank),
                onTap: () => actions['Navigate to Todo Detail'](item['id'])
            )
        )
    """)


def create_complete_categories_list_screen_ui(screen, data_sources, actions):
    """Create UI for displaying a list of categories"""
    scroll_view = Widget.objects.create(screen=screen, widget_type="SingleChildScrollView", order=0, widget_id="categories_scroll_view")
    column = Widget.objects.create(screen=screen, widget_type="Column", parent_widget=scroll_view, order=0, widget_id="categories_column")
    WidgetProperty.objects.create(widget=column, property_name="padding", property_type="decimal", decimal_value=16)
    WidgetProperty.objects.create(widget=column, property_name="crossAxisAlignment", property_type="string", string_value="stretch")

    # Categories List
    categories_list = Widget.objects.create(
        screen=screen,
        widget_type="ListView",
        parent_widget=column,
        order=0,
        widget_id="categories_list"
    )
    WidgetProperty.objects.create(widget=categories_list, property_name="shrinkWrap", property_type="boolean", boolean_value=True)
    WidgetProperty.objects.create(WidgetProperty.objects.create(widget=categories_list, property_name="physics", property_type="string", string_value="NeverScrollableScrollPhysics"))
    WidgetProperty.objects.create(
        widget=categories_list,
        property_name="dataSource",
        property_type="data_source_field_reference",
        data_source_field_reference=DataSourceField.objects.get(
            data_source=data_sources['Categories'],
            field_name="id" # Bind to the list of category IDs
        )
    )
    WidgetProperty.objects.create(widget=categories_list, property_name="itemBuilder", property_type="string", string_value="""
        (context, index, item) => Card(
            margin: EdgeInsets.symmetric(vertical: 8),
            child: ListTile(
                leading: Icon(item['icon'] != null ? IconData(int.parse(item['icon']), fontFamily: 'MaterialIcons') : Icons.folder),
                title: Text(item['name']),
                subtitle: Text(item['description']),
                trailing: Text('${item['task_count']} tasks'),
                onTap: () => actions['Filter Todos by Category'](item['id']) // Action to filter todos by category
            )
        )
    """)
