from django.db import models
from django.core.validators import RegexValidator
from colorfield.fields import ColorField
import uuid
import os


class Theme(models.Model):
    """Visual styling configuration for Flutter applications"""
    
    name = models.CharField(
        max_length=100,
        verbose_name="Theme Name",
        help_text="A descriptive name for this color scheme (e.g., 'Blue Ocean', 'Dark Mode')"
    )
    primary_color = ColorField(
        default='#2196F3',
        verbose_name="Main Color",
        help_text="The primary color used for buttons, headers, and main elements"
    )
    accent_color = ColorField(
        default='#FF4081',
        verbose_name="Accent Color", 
        help_text="Secondary color used for highlights and special elements"
    )
    background_color = ColorField(
        default='#FFFFFF',
        verbose_name="Background Color",
        help_text="Main background color of the app"
    )
    text_color = ColorField(
        default='#000000',
        verbose_name="Text Color",
        help_text="Default color for text throughout the app"
    )
    font_family = models.CharField(
        max_length=50,
        default='Roboto',
        verbose_name="Font Style",
        help_text="The font family to use throughout the app"
    )
    is_dark_mode = models.BooleanField(
        default=False,
        verbose_name="Dark Mode",
        help_text="Enable dark mode styling"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "App Theme"
        verbose_name_plural = "App Themes"

    def __str__(self):
        return self.name


class Application(models.Model):
    """Represents a complete Flutter application"""
    
    BUILD_STATUS_CHOICES = [
        ('not_built', 'Not Built Yet'),
        ('building', 'Currently Building'),
        ('success', 'Build Successful'),
        ('failed', 'Build Failed'),
    ]
    
    name = models.CharField(
        max_length=100,
        verbose_name="App Name",
        help_text="The display name of your app (e.g., 'My Shopping App')"
    )
    description = models.TextField(
        blank=True,
        verbose_name="App Description",
        help_text="A brief description of what your app does"
    )
    package_name = models.CharField(
        max_length=100,
        unique=True,
        validators=[RegexValidator(
            regex=r'^[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*)*$',
            message='Package name must be in format: com.company.appname (lowercase letters, numbers, dots, underscores only)'
        )],
        verbose_name="Package Identifier",
        help_text="Unique identifier for your app (e.g., 'com.mycompany.myapp'). This cannot be changed after creation."
    )
    version = models.CharField(
        max_length=20,
        default='1.0.0',
        verbose_name="App Version",
        help_text="Version number of your app (e.g., '1.0.0', '2.1.3')"
    )
    theme = models.ForeignKey(
        Theme,
        on_delete=models.CASCADE,
        verbose_name="App Theme",
        help_text="Choose the color scheme and styling for your app"
    )
    build_status = models.CharField(
        max_length=20,
        choices=BUILD_STATUS_CHOICES,
        default='not_built',
        verbose_name="Build Status"
    )
    apk_file = models.FileField(
        upload_to='apks/',
        blank=True,
        null=True,
        verbose_name="APK File",
        help_text="The built Android app file (APK)"
    )
    source_code_zip = models.FileField(
        upload_to='source_zips/',
        blank=True,
        null=True,
        verbose_name="Source Code ZIP",
        help_text="ZIP file containing the Flutter project source code"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Flutter Application"
        verbose_name_plural = "Flutter Applications"

    def __str__(self):
        return self.name


class DataSource(models.Model):
    """External data sources for dynamic content"""
    
    DATA_SOURCE_TYPES = [
        ('REST_API', 'REST API (Web Service)'),
    ]

    # Add this field to make base_url optional/configurable
    use_dynamic_base_url = models.BooleanField(
        default=False,
        verbose_name="Use Dynamic Base URL",
        help_text="If enabled, the base URL can be configured from the app's Configuration screen"
    )
    
    HTTP_METHODS = [
        ('GET', 'GET (Retrieve Data)'),
        ('POST', 'POST (Send Data)'),
        ('PUT', 'PUT (Update Data)'),
        ('DELETE', 'DELETE (Remove Data)'),
    ]
    
    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name='data_sources',
        verbose_name="Application"
    )
    name = models.CharField(
        max_length=100,
        verbose_name="Data Source Name",
        help_text="A descriptive name for this data source (e.g., 'Product List', 'User Profile')"
    )
    data_source_type = models.CharField(
        max_length=20,
        choices=DATA_SOURCE_TYPES,
        default='REST_API',
        verbose_name="Data Source Type",
        help_text="How your app will get the data"
    )
    base_url = models.URLField(
        blank=True,
        verbose_name="API Base URL",
        help_text="The main web address for your data (e.g., 'https://api.mystore.com')"
    )
    endpoint = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="API Endpoint",
        help_text="The specific path to get data (e.g., '/products', '/users/profile')"
    )
    method = models.CharField(
        max_length=10,
        choices=HTTP_METHODS,
        default='GET',
        verbose_name="Request Method",
        help_text="How to request the data from the server"
    )
    headers = models.TextField(
        blank=True,
        verbose_name="Request Headers",
        help_text="Additional information to send with requests (one per line, format: 'Key: Value')"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Data Source"
        verbose_name_plural = "Data Sources"
        unique_together = ['application', 'name']

    def __str__(self):
        return f"{self.application.name} - {self.name}"


class DataSourceField(models.Model):
    """Individual fields available from a data source"""
    
    FIELD_TYPES = [
        ('string', 'Text'),
        ('integer', 'Number (Whole)'),
        ('decimal', 'Number (Decimal)'),
        ('boolean', 'True/False'),
        ('date', 'Date'),
        ('datetime', 'Date and Time'),
        ('url', 'Web Address (URL)'),
        ('image_url', 'Image Web Address'),
        ('email', 'Email Address'),
    ]
    
    data_source = models.ForeignKey(
        DataSource,
        on_delete=models.CASCADE,
        related_name='fields',
        verbose_name="Data Source"
    )
    field_name = models.CharField(
        max_length=100,
        verbose_name="Field Name",
        help_text="The name of this data field (e.g., 'product_name', 'price', 'description')"
    )
    field_type = models.CharField(
        max_length=20,
        choices=FIELD_TYPES,
        verbose_name="Field Type",
        help_text="What type of information this field contains"
    )
    display_name = models.CharField(
        max_length=100,
        verbose_name="Display Name",
        help_text="Human-readable name for this field (e.g., 'Product Name', 'Price')"
    )
    is_required = models.BooleanField(
        default=False,
        verbose_name="Required Field",
        help_text="Is this field always present in the data?"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Data Field"
        verbose_name_plural = "Data Fields"
        unique_together = ['data_source', 'field_name']

    def __str__(self):
        return f"{self.data_source.name} - {self.display_name}"


class Screen(models.Model):
    """Represents a single screen/page in the Flutter application"""
    
    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name='screens',
        verbose_name="Application"
    )
    name = models.CharField(
        max_length=100,
        verbose_name="Screen Name",
        help_text="A descriptive name for this screen (e.g., 'Home Page', 'Product List', 'Settings')"
    )
    route_name = models.CharField(
        max_length=100,
        verbose_name="Screen Route",
        help_text="Internal navigation name (e.g., '/home', '/products', '/settings'). Must start with '/'"
    )
    is_home_screen = models.BooleanField(
        default=False,
        verbose_name="Home Screen",
        help_text="Is this the first screen users see when they open the app?"
    )
    app_bar_title = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Top Bar Title",
        help_text="Text shown in the top bar of this screen"
    )
    show_app_bar = models.BooleanField(
        default=True,
        verbose_name="Show Top Bar",
        help_text="Should this screen have a top bar with title and navigation?"
    )
    show_back_button = models.BooleanField(
        default=True,
        verbose_name="Show Back Button",
        help_text="Should users be able to go back to the previous screen?"
    )
    background_color = ColorField(
        blank=True,
        null=True,
        verbose_name="Background Color",
        help_text="Custom background color for this screen (leave empty to use theme default)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "App Screen"
        verbose_name_plural = "App Screens"
        unique_together = ['application', 'route_name']

    def __str__(self):
        return f"{self.application.name} - {self.name}"


class Widget(models.Model):
    """Represents individual Flutter widgets/components"""
    
    WIDGET_TYPES = [
        # Layout Widgets
        ('Column', 'Vertical Layout (Column)'),
        ('Row', 'Horizontal Layout (Row)'),
        ('Container', 'Container (Box)'),
        ('Padding', 'Padding (Spacing)'),
        ('Center', 'Center Alignment'),
        ('Expanded', 'Expanded (Fill Space)'),
        ('Flexible', 'Flexible (Adjust Size)'),
        ('Wrap', 'Wrap (Flow Layout)'),
        ('Stack', 'Stack (Layered)'),
        ('Positioned', 'Positioned (Absolute)'),
        
        # Display Widgets
        ('Text', 'Text'),
        ('Image', 'Image'),
        ('Icon', 'Icon'),
        ('Divider', 'Divider Line'),
        ('Card', 'Card'),
        ('ListTile', 'List Item'),
        
        # Input Widgets
        ('TextField', 'Text Input'),
        ('ElevatedButton', 'Raised Button'),
        ('TextButton', 'Text Button'),
        ('IconButton', 'Icon Button'),
        ('FloatingActionButton', 'Floating Action Button'),
        ('Switch', 'On/Off Switch'),
        ('Checkbox', 'Checkbox'),
        ('Radio', 'Radio Button'),
        ('Slider', 'Slider'),
        ('DropdownButton', 'Dropdown Menu'),
        
        # Scrollable Widgets
        ('ListView', 'Scrollable List'),
        ('GridView', 'Grid Layout'),
        ('SingleChildScrollView', 'Scrollable Area'),
        ('PageView', 'Page Swiper'),
        
        # Navigation Widgets
        ('AppBar', 'Top Navigation Bar'),
        ('BottomNavigationBar', 'Bottom Navigation'),
        ('TabBar', 'Tab Bar'),
        ('Drawer', 'Side Menu'),
        
        # Special Widgets
        ('Scaffold', 'Screen Structure'),
        ('SafeArea', 'Safe Area'),
        ('SizedBox', 'Fixed Size Box'),
        ('AspectRatio', 'Aspect Ratio'),
        ('FutureBuilder', 'Data Loader'),
        ('StreamBuilder', 'Live Data Stream'),
    ]
    
    screen = models.ForeignKey(
        Screen,
        on_delete=models.CASCADE,
        related_name='widgets',
        verbose_name="Screen"
    )
    widget_type = models.CharField(
        max_length=50,
        choices=WIDGET_TYPES,
        verbose_name="Widget Type",
        help_text="What type of element do you want to add?"
    )
    parent_widget = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='child_widgets',
        verbose_name="Parent Widget",
        help_text="Which widget should contain this widget? (leave empty for root level)"
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Display Order",
        help_text="Order in which this widget appears (0 = first, 1 = second, etc.)"
    )
    widget_id = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Widget ID",
        help_text="Unique identifier for this widget (used for actions and data binding)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Widget"
        verbose_name_plural = "Widgets"
        ordering = ['order']

    def __str__(self):
        return f"{self.screen.name} - {self.widget_type} ({self.order})"


class WidgetProperty(models.Model):
    """Properties/attributes for widgets"""

    PROPERTY_TYPES = [
        ('string', 'Text'),
        ('integer', 'Number (Whole)'),
        ('decimal', 'Number (Decimal)'),
        ('boolean', 'True/False'),
        ('color', 'Color'),
        ('icon', 'Icon'),
        ('alignment', 'Alignment'),
        ('action_reference', 'Action (What Happens)'),
        ('data_source_field_reference', 'Data Field'),
        ('screen_reference', 'Screen Navigation'),
        ('asset_reference', 'Image/File'),
        ('url', 'Web Address'),
        ('json', 'Complex Data'),
        # New property types for marketplace
        ('file_upload', 'File Upload'),
        ('date_picker', 'Date Picker'),
        ('time_picker', 'Time Picker'),
        ('map_location', 'Map Location'),
        ('rich_text', 'Rich Text Editor'),
    ]
    
    ALIGNMENT_CHOICES = [
        ('center', 'Center'),
        ('left', 'Left'),
        ('right', 'Right'),
        ('top', 'Top'),
        ('bottom', 'Bottom'),
        ('topLeft', 'Top Left'),
        ('topRight', 'Top Right'),
        ('bottomLeft', 'Bottom Left'),
        ('bottomRight', 'Bottom Right'),
    ]
    
    widget = models.ForeignKey(
        Widget,
        on_delete=models.CASCADE,
        related_name='properties',
        verbose_name="Widget"
    )
    property_name = models.CharField(
        max_length=100,
        verbose_name="Property Name",
        help_text="What aspect of the widget are you configuring? (e.g., 'text', 'color', 'onPressed')"
    )
    property_type = models.CharField(
        max_length=30,
        choices=PROPERTY_TYPES,
        verbose_name="Property Type",
        help_text="What type of value does this property need?"
    )
    
    # Value fields for different types
    string_value = models.TextField(
        blank=True,
        verbose_name="Text Value",
        help_text="Enter the text content"
    )
    integer_value = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Number Value",
        help_text="Enter a whole number"
    )
    decimal_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Decimal Value",
        help_text="Enter a decimal number"
    )
    boolean_value = models.BooleanField(
        default=False,
        verbose_name="True/False Value"
    )
    color_value = ColorField(
        blank=True,
        null=True,
        verbose_name="Color Value",
        help_text="Choose a color"
    )
    alignment_value = models.CharField(
        max_length=20,
        choices=ALIGNMENT_CHOICES,
        blank=True,
        verbose_name="Alignment Value"
    )
    url_value = models.URLField(
        blank=True,
        verbose_name="URL Value",
        help_text="Enter a web address"
    )
    json_value = models.TextField(
        blank=True,
        verbose_name="JSON Value",
        help_text="Enter JSON data"
    )
    
    # Reference fields
    action_reference = models.ForeignKey(
        'Action',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Action Reference",
        help_text="What action should happen?"
    )
    data_source_field_reference = models.ForeignKey(
        DataSourceField,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Data Field Reference",
        help_text="Which data field should be displayed?"
    )
    screen_reference = models.ForeignKey(
        Screen,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Screen Reference",
        help_text="Which screen should be opened?"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Widget Property"
        verbose_name_plural = "Widget Properties"
        unique_together = ['widget', 'property_name']

    def __str__(self):
        return f"{self.widget} - {self.property_name}"

    def get_value(self):
        """Return the appropriate value based on property_type"""
        if self.property_type == 'string':
            return self.string_value
        elif self.property_type == 'integer':
            return self.integer_value
        elif self.property_type == 'decimal':
            return self.decimal_value
        elif self.property_type == 'boolean':
            return self.boolean_value
        elif self.property_type == 'color':
            return self.color_value
        elif self.property_type == 'alignment':
            return self.alignment_value
        elif self.property_type == 'url':
            return self.url_value
        elif self.property_type == 'json':
            return self.json_value
        elif self.property_type == 'action_reference':
            return self.action_reference
        elif self.property_type == 'data_source_field_reference':
            return self.data_source_field_reference
        elif self.property_type == 'screen_reference':
            return self.screen_reference
        return None


class Action(models.Model):
    """Defines dynamic behaviors and interactions"""
    
    ACTION_TYPES = [
        ('navigate', 'Navigate to Screen'),
        ('navigate_back', 'Go Back'),
        ('api_call', 'Call Web Service'),
        ('show_dialog', 'Show Popup Message'),
        ('show_snackbar', 'Show Bottom Message'),
        ('open_url', 'Open Web Page'),
        ('send_email', 'Send Email'),
        ('make_phone_call', 'Make Phone Call'),
        ('share_content', 'Share Content'),
        ('take_photo', 'Take Photo'),
        ('pick_image', 'Pick Image from Gallery'),
        ('save_data', 'Save Data Locally'),
        ('load_data', 'Load Saved Data'),
        ('refresh_data', 'Refresh Data'),
        ('submit_form', 'Submit Form'),
        ('validate_form', 'Validate Form'),
        ('clear_form', 'Clear Form'),
        ('toggle_visibility', 'Show/Hide Element'),
        ('play_sound', 'Play Sound'),
        ('vibrate', 'Vibrate Device'),
    ]
    
    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name='actions',
        verbose_name="Application"
    )
    name = models.CharField(
        max_length=100,
        verbose_name="Action Name",
        help_text="A descriptive name for this action (e.g., 'Go to Product Details', 'Submit Order')"
    )
    action_type = models.CharField(
        max_length=30,
        choices=ACTION_TYPES,
        verbose_name="Action Type",
        help_text="What should happen when this action is triggered?"
    )
    
    # Navigation parameters
    target_screen = models.ForeignKey(
        Screen,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Target Screen",
        help_text="Which screen to navigate to (for navigation actions)"
    )
    
    # API call parameters
    api_data_source = models.ForeignKey(
        DataSource,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="API Data Source",
        help_text="Which data source to call (for API actions)"
    )
    
    # General parameters
    parameters = models.TextField(
        blank=True,
        verbose_name="Action Parameters",
        help_text="Additional parameters for this action (JSON format)"
    )
    
    # Dialog/Message parameters
    dialog_title = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Dialog Title",
        help_text="Title for popup messages"
    )
    dialog_message = models.TextField(
        blank=True,
        verbose_name="Dialog Message",
        help_text="Content for popup messages"
    )
    
    # URL parameters
    url = models.URLField(
        blank=True,
        verbose_name="URL",
        help_text="Web address for URL-based actions"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Action"
        verbose_name_plural = "Actions"
        unique_together = ['application', 'name']

    def __str__(self):
        return f"{self.application.name} - {self.name}"


class BuildHistory(models.Model):
    """Tracks build attempts and their results"""
    
    BUILD_STATUS_CHOICES = [
        ('started', 'Build Started'),
        ('generating_code', 'Generating Flutter Code'),
        ('code_generated', 'Code Generated Successfully'),
        ('code_generation_failed', 'Code Generation Failed'),
        ('building_apk', 'Building APK'),
        ('success', 'Build Completed Successfully'),
        ('failed', 'Build Failed'),
    ]
    
    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name='build_history',
        verbose_name="Application"
    )
    build_id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        verbose_name="Build ID"
    )
    status = models.CharField(
        max_length=30,
        choices=BUILD_STATUS_CHOICES,
        default='started',
        verbose_name="Build Status"
    )
    build_start_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Build Started"
    )
    build_end_time = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Build Completed"
    )
    log_output = models.TextField(
        blank=True,
        verbose_name="Build Logs",
        help_text="Detailed logs from the build process"
    )
    error_message = models.TextField(
        blank=True,
        verbose_name="Error Message",
        help_text="Error details if build failed"
    )
    apk_file = models.FileField(
        upload_to='build_apks/',
        blank=True,
        null=True,
        verbose_name="Generated APK"
    )
    source_code_zip = models.FileField(
        upload_to='build_source_zips/',
        blank=True,
        null=True,
        verbose_name="Generated Source Code"
    )
    apk_size_mb = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="APK Size (MB)"
    )

    class Meta:
        verbose_name = "Build History"
        verbose_name_plural = "Build History"
        ordering = ['-build_start_time']

    def __str__(self):
        return f"{self.application.name} - Build {self.build_id.hex[:8]} ({self.status})"

    @property
    def duration(self):
        """Calculate build duration"""
        if self.build_end_time and self.build_start_time:
            return self.build_end_time - self.build_start_time
        return None

    @property
    def duration_seconds(self):
        """Get duration in seconds"""
        duration = self.duration
        if duration:
            return duration.total_seconds()
        return None


class CustomPubDevWidget(models.Model):
    """Custom widgets from pub.dev packages"""
    
    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name='custom_widgets',
        verbose_name="Application"
    )
    package_name = models.CharField(
        max_length=100,
        verbose_name="Package Name",
        help_text="Name of the pub.dev package (e.g., 'flutter_staggered_grid_view')"
    )
    package_version = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Package Version",
        help_text="Specific version to use (leave empty for latest)"
    )
    widget_class_name = models.CharField(
        max_length=100,
        verbose_name="Widget Class Name",
        help_text="Name of the widget class from the package (e.g., 'StaggeredGridView')"
    )
    import_statement = models.CharField(
        max_length=200,
        verbose_name="Import Statement",
        help_text="Full import statement (e.g., 'package:flutter_staggered_grid_view/flutter_staggered_grid_view.dart')"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Description",
        help_text="What does this widget do?"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Active",
        help_text="Is this widget available for use?"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Custom Widget (pub.dev)"
        verbose_name_plural = "Custom Widgets (pub.dev)"
        unique_together = ['application', 'package_name', 'widget_class_name']

    def __str__(self):
        return f"{self.application.name} - {self.widget_class_name}"