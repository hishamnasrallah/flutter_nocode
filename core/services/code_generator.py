import os
import shutil
import json
import zipfile
from pathlib import Path
from django.conf import settings
from django.template.loader import render_to_string
from ..models import Application, Screen, Widget, WidgetProperty, Action, DataSource, DataSourceField, CustomPubDevWidget


class FlutterCodeGenerator:
    """Generates Flutter source code from database configuration"""
    
    def __init__(self, application):
        self.application = application
        self.project_path = settings.GENERATED_CODE_PATH / f"{application.package_name.replace('.', '_')}"
        self.lib_path = self.project_path / 'lib'
        
    def generate_project(self):
        """Generate complete Flutter project"""
        try:
            # Clean and create project directory with retry logic for Windows file locks
            if self.project_path.exists():
                # Try to remove the directory with retries
                max_retries = 3
                for attempt in range(max_retries):
                    try:
                        # First, try to clean build artifacts that might be locked
                        build_path = self.project_path / 'build'
                        if build_path.exists():
                            # Use Windows-specific cleanup if on Windows
                            if os.name == 'nt':
                                import subprocess
                                # Force close any Java/Gradle processes that might be locking files
                                subprocess.run(['taskkill', '/F', '/IM', 'java.exe'],
                                             capture_output=True, shell=True)
                                subprocess.run(['taskkill', '/F', '/IM', 'gradle.exe'],
                                             capture_output=True, shell=True)
                                # Small delay to let processes release files
                                import time
                                time.sleep(1)

                                # Try to remove read-only attributes
                                subprocess.run(['attrib', '-R', f'{build_path}\\*', '/S'],
                                             capture_output=True, shell=True)

                        # Now try to remove the directory
                        shutil.rmtree(self.project_path, ignore_errors=False)
                        break  # Success, exit the retry loop

                    except PermissionError as e:
                        if attempt < max_retries - 1:
                            print(f"Attempt {attempt + 1} failed to clean directory, retrying...")
                            import time
                            time.sleep(2)  # Wait before retry
                        else:
                            # Last attempt - try to at least clean the build directory
                            print(f"Cannot fully clean project directory, attempting partial cleanup")
                            build_path = self.project_path / 'build'
                            if build_path.exists():
                                try:
                                    shutil.rmtree(build_path, ignore_errors=True)
                                except:
                                    pass
                            # Continue without full cleanup
                            break
                    except Exception as e:
                        print(f"Unexpected error during cleanup: {e}")
                        break

            # Create project directory
            self.project_path.mkdir(parents=True, exist_ok=True)
            
            # Generate project structure
            self._create_project_structure()
            self._generate_pubspec_yaml()
            self._generate_main_dart()
            self._generate_theme()
            self._generate_routes()
            self._generate_screens()
            self._generate_services()
            self._generate_models()
            self._generate_widgets()
            # Note: Android gradle is updated in _create_project_structure
            
            # Create source code ZIP
            zip_path = self._create_source_zip()
            
            # Update application with generated files
            self.application.source_code_zip.name = f"source_zips/{self.application.package_name}_source.zip"
            self.application.save()
            
            return True, f"Flutter project generated successfully at {self.project_path}"
            
        except Exception as e:
            return False, f"Error generating Flutter project: {str(e)}"

    def _create_project_structure(self):
        """Create complete Flutter project structure using Flutter CLI"""
        import subprocess
        import shutil

        # Get Flutter executable path
        flutter_exe = os.path.join(settings.FLUTTER_SDK_PATH, 'bin', 'flutter.bat' if os.name == 'nt' else 'flutter')

        if not os.path.exists(flutter_exe):
            raise Exception(f"Flutter not found at {flutter_exe}")

        # Clean existing project if it exists
        if self.project_path.exists():
            shutil.rmtree(self.project_path)

        # Create parent directory
        self.project_path.parent.mkdir(parents=True, exist_ok=True)

        # Extract package name and org from full package identifier
        package_parts = self.application.package_name.split('.')
        project_name = package_parts[-1]  # e.g., 'ecommerce_store'
        org = '.'.join(package_parts[:-1]) if len(package_parts) > 1 else 'com.example'  # e.g., 'com.example'

        # Run flutter create with proper parameters
        create_command = [
            flutter_exe, 'create',
            '--project-name', project_name,
            '--org', org,
            '--platforms', 'android,ios',
            '--no-pub',  # Don't run pub get yet
            str(self.project_path)
        ]

        print(f"Creating Flutter project: {' '.join(create_command)}")

        result = subprocess.run(
            create_command,
            capture_output=True,
            text=True,
            timeout=120,
            env=os.environ.copy()
        )

        if result.returncode != 0:
            error_msg = f"Flutter create failed: {result.stderr}"
            print(error_msg)
            raise Exception(error_msg)

        print(f"Flutter project created successfully at {self.project_path}")

        # Ensure our custom directories exist
        custom_directories = [
            'lib/screens',
            'lib/widgets',
            'lib/services',
            'lib/models',
            'lib/theme',
            'lib/routes',
            'lib/utils',
            'assets/images',
            'assets/fonts',
        ]

        for directory in custom_directories:
            (self.project_path / directory).mkdir(parents=True, exist_ok=True)

        # Update android/app/build.gradle to add NDK version
        self._update_android_gradle()

    def _create_manual_structure(self):
        """Manually create Flutter project structure if Flutter CLI is not available"""
        directories = [
            'lib',
            'lib/screens',
            'lib/widgets',
            'lib/services',
            'lib/models',
            'lib/theme',
            'lib/routes',
            'lib/utils',
            'android/app/src/main/kotlin/com/example/app',
            'android/app/src/main/res/drawable',
            'android/app/src/main/res/values',
            'android/gradle/wrapper',
            'ios/Runner',
            'test',
            'assets/images',
            'assets/fonts',
        ]
        
        for directory in directories:
            (self.project_path / directory).mkdir(parents=True, exist_ok=True)

    def _create_android_gradle_files(self):
        """Create Android Gradle configuration files with proper NDK version"""
        android_app_path = self.project_path / 'android' / 'app'
        android_app_path.mkdir(parents=True, exist_ok=True)

        # Create build.gradle for app module
        build_gradle_content = '''
android {
    compileSdkVersion 34
    ndkVersion "27.0.12077973"

    defaultConfig {
        applicationId "''' + self.application.package_name + '''"
        minSdkVersion 21
        targetSdkVersion 34
        versionCode 1
        versionName "1.0"
    }

    buildTypes {
        release {
            minifyEnabled true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
}

dependencies {
    implementation "org.jetbrains.kotlin:kotlin-stdlib-jdk8:$kotlin_version"
}
'''

        build_gradle_path = android_app_path / 'build.gradle'
        with open(build_gradle_path, 'w', encoding='utf-8') as f:
            f.write(build_gradle_content)

    def _generate_pubspec_yaml(self):
        """Generate pubspec.yaml with dependencies"""
        # Get custom pub.dev widgets
        custom_widgets = CustomPubDevWidget.objects.filter(
            application=self.application,
            is_active=True
        )
        
        # Base dependencies
        dependencies = {
            'flutter': {'sdk': 'flutter'},
            'http': '^1.1.0',
            'shared_preferences': '^2.2.2',
            'url_launcher': '^6.2.1',
            'image_picker': '^1.0.4',
            'path_provider': '^2.1.1',
        }
        
        # Add custom widget dependencies
        for widget in custom_widgets:
            if widget.package_version:
                dependencies[widget.package_name] = f"^{widget.package_version}"
            else:
                dependencies[widget.package_name] = 'any'
        
        pubspec_content = {
            'name': self.application.package_name.split('.')[-1],
            'description': self.application.description or 'A Flutter application generated by Flutter App Builder',
            'version': f"{self.application.version}+1",
            'environment': {
                'sdk': '>=3.0.0 <4.0.0'  # This will be properly quoted by _write_yaml
            },
            'dependencies': dependencies,
            'dev_dependencies': {
                'flutter_test': {'sdk': 'flutter'},
                'flutter_lints': '^3.0.0'
            },
            'flutter': {
                'uses-material-design': True,
                'assets': [
                    'assets/images/',
                ]
            }
        }
        
        # Write pubspec.yaml
        with open(self.project_path / 'pubspec.yaml', 'w', encoding='utf-8') as f:
            self._write_yaml(f, pubspec_content)
    
    def _write_yaml(self, file, data, indent=0):
        """Write YAML content manually with proper formatting"""
        for key, value in data.items():
            if isinstance(value, dict):
                file.write('  ' * indent + f"{key}:\n")
                self._write_yaml(file, value, indent + 1)
            elif isinstance(value, list):
                file.write('  ' * indent + f"{key}:\n")
                for item in value:
                    file.write('  ' * (indent + 1) + f"- {item}\n")
            elif isinstance(value, str):
                # Check if string needs quoting (contains special characters)
                if any(char in value for char in ['>', '<', ':', '{', '}', '[', ']', ',', '&', '*', '#', '?', '|', '-', '=', '!', '%', '@', '`']):
                    file.write('  ' * indent + f"{key}: '{value}'\n")
                else:
                    file.write('  ' * indent + f"{key}: {value}\n")
            elif isinstance(value, bool):
                file.write('  ' * indent + f"{key}: {str(value).lower()}\n")
            elif value is None:
                file.write('  ' * indent + f"{key}: null\n")
            else:
                file.write('  ' * indent + f"{key}: {value}\n")
    
    def _generate_main_dart(self):
        """Generate main.dart file"""
        screens = Screen.objects.filter(application=self.application)
        home_screen = screens.filter(is_home_screen=True).first()
        
        if not home_screen:
            home_screen = screens.first()
        
        main_content = f'''import 'package:flutter/material.dart';
import 'theme/app_theme.dart';
import 'routes/app_routes.dart';
{self._generate_screen_imports()}

void main() {{
  runApp(MyApp());
}}

class MyApp extends StatelessWidget {{
  @override
  Widget build(BuildContext context) {{
    return MaterialApp(
      title: '{self.application.name}',
      theme: AppTheme.lightTheme,
      darkTheme: AppTheme.darkTheme,
      themeMode: {('ThemeMode.dark' if self.application.theme.is_dark_mode else 'ThemeMode.light')},
      initialRoute: '{home_screen.route_name if home_screen else '/'}',
      routes: AppRoutes.routes,
      debugShowCheckedModeBanner: false,
    );
  }}
}}
'''
        
        with open(self.lib_path / 'main.dart', 'w', encoding='utf-8') as f:
            f.write(main_content)
    
    def _generate_screen_imports(self):
        """Generate import statements for all screens"""
        screens = Screen.objects.filter(application=self.application)
        imports = []
        
        for screen in screens:
            screen_file_name = self._to_snake_case(screen.name) + '_screen.dart'
            imports.append(f"import 'screens/{screen_file_name}';")
        
        return '\n'.join(imports)
    
    def _generate_theme(self):
        """Generate theme configuration"""
        theme = self.application.theme
        
        theme_content = f'''import 'package:flutter/material.dart';

class AppTheme {{
  static const Color primaryColor = Color(0xFF{theme.primary_color.lstrip('#')});
  static const Color accentColor = Color(0xFF{theme.accent_color.lstrip('#')});
  static const Color backgroundColor = Color(0xFF{theme.background_color.lstrip('#')});
  static const Color textColor = Color(0xFF{theme.text_color.lstrip('#')});
  
  static ThemeData get lightTheme {{
    return ThemeData(
      primarySwatch: _createMaterialColor(primaryColor),
      primaryColor: primaryColor,
      colorScheme: ColorScheme.fromSeed(
        seedColor: primaryColor,
        brightness: Brightness.light,
      ),
      scaffoldBackgroundColor: backgroundColor,
      fontFamily: '{theme.font_family}',
      textTheme: TextTheme(
        bodyLarge: TextStyle(color: textColor),
        bodyMedium: TextStyle(color: textColor),
        titleLarge: TextStyle(color: textColor),
      ),
      appBarTheme: AppBarTheme(
        backgroundColor: primaryColor,
        foregroundColor: Colors.white,
        elevation: 2,
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: primaryColor,
          foregroundColor: Colors.white,
        ),
      ),
      floatingActionButtonTheme: FloatingActionButtonThemeData(
        backgroundColor: accentColor,
      ),
    );
  }}
  
  static ThemeData get darkTheme {{
    return ThemeData(
      primarySwatch: _createMaterialColor(primaryColor),
      primaryColor: primaryColor,
      colorScheme: ColorScheme.fromSeed(
        seedColor: primaryColor,
        brightness: Brightness.dark,
      ),
      scaffoldBackgroundColor: Color(0xFF121212),
      fontFamily: '{theme.font_family}',
      textTheme: TextTheme(
        bodyLarge: TextStyle(color: Colors.white),
        bodyMedium: TextStyle(color: Colors.white),
        titleLarge: TextStyle(color: Colors.white),
      ),
      appBarTheme: AppBarTheme(
        backgroundColor: primaryColor,
        foregroundColor: Colors.white,
        elevation: 2,
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: primaryColor,
          foregroundColor: Colors.white,
        ),
      ),
      floatingActionButtonTheme: FloatingActionButtonThemeData(
        backgroundColor: accentColor,
      ),
    );
  }}
  
  static MaterialColor _createMaterialColor(Color color) {{
    List strengths = <double>[.05];
    Map<int, Color> swatch = {{}};
    final int r = color.red, g = color.green, b = color.blue;

    for (int i = 1; i < 10; i++) {{
      strengths.add(0.1 * i);
    }}
    
    for (var strength in strengths) {{
      final double ds = 0.5 - strength;
      swatch[(strength * 1000).round()] = Color.fromRGBO(
        r + ((ds < 0 ? r : (255 - r)) * ds).round(),
        g + ((ds < 0 ? g : (255 - g)) * ds).round(),
        b + ((ds < 0 ? b : (255 - b)) * ds).round(),
        1,
      );
    }}
    
    return MaterialColor(color.value, swatch);
  }}
}}
'''
        
        with open(self.lib_path / 'theme' / 'app_theme.dart', 'w', encoding='utf-8') as f:
            f.write(theme_content)
    
    def _generate_routes(self):
        """Generate route configuration"""
        screens = Screen.objects.filter(application=self.application)
        
        routes_content = '''import 'package:flutter/material.dart';
'''
        
        # Add screen imports
        for screen in screens:
            screen_file_name = self._to_snake_case(screen.name) + '_screen.dart'
            screen_class_name = self._to_pascal_case(screen.name) + 'Screen'
            routes_content += f"import '../screens/{screen_file_name}';\n"
        
        routes_content += '''
class AppRoutes {
  static Map<String, WidgetBuilder> get routes {
    return {
'''
        
        # Add route mappings
        for screen in screens:
            screen_class_name = self._to_pascal_case(screen.name) + 'Screen'
            routes_content += f"      '{screen.route_name}': (context) => {screen_class_name}(),\n"
        
        routes_content += '''    };
  }
}
'''
        
        with open(self.lib_path / 'routes' / 'app_routes.dart', 'w', encoding='utf-8') as f:
            f.write(routes_content)
    
    def _generate_screens(self):
        """Generate screen files"""
        screens = Screen.objects.filter(application=self.application)
        
        for screen in screens:
            self._generate_single_screen(screen)
    
    def _generate_single_screen(self, screen):
        """Generate a single screen file"""
        screen_file_name = self._to_snake_case(screen.name) + '_screen.dart'
        screen_class_name = self._to_pascal_case(screen.name) + 'Screen'
        
        # Get root widgets for this screen
        root_widgets = Widget.objects.filter(
            screen=screen,
            parent_widget=None
        ).order_by('order')
        
        screen_content = f'''import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../models/app_models.dart';

class {screen_class_name} extends StatefulWidget {{
  @override
  _{screen_class_name}State createState() => _{screen_class_name}State();
}}

class _{screen_class_name}State extends State<{screen_class_name}> {{
  final ApiService _apiService = ApiService();
  
  @override
  Widget build(BuildContext context) {{
    return Scaffold(
'''
        
        # Add AppBar if needed
        if screen.show_app_bar:
            screen_content += f'''      appBar: AppBar(
        title: Text('{screen.app_bar_title or screen.name}'),
        automaticallyImplyLeading: {str(screen.show_back_button).lower()},
      ),
'''
        
        # Add body
        screen_content += '''      body: '''
        
        if root_widgets.count() == 1:
            screen_content += self._generate_widget_code(root_widgets.first(), 0)
        elif root_widgets.count() > 1:
            screen_content += '''Column(
        children: [
'''
            for widget in root_widgets:
                screen_content += '          ' + self._generate_widget_code(widget, 2) + ',\n'
            screen_content += '''        ],
      )'''
        else:
            screen_content += '''Center(
        child: Text('No content configured for this screen'),
      )'''
        
        screen_content += ''',
    );
  }
}
'''
        
        with open(self.lib_path / 'screens' / screen_file_name, 'w', encoding='utf-8') as f:
            f.write(screen_content)

    def _generate_widget_code(self, widget, indent_level):
        """Generate Dart code for a widget - 100% dynamic from database"""
        indent = '  ' * indent_level
        widget_code = ''

        # Get widget properties from database
        properties = WidgetProperty.objects.filter(widget=widget)
        prop_dict = {prop.property_name: prop for prop in properties}

        # Get child widgets from database
        child_widgets = Widget.objects.filter(
            parent_widget=widget
        ).order_by('order')

        # Build widget based on type and properties from database
        if widget.widget_type == 'Text':
            text_value = self._get_property_value(prop_dict, 'text', 'Text')
            # Escape special characters and remove problematic Unicode
            text_value = self._escape_dart_string(text_value)
            style_code = self._generate_text_style(prop_dict)
            widget_code = f"Text('{text_value}'{style_code})"

        elif widget.widget_type in ['ElevatedButton', 'TextButton', 'OutlinedButton']:
            text = self._get_property_value(prop_dict, 'text', 'Button')
            text = self._escape_dart_string(text)  # Escape the text
            action_code = self._generate_action_from_property(prop_dict.get('onPressed'))
            widget_code = f'''{widget.widget_type}(
{indent}  onPressed: {action_code},
{indent}  child: Text('{text}'),
{indent})'''

        elif widget.widget_type == 'IconButton':
            icon = self._get_property_value(prop_dict, 'icon', 'add')
            action_code = self._generate_action_from_property(prop_dict.get('onPressed'))
            widget_code = f'''IconButton(
{indent}  icon: Icon(Icons.{icon}),
{indent}  onPressed: {action_code},
{indent})'''

        elif widget.widget_type == 'FloatingActionButton':
            icon = self._get_property_value(prop_dict, 'icon', 'add')
            action_code = self._generate_action_from_property(prop_dict.get('onPressed'))
            widget_code = f'''FloatingActionButton(
{indent}  onPressed: {action_code},
{indent}  child: Icon(Icons.{icon}),
{indent})'''

        elif widget.widget_type in ['Column', 'Row']:
            axis = 'mainAxisAlignment'
            alignment = self._get_property_value(prop_dict, axis, 'start')
            widget_code = f'''{widget.widget_type}(
{indent}  mainAxisAlignment: MainAxisAlignment.{alignment},
{indent}  children: [
'''
            for child in child_widgets:
                widget_code += f"{indent}    {self._generate_widget_code(child, indent_level + 2)},\n"
            widget_code += f"{indent}  ],\n{indent})"

        elif widget.widget_type == 'Container':
            widget_code = self._generate_container(prop_dict, child_widgets, indent_level)

        elif widget.widget_type == 'TextField':
            hint = self._escape_dart_string(self._get_property_value(prop_dict, 'hintText', 'Enter text...'))
            label = self._escape_dart_string(self._get_property_value(prop_dict, 'labelText', ''))
            widget_code = f'''TextField(
{indent}  decoration: InputDecoration(
{indent}    hintText: '{hint}','''
            if label:
                widget_code += f"\n{indent}    labelText: '{label}',"
            widget_code += f'''
{indent}    border: OutlineInputBorder(),
{indent}  ),
{indent})'''

        elif widget.widget_type == 'Image':
            widget_code = self._generate_image(prop_dict)

        elif widget.widget_type == 'Card':
            elevation = self._get_property_value(prop_dict, 'elevation', '4')
            widget_code = f'''Card(
{indent}  elevation: {elevation},
{indent}  child: '''
            if child_widgets.exists():
                if child_widgets.count() == 1:
                    widget_code += self._generate_widget_code(child_widgets.first(), indent_level + 1)
                else:
                    widget_code += self._generate_children_column(child_widgets, indent_level + 1)
            else:
                widget_code += "Container()"
            widget_code += f",\n{indent})"

        elif widget.widget_type == 'ListView':
            widget_code = self._generate_list_view(widget, prop_dict, child_widgets, indent_level)

        elif widget.widget_type == 'GridView':
            widget_code = self._generate_grid_view(widget, prop_dict, child_widgets, indent_level)

        elif widget.widget_type == 'Stack':
            widget_code = f'''Stack(
{indent}  children: [
'''
            for child in child_widgets:
                widget_code += f"{indent}    {self._generate_widget_code(child, indent_level + 2)},\n"
            widget_code += f"{indent}  ],\n{indent})"

        elif widget.widget_type == 'Expanded':
            flex = self._get_property_value(prop_dict, 'flex', '1')
            widget_code = f'''Expanded(
{indent}  flex: {flex},
{indent}  child: '''
            if child_widgets.exists():
                widget_code += self._generate_widget_code(child_widgets.first(), indent_level + 1)
            else:
                widget_code += "Container()"
            widget_code += f",\n{indent})"

        elif widget.widget_type == 'SizedBox':
            width = self._get_property_value(prop_dict, 'width', None)
            height = self._get_property_value(prop_dict, 'height', None)
            widget_code = f"SizedBox("
            if width:
                widget_code += f"width: {width}, "
            if height:
                widget_code += f"height: {height}, "
            if child_widgets.exists():
                widget_code += f"child: {self._generate_widget_code(child_widgets.first(), indent_level)}"
            widget_code += ")"

        elif widget.widget_type == 'Padding':
            padding = self._get_property_value(prop_dict, 'padding', '8.0')
            widget_code = f'''Padding(
{indent}  padding: EdgeInsets.all({padding}),
{indent}  child: '''
            if child_widgets.exists():
                widget_code += self._generate_widget_code(child_widgets.first(), indent_level + 1)
            else:
                widget_code += "Container()"
            widget_code += f",\n{indent})"

        elif widget.widget_type == 'Center':
            widget_code = f"Center(child: "
            if child_widgets.exists():
                widget_code += self._generate_widget_code(child_widgets.first(), indent_level)
            else:
                widget_code += "Container()"
            widget_code += ")"

        elif widget.widget_type == 'ListTile':
            title = self._escape_dart_string(self._get_property_value(prop_dict, 'title', 'Title'))
            subtitle = self._escape_dart_string(self._get_property_value(prop_dict, 'subtitle', ''))
            widget_code = f'''ListTile(
{indent}  title: Text('{title}'),'''
            if subtitle:
                widget_code += f"\n{indent}  subtitle: Text('{subtitle}'),"
            if 'leading' in prop_dict:
                widget_code += f"\n{indent}  leading: Icon(Icons.{self._get_property_value(prop_dict, 'leading', 'info')}),"
            if 'trailing' in prop_dict:
                widget_code += f"\n{indent}  trailing: Icon(Icons.{self._get_property_value(prop_dict, 'trailing', 'arrow_forward')}),"
            if 'onTap' in prop_dict:
                action_code = self._generate_action_from_property(prop_dict.get('onTap'))
                widget_code += f"\n{indent}  onTap: {action_code},"
            widget_code += f"\n{indent})"

        else:
            # For any other widget type, generate a placeholder
            widget_code = f"Container(child: Text('{widget.widget_type}'))"

        return widget_code

    def _get_property_value(self, prop_dict, property_name, default_value=''):
        """Get property value from database or return default"""
        if property_name in prop_dict:
            prop = prop_dict[property_name]
            value = prop.get_value()
            if value is not None and value != '':
                return value
        return default_value

    def _escape_dart_string(self, text):
        """Escape string for Dart code and handle special characters"""
        if not text:
            return ''

        # Remove or replace problematic Unicode characters
        # Replace emoji with text equivalents
        replacements = {
            '🔴': '[RED]',
            '🟢': '[GREEN]',
            '🔵': '[BLUE]',
            '🟡': '[YELLOW]',
            '⚠️': '[WARNING]',
            '❌': '[X]',
            '✅': '[CHECK]',
            '📱': '[PHONE]',
            '🛒': '[CART]',
            '📰': '[NEWS]',
        }

        for emoji, replacement in replacements.items():
            text = text.replace(emoji, replacement)

        # Escape special characters for Dart strings
        text = text.replace('\\', '\\\\')  # Escape backslashes first
        text = text.replace("'", "\\'")  # Escape single quotes
        text = text.replace('"', '\\"')  # Escape double quotes
        text = text.replace('\n', '\\n')  # Escape newlines
        text = text.replace('\r', '\\r')  # Escape carriage returns
        text = text.replace('\t', '\\t')  # Escape tabs
        text = text.replace('$', '\\$')  # Escape dollar signs (Dart string interpolation)

        # Remove any other non-ASCII characters that might cause issues
        import unicodedata
        text = ''.join(
            char if ord(char) < 128 else unicodedata.normalize('NFKD', char).encode('ascii', 'ignore').decode(
                'ascii') or ''
            for char in text
        )

        return text
    def _generate_text_style(self, prop_dict):
        """Generate TextStyle code from properties"""
        style_parts = []

        if 'color' in prop_dict:
            color = prop_dict['color'].get_value()
            if color:
                style_parts.append(f"color: Color(0xFF{color.lstrip('#')})")

        if 'fontSize' in prop_dict:
            size = prop_dict['fontSize'].get_value()
            if size:
                style_parts.append(f"fontSize: {size}")

        if 'fontWeight' in prop_dict:
            weight = prop_dict['fontWeight'].get_value()
            if weight:
                style_parts.append(f"fontWeight: FontWeight.{weight}")

        if style_parts:
            return f", style: TextStyle({', '.join(style_parts)})"
        return ''

    def _generate_action_from_property(self, prop):
        """Generate action code from property"""
        if not prop:
            return 'null'

        if prop.action_reference:
            return self._generate_action_code(prop.action_reference)
        elif prop.screen_reference:
            return f"() {{ Navigator.pushNamed(context, '{prop.screen_reference.route_name}'); }}"
        else:
            return 'null'

    def _generate_container(self, prop_dict, child_widgets, indent_level):
        """Generate Container widget from properties"""
        indent = '  ' * indent_level
        widget_code = f"Container(\n"

        # Add all container properties from database
        if 'width' in prop_dict:
            width = self._get_property_value(prop_dict, 'width')
            if width:
                widget_code += f"{indent}  width: {width},\n"

        if 'height' in prop_dict:
            height = self._get_property_value(prop_dict, 'height')
            if height:
                widget_code += f"{indent}  height: {height},\n"

        if 'padding' in prop_dict:
            padding = self._get_property_value(prop_dict, 'padding')
            if padding:
                widget_code += f"{indent}  padding: EdgeInsets.all({padding}),\n"

        if 'margin' in prop_dict:
            margin = self._get_property_value(prop_dict, 'margin')
            if margin:
                widget_code += f"{indent}  margin: EdgeInsets.all({margin}),\n"

        if 'color' in prop_dict:
            color = self._get_property_value(prop_dict, 'color')
            if color:
                widget_code += f"{indent}  decoration: BoxDecoration(color: Color(0xFF{color.lstrip('#')})),\n"

        # Add child if exists
        if child_widgets.exists():
            widget_code += f"{indent}  child: "
            if child_widgets.count() == 1:
                widget_code += self._generate_widget_code(child_widgets.first(), indent_level + 1)
            else:
                widget_code += self._generate_children_column(child_widgets, indent_level + 1)
            widget_code += ",\n"

        widget_code += f"{indent})"
        return widget_code

    def _generate_image(self, prop_dict):
        """Generate Image widget from properties"""
        url_prop = None
        for prop_name in ['imageUrl', 'url', 'src', 'source']:
            if prop_name in prop_dict:
                url_prop = prop_dict[prop_name]
                break

        if url_prop:
            url = url_prop.get_value()
            if url and url.startswith('http'):
                return f"Image.network('{url}', fit: BoxFit.cover, errorBuilder: (c,e,s) => Icon(Icons.image))"
            elif url:
                return f"Image.asset('{url}', fit: BoxFit.cover)"

        return "Icon(Icons.image, size: 50)"

    def _generate_list_view(self, widget, prop_dict, child_widgets, indent_level):
        """Generate ListView from database configuration"""
        indent = '  ' * indent_level

        # Check if there's a data source
        data_source_prop = prop_dict.get('dataSource')

        if data_source_prop and data_source_prop.data_source_field_reference:
            # Dynamic ListView with data source - need to wrap in widget that can expand
            data_source = data_source_prop.data_source_field_reference.data_source
            field = data_source_prop.data_source_field_reference

            # For ListViews with data, always wrap in Flexible or Expanded if not at root
            wrapper_start = ""
            wrapper_end = ""
            if indent_level > 0:  # Not at root level
                wrapper_start = f"Flexible(child: "
                wrapper_end = ")"

            return f'''{wrapper_start}FutureBuilder<List<dynamic>>(
{indent}  future: _apiService.fetchData('{data_source.name}'),
{indent}  builder: (context, snapshot) {{
{indent}    if (snapshot.connectionState == ConnectionState.waiting) {{
{indent}      return Center(child: CircularProgressIndicator());
{indent}    }}
{indent}    if (snapshot.hasError) {{
{indent}      return Center(child: Text('Error loading data'));
{indent}    }}
{indent}    final items = snapshot.data ?? [];
{indent}    if (items.isEmpty) {{
{indent}      return Center(child: Text('No items available'));
{indent}    }}
{indent}    return ListView.builder(
{indent}      shrinkWrap: true,
{indent}      physics: NeverScrollableScrollPhysics(),
{indent}      itemCount: items.length > 10 ? 10 : items.length,
{indent}      itemBuilder: (context, index) {{
{indent}        final item = items[index];
{indent}        return Card(
{indent}          margin: EdgeInsets.symmetric(horizontal: 8, vertical: 4),
{indent}          child: ListTile(
{indent}            title: Text(item['{field.field_name}']?.toString() ?? 'Item'),
{indent}            onTap: () {{}},
{indent}          ),
{indent}        );
{indent}      }},
{indent}    );
{indent}  }},
{indent}){wrapper_end}'''
        else:
            # Static ListView with child widgets
            if child_widgets.exists():
                code = f"ListView(\n{indent}  shrinkWrap: true,\n{indent}  children: [\n"
                for child in child_widgets:
                    code += f"{indent}    {self._generate_widget_code(child, indent_level + 2)},\n"
                code += f"{indent}  ],\n{indent})"
                return code
            else:
                return "ListView(shrinkWrap: true, children: [])"

    def _generate_grid_view(self, widget, prop_dict, child_widgets, indent_level):
        """Generate GridView from database configuration"""
        indent = '  ' * indent_level

        # Get grid properties
        columns = self._get_property_value(prop_dict, 'crossAxisCount', '2')

        # Check if there's a data source
        data_source_prop = prop_dict.get('dataSource')

        if data_source_prop and data_source_prop.data_source_field_reference:
            # Dynamic GridView with data source
            data_source = data_source_prop.data_source_field_reference.data_source
            field = data_source_prop.data_source_field_reference

            return f'''FutureBuilder<List<dynamic>>(
{indent}  future: _apiService.fetchData('{data_source.name}'),
{indent}  builder: (context, snapshot) {{
{indent}    if (snapshot.connectionState == ConnectionState.waiting) {{
{indent}      return Center(child: CircularProgressIndicator());
{indent}    }}
{indent}    if (snapshot.hasError) {{
{indent}      return Center(child: Text('Error loading data'));
{indent}    }}
{indent}    final data = snapshot.data ?? [];
{indent}    if (data.isEmpty) {{
{indent}      return Center(child: Text('No items'));
{indent}    }}
{indent}    return GridView.builder(
{indent}      shrinkWrap: true,
{indent}      gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
{indent}        crossAxisCount: {columns},
{indent}        crossAxisSpacing: 10,
{indent}        mainAxisSpacing: 10,
{indent}      ),
{indent}      itemCount: data.length,
{indent}      itemBuilder: (context, index) {{
{indent}        final item = data[index];
{indent}        return Card(
{indent}          child: Center(
{indent}            child: Text(item['{field.field_name}']?.toString() ?? ''),
{indent}          ),
{indent}        );
{indent}      }},
{indent}    );
{indent}  }},
{indent})'''
        else:
            # Static GridView
            return f'''GridView.count(
{indent}  crossAxisCount: {columns},
{indent}  shrinkWrap: true,
{indent}  children: [],
{indent})'''

    def _generate_children_column(self, child_widgets, indent_level):
            """Generate a Column for multiple children"""
            indent = '  ' * indent_level
            code = f"Column(\n{indent}  children: [\n"
            for child in child_widgets:
                code += f"{indent}    {self._generate_widget_code(child, indent_level + 2)},\n"
            code += f"{indent}  ],\n{indent})"
            return code
    
    def _generate_action_code(self, action):
        """Generate Dart code for actions"""
        if action.action_type == 'navigate':
            if action.target_screen:
                return f"() {{ Navigator.pushNamed(context, '{action.target_screen.route_name}'); }}"
        elif action.action_type == 'navigate_back':
            return "() { Navigator.pop(context); }"
        elif action.action_type == 'show_dialog':
            return f'''() {{
              showDialog(
                context: context,
                builder: (context) => AlertDialog(
                  title: Text('{action.dialog_title or 'Alert'}'),
                  content: Text('{action.dialog_message or 'Message'}'),
                  actions: [
                    TextButton(
                      onPressed: () => Navigator.pop(context),
                      child: Text('OK'),
                    ),
                  ],
                ),
              );
            }}'''
        elif action.action_type == 'api_call':
            if action.api_data_source:
                return f"() {{ _apiService.fetchData('{action.api_data_source.name}'); }}"
        
        return "null"
    
    def _generate_services(self):
        """Generate API service"""
        data_sources = DataSource.objects.filter(application=self.application)
        
        service_content = '''import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  static final ApiService _instance = ApiService._internal();
  factory ApiService() => _instance;
  ApiService._internal();
  
'''
        
        # Generate methods for each data source
        for data_source in data_sources:
            method_name = self._to_camel_case(data_source.name)
            
            if data_source.data_source_type == 'REST_API':
                service_content += f'''
  Future<List<dynamic>> fetch{self._to_pascal_case(data_source.name)}() async {{
    try {{
      final url = '{data_source.base_url}{data_source.endpoint}';
      final response = await http.{data_source.method.lower()}(
        Uri.parse(url),
        headers: {{
          'Content-Type': 'application/json',
'''
                
                # Add custom headers
                if data_source.headers:
                    for line in data_source.headers.split('\n'):
                        if ':' in line:
                            key, value = line.split(':', 1)
                            service_content += f"          '{key.strip()}': '{value.strip()}',\n"
                
                service_content += '''        },
      );
      
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return data is List ? data : [data];
      } else {
        throw Exception('Failed to load data: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Network error: $e');
    }
  }
'''

            elif data_source.data_source_type == 'STATIC_JSON':
                # Generate method that loads from mock data file
                service_content += f'''
  Future<List<dynamic>> fetch{self._to_pascal_case(data_source.name)}() async {{
    try {{
      // Load from mock data file
      await Future.delayed(Duration(milliseconds: 300)); // Simulate network delay
      
      final data = MockData.get{self._to_pascal_case(data_source.name)}();
      print('Loaded {data_source.name}: ${{data.length}} items from mock data');
      return data;
    }} catch (e) {{
      print('Error loading {data_source.name}: $e');
      return [];
    }}
  }}
'''
        
        # Add generic fetchData method
        service_content += '''
  Future<List<dynamic>> fetchData(String dataSourceName) async {
    switch (dataSourceName) {
'''
        
        for data_source in data_sources:
            service_content += f"      case '{data_source.name}': return fetch{self._to_pascal_case(data_source.name)}();\n"
        
        service_content += '''      default: throw Exception('Unknown data source: $dataSourceName');
    }
  }
}
'''
        
        with open(self.lib_path / 'services' / 'api_service.dart', 'w', encoding='utf-8') as f:
            f.write(service_content)
    
    def _generate_models(self):
        """Generate data models"""
        models_content = '''// Data models for the application

class AppData {
  final Map<String, dynamic> data;
  
  AppData(this.data);
  
  factory AppData.fromJson(Map<String, dynamic> json) {
    return AppData(json);
  }
  
  Map<String, dynamic> toJson() {
    return data;
  }
  
  dynamic operator [](String key) => data[key];
  void operator []=(String key, dynamic value) => data[key] = value;
}
'''
        
        with open(self.lib_path / 'models' / 'app_models.dart', 'w', encoding='utf-8') as f:
            f.write(models_content)
    
    def _generate_widgets(self):
        """Generate custom widget components"""
        widgets_content = '''import 'package:flutter/material.dart';

// Custom widgets for the application

class AppCard extends StatelessWidget {
  final Widget child;
  final EdgeInsets? padding;
  final Color? backgroundColor;
  
  const AppCard({
    Key? key,
    required this.child,
    this.padding,
    this.backgroundColor,
  }) : super(key: key);
  
  @override
  Widget build(BuildContext context) {
    return Card(
      color: backgroundColor,
      child: Padding(
        padding: padding ?? EdgeInsets.all(16.0),
        child: child,
      ),
    );
  }
}

class LoadingWidget extends StatelessWidget {
  final String? message;
  
  const LoadingWidget({Key? key, this.message}) : super(key: key);
  
  @override
  Widget build(BuildContext context) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          CircularProgressIndicator(),
          if (message != null) ...[
            SizedBox(height: 16),
            Text(message!),
          ],
        ],
      ),
    );
  }
}

class ErrorWidget extends StatelessWidget {
  final String message;
  final VoidCallback? onRetry;
  
  const ErrorWidget({
    Key? key,
    required this.message,
    this.onRetry,
  }) : super(key: key);
  
  @override
  Widget build(BuildContext context) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(Icons.error_outline, size: 64, color: Colors.red),
          SizedBox(height: 16),
          Text(message, textAlign: TextAlign.center),
          if (onRetry != null) ...[
            SizedBox(height: 16),
            ElevatedButton(
              onPressed: onRetry,
              child: Text('Retry'),
            ),
          ],
        ],
      ),
    );
  }
}
'''
        
        with open(self.lib_path / 'widgets' / 'custom_widgets.dart', 'w', encoding='utf-8') as f:
            f.write(widgets_content)
    
    def _create_source_zip(self):
        """Create ZIP file of the generated source code"""
        zip_path = settings.SOURCE_ZIP_STORAGE_PATH / f"{self.application.package_name}_source.zip"
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(self.project_path):
                for file in files:
                    file_path = Path(root) / file
                    arcname = file_path.relative_to(self.project_path)
                    zipf.write(file_path, arcname)
        
        return zip_path
    
    def _to_snake_case(self, text):
        """Convert text to snake_case"""
        import re
        text = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', text)
        text = re.sub(r'([a-z\d])([A-Z])', r'\1_\2', text)
        return text.lower().replace(' ', '_').replace('-', '_')
    
    def _to_pascal_case(self, text):
        """Convert text to PascalCase"""
        return ''.join(word.capitalize() for word in text.replace('_', ' ').replace('-', ' ').split())
    
    def _to_camel_case(self, text):
        """Convert text to camelCase"""
        pascal = self._to_pascal_case(text)
        return pascal[0].lower() + pascal[1:] if pascal else ''

    def _update_android_gradle(self):
        """Update Android build.gradle with proper NDK version"""
        build_gradle_path = self.project_path / 'android' / 'app' / 'build.gradle'

        if not build_gradle_path.exists():
            print(f"Warning: build.gradle not found at {build_gradle_path}")
            return

        # Read the existing build.gradle
        with open(build_gradle_path, 'r') as f:
            content = f.read()

        # Add ndkVersion after compileSdkVersion
        if 'ndkVersion' not in content:
            # Find the android block and add ndkVersion
            android_block_start = content.find('android {')
            if android_block_start != -1:
                # Find the next line after android {
                next_line_start = content.find('\n', android_block_start) + 1
                # Insert ndkVersion
                content = (
                        content[:next_line_start] +
                        '    ndkVersion "27.0.12077973"\n' +
                        content[next_line_start:]
                )

        # Write the updated content back
        with open(build_gradle_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"Updated Android build.gradle with NDK version")