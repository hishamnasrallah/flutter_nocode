# Flutter App Builder - No-Code Flutter Application Generator

A comprehensive Django-based platform that allows non-technical users to create Flutter mobile applications through an intuitive admin interface. Generate complete Flutter apps with APK builds without writing a single line of code.

## 🚀 Features

### For Non-Technical Users
- **Visual App Builder**: Create apps using a user-friendly web interface
- **No Coding Required**: Build complete Flutter applications without programming knowledge
- **Real-Time Preview**: See your app structure as you build it
- **One-Click APK Generation**: Build and download your Android app instantly
- **Sample Applications**: Pre-built templates for e-commerce, social media, and news apps

### For Developers
- **100% Dynamic Generation**: Every aspect of the Flutter app is generated from database configuration
- **Extensible Architecture**: Easy to add new widget types, actions, and data sources
- **Clean Code Output**: Generates production-ready Flutter code
- **Scalable Design**: Horizontal and vertical scaling support
- **Comprehensive API**: RESTful APIs for integration with external systems

## 🏗️ Architecture

### Core Components
1. **Django Backend**: Manages app configuration, user interface, and build orchestration
2. **Code Generation Engine**: Converts database models to Flutter Dart code
3. **Build Service**: Handles APK compilation and distribution
4. **Admin Interface**: Customized Django admin for non-technical users

### Database Schema
- **Applications**: Complete app definitions with metadata and build status
- **Screens**: Individual app pages with navigation and styling
- **Widgets**: UI components with hierarchical relationships
- **Actions**: User interactions and behaviors
- **Data Sources**: External APIs and static data integration
- **Themes**: Visual styling and branding

## 📱 Supported Features

### UI Components
- Layout widgets (Column, Row, Container, Stack)
- Display widgets (Text, Image, Icon, Card)
- Input widgets (TextField, Button, Switch, Dropdown)
- Navigation widgets (AppBar, BottomNavigation, Drawer)
- Scrollable widgets (ListView, GridView, PageView)

### Functionality
- **Navigation**: Multi-screen apps with route management
- **Data Integration**: REST API and static JSON data sources
- **User Interactions**: Buttons, forms, and gesture handling
- **Theming**: Custom colors, fonts, and styling
- **Actions**: Navigation, API calls, dialogs, and external integrations

### Advanced Features
- **Pub.dev Integration**: Add any Flutter package dynamically
- **Build History**: Track all build attempts with detailed logs
- **Sample Apps**: Complex pre-built applications for learning
- **Custom Widgets**: Extend with community packages

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- Django 4.2.7
- SQLite (development) or PostgreSQL (production)

### Quick Start
```bash
# Install dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

### Access the Platform
1. Open http://localhost:8000/admin
2. Log in with your admin credentials
3. Start creating Flutter applications!

## 📖 Usage

### Creating Your First App

1. **Create Application**
   - Go to "Flutter Applications" → "Add Flutter Application"
   - Fill in app name, package identifier, and description
   - Choose a theme or create a new one

2. **Design Screens**
   - Add screens for different pages (Home, Products, Contact, etc.)
   - Configure navigation routes and app bar settings

3. **Add Content**
   - Create widgets (Text, Images, Buttons, Lists)
   - Set widget properties and arrange them hierarchically
   - Connect widgets to data sources and actions

4. **Configure Data**
   - Set up data sources (REST APIs or static JSON)
   - Define data fields and their types
   - Bind data to widgets for dynamic content

5. **Define Actions**
   - Create actions for user interactions
   - Configure navigation, API calls, and dialogs
   - Connect actions to buttons and other interactive widgets

6. **Build Your App**
   - Generate Flutter source code
   - Build APK file
   - Download and install on your Android device

### Sample Applications

Generate complete sample applications to learn the platform:

```bash
# Create e-commerce app
python manage.py create_sample_app ecommerce --name "My Store"

# Create social media app
python manage.py create_sample_app social_media --name "My Social App"

# Create news app
python manage.py create_sample_app news --name "My News App"
```

## 📚 Documentation

### User Manuals
- **[Non-Technical User Manual](docs/USER_MANUAL_NON_TECHNICAL.md)**: Step-by-step guide for creating apps without coding knowledge
- **[Technical Manual](docs/TECHNICAL_MANUAL.md)**: Comprehensive developer documentation

### Key Concepts

#### Widgets and Properties
Widgets are the building blocks of your app. Each widget has properties that define its appearance and behavior:

```python
# Example: Text widget with color property
text_widget = Widget.objects.create(
    screen=home_screen,
    widget_type="Text",
    order=0
)

WidgetProperty.objects.create(
    widget=text_widget,
    property_name="text",
    property_type="string",
    string_value="Welcome to my app!"
)
```

#### Data Sources and Binding
Connect your app to external data sources:

```python
# Create data source
products_api = DataSource.objects.create(
    application=app,
    name="Products",
    data_source_type="REST_API",
    base_url="https://api.mystore.com",
    endpoint="/products"
)

# Bind to widget
WidgetProperty.objects.create(
    widget=list_widget,
    property_name="dataSource",
    property_type="data_source_field_reference",
    data_source_field_reference=product_name_field
)
```

#### Actions and Interactions
Define what happens when users interact with your app:

```python
# Create navigation action
navigate_action = Action.objects.create(
    application=app,
    name="Go to Product Details",
    action_type="navigate",
    target_screen=product_details_screen
)

# Connect to button
WidgetProperty.objects.create(
    widget=button_widget,
    property_name="onPressed",
    property_type="action_reference",
    action_reference=navigate_action
)
```

## 🔧 Development

### Project Structure
```
flutter_generator/
├── core/                          # Main Django app
│   ├── models.py                  # Database models
│   ├── admin.py                   # Admin interface customization
│   ├── services/                  # Core services
│   │   ├── code_generator.py      # Flutter code generation
│   │   └── build_service.py       # APK build management
│   └── management/commands/       # Management commands
├── templates/                     # Custom admin templates
├── static/                        # Static files (CSS, JS)
├── docs/                         # Documentation
└── requirements.txt              # Python dependencies
```

### Extending the Platform

#### Adding New Widget Types
1. Update `WIDGET_TYPES` in `models.py`
2. Add code generation logic in `code_generator.py`
3. Update admin interface with help text

#### Adding New Action Types
1. Update `ACTION_TYPES` in `models.py`
2. Add action handling in `_generate_action_code()`
3. Test with sample applications

#### Custom Data Sources
1. Extend `DATA_SOURCE_TYPES`
2. Update API service generation
3. Add validation and error handling

## 🚀 Production Deployment

### Database Configuration
Use PostgreSQL for production:

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
The platform requires a separate Flutter build server:
- Flutter SDK installed and configured
- Android SDK with build tools
- API endpoints for project submission and APK retrieval
- Proper authentication and security measures

### Environment Variables
```env
SECRET_KEY=your-secret-key
DEBUG=False
BUILD_SERVER_URL=https://your-build-server.com
BUILD_SERVER_API_KEY=your-api-key
DATABASE_URL=postgresql://user:pass@localhost/dbname
```

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Submit a pull request

### Development Setup
```bash
# Clone repository
git clone <repository-url>
cd flutter-app-builder

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt

# Run tests
python manage.py test

# Start development server
python manage.py runserver
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

### Getting Help
- **Documentation**: Check the user manuals in the `docs/` directory
- **Sample Apps**: Use the sample applications to understand the platform
- **Build History**: Check build logs for troubleshooting
- **Admin Interface**: All features include helpful tooltips and descriptions

### Common Issues
- **Build Failures**: Check build history for detailed error logs
- **Widget Issues**: Ensure all required properties are set
- **Data Source Problems**: Verify API endpoints and data field definitions
- **Navigation Issues**: Check screen routes and action configurations

## 🎯 Roadmap

### Upcoming Features
- **iOS Support**: Generate iOS apps in addition to Android
- **Real-time Preview**: Live preview of app changes
- **Advanced Animations**: Support for complex animations and transitions
- **Database Integration**: Direct database connectivity
- **User Authentication**: Built-in user management systems
- **Push Notifications**: Integrated notification services
- **Analytics Integration**: Built-in analytics and tracking

### Long-term Goals
- **Visual Designer**: Drag-and-drop interface for app design
- **Marketplace**: Share and sell app templates
- **Collaboration Tools**: Multi-user app development
- **Version Control**: Track and manage app versions
- **A/B Testing**: Built-in testing and optimization tools

---

**Flutter App Builder** - Empowering everyone to create mobile applications without coding barriers.