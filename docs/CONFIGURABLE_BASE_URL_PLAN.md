# Configurable Base URL Implementation Plan

## Overview
This plan implements a configurable base URL system that allows users to modify the API base URL from the splash screen while maintaining a sensible default.

## Current State Analysis
- The system currently uses hardcoded `http://localhost:8000` in various places
- The `create_full_marketplace.py` command sets base URLs for data sources
- We need to make this configurable from the mobile app while maintaining defaults

## Implementation Strategy

### Phase 1: Backend Configuration Support

#### 1.1 Add Base URL Configuration to Application Model
Modify `core/models.py` to add a new field to the `Application` model:

```python
class Application(models.Model):
    # ... existing fields ...
    default_api_base_url = models.URLField(
        default='http://localhost:8000',
        verbose_name="Default API Base URL",
        help_text="Default base URL that the generated app will use for API calls"
    )
    allow_url_override = models.BooleanField(
        default=True,
        verbose_name="Allow URL Override",
        help_text="Allow users to change the base URL from the app splash screen"
    )
    # ... rest of existing fields ...
```

#### 1.2 Create Database Migration
Run the following commands to create and apply the migration:

```bash
python manage.py makemigrations core
python manage.py migrate
```

#### 1.3 Update Marketplace Creation Command
Modify `core/management/commands/create_full_marketplace.py`:

```python
def create_full_marketplace(custom_name=None, package_name=None, base_url=None):
    """Create a complete marketplace application with configurable base URL"""
    
    # Use provided base_url or default
    api_base_url = base_url or 'http://localhost:8000'
    
    # Create application with configurable base URL
    app = Application.objects.create(
        name=custom_name or "Complete Marketplace Platform",
        description="""...""",
        package_name=package_name or "com.marketplace.complete",
        version="1.0.0",
        theme=theme,
        default_api_base_url=api_base_url,  # Set the configurable base URL
        allow_url_override=True
    )
    
    # Use the configured base URL for all data sources
    base_url = app.default_api_base_url  # Use from application config
    
    # Rest of the function remains the same, but uses base_url variable
```

#### 1.4 Add Management Command Parameter
Update the command to accept base_url parameter:

```python
class Command(BaseCommand):
    help = 'Create a complete marketplace application'

    def add_arguments(self, parser):
        parser.add_argument(
            '--name',
            type=str,
            default='Complete Marketplace',
            help='Custom name for the marketplace application'
        )
        parser.add_argument(
            '--package',
            type=str,
            default='com.marketplace.complete',
            help='Package identifier for the application'
        )
        parser.add_argument(
            '--base-url',
            type=str,
            default='http://localhost:8000',
            help='Base URL for API endpoints'
        )

    def handle(self, *args, **options):
        app_name = options['name']
        package_name = options['package']
        base_url = options['base_url']

        try:
            with transaction.atomic():
                app = create_full_marketplace(app_name, package_name, base_url)
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully created marketplace application: {app.name} with base URL: {base_url}'
                    )
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating marketplace: {str(e)}')
            )
```

#### 1.5 Create API Endpoint for App Configuration
Add new view in `core/views.py`:

```python
@csrf_exempt
@require_http_methods(["GET"])
def get_app_config(request, app_id):
    """Get application configuration including base URL"""
    try:
        app = Application.objects.get(id=app_id)
        config = {
            "app_id": app.id,
            "app_name": app.name,
            "default_base_url": app.default_api_base_url,
            "allow_url_override": app.allow_url_override,
            "version": app.version
        }
        return JsonResponse(config)
    except Application.DoesNotExist:
        return JsonResponse({"error": "Application not found"}, status=404)

@csrf_exempt
@require_http_methods(["POST"])
def validate_base_url(request):
    """Validate if a base URL is accessible"""
    try:
        data = json.loads(request.body)
        test_url = data.get('base_url')
        
        if not test_url:
            return JsonResponse({"valid": False, "error": "No URL provided"})
        
        # Test the URL by trying to reach a common endpoint
        import requests
        test_endpoint = f"{test_url.rstrip('/')}/api/marketplace/categories"
        
        try:
            response = requests.get(test_endpoint, timeout=5)
            is_valid = response.status_code == 200
            return JsonResponse({
                "valid": is_valid,
                "status_code": response.status_code,
                "message": "URL is accessible" if is_valid else "URL returned error"
            })
        except requests.exceptions.RequestException as e:
            return JsonResponse({
                "valid": False,
                "error": f"Connection failed: {str(e)}"
            })
            
    except json.JSONDecodeError:
        return JsonResponse({"valid": False, "error": "Invalid JSON"})
    except Exception as e:
        return JsonResponse({"valid": False, "error": str(e)})
```

#### 1.6 Add URL Patterns
Update `flutter_nocode/urls.py`:

```python
urlpatterns += [
    # App Configuration Endpoints
    path('api/app-config/<int:app_id>/', views.get_app_config, name='get_app_config'),
    path('api/validate-url/', views.validate_base_url, name='validate_base_url'),
]
```

### Phase 2: Flutter Code Generation Updates

#### 2.1 Generate App Configuration Manager
Update `core/services/code_generator.py` to generate a configuration service:

```python
def _generate_app_config_service(self):
    """Generate app configuration service for managing base URL"""
    config_service = f'''
import 'package:shared_preferences/shared_preferences.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class AppConfigManager {{
  static const String _baseUrlKey = 'app_base_url';
  static const String _defaultUrlKey = 'app_default_url';
  static const String _appIdKey = 'app_id';
  
  static String _currentBaseUrl = '{self.application.default_api_base_url}';
  static String _defaultBaseUrl = '{self.application.default_api_base_url}';
  static bool _allowOverride = {str(self.application.allow_url_override).lower()};
  static const String _appId = '{self.application.id}';
  
  static String get currentBaseUrl => _currentBaseUrl;
  static String get defaultBaseUrl => _defaultBaseUrl;
  static bool get allowOverride => _allowOverride;
  static String get appId => _appId;
  
  /// Initialize the configuration manager
  static Future<void> initialize() async {{
    try {{
      final prefs = await SharedPreferences.getInstance();
      
      // Try to load saved custom URL first
      final savedUrl = prefs.getString(_baseUrlKey);
      if (savedUrl != null && savedUrl.isNotEmpty) {{
        _currentBaseUrl = savedUrl;
        return;
      }}
      
      // If no saved URL, try to fetch default from server
      await _fetchDefaultConfig();
      
      // Fall back to hardcoded default if server fetch fails
      final defaultUrl = prefs.getString(_defaultUrlKey) ?? '{self.application.default_api_base_url}';
      _defaultBaseUrl = defaultUrl;
      _currentBaseUrl = defaultUrl;
      
    }} catch (e) {{
      print('Error initializing app config: $e');
      // Use hardcoded defaults as fallback
      _currentBaseUrl = '{self.application.default_api_base_url}';
      _defaultBaseUrl = '{self.application.default_api_base_url}';
    }}
  }}
  
  /// Fetch default configuration from server
  static Future<void> _fetchDefaultConfig() async {{
    try {{
      // Try multiple potential server URLs to fetch config
      final potentialUrls = [
        '{self.application.default_api_base_url}',
        'http://localhost:8000',
        'http://10.0.2.2:8000', // Android emulator
        'http://192.168.1.100:8000', // Common local network
      ];
      
      for (String baseUrl in potentialUrls) {{
        try {{
          final response = await http.get(
            Uri.parse('$baseUrl/api/app-config/$_appId/'),
            headers: {{'Content-Type': 'application/json'}},
          ).timeout(Duration(seconds: 5));
          
          if (response.statusCode == 200) {{
            final config = json.decode(response.body);
            _defaultBaseUrl = config['default_base_url'] ?? '{self.application.default_api_base_url}';
            _allowOverride = config['allow_url_override'] ?? true;
            
            // Save the working server URL as default
            final prefs = await SharedPreferences.getInstance();
            await prefs.setString(_defaultUrlKey, _defaultBaseUrl);
            
            _currentBaseUrl = _defaultBaseUrl;
            return;
          }}
        }} catch (e) {{
          // Try next URL
          continue;
        }}
      }}
    }} catch (e) {{
      print('Failed to fetch default config: $e');
    }}
  }}
  
  /// Update the base URL and save to preferences
  static Future<bool> updateBaseUrl(String newUrl) async {{
    try {{
      if (newUrl.isEmpty) return false;
      
      // Ensure URL doesn't end with slash
      final cleanUrl = newUrl.endsWith('/') ? newUrl.substring(0, newUrl.length - 1) : newUrl;
      
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString(_baseUrlKey, cleanUrl);
      _currentBaseUrl = cleanUrl;
      
      return true;
    }} catch (e) {{
      print('Error updating base URL: $e');
      return false;
    }}
  }}
  
  /// Reset to default URL
  static Future<void> resetToDefault() async {{
    try {{
      final prefs = await SharedPreferences.getInstance();
      await prefs.remove(_baseUrlKey);
      _currentBaseUrl = _defaultBaseUrl;
    }} catch (e) {{
      print('Error resetting to default: $e');
    }}
  }}
  
  /// Validate if a URL is accessible
  static Future<Map<String, dynamic>> validateUrl(String url) async {{
    try {{
      final cleanUrl = url.endsWith('/') ? url.substring(0, url.length - 1) : url;
      final testEndpoint = '$cleanUrl/api/marketplace/categories';
      
      final response = await http.get(
        Uri.parse(testEndpoint),
        headers: {{'Content-Type': 'application/json'}},
      ).timeout(Duration(seconds: 10));
      
      return {{
        'valid': response.statusCode == 200,
        'status_code': response.statusCode,
        'message': response.statusCode == 200 
          ? 'URL is accessible' 
          : 'Server returned error ${{response.statusCode}}'
      }};
    }} catch (e) {{
      return {{
        'valid': false,
        'error': 'Connection failed: ${{e.toString()}}'
      }};
    }}
  }}
}}
'''
    
    config_file_path = self.project_path / 'lib' / 'services' / 'app_config_manager.dart'
    config_file_path.parent.mkdir(parents=True, exist_ok=True)
    config_file_path.write_text(config_service)
```

#### 2.2 Generate Enhanced Splash Screen
Generate a splash screen with URL configuration:

```python
def _generate_splash_screen(self):
    """Generate splash screen with configurable base URL"""
    splash_screen = f'''
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'services/app_config_manager.dart';
import 'screens/home_screen.dart';

class SplashScreen extends StatefulWidget {{
  @override
  _SplashScreenState createState() => _SplashScreenState();
}}

class _SplashScreenState extends State<SplashScreen> {{
  final TextEditingController _urlController = TextEditingController();
  bool _showUrlConfig = false;
  bool _isLoading = true;
  bool _isValidating = false;
  String _validationMessage = '';
  bool _isValidUrl = true;
  
  @override
  void initState() {{
    super.initState();
    _initializeApp();
  }}
  
  Future<void> _initializeApp() async {{
    try {{
      // Initialize app configuration
      await AppConfigManager.initialize();
      
      // Pre-fill the URL field with current base URL
      _urlController.text = AppConfigManager.currentBaseUrl;
      
      setState(() {{
        _isLoading = false;
      }});
      
      // Auto-navigate after 3 seconds if URL override is not allowed
      if (!AppConfigManager.allowOverride) {{
        await Future.delayed(Duration(seconds: 3));
        _navigateToHome();
      }}
    }} catch (e) {{
      setState(() {{
        _isLoading = false;
        _validationMessage = 'Initialization error: ${{e.toString()}}';
      }});
    }}
  }}
  
  Future<void> _validateAndSaveUrl() async {{
    final url = _urlController.text.trim();
    
    if (url.isEmpty) {{
      setState(() {{
        _validationMessage = 'Please enter a URL';
        _isValidUrl = false;
      }});
      return;
    }}
    
    setState(() {{
      _isValidating = true;
      _validationMessage = 'Validating URL...';
    }});
    
    try {{
      final result = await AppConfigManager.validateUrl(url);
      
      if (result['valid'] == true) {{
        await AppConfigManager.updateBaseUrl(url);
        setState(() {{
          _validationMessage = 'URL validated successfully!';
          _isValidUrl = true;
        }});
        
        // Navigate after short delay
        await Future.delayed(Duration(seconds: 1));
        _navigateToHome();
      }} else {{
        setState(() {{
          _validationMessage = result['error'] ?? result['message'] ?? 'URL validation failed';
          _isValidUrl = false;
        }});
      }}
    }} catch (e) {{
      setState(() {{
        _validationMessage = 'Validation error: ${{e.toString()}}';
        _isValidUrl = false;
      }});
    }} finally {{
      setState(() {{
        _isValidating = false;
      }});
    }}
  }}
  
  Future<void> _resetToDefault() async {{
    await AppConfigManager.resetToDefault();
    setState(() {{
      _urlController.text = AppConfigManager.defaultBaseUrl;
      _validationMessage = 'Reset to default URL';
      _isValidUrl = true;
    }});
  }}
  
  void _navigateToHome() {{
    Navigator.of(context).pushReplacement(
      MaterialPageRoute(builder: (context) => HomeScreen()),
    );
  }}
  
  @override
  Widget build(BuildContext context) {{
    return Scaffold(
      backgroundColor: Theme.of(context).primaryColor,
      body: SafeArea(
        child: Padding(
          padding: EdgeInsets.all(24.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              // App Logo and Title
              Icon(
                Icons.shopping_bag,
                size: 80,
                color: Colors.white,
              ),
              SizedBox(height: 16),
              Text(
                '{self.application.name}',
                style: TextStyle(
                  fontSize: 28,
                  fontWeight: FontWeight.bold,
                  color: Colors.white,
                ),
                textAlign: TextAlign.center,
              ),
              SizedBox(height: 8),
              Text(
                'Version {self.application.version}',
                style: TextStyle(
                  fontSize: 16,
                  color: Colors.white70,
                ),
              ),
              SizedBox(height: 40),
              
              // Loading indicator or configuration
              if (_isLoading)
                Column(
                  children: [
                    CircularProgressIndicator(color: Colors.white),
                    SizedBox(height: 16),
                    Text(
                      'Initializing...',
                      style: TextStyle(color: Colors.white70),
                    ),
                  ],
                )
              else if (AppConfigManager.allowOverride) ...[
                // URL Configuration Section
                Card(
                  child: Padding(
                    padding: EdgeInsets.all(16),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: [
                        Text(
                          'API Server Configuration',
                          style: TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        SizedBox(height: 16),
                        
                        // URL Input Field
                        TextField(
                          controller: _urlController,
                          decoration: InputDecoration(
                            labelText: 'Server URL',
                            hintText: 'http://your-server.com:8000',
                            border: OutlineInputBorder(),
                            prefixIcon: Icon(Icons.link),
                            errorText: !_isValidUrl && _validationMessage.isNotEmpty 
                              ? _validationMessage 
                              : null,
                          ),
                          keyboardType: TextInputType.url,
                          enabled: !_isValidating,
                        ),
                        SizedBox(height: 12),
                        
                        // Validation Message
                        if (_validationMessage.isNotEmpty)
                          Container(
                            padding: EdgeInsets.all(8),
                            decoration: BoxDecoration(
                              color: _isValidUrl ? Colors.green.shade100 : Colors.red.shade100,
                              borderRadius: BorderRadius.circular(4),
                            ),
                            child: Text(
                              _validationMessage,
                              style: TextStyle(
                                color: _isValidUrl ? Colors.green.shade800 : Colors.red.shade800,
                                fontSize: 12,
                              ),
                            ),
                          ),
                        SizedBox(height: 16),
                        
                        // Action Buttons
                        Row(
                          children: [
                            Expanded(
                              child: ElevatedButton(
                                onPressed: _isValidating ? null : _resetToDefault,
                                child: Text('Use Default'),
                                style: ElevatedButton.styleFrom(
                                  backgroundColor: Colors.grey.shade600,
                                ),
                              ),
                            ),
                            SizedBox(width: 12),
                            Expanded(
                              flex: 2,
                              child: ElevatedButton(
                                onPressed: _isValidating ? null : _validateAndSaveUrl,
                                child: _isValidating
                                  ? SizedBox(
                                      height: 20,
                                      width: 20,
                                      child: CircularProgressIndicator(
                                        strokeWidth: 2,
                                        color: Colors.white,
                                      ),
                                    )
                                  : Text('Save & Continue'),
                                style: ElevatedButton.styleFrom(
                                  backgroundColor: Theme.of(context).primaryColor,
                                ),
                              ),
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),
                ),
              ] else
                // Auto-loading when override is not allowed
                Column(
                  children: [
                    CircularProgressIndicator(color: Colors.white),
                    SizedBox(height: 16),
                    Text(
                      'Loading application...',
                      style: TextStyle(color: Colors.white70),
                    ),
                  ],
                ),
              
              SizedBox(height: 40),
              
              // App Info
              Text(
                'Powered by Flutter App Builder',
                style: TextStyle(
                  fontSize: 12,
                  color: Colors.white60,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }}
  
  @override
  void dispose() {{
    _urlController.dispose();
    super.dispose();
  }}
}}
'''
    
    splash_file_path = self.project_path / 'lib' / 'screens' / 'splash_screen.dart'
    splash_file_path.parent.mkdir(parents=True, exist_ok=True)
    splash_file_path.write_text(splash_screen)
```

#### 2.3 Update API Service Generation
Modify the API service to use configurable base URL:

```python
def _generate_api_service(self):
    """Generate API service that uses configurable base URL"""
    api_service = f'''
import 'package:http/http.dart' as http;
import 'dart:convert';
import '../services/app_config_manager.dart';

class ApiService {{
  static String get baseUrl => AppConfigManager.currentBaseUrl;
  
  static Map<String, String> get defaultHeaders => {{
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  }};
  
  static Future<http.Response> get(String endpoint, {{Map<String, String>? headers}}) async {{
    final url = Uri.parse('$baseUrl$endpoint');
    final mergedHeaders = {{...defaultHeaders, ...?headers}};
    
    try {{
      final response = await http.get(url, headers: mergedHeaders);
      return response;
    }} catch (e) {{
      print('API GET Error: $e');
      rethrow;
    }}
  }}
  
  static Future<http.Response> post(String endpoint, {{
    Map<String, dynamic>? body,
    Map<String, String>? headers,
  }}) async {{
    final url = Uri.parse('$baseUrl$endpoint');
    final mergedHeaders = {{...defaultHeaders, ...?headers}};
    
    try {{
      final response = await http.post(
        url,
        headers: mergedHeaders,
        body: body != null ? json.encode(body) : null,
      );
      return response;
    }} catch (e) {{
      print('API POST Error: $e');
      rethrow;
    }}
  }}
  
  static Future<http.Response> put(String endpoint, {{
    Map<String, dynamic>? body,
    Map<String, String>? headers,
  }}) async {{
    final url = Uri.parse('$baseUrl$endpoint');
    final mergedHeaders = {{...defaultHeaders, ...?headers}};
    
    try {{
      final response = await http.put(
        url,
        headers: mergedHeaders,
        body: body != null ? json.encode(body) : null,
      );
      return response;
    }} catch (e) {{
      print('API PUT Error: $e');
      rethrow;
    }}
  }}
  
  static Future<http.Response> delete(String endpoint, {{Map<String, String>? headers}}) async {{
    final url = Uri.parse('$baseUrl$endpoint');
    final mergedHeaders = {{...defaultHeaders, ...?headers}};
    
    try {{
      final response = await http.delete(url, headers: mergedHeaders);
      return response;
    }} catch (e) {{
      print('API DELETE Error: $e');
      rethrow;
    }}
  }}
}}
'''
    
    api_file_path = self.project_path / 'lib' / 'services' / 'api_service.dart'
    api_file_path.parent.mkdir(parents=True, exist_ok=True)
    api_file_path.write_text(api_service)
```

#### 2.4 Update pubspec.yaml Dependencies
Ensure the generated pubspec.yaml includes required dependencies:

```python
def _generate_pubspec_yaml(self):
    """Generate pubspec.yaml with required dependencies"""
    dependencies = {
        'flutter': {'sdk': 'flutter'},
        'http': '^1.1.0',
        'shared_preferences': '^2.2.2',
        'cupertino_icons': '^1.0.2',
    }
    
    # Add existing dependencies...
    # Rest of the method remains the same
```

### Phase 3: Admin Interface Updates

#### 3.1 Update Application Admin
Modify `core/admin.py` to include the new fields:

```python
@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'package_name', 'version', 'default_api_base_url', 'allow_url_override', 'build_status', 'updated_at')
    list_filter = ('build_status', 'allow_url_override', 'theme', 'created_at')
    search_fields = ('name', 'package_name', 'description', 'default_api_base_url')
    readonly_fields = ('build_status', 'created_at', 'updated_at')
    
    fieldsets = (
        ('App Information', {
            'fields': ('name', 'description', 'package_name', 'version'),
            'description': 'Basic information about your Flutter application'
        }),
        ('API Configuration', {
            'fields': ('default_api_base_url', 'allow_url_override'),
            'description': 'Configure the default API base URL and whether users can override it'
        }),
        ('Styling', {
            'fields': ('theme',),
            'description': 'Choose how your app looks'
        }),
        ('Build Status', {
            'fields': ('build_status',),
            'classes': ('collapse',)
        }),
        ('Generated Files', {
            'fields': ('apk_file', 'source_code_zip'),
            'classes': ('collapse',),
            'description': 'Download your built app and source code'
        }),
    )
    
    # Rest of the admin configuration remains the same...
```

### Phase 4: Testing and Validation

#### 4.1 Backend Testing
Create test cases to verify the new functionality:

```python
# In core/tests.py (create if doesn't exist)
from django.test import TestCase, Client
from django.urls import reverse
from core.models import Application, Theme
import json

class ConfigurableBaseUrlTests(TestCase):
    def setUp(self):
        self.theme = Theme.objects.create(name="Test Theme")
        self.app = Application.objects.create(
            name="Test App",
            package_name="com.test.app",
            theme=self.theme,
            default_api_base_url="http://test-server.com:8000",
            allow_url_override=True
        )
        self.client = Client()
    
    def test_get_app_config(self):
        """Test getting application configuration"""
        response = self.client.get(f'/api/app-config/{self.app.id}/')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertEqual(data['default_base_url'], "http://test-server.com:8000")
        self.assertTrue(data['allow_url_override'])
    
    def test_validate_base_url(self):
        """Test URL validation endpoint"""
        test_data = {"base_url": "http://localhost:8000"}
        response = self.client.post(
            '/api/validate-url/',
            data=json.dumps(test_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertIn('valid', data)
```

#### 4.2 Integration Testing
Test the complete flow:

1. Create a marketplace app with custom base URL
2. Generate Flutter code
3. Verify the generated code includes the correct configuration
4. Test the API endpoints

### Phase 5: Documentation Updates

#### 5.1 Update User Manual
Add section to `docs/USER_MANUAL_NON_TECHNICAL.md`:

```markdown
## Configuring API Server URL

### What is the API Server URL?
The API Server URL is the web address where your app gets its data from. By default, this is set to work with your local development server.

### Changing the Server URL
1. When you first open your app, you'll see a splash screen
2. If URL configuration is enabled, you'll see a "Server URL" field
3. You can modify this URL to point to your production server
4. Tap "Save & Continue" to use the new URL
5. Tap "Use Default" to reset to the original URL

### URL Format
- URLs should start with `http://` or `https://`
- Include the port number if needed (e.g., `:8000`)
- Don't include trailing slashes
- Example: `https://api.mystore.com` or `http://192.168.1.100:8000`
```

#### 5.2 Update Technical Manual
Add section to `docs/TECHNICAL_MANUAL.md`:

```markdown
## Configurable Base URL System

### Overview
The system now supports configurable base URLs, allowing generated Flutter applications to connect to different API servers without recompilation.

### Backend Implementation
- `Application.default_api_base_url`: Stores the default base URL
- `Application.allow_url_override`: Controls whether users can change the URL
- API endpoints for configuration retrieval and URL validation

### Frontend Implementation
- `AppConfigManager`: Manages base URL configuration and persistence
- Enhanced splash screen with URL configuration UI
- `ApiService`: Uses configurable base URL for all requests
- `SharedPreferences`: Persists user-configured URLs

### Usage in Management Commands
```bash
python manage.py create_full_marketplace --name "My Store" --base-url "https://api.mystore.com"
```
```

### Phase 6: Deployment Considerations

#### 6.1 Production Checklist
- [ ] Database migration applied
- [ ] Default base URLs configured for existing applications
- [ ] API endpoints tested and secured
- [ ] Flutter dependencies verified
- [ ] URL validation working correctly
- [ ] Error handling implemented
- [ ] Documentation updated

#### 6.2 Migration Strategy
For existing applications:

```python
# Create a data migration to set default base URLs
from django.db import migrations

def set_default_base_urls(apps, schema_editor):
    Application = apps.get_model('core', 'Application')
    for app in Application.objects.all():
        if not app.default_api_base_url:
            app.default_api_base_url = 'http://localhost:8000'
            app.allow_url_override = True
            app.save()

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0002_application_default_api_base_url'),
    ]

    operations = [
        migrations.RunPython(set_default_base_urls),
    ]
```

## Summary

This implementation provides:

1. **Flexible Configuration**: Apps can have different default base URLs
2. **User Control**: Users can override URLs from the splash screen
3. **Validation**: URLs are tested before being saved
4. **Persistence**: Custom URLs are saved and restored
5. **Fallback**: Multiple fallback mechanisms ensure apps always work
6. **Admin Control**: Administrators can control whether URL override is allowed

The system maintains backward compatibility while adding powerful new configuration capabilities.