# Flutter App Builder - Technical Manual

## Overview

Flutter App Builder is a comprehensive no-code platform for generating Flutter applications. The system uses Django as the backend with a sophisticated database schema to represent every aspect of a Flutter application, from UI components to data sources and user interactions.

## Architecture

### System Components

1. **Django Backend**: Core application logic, database models, and admin interface
2. **Code Generation Engine**: Converts database configuration to Flutter Dart code
3. **Build Service**: Handles APK compilation (requires external build server)
4. **Admin Interface**: Customized Django admin for non-technical users

### Technology Stack

- **Backend**: Django 4.2.7, Python 3.8+
- **Database**: SQLite (development), PostgreSQL (production recommended)
- **Frontend**: Django Admin with custom templates and CSS
- **Generated Apps**: Flutter 3.0+, Dart
- **Dependencies**: See `requirements.txt`

## Database Schema

### Core Models

#### Application Model
Represents a complete Flutter application with metadata, build status, and file references.

```python
class Application(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    package_name = models.CharField(max_length=100, unique=True)
    version = models.CharField(max_length=20, default='1.0.0')
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)
    build_status = models.CharField(max_length=20, choices=BUILD_STATUS_CHOICES)
    apk_file = models.FileField(upload_to='apks/', blank=True, null=True)
    source_code_zip = models.FileField(upload_to='source_zips/', blank=True, null=True)
```

#### Widget Model
The most critical model for dynamism. Represents individual Flutter widgets with hierarchical relationships.

```python
class Widget(models.Model):
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE)
    widget_type = models.CharField(max_length=50, choices=WIDGET_TYPES)
    parent_widget = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    widget_id = models.CharField(max_length=100, blank=True)
```

#### WidgetProperty Model
Stores individual properties for widgets without using JSON fields, maintaining full relational integrity.

```python
class WidgetProperty(models.Model):
    widget = models.ForeignKey(Widget, on_delete=models.CASCADE)
    property_name = models.CharField(max_length=100)
    property_type = models.CharField(max_length=30, choices=PROPERTY_TYPES)
    
    # Type-specific value fields
    string_value = models.TextField(blank=True)
    integer_value = models.IntegerField(blank=True, null=True)
    boolean_value = models.BooleanField(default=False)
    color_value = ColorField(blank=True, null=True)
    # ... other value fields
    
    # Reference fields
    action_reference = models.ForeignKey('Action', on_delete=models.CASCADE, blank=True, null=True)
    data_source_field_reference = models.ForeignKey(DataSourceField, on_delete=models.CASCADE, blank=True, null=True)
    screen_reference = models.ForeignKey(Screen, on_delete=models.CASCADE, blank=True, null=True)
```

### Data Management Models

#### DataSource Model
Defines external data sources (REST APIs, static JSON) with full configuration.

#### DataSourceField Model
Defines individual fields available from data sources, enabling type-safe data binding.

#### Action Model
Defines dynamic behaviors and interactions with comprehensive parameter support.

### Build Management

#### BuildHistory Model
Tracks all build attempts with detailed logging, timing, and file management.

## Code Generation Engine

### FlutterCodeGenerator Class

Located in `core/services/code_generator.py`, this class handles the complete transformation from database configuration to Flutter source code.

#### Key Methods

```python
def generate_project(self):
    """Generate complete Flutter project"""
    self._create_project_structure()
    self._generate_pubspec_yaml()
    self._generate_main_dart()
    self._generate_theme()
    self._generate_routes()
    self._generate_screens()
    self._generate_services()
    self._generate_models()
    self._generate_widgets()
```

#### Widget Code Generation

The system recursively traverses the widget hierarchy and generates appropriate Dart code:

```python
def _generate_widget_code(self, widget, indent_level):
    """Generate Dart code for a widget"""
    # Get widget properties
    properties = WidgetProperty.objects.filter(widget=widget)
    prop_dict = {prop.property_name: prop for prop in properties}
    
    # Get child widgets
    child_widgets = Widget.objects.filter(parent_widget=widget).order_by('order')
    
    # Generate widget-specific code based on widget_type
    if widget.widget_type == 'Text':
        # Handle text widgets with dynamic content
    elif widget.widget_type == 'ElevatedButton':
        # Handle buttons with actions
    # ... other widget types
```

#### Dynamic Features

1. **Data Binding**: Automatically generates `FutureBuilder` patterns for API data
2. **Action Handling**: Converts action references to appropriate Dart callbacks
3. **Navigation**: Generates route-based navigation with parameter passing
4. **Theming**: Creates comprehensive theme configurations
5. **API Services**: Generates service classes for data source interactions

### Pub.dev Integration

The system supports dynamic integration of pub.dev packages:

```python
# Add custom widget dependencies to pubspec.yaml
custom_widgets = CustomPubDevWidget.objects.filter(application=self.application, is_active=True)
for widget in custom_widgets:
    dependencies[widget.package_name] = f"^{widget.package_version}" if widget.package_version else 'any'
```

## Build Service

### BuildService Class

Located in `core/services/build_service.py`, handles the APK build process.

#### Build Process Flow

1. **Code Generation**: Generate Flutter source code
2. **Project Packaging**: Create ZIP file of Flutter project
3. **Build Server Communication**: Send project to build server
4. **APK Retrieval**: Download and store generated APK
5. **Build History**: Log all build attempts and results

#### Build Server Integration

The system is designed to work with an external Flutter build server:

```python
def _send_to_build_server(self, project_zip_path, application, build_history):
    """Send project to build server"""
    build_endpoint = f"{self.build_server_url}/api/build"
    
    with open(project_zip_path, 'rb') as zip_file:
        files = {'project': zip_file}
        data = {
            'package_name': application.package_name,
            'app_name': application.name,
            'version': application.version,
            'build_id': str(build_history.build_id),
        }
        
        response = requests.post(build_endpoint, files=files, data=data, headers=headers, timeout=300)
```

## Admin Interface Customization

### Custom Admin Classes

The Django admin is heavily customized for non-technical users:

#### ApplicationAdmin

```python
@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    actions = ['generate_flutter_code', 'build_apk', 'create_sample_ecommerce']
    
    def generate_flutter_code(self, request, queryset):
        """Generate Flutter source code for selected applications"""
        for app in queryset:
            generator = FlutterCodeGenerator(app)
            success, message = generator.generate_project()
```

#### Inline Management

Extensive use of Django inlines for hierarchical editing:

```python
class WidgetPropertyInline(admin.StackedInline):
    model = WidgetProperty
    extra = 0
    
    def get_formset(self, request, obj=None, **kwargs):
        # Filter references based on application context
        formset = super().get_formset(request, obj, **kwargs)
        if obj and obj.screen:
            application = obj.screen.application
            formset.form.base_fields['action_reference'].queryset = Action.objects.filter(application=application)
```

### Custom Actions and Views

The admin includes custom actions for:
- Code generation
- APK building
- Sample app creation
- File downloads
- Build status monitoring

## Sample Application Generation

### Management Commands

The system includes Django management commands for creating sample applications:

```bash
python manage.py create_sample_app ecommerce --name "My Store"
python manage.py create_sample_app social_media --name "My Social App"
python manage.py create_sample_app news --name "My News App"
```

### Sample App Functions

Located in `core/management/commands/create_sample_app.py`:

```python
def create_ecommerce_app(custom_name=None):
    """Create a comprehensive e-commerce application"""
    # Create theme, application, data sources, screens, widgets, actions
    # Demonstrates complex app structure with:
    # - Product catalog with API integration
    # - Shopping cart functionality
    # - User authentication flows
    # - Order management
    # - Search and filtering
```

Each sample app creates a complete, functional application structure that demonstrates the platform's capabilities.

## Development Setup

### Prerequisites

- Python 3.8+
- Django 4.2.7
- SQLite (development) or PostgreSQL (production)

### Installation

```bash
# Clone repository
git clone <repository-url>
cd flutter-app-builder

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### Environment Variables

Create a `.env` file:

```env
SECRET_KEY=your-secret-key
DEBUG=True
BUILD_SERVER_URL=http://localhost:8001
BUILD_SERVER_API_KEY=your-build-server-api-key
```

## Extending the Platform

### Adding New Widget Types

1. **Update Widget Model**: Add new widget type to `WIDGET_TYPES` choices
2. **Update Code Generator**: Add handling in `_generate_widget_code()` method
3. **Update Admin**: Add help text and property suggestions

```python
# In models.py
WIDGET_TYPES = [
    # ... existing types
    ('CustomWidget', 'My Custom Widget'),
]

# In code_generator.py
elif widget.widget_type == 'CustomWidget':
    # Generate custom widget code
    widget_code = f"CustomWidget({self._generate_properties(prop_dict)})"
```

### Adding New Action Types

1. **Update Action Model**: Add to `ACTION_TYPES` choices
2. **Update Code Generator**: Add handling in `_generate_action_code()` method
3. **Update Admin**: Add relevant form fields

### Adding New Data Source Types

1. **Update DataSource Model**: Add to `DATA_SOURCE_TYPES` choices
2. **Update API Service Generator**: Add handling in `_generate_services()` method
3. **Test with sample data**

## Production Deployment

### Database Configuration

For production, use PostgreSQL:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'flutter_app_builder',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Build Server Setup

The platform requires a separate build server with:
- Flutter SDK installed
- Android SDK configured
- API endpoints for receiving projects and returning APKs
- Proper security and authentication

### Scaling Considerations

#### Horizontal Scaling
- Use load balancers for Django instances
- Separate build servers for different regions
- CDN for APK and source code distribution

#### Vertical Scaling
- Database optimization with proper indexing
- Caching for frequently accessed data
- Background task processing for builds

### Security Considerations

1. **Input Validation**: All user inputs are validated
2. **File Upload Security**: APK and ZIP files are properly validated
3. **API Security**: Build server communication uses authentication
4. **User Permissions**: Django admin permissions control access

## Testing

### Unit Tests

```python
# Test code generation
class CodeGeneratorTests(TestCase):
    def test_widget_code_generation(self):
        # Test widget code generation
        
    def test_action_code_generation(self):
        # Test action code generation
```

### Integration Tests

```python
# Test complete app generation
class AppGenerationTests(TestCase):
    def test_complete_app_generation(self):
        # Test end-to-end app generation
```

### Sample App Tests

```python
# Test sample app creation
class SampleAppTests(TestCase):
    def test_ecommerce_sample_creation(self):
        # Test e-commerce sample app creation
```

## Monitoring and Logging

### Build Monitoring

The system tracks all build attempts with detailed logging:

```python
class BuildHistory(models.Model):
    build_id = models.UUIDField(default=uuid.uuid4, unique=True)
    status = models.CharField(max_length=30, choices=BUILD_STATUS_CHOICES)
    log_output = models.TextField(blank=True)
    error_message = models.TextField(blank=True)
    build_start_time = models.DateTimeField(auto_now_add=True)
    build_end_time = models.DateTimeField(blank=True, null=True)
```

### Performance Monitoring

- Track code generation times
- Monitor build server response times
- Log database query performance
- Monitor file storage usage

## API Documentation

### Build Server API

The platform expects a build server with these endpoints:

#### POST /api/build
Accepts Flutter project ZIP and returns build status.

**Request:**
```json
{
    "project": "<zip_file>",
    "package_name": "com.example.app",
    "app_name": "My App",
    "version": "1.0.0",
    "build_id": "uuid"
}
```

**Response:**
```json
{
    "status": "success",
    "build_id": "uuid",
    "apk_url": "https://build-server.com/apks/app.apk",
    "logs": "Build completed successfully"
}
```

## Troubleshooting

### Common Issues

#### Code Generation Failures
- Check widget hierarchy for circular references
- Verify all required properties are set
- Ensure data source fields are properly defined

#### Build Failures
- Verify build server connectivity
- Check Flutter project structure
- Review build logs for specific errors

#### Performance Issues
- Optimize database queries with select_related/prefetch_related
- Implement caching for frequently accessed data
- Consider pagination for large datasets

### Debug Mode

Enable debug logging:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'core.services': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```

This technical manual provides comprehensive information for developers working with or extending the Flutter App Builder platform. The system is designed to be modular and extensible while maintaining the core principle of 100% dynamic application generation.