# File: core/management/commands/create_weather_app.py
"""
Management command to create a comprehensive weather application
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import (
    Application, Theme, Screen, Widget, WidgetProperty,
    Action, DataSource, DataSourceField
)


class Command(BaseCommand):
    help = 'Create a comprehensive weather application with all features'

    def add_arguments(self, parser):
        parser.add_argument(
            '--name',
            type=str,
            default='WeatherPro',
            help='Custom name for the weather application'
        )
        parser.add_argument(
            '--package',
            type=str,
            default='com.weatherpro.app',
            help='Package identifier for the application'
        )

    def handle(self, *args, **options):
        app_name = options['name']
        package_name = options['package']

        try:
            with transaction.atomic():
                app = create_comprehensive_weather_app(app_name, package_name)
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully created weather application: {app.name}'
                    )
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating weather application: {str(e)}')
            )


def create_comprehensive_weather_app(custom_name=None, package_name=None):
    """Create a comprehensive weather application with all features"""

    # Create professional weather theme
    theme = Theme.objects.create(
        name="Weather Professional Theme",
        primary_color="#1976D2",  # Weather blue
        accent_color="#FFC107",   # Sunny yellow accent
        background_color="#F5F5F5",  # Light grey background
        text_color="#212121",  # Dark grey text
        font_family="Roboto",
        is_dark_mode=False
    )

    # Create application
    app = Application.objects.create(
        name=custom_name or "WeatherPro - Advanced Weather Forecast",
        description="""A comprehensive weather application featuring real-time weather updates, 
        7-day forecasts, interactive weather maps, severe weather alerts, location-based services, 
        air quality monitoring, UV index, precipitation radar, and personalized weather notifications.""",
        package_name=package_name or "com.weatherpro.app",
        version="1.0.0",
        theme=theme
    )

    # Base URL for mock APIs (using dynamic URL for flexibility)
    base_url = "DYNAMIC"  # Will use configuration screen

    # Create comprehensive data sources
    data_sources = create_data_sources(app, base_url)

    # Create actions
    actions = create_actions(app, data_sources)

    # Create screens
    screens = create_screens(app)

    # Update actions with screen references
    update_action_targets(actions, screens)

    # Create widgets for each screen
    create_splash_screen_widgets(screens['splash'], data_sources, actions)
    create_configuration_screen_widgets(screens['configuration'], data_sources, actions)
    create_home_screen_widgets(screens['home'], data_sources, actions)
    create_profile_screen_widgets(screens['profile'], data_sources, actions)
    create_settings_screen_widgets(screens['settings'], data_sources, actions)
    create_subscription_screen_widgets(screens['subscription'], data_sources, actions)
    create_location_screen_widgets(screens['location'], data_sources, actions)
    create_weather_maps_screen_widgets(screens['weather_maps'], data_sources, actions)
    create_about_screen_widgets(screens['about'], data_sources, actions)
    create_support_screen_widgets(screens['support'], data_sources, actions)
    create_payment_screen_widgets(screens['payment'], data_sources, actions)
    create_register_screen_widgets(screens['register'], data_sources, actions)
    create_login_screen_widgets(screens['login'], data_sources, actions)
    create_forgot_password_screen_widgets(screens['forgot_password'], data_sources, actions)
    create_change_password_screen_widgets(screens['change_password'], data_sources, actions)

    return app


def create_data_sources(app, base_url):
    """Create all data sources for the weather app"""
    data_sources = {}

    # Current weather data source
    current_weather_ds = DataSource.objects.create(
        application=app,
        name="Current Weather",
        data_source_type="REST_API",
        base_url=base_url,
        endpoint="/api/mock/weather/current",
        method="GET",
        use_dynamic_base_url=True
    )

    weather_fields = [
        ("location", "string", "Location", True),
        ("temperature", "decimal", "Temperature", True),
        ("description", "string", "Description", True),
        ("humidity", "integer", "Humidity", True),
        ("windSpeed", "decimal", "Wind Speed", True),
        ("pressure", "integer", "Pressure", True),
        ("feelsLike", "decimal", "Feels Like", True),
        ("icon", "string", "Weather Icon", True),
        ("uvIndex", "integer", "UV Index", False),
        ("visibility", "decimal", "Visibility", False),
    ]

    for field_name, field_type, display_name, is_required in weather_fields:
        DataSourceField.objects.create(
            data_source=current_weather_ds,
            field_name=field_name,
            field_type=field_type,
            display_name=display_name,
            is_required=is_required
        )

    data_sources['current_weather'] = current_weather_ds

    # Forecast data source
    forecast_ds = DataSource.objects.create(
        application=app,
        name="Weather Forecast",
        data_source_type="REST_API",
        base_url=base_url,
        endpoint="/api/mock/weather/forecast",
        method="GET",
        use_dynamic_base_url=True
    )

    forecast_fields = [
        ("date", "date", "Date", True),
        ("tempMax", "decimal", "Max Temperature", True),
        ("tempMin", "decimal", "Min Temperature", True),
        ("description", "string", "Description", True),
        ("icon", "string", "Weather Icon", True),
        ("precipitation", "integer", "Precipitation %", False),
        ("windSpeed", "decimal", "Wind Speed", False),
    ]

    for field_name, field_type, display_name, is_required in forecast_fields:
        DataSourceField.objects.create(
            data_source=forecast_ds,
            field_name=field_name,
            field_type=field_type,
            display_name=display_name,
            is_required=is_required
        )

    data_sources['forecast'] = forecast_ds

    # Hourly forecast data source
    hourly_ds = DataSource.objects.create(
        application=app,
        name="Hourly Forecast",
        data_source_type="REST_API",
        base_url=base_url,
        endpoint="/api/mock/weather/hourly",
        method="GET",
        use_dynamic_base_url=True
    )

    hourly_fields = [
        ("time", "string", "Time", True),
        ("temperature", "decimal", "Temperature", True),
        ("description", "string", "Description", True),
        ("icon", "string", "Icon", True),
        ("precipitation", "integer", "Precipitation %", False),
    ]

    for field_name, field_type, display_name, is_required in hourly_fields:
        DataSourceField.objects.create(
            data_source=hourly_ds,
            field_name=field_name,
            field_type=field_type,
            display_name=display_name,
            is_required=is_required
        )

    data_sources['hourly'] = hourly_ds

    # Locations data source
    locations_ds = DataSource.objects.create(
        application=app,
        name="Saved Locations",
        data_source_type="REST_API",
        base_url=base_url,
        endpoint="/api/mock/weather/locations",
        method="GET",
        use_dynamic_base_url=True
    )

    location_fields = [
        ("id", "string", "Location ID", True),
        ("name", "string", "Location Name", True),
        ("country", "string", "Country", True),
        ("latitude", "decimal", "Latitude", True),
        ("longitude", "decimal", "Longitude", True),
        ("isDefault", "boolean", "Default Location", False),
    ]

    for field_name, field_type, display_name, is_required in location_fields:
        DataSourceField.objects.create(
            data_source=locations_ds,
            field_name=field_name,
            field_type=field_type,
            display_name=display_name,
            is_required=is_required
        )

    data_sources['locations'] = locations_ds

    # Alerts data source
    alerts_ds = DataSource.objects.create(
        application=app,
        name="Weather Alerts",
        data_source_type="REST_API",
        base_url=base_url,
        endpoint="/api/mock/weather/alerts",
        method="GET",
        use_dynamic_base_url=True
    )

    alert_fields = [
        ("id", "string", "Alert ID", True),
        ("type", "string", "Alert Type", True),
        ("severity", "string", "Severity", True),
        ("title", "string", "Title", True),
        ("description", "string", "Description", True),
        ("startTime", "datetime", "Start Time", True),
        ("endTime", "datetime", "End Time", False),
    ]

    for field_name, field_type, display_name, is_required in alert_fields:
        DataSourceField.objects.create(
            data_source=alerts_ds,
            field_name=field_name,
            field_type=field_type,
            display_name=display_name,
            is_required=is_required
        )

    data_sources['alerts'] = alerts_ds

    # Air quality data source
    air_quality_ds = DataSource.objects.create(
        application=app,
        name="Air Quality",
        data_source_type="REST_API",
        base_url=base_url,
        endpoint="/api/mock/weather/air-quality",
        method="GET",
        use_dynamic_base_url=True
    )

    air_quality_fields = [
        ("aqi", "integer", "Air Quality Index", True),
        ("level", "string", "Quality Level", True),
        ("pm25", "decimal", "PM2.5", False),
        ("pm10", "decimal", "PM10", False),
        ("o3", "decimal", "Ozone", False),
        ("no2", "decimal", "NO2", False),
    ]

    for field_name, field_type, display_name, is_required in air_quality_fields:
        DataSourceField.objects.create(
            data_source=air_quality_ds,
            field_name=field_name,
            field_type=field_type,
            display_name=display_name,
            is_required=is_required
        )

    data_sources['air_quality'] = air_quality_ds

    # User profile data source
    profile_ds = DataSource.objects.create(
        application=app,
        name="User Profile",
        data_source_type="REST_API",
        base_url=base_url,
        endpoint="/api/mock/weather/profile",
        method="GET",
        use_dynamic_base_url=True
    )

    profile_fields = [
        ("id", "string", "User ID", True),
        ("name", "string", "Name", True),
        ("email", "email", "Email", True),
        ("avatar", "image_url", "Avatar", False),
        ("preferredUnit", "string", "Preferred Unit", True),
        ("notificationsEnabled", "boolean", "Notifications", True),
    ]

    for field_name, field_type, display_name, is_required in profile_fields:
        DataSourceField.objects.create(
            data_source=profile_ds,
            field_name=field_name,
            field_type=field_type,
            display_name=display_name,
            is_required=is_required
        )

    data_sources['profile'] = profile_ds

    # Subscription plans data source
    subscription_ds = DataSource.objects.create(
        application=app,
        name="Subscription Plans",
        data_source_type="REST_API",
        base_url=base_url,
        endpoint="/api/mock/weather/subscriptions",
        method="GET",
        use_dynamic_base_url=True
    )

    subscription_fields = [
        ("id", "string", "Plan ID", True),
        ("name", "string", "Plan Name", True),
        ("price", "decimal", "Price", True),
        ("features", "string", "Features", True),
        ("duration", "string", "Duration", True),
        ("isPopular", "boolean", "Popular", False),
    ]

    for field_name, field_type, display_name, is_required in subscription_fields:
        DataSourceField.objects.create(
            data_source=subscription_ds,
            field_name=field_name,
            field_type=field_type,
            display_name=display_name,
            is_required=is_required
        )

    data_sources['subscription'] = subscription_ds

    return data_sources


def create_actions(app, data_sources):
    """Create all actions for the weather app"""
    actions = {}

    # Navigation actions
    nav_actions = [
        ("Navigate to Home", "navigate"),
        ("Navigate to Profile", "navigate"),
        ("Navigate to Settings", "navigate"),
        ("Navigate to Subscription", "navigate"),
        ("Navigate to Location", "navigate"),
        ("Navigate to Weather Maps", "navigate"),
        ("Navigate to About", "navigate"),
        ("Navigate to Support", "navigate"),
        ("Navigate to Payment", "navigate"),
        ("Navigate to Login", "navigate"),
        ("Navigate to Register", "navigate"),
        ("Navigate to Forgot Password", "navigate"),
        ("Navigate to Change Password", "navigate"),
        ("Navigate to Configuration", "navigate"),
        ("Go Back", "navigate_back"),
    ]

    for name, action_type in nav_actions:
        action = Action.objects.create(
            application=app,
            name=name,
            action_type=action_type
        )
        actions[name] = action

    # Data actions
    actions["Refresh Weather"] = Action.objects.create(
        application=app,
        name="Refresh Weather",
        action_type="refresh_data"
    )

    actions["Load Forecast"] = Action.objects.create(
        application=app,
        name="Load Forecast",
        action_type="api_call",
        api_data_source=data_sources['forecast']
    )

    actions["Load Hourly"] = Action.objects.create(
        application=app,
        name="Load Hourly",
        action_type="api_call",
        api_data_source=data_sources['hourly']
    )

    # User actions
    actions["Login User"] = Action.objects.create(
        application=app,
        name="Login User",
        action_type="api_call"
    )

    actions["Register User"] = Action.objects.create(
        application=app,
        name="Register User",
        action_type="api_call"
    )

    actions["Save Location"] = Action.objects.create(
        application=app,
        name="Save Location",
        action_type="save_data"
    )

    actions["Share Weather"] = Action.objects.create(
        application=app,
        name="Share Weather",
        action_type="share_content"
    )

    actions["Show Alert"] = Action.objects.create(
        application=app,
        name="Show Alert",
        action_type="show_dialog",
        dialog_title="Weather Alert",
        dialog_message="Severe weather warning in your area"
    )

    return actions


def create_screens(app):
    """Create all screens for the weather app"""
    screens = {}

    screens['splash'] = Screen.objects.create(
        application=app,
        name="SplashScreen",
        route_name="/",
        is_home_screen=False,
        app_bar_title="",
        show_app_bar=False,
        show_back_button=False
    )

    screens['configuration'] = Screen.objects.create(
        application=app,
        name="Configuration",
        route_name="/configuration",
        is_home_screen=False,
        app_bar_title="Server Configuration",
        show_app_bar=True,
        show_back_button=False
    )

    screens['home'] = Screen.objects.create(
        application=app,
        name="Home",
        route_name="/home",
        is_home_screen=True,
        app_bar_title="WeatherPro",
        show_app_bar=True,
        show_back_button=False
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

    screens['settings'] = Screen.objects.create(
        application=app,
        name="Settings",
        route_name="/settings",
        is_home_screen=False,
        app_bar_title="Settings",
        show_app_bar=True,
        show_back_button=True
    )

    screens['subscription'] = Screen.objects.create(
        application=app,
        name="Subscription",
        route_name="/subscription",
        is_home_screen=False,
        app_bar_title="Premium Plans",
        show_app_bar=True,
        show_back_button=True
    )

    screens['location'] = Screen.objects.create(
        application=app,
        name="Location",
        route_name="/location",
        is_home_screen=False,
        app_bar_title="Manage Locations",
        show_app_bar=True,
        show_back_button=True
    )

    screens['weather_maps'] = Screen.objects.create(
        application=app,
        name="Weather Maps",
        route_name="/weather-maps",
        is_home_screen=False,
        app_bar_title="Weather Maps",
        show_app_bar=True,
        show_back_button=True
    )

    screens['about'] = Screen.objects.create(
        application=app,
        name="About Us",
        route_name="/about",
        is_home_screen=False,
        app_bar_title="About WeatherPro",
        show_app_bar=True,
        show_back_button=True
    )

    screens['support'] = Screen.objects.create(
        application=app,
        name="Support",
        route_name="/support",
        is_home_screen=False,
        app_bar_title="Contact Support",
        show_app_bar=True,
        show_back_button=True
    )

    screens['payment'] = Screen.objects.create(
        application=app,
        name="Payment",
        route_name="/payment",
        is_home_screen=False,
        app_bar_title="Payment",
        show_app_bar=True,
        show_back_button=True
    )

    screens['register'] = Screen.objects.create(
        application=app,
        name="Register",
        route_name="/register",
        is_home_screen=False,
        app_bar_title="Create Account",
        show_app_bar=True,
        show_back_button=True
    )

    screens['login'] = Screen.objects.create(
        application=app,
        name="Login",
        route_name="/login",
        is_home_screen=False,
        app_bar_title="Sign In",
        show_app_bar=True,
        show_back_button=True
    )

    screens['forgot_password'] = Screen.objects.create(
        application=app,
        name="Forgot Password",
        route_name="/forgot-password",
        is_home_screen=False,
        app_bar_title="Reset Password",
        show_app_bar=True,
        show_back_button=True
    )

    screens['change_password'] = Screen.objects.create(
        application=app,
        name="Change Password",
        route_name="/change-password",
        is_home_screen=False,
        app_bar_title="Change Password",
        show_app_bar=True,
        show_back_button=True
    )

    return screens


def update_action_targets(actions, screens):
    """Update navigation actions with their target screens"""
    action_screen_mapping = {
        "Navigate to Home": screens['home'],
        "Navigate to Profile": screens['profile'],
        "Navigate to Settings": screens['settings'],
        "Navigate to Subscription": screens['subscription'],
        "Navigate to Location": screens['location'],
        "Navigate to Weather Maps": screens['weather_maps'],
        "Navigate to About": screens['about'],
        "Navigate to Support": screens['support'],
        "Navigate to Payment": screens['payment'],
        "Navigate to Login": screens['login'],
        "Navigate to Register": screens['register'],
        "Navigate to Forgot Password": screens['forgot_password'],
        "Navigate to Change Password": screens['change_password'],
        "Navigate to Configuration": screens['configuration'],
    }

    for action_name, target_screen in action_screen_mapping.items():
        if action_name in actions:
            actions[action_name].target_screen = target_screen
            actions[action_name].save()


def create_splash_screen_widgets(screen, data_sources, actions):
    """Create widgets for splash screen"""
    # Main container
    main_container = Widget.objects.create(
        screen=screen,
        widget_type="Container",
        order=0,
        widget_id="splash_container"
    )

    WidgetProperty.objects.create(
        widget=main_container,
        property_name="color",
        property_type="color",
        color_value="#1976D2"
    )

    # Center widget
    center = Widget.objects.create(
        screen=screen,
        widget_type="Center",
        parent_widget=main_container,
        order=0,
        widget_id="splash_center"
    )

    # Column for logo and text
    column = Widget.objects.create(
        screen=screen,
        widget_type="Column",
        parent_widget=center,
        order=0,
        widget_id="splash_column"
    )

    WidgetProperty.objects.create(
        widget=column,
        property_name="mainAxisAlignment",
        property_type="string",
        string_value="center"
    )

    # Weather icon
    icon = Widget.objects.create(
        screen=screen,
        widget_type="Icon",
        parent_widget=column,
        order=0,
        widget_id="splash_icon"
    )

    WidgetProperty.objects.create(
        widget=icon,
        property_name="icon",
        property_type="string",
        string_value="cloud"
    )

    WidgetProperty.objects.create(
        widget=icon,
        property_name="size",
        property_type="integer",
        integer_value=100
    )

    WidgetProperty.objects.create(
        widget=icon,
        property_name="color",
        property_type="color",
        color_value="#FFFFFF"
    )

    # App name
    app_name = Widget.objects.create(
        screen=screen,
        widget_type="Text",
        parent_widget=column,
        order=1,
        widget_id="splash_app_name"
    )

    WidgetProperty.objects.create(
        widget=app_name,
        property_name="text",
        property_type="string",
        string_value="WeatherPro"
    )

    WidgetProperty.objects.create(
        widget=app_name,
        property_name="fontSize",
        property_type="integer",
        integer_value=32
    )

    WidgetProperty.objects.create(
        widget=app_name,
        property_name="color",
        property_type="color",
        color_value="#FFFFFF"
    )

    # Loading indicator
    loading = Widget.objects.create(
        screen=screen,
        widget_type="Container",
        parent_widget=column,
        order=2,
        widget_id="splash_loading"
    )

    WidgetProperty.objects.create(
        widget=loading,
        property_name="padding",
        property_type="integer",
        integer_value=20
    )


def create_configuration_screen_widgets(screen, data_sources, actions):
    """Create widgets for configuration screen"""
    # Configuration screen is handled specially by the generator
    pass


def create_home_screen_widgets(screen, data_sources, actions):
    """Create widgets for home screen"""
    # Main scroll view
    scroll_view = Widget.objects.create(
        screen=screen,
        widget_type="SingleChildScrollView",
        order=0,
        widget_id="home_scroll"
    )

    # Main column
    main_column = Widget.objects.create(
        screen=screen,
        widget_type="Column",
        parent_widget=scroll_view,
        order=0,
        widget_id="home_column"
    )

    # Current weather card
    weather_card = Widget.objects.create(
        screen=screen,
        widget_type="Card",
        parent_widget=main_column,
        order=0,
        widget_id="current_weather_card"
    )

    WidgetProperty.objects.create(
        widget=weather_card,
        property_name="elevation",
        property_type="integer",
        integer_value=4
    )

    WidgetProperty.objects.create(
        widget=weather_card,
        property_name="margin",
        property_type="integer",
        integer_value=16
    )

    # Weather content using FutureBuilder
    weather_future = Widget.objects.create(
        screen=screen,
        widget_type="FutureBuilder",
        parent_widget=weather_card,
        order=0,
        widget_id="weather_future_builder"
    )

    WidgetProperty.objects.create(
        widget=weather_future,
        property_name="dataSource",
        property_type="data_source_field_reference",
        data_source_field_reference=DataSourceField.objects.get(
            data_source=data_sources['current_weather'],
            field_name="temperature"
        )
    )

    # Weather display column
    weather_column = Widget.objects.create(
        screen=screen,
        widget_type="Column",
        parent_widget=weather_future,
        order=0,
        widget_id="weather_display"
    )

    # Temperature text
    temp_text = Widget.objects.create(
        screen=screen,
        widget_type="Text",
        parent_widget=weather_column,
        order=0,
        widget_id="temperature_text"
    )

    WidgetProperty.objects.create(
        widget=temp_text,
        property_name="text",
        property_type="string",
        string_value="25°C"
    )

    WidgetProperty.objects.create(
        widget=temp_text,
        property_name="fontSize",
        property_type="integer",
        integer_value=48
    )

    # Description text
    desc_text = Widget.objects.create(
        screen=screen,
        widget_type="Text",
        parent_widget=weather_column,
        order=1,
        widget_id="description_text"
    )

    WidgetProperty.objects.create(
        widget=desc_text,
        property_name="text",
        property_type="string",
        string_value="Partly Cloudy"
    )

    WidgetProperty.objects.create(
        widget=desc_text,
        property_name="fontSize",
        property_type="integer",
        integer_value=20
    )

    # Hourly forecast section
    hourly_title = Widget.objects.create(
        screen=screen,
        widget_type="Padding",
        parent_widget=main_column,
        order=1,
        widget_id="hourly_title_padding"
    )

    WidgetProperty.objects.create(
        widget=hourly_title,
        property_name="padding",
        property_type="integer",
        integer_value=16
    )

    hourly_text = Widget.objects.create(
        screen=screen,
        widget_type="Text",
        parent_widget=hourly_title,
        order=0,
        widget_id="hourly_title"
    )

    WidgetProperty.objects.create(
        widget=hourly_text,
        property_name="text",
        property_type="string",
        string_value="Hourly Forecast"
    )

    WidgetProperty.objects.create(
        widget=hourly_text,
        property_name="fontSize",
        property_type="integer",
        integer_value=18
    )

    # Hourly forecast list (horizontal)
    hourly_container = Widget.objects.create(
        screen=screen,
        widget_type="Container",
        parent_widget=main_column,
        order=2,
        widget_id="hourly_container"
    )

    WidgetProperty.objects.create(
        widget=hourly_container,
        property_name="height",
        property_type="integer",
        integer_value=120
    )

    hourly_list = Widget.objects.create(
        screen=screen,
        widget_type="ListView",
        parent_widget=hourly_container,
        order=0,
        widget_id="hourly_list"
    )

    WidgetProperty.objects.create(
        widget=hourly_list,
        property_name="scrollDirection",
        property_type="string",
        string_value="horizontal"
    )

    WidgetProperty.objects.create(
        widget=hourly_list,
        property_name="dataSource",
        property_type="data_source_field_reference",
        data_source_field_reference=DataSourceField.objects.get(
            data_source=data_sources['hourly'],
            field_name="temperature"
        )
    )

    # 7-day forecast section
    forecast_title = Widget.objects.create(
        screen=screen,
        widget_type="Padding",
        parent_widget=main_column,
        order=3,
        widget_id="forecast_title_padding"
    )

    WidgetProperty.objects.create(
        widget=forecast_title,
        property_name="padding",
        property_type="integer",
        integer_value=16
    )

    forecast_text = Widget.objects.create(
        screen=screen,
        widget_type="Text",
        parent_widget=forecast_title,
        order=0,
        widget_id="forecast_title"
    )

    WidgetProperty.objects.create(
        widget=forecast_text,
        property_name="text",
        property_type="string",
        string_value="7-Day Forecast"
    )

    WidgetProperty.objects.create(
        widget=forecast_text,
        property_name="fontSize",
        property_type="integer",
        integer_value=18
    )

    # Forecast list
    forecast_list = Widget.objects.create(
        screen=screen,
        widget_type="ListView",
        parent_widget=main_column,
        order=4,
        widget_id="forecast_list"
    )

    WidgetProperty.objects.create(
        widget=forecast_list,
        property_name="dataSource",
        property_type="data_source_field_reference",
        data_source_field_reference=DataSourceField.objects.get(
            data_source=data_sources['forecast'],
            field_name="tempMax"
        )
    )

    # Bottom navigation
    bottom_nav = Widget.objects.create(
        screen=screen,
        widget_type="BottomNavigationBar",
        order=1,
        widget_id="home_bottom_nav"
    )

    # Navigation items
    nav_items = [
        ("home", "Home", None),
        ("map", "Maps", actions["Navigate to Weather Maps"]),
        ("location_on", "Location", actions["Navigate to Location"]),
        ("person", "Profile", actions["Navigate to Profile"]),
    ]

    for i, (icon_name, label, action) in enumerate(nav_items):
        nav_item = Widget.objects.create(
            screen=screen,
            widget_type="BottomNavigationBarItem",
            parent_widget=bottom_nav,
            order=i,
            widget_id=f"nav_{icon_name}"
        )

        WidgetProperty.objects.create(
            widget=nav_item,
            property_name="icon",
            property_type="string",
            string_value=icon_name
        )

        WidgetProperty.objects.create(
            widget=nav_item,
            property_name="label",
            property_type="string",
            string_value=label
        )

        if action:
            WidgetProperty.objects.create(
                widget=nav_item,
                property_name="onTap",
                property_type="action_reference",
                action_reference=action
            )


def create_profile_screen_widgets(screen, data_sources, actions):
    """Create widgets for profile screen"""
    # Profile screen with user info and preferences
    scroll_view = Widget.objects.create(
        screen=screen,
        widget_type="SingleChildScrollView",
        order=0,
        widget_id="profile_scroll"
    )

    column = Widget.objects.create(
        screen=screen,
        widget_type="Column",
        parent_widget=scroll_view,
        order=0,
        widget_id="profile_column"
    )

    # Profile header
    header = Widget.objects.create(
        screen=screen,
        widget_type="Container",
        parent_widget=column,
        order=0,
        widget_id="profile_header"
    )

    WidgetProperty.objects.create(
        widget=header,
        property_name="padding",
        property_type="integer",
        integer_value=20
    )

    WidgetProperty.objects.create(
        widget=header,
        property_name="color",
        property_type="color",
        color_value="#1976D2"
    )

    # Avatar icon
    avatar = Widget.objects.create(
        screen=screen,
        widget_type="Icon",
        parent_widget=header,
        order=0,
        widget_id="profile_avatar"
    )

    WidgetProperty.objects.create(
        widget=avatar,
        property_name="icon",
        property_type="string",
        string_value="account_circle"
    )

    WidgetProperty.objects.create(
        widget=avatar,
        property_name="size",
        property_type="integer",
        integer_value=80
    )

    WidgetProperty.objects.create(
        widget=avatar,
        property_name="color",
        property_type="color",
        color_value="#FFFFFF"
    )

    # Settings options
    settings_items = [
        ("settings", "Settings", actions["Navigate to Settings"]),
        ("card_membership", "Subscription", actions["Navigate to Subscription"]),
        ("lock", "Change Password", actions["Navigate to Change Password"]),
        ("help", "Support", actions["Navigate to Support"]),
        ("info", "About", actions["Navigate to About"]),
    ]

    for i, (icon_name, title, action) in enumerate(settings_items):
        list_tile = Widget.objects.create(
            screen=screen,
            widget_type="ListTile",
            parent_widget=column,
            order=i + 1,
            widget_id=f"profile_{icon_name}_tile"
        )

        WidgetProperty.objects.create(
            widget=list_tile,
            property_name="leading",
            property_type="string",
            string_value=icon_name
        )

        WidgetProperty.objects.create(
            widget=list_tile,
            property_name="title",
            property_type="string",
            string_value=title
        )

        WidgetProperty.objects.create(
            widget=list_tile,
            property_name="trailing",
            property_type="string",
            string_value="arrow_forward_ios"
        )

        if action:
            WidgetProperty.objects.create(
                widget=list_tile,
                property_name="onTap",
                property_type="action_reference",
                action_reference=action
            )


def create_settings_screen_widgets(screen, data_sources, actions):
    """Create widgets for settings screen"""
    column = Widget.objects.create(
        screen=screen,
        widget_type="Column",
        order=0,
        widget_id="settings_column"
    )

    # Settings options
    settings = [
        ("Temperature Unit", "Celsius / Fahrenheit"),
        ("Wind Speed", "km/h / mph"),
        ("Notifications", "Enable weather alerts"),
        ("Auto Refresh", "Update weather automatically"),
        ("Dark Mode", "Enable dark theme"),
    ]

    for i, (title, subtitle) in enumerate(settings):
        tile = Widget.objects.create(
            screen=screen,
            widget_type="ListTile",
            parent_widget=column,
            order=i,
            widget_id=f"setting_{i}"
        )

        WidgetProperty.objects.create(
            widget=tile,
            property_name="title",
            property_type="string",
            string_value=title
        )

        WidgetProperty.objects.create(
            widget=tile,
            property_name="subtitle",
            property_type="string",
            string_value=subtitle
        )

        # Add switch for some settings
        if i in [2, 3, 4]:  # Notifications, Auto Refresh, Dark Mode
            switch = Widget.objects.create(
                screen=screen,
                widget_type="Switch",
                parent_widget=tile,
                order=0,
                widget_id=f"setting_switch_{i}"
            )

            WidgetProperty.objects.create(
                widget=switch,
                property_name="value",
                property_type="boolean",
                boolean_value=True
            )


def create_subscription_screen_widgets(screen, data_sources, actions):
    """Create widgets for subscription screen"""
    scroll_view = Widget.objects.create(
        screen=screen,
        widget_type="SingleChildScrollView",
        order=0,
        widget_id="subscription_scroll"
    )

    column = Widget.objects.create(
        screen=screen,
        widget_type="Column",
        parent_widget=scroll_view,
        order=0,
        widget_id="subscription_column"
    )

    # Title
    title = Widget.objects.create(
        screen=screen,
        widget_type="Padding",
        parent_widget=column,
        order=0,
        widget_id="subscription_title_padding"
    )

    WidgetProperty.objects.create(
        widget=title,
        property_name="padding",
        property_type="integer",
        integer_value=16
    )

    title_text = Widget.objects.create(
        screen=screen,
        widget_type="Text",
        parent_widget=title,
        order=0,
        widget_id="subscription_title"
    )

    WidgetProperty.objects.create(
        widget=title_text,
        property_name="text",
        property_type="string",
        string_value="Choose Your Plan"
    )

    WidgetProperty.objects.create(
        widget=title_text,
        property_name="fontSize",
        property_type="integer",
        integer_value=24
    )

    # Plans list
    plans_list = Widget.objects.create(
        screen=screen,
        widget_type="ListView",
        parent_widget=column,
        order=1,
        widget_id="plans_list"
    )

    WidgetProperty.objects.create(
        widget=plans_list,
        property_name="dataSource",
        property_type="data_source_field_reference",
        data_source_field_reference=DataSourceField.objects.get(
            data_source=data_sources['subscription'],
            field_name="name"
        )
    )


def create_location_screen_widgets(screen, data_sources, actions):
    """Create widgets for location management screen"""
    column = Widget.objects.create(
        screen=screen,
        widget_type="Column",
        order=0,
        widget_id="location_column"
    )

    # Search bar
    search_container = Widget.objects.create(
        screen=screen,
        widget_type="Padding",
        parent_widget=column,
        order=0,
        widget_id="location_search_padding"
    )

    WidgetProperty.objects.create(
        widget=search_container,
        property_name="padding",
        property_type="integer",
        integer_value=16
    )

    search_field = Widget.objects.create(
        screen=screen,
        widget_type="TextField",
        parent_widget=search_container,
        order=0,
        widget_id="location_search"
    )

    WidgetProperty.objects.create(
        widget=search_field,
        property_name="hintText",
        property_type="string",
        string_value="Search for a location..."
    )

    WidgetProperty.objects.create(
        widget=search_field,
        property_name="labelText",
        property_type="string",
        string_value="Search Location"
    )

    # Saved locations list
    locations_list = Widget.objects.create(
        screen=screen,
        widget_type="ListView",
        parent_widget=column,
        order=1,
        widget_id="saved_locations_list"
    )

    WidgetProperty.objects.create(
        widget=locations_list,
        property_name="dataSource",
        property_type="data_source_field_reference",
        data_source_field_reference=DataSourceField.objects.get(
            data_source=data_sources['locations'],
            field_name="name"
        )
    )


def create_weather_maps_screen_widgets(screen, data_sources, actions):
    """Create widgets for weather maps screen"""
    column = Widget.objects.create(
        screen=screen,
        widget_type="Column",
        order=0,
        widget_id="maps_column"
    )

    # Map type selector
    selector_row = Widget.objects.create(
        screen=screen,
        widget_type="Row",
        parent_widget=column,
        order=0,
        widget_id="map_selector_row"
    )

    WidgetProperty.objects.create(
        widget=selector_row,
        property_name="mainAxisAlignment",
        property_type="string",
        string_value="spaceEvenly"
    )

    map_types = ["Radar", "Satellite", "Temperature", "Precipitation"]
    for i, map_type in enumerate(map_types):
        btn = Widget.objects.create(
            screen=screen,
            widget_type="ElevatedButton",
            parent_widget=selector_row,
            order=i,
            widget_id=f"map_btn_{map_type.lower()}"
        )

        WidgetProperty.objects.create(
            widget=btn,
            property_name="text",
            property_type="string",
            string_value=map_type
        )

    # Map container (placeholder)
    map_container = Widget.objects.create(
        screen=screen,
        widget_type="Expanded",
        parent_widget=column,
        order=1,
        widget_id="map_container"
    )

    WidgetProperty.objects.create(
        widget=map_container,
        property_name="flex",
        property_type="integer",
        integer_value=1
    )

    map_placeholder = Widget.objects.create(
        screen=screen,
        widget_type="Container",
        parent_widget=map_container,
        order=0,
        widget_id="map_placeholder"
    )

    WidgetProperty.objects.create(
        widget=map_placeholder,
        property_name="color",
        property_type="color",
        color_value="#E0E0E0"
    )

    map_center = Widget.objects.create(
        screen=screen,
        widget_type="Center",
        parent_widget=map_placeholder,
        order=0,
        widget_id="map_center"
    )

    map_text = Widget.objects.create(
        screen=screen,
        widget_type="Text",
        parent_widget=map_center,
        order=0,
        widget_id="map_text"
    )

    WidgetProperty.objects.create(
        widget=map_text,
        property_name="text",
        property_type="string",
        string_value="Interactive Weather Map"
    )


def create_about_screen_widgets(screen, data_sources, actions):
    """Create widgets for about screen"""
    scroll_view = Widget.objects.create(
        screen=screen,
        widget_type="SingleChildScrollView",
        order=0,
        widget_id="about_scroll"
    )

    column = Widget.objects.create(
        screen=screen,
        widget_type="Column",
        parent_widget=scroll_view,
        order=0,
        widget_id="about_column"
    )

    # App logo and version
    logo_container = Widget.objects.create(
        screen=screen,
        widget_type="Center",
        parent_widget=column,
        order=0,
        widget_id="about_logo_center"
    )

    logo = Widget.objects.create(
        screen=screen,
        widget_type="Icon",
        parent_widget=logo_container,
        order=0,
        widget_id="about_logo"
    )

    WidgetProperty.objects.create(
        widget=logo,
        property_name="icon",
        property_type="string",
        string_value="cloud"
    )

    WidgetProperty.objects.create(
        widget=logo,
        property_name="size",
        property_type="integer",
        integer_value=80
    )

    WidgetProperty.objects.create(
        widget=logo,
        property_name="color",
        property_type="color",
        color_value="#1976D2"
    )

    # App name
    name_text = Widget.objects.create(
        screen=screen,
        widget_type="Center",
        parent_widget=column,
        order=1,
        widget_id="about_name_center"
    )

    name = Widget.objects.create(
        screen=screen,
        widget_type="Text",
        parent_widget=name_text,
        order=0,
        widget_id="about_name"
    )

    WidgetProperty.objects.create(
        widget=name,
        property_name="text",
        property_type="string",
        string_value="WeatherPro"
    )

    WidgetProperty.objects.create(
        widget=name,
        property_name="fontSize",
        property_type="integer",
        integer_value=24
    )

    # Version
    version_text = Widget.objects.create(
        screen=screen,
        widget_type="Center",
        parent_widget=column,
        order=2,
        widget_id="about_version_center"
    )

    version = Widget.objects.create(
        screen=screen,
        widget_type="Text",
        parent_widget=version_text,
        order=0,
        widget_id="about_version"
    )

    WidgetProperty.objects.create(
        widget=version,
        property_name="text",
        property_type="string",
        string_value="Version 1.0.0"
    )

    # Description
    desc_padding = Widget.objects.create(
        screen=screen,
        widget_type="Padding",
        parent_widget=column,
        order=3,
        widget_id="about_desc_padding"
    )

    WidgetProperty.objects.create(
        widget=desc_padding,
        property_name="padding",
        property_type="integer",
        integer_value=20
    )

    description = Widget.objects.create(
        screen=screen,
        widget_type="Text",
        parent_widget=desc_padding,
        order=0,
        widget_id="about_description"
    )

    WidgetProperty.objects.create(
        widget=description,
        property_name="text",
        property_type="string",
        string_value="WeatherPro provides accurate weather forecasts, interactive maps, and real-time alerts to keep you informed about weather conditions worldwide."
    )


def create_support_screen_widgets(screen, data_sources, actions):
    """Create widgets for support/contact screen"""
    scroll_view = Widget.objects.create(
        screen=screen,
        widget_type="SingleChildScrollView",
        order=0,
        widget_id="support_scroll"
    )

    column = Widget.objects.create(
        screen=screen,
        widget_type="Column",
        parent_widget=scroll_view,
        order=0,
        widget_id="support_column"
    )

    # Contact form
    form_padding = Widget.objects.create(
        screen=screen,
        widget_type="Padding",
        parent_widget=column,
        order=0,
        widget_id="support_form_padding"
    )

    WidgetProperty.objects.create(
        widget=form_padding,
        property_name="padding",
        property_type="integer",
        integer_value=16
    )

    form_column = Widget.objects.create(
        screen=screen,
        widget_type="Column",
        parent_widget=form_padding,
        order=0,
        widget_id="support_form_column"
    )

    # Subject field
    subject_field = Widget.objects.create(
        screen=screen,
        widget_type="TextField",
        parent_widget=form_column,
        order=0,
        widget_id="support_subject"
    )

    WidgetProperty.objects.create(
        widget=subject_field,
        property_name="labelText",
        property_type="string",
        string_value="Subject"
    )

    WidgetProperty.objects.create(
        widget=subject_field,
        property_name="hintText",
        property_type="string",
        string_value="Enter subject..."
    )

    # Spacer
    spacer1 = Widget.objects.create(
        screen=screen,
        widget_type="SizedBox",
        parent_widget=form_column,
        order=1,
        widget_id="support_spacer1"
    )

    WidgetProperty.objects.create(
        widget=spacer1,
        property_name="height",
        property_type="integer",
        integer_value=16
    )

    # Message field
    message_field = Widget.objects.create(
        screen=screen,
        widget_type="TextField",
        parent_widget=form_column,
        order=2,
        widget_id="support_message"
    )

    WidgetProperty.objects.create(
        widget=message_field,
        property_name="labelText",
        property_type="string",
        string_value="Message"
    )

    WidgetProperty.objects.create(
        widget=message_field,
        property_name="hintText",
        property_type="string",
        string_value="Describe your issue..."
    )

    # Send button
    send_btn = Widget.objects.create(
        screen=screen,
        widget_type="ElevatedButton",
        parent_widget=form_column,
        order=3,
        widget_id="support_send_btn"
    )

    WidgetProperty.objects.create(
        widget=send_btn,
        property_name="text",
        property_type="string",
        string_value="Send Message"
    )

    # Contact info
    contact_info = Widget.objects.create(
        screen=screen,
        widget_type="Card",
        parent_widget=column,
        order=1,
        widget_id="support_contact_card"
    )

    WidgetProperty.objects.create(
        widget=contact_info,
        property_name="margin",
        property_type="integer",
        integer_value=16
    )

    contact_column = Widget.objects.create(
        screen=screen,
        widget_type="Column",
        parent_widget=contact_info,
        order=0,
        widget_id="support_contact_column"
    )

    # Email
    email_tile = Widget.objects.create(
        screen=screen,
        widget_type="ListTile",
        parent_widget=contact_column,
        order=0,
        widget_id="support_email_tile"
    )

    WidgetProperty.objects.create(
        widget=email_tile,
        property_name="leading",
        property_type="string",
        string_value="email"
    )

    WidgetProperty.objects.create(
        widget=email_tile,
        property_name="title",
        property_type="string",
        string_value="Email"
    )

    WidgetProperty.objects.create(
        widget=email_tile,
        property_name="subtitle",
        property_type="string",
        string_value="support@weatherpro.com"
    )


def create_payment_screen_widgets(screen, data_sources, actions):
    """Create widgets for payment screen"""
    column = Widget.objects.create(
        screen=screen,
        widget_type="Column",
        order=0,
        widget_id="payment_column"
    )

    # Payment form placeholder
    form_card = Widget.objects.create(
        screen=screen,
        widget_type="Card",
        parent_widget=column,
        order=0,
        widget_id="payment_form_card"
    )

    WidgetProperty.objects.create(
        widget=form_card,
        property_name="margin",
        property_type="integer",
        integer_value=16
    )

    form_column = Widget.objects.create(
        screen=screen,
        widget_type="Column",
        parent_widget=form_card,
        order=0,
        widget_id="payment_form_column"
    )

    # Card number field
    card_field = Widget.objects.create(
        screen=screen,
        widget_type="TextField",
        parent_widget=form_column,
        order=0,
        widget_id="payment_card_number"
    )

    WidgetProperty.objects.create(
        widget=card_field,
        property_name="labelText",
        property_type="string",
        string_value="Card Number"
    )

    WidgetProperty.objects.create(
        widget=card_field,
        property_name="hintText",
        property_type="string",
        string_value="1234 5678 9012 3456"
    )

    # Pay button
    pay_btn = Widget.objects.create(
        screen=screen,
        widget_type="ElevatedButton",
        parent_widget=form_column,
        order=1,
        widget_id="payment_pay_btn"
    )

    WidgetProperty.objects.create(
        widget=pay_btn,
        property_name="text",
        property_type="string",
        string_value="Complete Payment"
    )


def create_register_screen_widgets(screen, data_sources, actions):
    """Create widgets for registration screen"""
    scroll_view = Widget.objects.create(
        screen=screen,
        widget_type="SingleChildScrollView",
        order=0,
        widget_id="register_scroll"
    )

    column = Widget.objects.create(
        screen=screen,
        widget_type="Column",
        parent_widget=scroll_view,
        order=0,
        widget_id="register_column"
    )

    # Form padding
    form_padding = Widget.objects.create(
        screen=screen,
        widget_type="Padding",
        parent_widget=column,
        order=0,
        widget_id="register_form_padding"
    )

    WidgetProperty.objects.create(
        widget=form_padding,
        property_name="padding",
        property_type="integer",
        integer_value=20
    )

    form_column = Widget.objects.create(
        screen=screen,
        widget_type="Column",
        parent_widget=form_padding,
        order=0,
        widget_id="register_form_column"
    )

    # Name field
    name_field = Widget.objects.create(
        screen=screen,
        widget_type="TextField",
        parent_widget=form_column,
        order=0,
        widget_id="register_name"
    )

    WidgetProperty.objects.create(
        widget=name_field,
        property_name="labelText",
        property_type="string",
        string_value="Full Name"
    )

    # Email field
    email_field = Widget.objects.create(
        screen=screen,
        widget_type="TextField",
        parent_widget=form_column,
        order=1,
        widget_id="register_email"
    )

    WidgetProperty.objects.create(
        widget=email_field,
        property_name="labelText",
        property_type="string",
        string_value="Email"
    )

    # Password field
    password_field = Widget.objects.create(
        screen=screen,
        widget_type="TextField",
        parent_widget=form_column,
        order=2,
        widget_id="register_password"
    )

    WidgetProperty.objects.create(
        widget=password_field,
        property_name="labelText",
        property_type="string",
        string_value="Password"
    )

    WidgetProperty.objects.create(
        widget=password_field,
        property_name="obscureText",
        property_type="boolean",
        boolean_value=True
    )

    # Register button
    register_btn = Widget.objects.create(
        screen=screen,
        widget_type="ElevatedButton",
        parent_widget=form_column,
        order=3,
        widget_id="register_submit_btn"
    )

    WidgetProperty.objects.create(
        widget=register_btn,
        property_name="text",
        property_type="string",
        string_value="Create Account"
    )

    WidgetProperty.objects.create(
        widget=register_btn,
        property_name="onPressed",
        property_type="action_reference",
        action_reference=actions["Register User"]
    )

    # Login link
    login_link = Widget.objects.create(
        screen=screen,
        widget_type="TextButton",
        parent_widget=form_column,
        order=4,
        widget_id="register_login_link"
    )

    WidgetProperty.objects.create(
        widget=login_link,
        property_name="text",
        property_type="string",
        string_value="Already have an account? Login"
    )

    WidgetProperty.objects.create(
        widget=login_link,
        property_name="onPressed",
        property_type="action_reference",
        action_reference=actions["Navigate to Login"]
    )


def create_login_screen_widgets(screen, data_sources, actions):
    """Create widgets for login screen"""
    scroll_view = Widget.objects.create(
        screen=screen,
        widget_type="SingleChildScrollView",
        order=0,
        widget_id="login_scroll"
    )

    column = Widget.objects.create(
        screen=screen,
        widget_type="Column",
        parent_widget=scroll_view,
        order=0,
        widget_id="login_column"
    )

    # Logo
    logo_center = Widget.objects.create(
        screen=screen,
        widget_type="Center",
        parent_widget=column,
        order=0,
        widget_id="login_logo_center"
    )

    logo = Widget.objects.create(
        screen=screen,
        widget_type="Icon",
        parent_widget=logo_center,
        order=0,
        widget_id="login_logo"
    )

    WidgetProperty.objects.create(
        widget=logo,
        property_name="icon",
        property_type="string",
        string_value="cloud"
    )

    WidgetProperty.objects.create(
        widget=logo,
        property_name="size",
        property_type="integer",
        integer_value=80
    )

    WidgetProperty.objects.create(
        widget=logo,
        property_name="color",
        property_type="color",
        color_value="#1976D2"
    )

    # Form
    form_padding = Widget.objects.create(
        screen=screen,
        widget_type="Padding",
        parent_widget=column,
        order=1,
        widget_id="login_form_padding"
    )

    WidgetProperty.objects.create(
        widget=form_padding,
        property_name="padding",
        property_type="integer",
        integer_value=20
    )

    form_column = Widget.objects.create(
        screen=screen,
        widget_type="Column",
        parent_widget=form_padding,
        order=0,
        widget_id="login_form_column"
    )

    # Email field
    email_field = Widget.objects.create(
        screen=screen,
        widget_type="TextField",
        parent_widget=form_column,
        order=0,
        widget_id="login_email"
    )

    WidgetProperty.objects.create(
        widget=email_field,
        property_name="labelText",
        property_type="string",
        string_value="Email"
    )

    # Password field
    password_field = Widget.objects.create(
        screen=screen,
        widget_type="TextField",
        parent_widget=form_column,
        order=1,
        widget_id="login_password"
    )

    WidgetProperty.objects.create(
        widget=password_field,
        property_name="labelText",
        property_type="string",
        string_value="Password"
    )

    WidgetProperty.objects.create(
        widget=password_field,
        property_name="obscureText",
        property_type="boolean",
        boolean_value=True
    )

    # Login button
    login_btn = Widget.objects.create(
        screen=screen,
        widget_type="ElevatedButton",
        parent_widget=form_column,
        order=2,
        widget_id="login_submit_btn"
    )

    WidgetProperty.objects.create(
        widget=login_btn,
        property_name="text",
        property_type="string",
        string_value="Sign In"
    )

    WidgetProperty.objects.create(
        widget=login_btn,
        property_name="onPressed",
        property_type="action_reference",
        action_reference=actions["Login User"]
    )

    # Forgot password link
    forgot_link = Widget.objects.create(
        screen=screen,
        widget_type="TextButton",
        parent_widget=form_column,
        order=3,
        widget_id="login_forgot_link"
    )

    WidgetProperty.objects.create(
        widget=forgot_link,
        property_name="text",
        property_type="string",
        string_value="Forgot Password?"
    )

    WidgetProperty.objects.create(
        widget=forgot_link,
        property_name="onPressed",
        property_type="action_reference",
        action_reference=actions["Navigate to Forgot Password"]
    )

    # Register link
    register_link = Widget.objects.create(
        screen=screen,
        widget_type="TextButton",
        parent_widget=form_column,
        order=4,
        widget_id="login_register_link"
    )

    WidgetProperty.objects.create(
        widget=register_link,
        property_name="text",
        property_type="string",
        string_value="Don't have an account? Register"
    )

    WidgetProperty.objects.create(
        widget=register_link,
        property_name="onPressed",
        property_type="action_reference",
        action_reference=actions["Navigate to Register"]
    )


def create_forgot_password_screen_widgets(screen, data_sources, actions):
    """Create widgets for forgot password screen"""
    column = Widget.objects.create(
        screen=screen,
        widget_type="Column",
        order=0,
        widget_id="forgot_column"
    )

    # Instructions
    instructions_padding = Widget.objects.create(
        screen=screen,
        widget_type="Padding",
        parent_widget=column,
        order=0,
        widget_id="forgot_instructions_padding"
    )

    WidgetProperty.objects.create(
        widget=instructions_padding,
        property_name="padding",
        property_type="integer",
        integer_value=20
    )

    instructions = Widget.objects.create(
        screen=screen,
        widget_type="Text",
        parent_widget=instructions_padding,
        order=0,
        widget_id="forgot_instructions"
    )

    WidgetProperty.objects.create(
        widget=instructions,
        property_name="text",
        property_type="string",
        string_value="Enter your email address and we'll send you a link to reset your password."
    )

    # Email field
    email_field = Widget.objects.create(
        screen=screen,
        widget_type="TextField",
        parent_widget=column,
        order=1,
        widget_id="forgot_email"
    )

    WidgetProperty.objects.create(
        widget=email_field,
        property_name="labelText",
        property_type="string",
        string_value="Email Address"
    )

    # Send button
    send_btn = Widget.objects.create(
        screen=screen,
        widget_type="ElevatedButton",
        parent_widget=column,
        order=2,
        widget_id="forgot_send_btn"
    )

    WidgetProperty.objects.create(
        widget=send_btn,
        property_name="text",
        property_type="string",
        string_value="Send Reset Link"
    )


def create_change_password_screen_widgets(screen, data_sources, actions):
    """Create widgets for change password screen"""
    column = Widget.objects.create(
        screen=screen,
        widget_type="Column",
        order=0,
        widget_id="change_password_column"
    )

    form_padding = Widget.objects.create(
        screen=screen,
        widget_type="Padding",
        parent_widget=column,
        order=0,
        widget_id="change_password_padding"
    )

    WidgetProperty.objects.create(
        widget=form_padding,
        property_name="padding",
        property_type="integer",
        integer_value=20
    )

    form_column = Widget.objects.create(
        screen=screen,
        widget_type="Column",
        parent_widget=form_padding,
        order=0,
        widget_id="change_password_form"
    )

    # Current password field
    current_field = Widget.objects.create(
        screen=screen,
        widget_type="TextField",
        parent_widget=form_column,
        order=0,
        widget_id="current_password"
    )

    WidgetProperty.objects.create(
        widget=current_field,
        property_name="labelText",
        property_type="string",
        string_value="Current Password"
    )

    WidgetProperty.objects.create(
        widget=current_field,
        property_name="obscureText",
        property_type="boolean",
        boolean_value=True
    )

    # New password field
    new_field = Widget.objects.create(
        screen=screen,
        widget_type="TextField",
        parent_widget=form_column,
        order=1,
        widget_id="new_password"
    )

    WidgetProperty.objects.create(
        widget=new_field,
        property_name="labelText",
        property_type="string",
        string_value="New Password"
    )

    WidgetProperty.objects.create(
        widget=new_field,
        property_name="obscureText",
        property_type="boolean",
        boolean_value=True
    )

    # Confirm password field
    confirm_field = Widget.objects.create(
        screen=screen,
        widget_type="TextField",
        parent_widget=form_column,
        order=2,
        widget_id="confirm_password"
    )

    WidgetProperty.objects.create(
        widget=confirm_field,
        property_name="labelText",
        property_type="string",
        string_value="Confirm New Password"
    )

    WidgetProperty.objects.create(
        widget=confirm_field,
        property_name="obscureText",
        property_type="boolean",
        boolean_value=True
    )

    # Change button
    change_btn = Widget.objects.create(
        screen=screen,
        widget_type="ElevatedButton",
        parent_widget=form_column,
        order=3,
        widget_id="change_password_btn"
    )

    WidgetProperty.objects.create(
        widget=change_btn,
        property_name="text",
        property_type="string",
        string_value="Update Password"
    )