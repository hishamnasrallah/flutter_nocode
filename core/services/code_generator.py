"""
Complete Dynamic Flutter Code Generator
File: core/services/code_generator.py

This is a completely generic code generator that works for ANY Flutter app
based purely on database configuration. No app-specific code.
"""

import os
import shutil
import json
import zipfile
from pathlib import Path
from django.conf import settings
from django.template.loader import render_to_string
from ..models import Application, Screen, Widget, WidgetProperty, Action, DataSource, DataSourceField, \
    CustomPubDevWidget


class FlutterCodeGenerator:
    """Generates Flutter source code from database configuration"""

    def __init__(self, application):
        self.application = application
        self.project_path = settings.GENERATED_CODE_PATH / f"{application.package_name.replace('.', '_')}"
        self.lib_path = self.project_path / 'lib'

    def generate_project(self):
        """Generate complete Flutter project"""
        try:
            # Clean and create project directory with enhanced retry logic for Windows
            if self.project_path.exists():
                import subprocess
                import time
                import shutil

                # First, try to kill all Flutter/Java/Gradle processes that might be locking files
                if os.name == 'nt':
                    print("Cleaning up locked processes...")

                    # Kill all potentially locking processes
                    processes_to_kill = [
                        'java.exe', 'javaw.exe', 'gradle.exe', 'dart.exe',
                        'flutter_tester.exe', 'flutter.bat', 'adb.exe',
                        'kotlin-compiler-daemon'
                    ]

                    for process in processes_to_kill:
                        try:
                            subprocess.run(['taskkill', '/F', '/IM', process],
                                           capture_output=True, shell=True, timeout=5)
                        except:
                            pass

                    # Also try to kill processes by window title
                    try:
                        subprocess.run(['taskkill', '/F', '/FI', 'WINDOWTITLE eq Gradle*'],
                                       capture_output=True, shell=True, timeout=5)
                    except:
                        pass

                    # Wait for processes to fully terminate
                    time.sleep(3)

                    # Remove read-only attributes from all files
                    try:
                        subprocess.run(['attrib', '-R', '-S', '-H', f'{self.project_path}\\*', '/S', '/D'],
                                       capture_output=True, shell=True, timeout=10)
                    except:
                        pass

                # Try multiple strategies to remove the directory
                max_retries = 5
                for attempt in range(max_retries):
                    try:
                        print(f"Attempt {attempt + 1} to clean project directory...")

                        # Strategy 1: Normal removal
                        if self.project_path.exists():
                            shutil.rmtree(self.project_path, ignore_errors=False)
                            print("Successfully cleaned project directory")
                            break

                    except PermissionError as e:
                        if attempt < max_retries - 1:
                            print(f"Permission error, trying alternative approach...")

                            # Strategy 2: Remove specific problematic directories first
                            problematic_dirs = [
                                self.project_path / 'build',
                                self.project_path / '.gradle',
                                self.project_path / '.dart_tool',
                                self.project_path / 'android' / '.gradle',
                                self.project_path / 'android' / 'build',
                            ]

                            for prob_dir in problematic_dirs:
                                if prob_dir.exists():
                                    try:
                                        if os.name == 'nt':
                                            # Use Windows rmdir command
                                            subprocess.run(['cmd', '/c', 'rmdir', '/S', '/Q', str(prob_dir)],
                                                           capture_output=True, shell=False, timeout=10)
                                        else:
                                            shutil.rmtree(prob_dir, ignore_errors=True)
                                    except:
                                        pass

                            time.sleep(2)

                            # Strategy 3: Rename the directory instead of deleting
                            if attempt == max_retries - 2 and self.project_path.exists():
                                try:
                                    import datetime
                                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                                    backup_path = self.project_path.parent / f"{self.project_path.name}_old_{timestamp}"

                                    print(f"Renaming old project to {backup_path}")
                                    self.project_path.rename(backup_path)

                                    # Schedule deletion of renamed directory (optional)
                                    if os.name == 'nt':
                                        try:
                                            # Try to delete the backup in background
                                            subprocess.Popen(['cmd', '/c', 'timeout', '/t', '10', '&&',
                                                              'rmdir', '/S', '/Q', str(backup_path)],
                                                             shell=True, stdout=subprocess.DEVNULL,
                                                             stderr=subprocess.DEVNULL)
                                        except:
                                            pass
                                    break
                                except Exception as rename_error:
                                    print(f"Could not rename: {rename_error}")
                        else:
                            # Last attempt failed
                            print(f"ERROR: Could not clean project directory after {max_retries} attempts")
                            print("Try these manual steps:")
                            print("1. Close any IDEs (VS Code, Android Studio, IntelliJ)")
                            print("2. Close any terminal/command windows")
                            print("3. Open Task Manager and end any Java/Gradle processes")
                            print(f"4. Manually delete: {self.project_path}")
                            print("5. Try building again")

                            # Try one more time with ignore_errors=True
                            if self.project_path.exists():
                                try:
                                    shutil.rmtree(self.project_path, ignore_errors=True)
                                except:
                                    pass

                            # Even if we couldn't fully clean, try to proceed
                            # The Flutter create command might handle it
                            break

                    except Exception as e:
                        print(f"Unexpected error during cleanup attempt {attempt + 1}: {e}")
                        if attempt < max_retries - 1:
                            time.sleep(2)
                        else:
                            # Continue anyway on last attempt
                            break

            # Create project directory (even if cleanup wasn't perfect)
            self.project_path.mkdir(parents=True, exist_ok=True)

            # Generate project structure
            self._create_project_structure()
            self._update_android_manifest()
            self._generate_pubspec_yaml()
            self._generate_main_dart()
            self._generate_theme()
            self._generate_routes()
            self._generate_screens()
            self._generate_services()
            self._generate_models()
            self._generate_widgets()

            # Create source code ZIP
            zip_path = self._create_source_zip()

            # Update application with generated files
            self.application.source_code_zip.name = f"source_zips/{self.application.package_name}_source.zip"
            self.application.save()

            return True, f"Flutter project generated successfully at {self.project_path}"

        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"Error details:\n{error_details}")
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
        project_name = package_parts[-1]  # e.g., 'myapp'
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

        # Wait a moment for files to be fully written
        import time
        time.sleep(1)

        # Update android/app/build.gradle to add NDK version
        self._update_android_gradle()

    def _update_android_gradle(self):
        """Update Android build.gradle with proper NDK version"""
        import time
        import re

        # Try multiple times in case file is still being written
        for attempt in range(3):
            # Check for both .gradle and .gradle.kts files
            build_gradle_path = self.project_path / 'android' / 'app' / 'build.gradle'
            build_gradle_kts_path = self.project_path / 'android' / 'app' / 'build.gradle.kts'

            gradle_file = None
            is_kotlin_script = False

            if build_gradle_kts_path.exists():
                gradle_file = build_gradle_kts_path
                is_kotlin_script = True
            elif build_gradle_path.exists():
                gradle_file = build_gradle_path
                is_kotlin_script = False
            else:
                if attempt < 2:
                    time.sleep(1)
                    continue
                print(f"Warning: No build.gradle or build.gradle.kts found after {attempt + 1} attempts")
                return

            try:
                # Read the existing gradle file
                with open(gradle_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                original_content = content  # Keep backup

                if is_kotlin_script:
                    # For Kotlin script (.gradle.kts)
                    # First remove any existing ndkVersion
                    content = re.sub(r'ndkVersion\s*=\s*"[\d.]+"', '', content)
                    content = re.sub(r'ndkVersion\("[\d.]+"\)', '', content)
                    content = re.sub(r'ndkVersion\s+"[\d.]+"', '', content)

                    # Find android block and add ndkVersion as first item
                    android_pattern = r'android\s*\{'
                    match = re.search(android_pattern, content)
                    if match:
                        insert_pos = match.end()
                        # Add on new line right after android {
                        content = (
                                content[:insert_pos] +
                                '\n    ndkVersion = "27.0.12077973"' +
                                content[insert_pos:]
                        )
                    else:
                        print(f"Warning: Could not find android block in {gradle_file.name}")
                        return
                else:
                    # For Groovy script (.gradle)
                    # First remove any existing ndkVersion
                    content = re.sub(r'ndkVersion\s*["\'][\d.]+["\']', '', content)

                    # Find android block and add ndkVersion
                    android_block_start = content.find('android {')
                    if android_block_start != -1:
                        # Find position right after android {
                        insert_pos = android_block_start + len('android {')
                        # Add ndkVersion on new line
                        content = (
                                content[:insert_pos] +
                                '\n    ndkVersion "27.0.12077973"' +
                                content[insert_pos:]
                        )
                    else:
                        print(f"Warning: Could not find android block in {gradle_file.name}")
                        return

                # Only write if content actually changed
                if content != original_content:
                    # Write the updated content back
                    with open(gradle_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"Successfully updated {gradle_file.name} with NDK version 27.0.12077973")
                else:
                    print(f"No changes needed in {gradle_file.name}")

                break  # Success, exit loop

            except Exception as e:
                if attempt < 2:
                    print(f"Attempt {attempt + 1} failed to update gradle file: {e}")
                    time.sleep(1)
                else:
                    print(f"Failed to update gradle file after {attempt + 1} attempts: {e}")

    def _update_android_manifest(self):
        """Add internet permission to Android manifest"""
        manifest_path = self.project_path / 'android' / 'app' / 'src' / 'main' / 'AndroidManifest.xml'

        if manifest_path.exists():
            with open(manifest_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check if internet permission already exists
            if 'android.permission.INTERNET' not in content:
                # Add internet permission after <manifest> tag
                content = content.replace(
                    '<application',
                    '<uses-permission android:name="android.permission.INTERNET"/>\n    <application'
                )

                with open(manifest_path, 'w', encoding='utf-8') as f:
                    f.write(content)

                print("Added Internet permission to AndroidManifest.xml")

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
                'sdk': '>=3.0.0 <4.0.0'
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
                if any(char in value for char in
                       ['>', '<', ':', '{', '}', '[', ']', ',', '&', '*', '#', '?', '|', '-', '=', '!', '%', '@', '`']):
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

        # Check if there's a splash screen - it should be the initial route
        splash_screen = screens.filter(name='SplashScreen').first()
        if splash_screen:
            initial_route = splash_screen.route_name
        else:
            home_screen = screens.filter(is_home_screen=True).first()
            initial_route = home_screen.route_name if home_screen else '/'

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
          initialRoute: '{initial_route}',
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

    return MaterialColor(color.value.toInt(), swatch);
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

        # Check if screen uses GridView with categories
        uses_category_grid = Widget.objects.filter(
            screen=screen,
            widget_type='GridView'
        ).exists()

        screen_content = f'''import 'package:flutter/material.dart';
    import '../services/api_service.dart';
    import '../models/app_models.dart';'''

        # Add SharedPreferences import for Configuration and Splash screens
        if screen.name in ['Configuration', 'SplashScreen']:
            screen_content += '''
    import 'package:shared_preferences/shared_preferences.dart';'''

        # Add http import for Configuration screen
        if screen.name == 'Configuration':
            screen_content += '''
    import 'package:http/http.dart' as http;'''

        screen_content += f'''

    class {screen_class_name} extends StatefulWidget {{
      @override
      _{screen_class_name}State createState() => _{screen_class_name}State();
    }}

    class _{screen_class_name}State extends State<{screen_class_name}> {{
      final ApiService _apiService = ApiService();
      final Map<String, TextEditingController> _controllers = {{}};
      final Map<String, dynamic> _stateVariables = {{}};'''

        # Add special initialization for Splash Screen
        if screen.name == 'SplashScreen':
            screen_content += '''

      @override
      void initState() {
        super.initState();
        _checkConfiguration();
      }

      Future<void> _checkConfiguration() async {
        final prefs = await SharedPreferences.getInstance();
        final savedUrl = prefs.getString('base_url');

        if (savedUrl == null || savedUrl.isEmpty) {
          // No configuration, go to configuration screen
          if (mounted) {
            Navigator.pushReplacementNamed(context, '/configuration');
          }
        } else {
          // Configuration exists, go to home
          if (mounted) {
            Navigator.pushReplacementNamed(context, '/home');
          }
        }
      }'''

        # Add save/load methods for Configuration Screen
        if screen.name == 'Configuration':
            screen_content += '''

              final TextEditingController _urlController = TextEditingController();
              bool _isValidating = false;

              @override
              void initState() {
                super.initState();
                _loadSavedUrl();
              }

              Future<void> _loadSavedUrl() async {
                final prefs = await SharedPreferences.getInstance();
                final savedUrl = prefs.getString('base_url');
                if (savedUrl != null) {
                  _urlController.text = savedUrl;
                }
              }

              Future<void> _validateUrl() async {
                setState(() => _isValidating = true);

                String url = _urlController.text.trim();
                if (url.isEmpty) {
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(content: Text('Please enter a URL')),
                  );
                  setState(() => _isValidating = false);
                  return;
                }

                // ... rest of _validateUrl method ...
              }

              Future<void> _saveConfiguration() async {
                String url = _urlController.text.trim();
                if (url.isEmpty) {
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(content: Text('Please enter a valid URL')),
                  );
                  return;
                }

                // Add protocol if missing
                if (!url.startsWith('http://') && !url.startsWith('https://')) {
                  url = 'https://' + url;
                }

                // Remove trailing slash if present
                if (url.endsWith('/')) {
                  url = url.substring(0, url.length - 1);
                }

                // Save to SharedPreferences
                final prefs = await SharedPreferences.getInstance();
                await prefs.setString('base_url', url);

                // Clear API cache
                _apiService.clearCache();

                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(
                    content: Text('Configuration saved successfully!'),
                    backgroundColor: Colors.green,
                    duration: Duration(seconds: 1),
                  ),
                );

                // Navigate to home after a short delay
                Future.delayed(Duration(seconds: 1), () {
                  Navigator.pushReplacementNamed(context, '/home');
                });
              }'''

        screen_content += '''

      @override
      void dispose() {{
        _controllers.forEach((key, controller) => controller.dispose());'''

        if screen.name == 'Configuration':
            screen_content += '''
        _urlController.dispose();'''

        screen_content += '''
        super.dispose();
      }}'''

        # Add helper method for category icons if needed
        if uses_category_grid:
            screen_content += '''

      Widget _buildCategoryIcon(Map<String, dynamic> item) {
        if (item['image'] != null) {
          return Container(
            width: 50,
            height: 50,
            child: Image.network(
              item['image'],
              fit: BoxFit.cover,
              errorBuilder: (c, e, s) => const Icon(Icons.category, size: 30),
            ),
          );
        }

        // Use icon name from data to select appropriate icon
        IconData iconData = Icons.category;
        final iconName = item['icon']?.toString().toLowerCase() ?? '';

        switch (iconName) {
          case 'devices':
            iconData = Icons.devices;
            break;
          case 'shopping_bag':
            iconData = Icons.shopping_bag;
            break;
          case 'home':
            iconData = Icons.home;
            break;
          case 'sports_soccer':
            iconData = Icons.sports_soccer;
            break;
          case 'menu_book':
            iconData = Icons.menu_book;
            break;
          case 'face':
            iconData = Icons.face;
            break;
          case 'restaurant':
            iconData = Icons.restaurant;
            break;
          case 'favorite':
            iconData = Icons.favorite;
            break;
          case 'directions_car':
            iconData = Icons.directions_car;
            break;
          case 'toys':
            iconData = Icons.toys;
            break;
          case 'pets':
            iconData = Icons.pets;
            break;
          default:
            iconData = Icons.category;
        }

        return Icon(
          iconData,
          size: 30,
          color: Theme.of(context).primaryColor,
        );
      }'''

        screen_content += '''

      @override
      Widget build(BuildContext context) {
        return Scaffold(
    '''

        # Add AppBar if needed
        if screen.show_app_bar:
            app_bar_title = self._escape_dart_string(screen.app_bar_title or screen.name)
            screen_content += f'''      appBar: AppBar(
                title: Text('{app_bar_title}'),
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

        # Handle bottom navigation separately if it exists
        bottom_nav = Widget.objects.filter(
            screen=screen,
            widget_type='BottomNavigationBar'
        ).first()

        if bottom_nav:
            screen_content += ''',
          bottomNavigationBar: '''
            screen_content += self._generate_widget_code(bottom_nav, 0)

        screen_content += ''',
        );
      }
    }'''

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
            text_value = self._escape_dart_string(text_value)
            style_code = self._generate_text_style(prop_dict)
            widget_code = f"Text('{text_value}'{style_code})"

        elif widget.widget_type in ['ElevatedButton', 'TextButton', 'OutlinedButton']:
            text = self._get_property_value(prop_dict, 'text', 'Button')
            text = self._escape_dart_string(text)
            action_code = self._generate_action_from_property(prop_dict.get('onPressed'))
            widget_code = f'''{widget.widget_type}(
{indent}  onPressed: {action_code},
{indent}  child: Text('{text}'),
{indent})'''

        elif widget.widget_type == 'IconButton':
            icon = self._get_property_value(prop_dict, 'icon', 'add')
            action_code = self._generate_action_from_property(prop_dict.get('onPressed'))
            color = self._get_property_value(prop_dict, 'color', None)
            size = self._get_property_value(prop_dict, 'size', None)

            widget_code = f'''IconButton(
{indent}  icon: Icon(Icons.{icon}'''
            if color:
                widget_code += f", color: Color(0xFF{color.lstrip('#')})"
            if size:
                widget_code += f", size: {size}"
            widget_code += f'''),
{indent}  onPressed: {action_code},
{indent})'''
        elif widget.widget_type == 'DatePicker':
            widget_code = f'''TextButton(
        {indent}  onPressed: () async {{
        {indent}    final date = await showDatePicker(
        {indent}      context: context,
        {indent}      initialDate: DateTime.now(),
        {indent}      firstDate: DateTime(2020),
        {indent}      lastDate: DateTime(2030),
        {indent}    );
        {indent}  }},
        {indent}  child: Text('Select Date'),
        {indent})'''

        elif widget.widget_type == 'TimePicker':
            widget_code = f'''TextButton(
        {indent}  onPressed: () async {{
        {indent}    final time = await showTimePicker(
        {indent}      context: context,
        {indent}      initialTime: TimeOfDay.now(),
        {indent}    );
        {indent}  }},
        {indent}  child: Text('Select Time'),
        {indent})'''

        elif widget.widget_type == 'FileUpload':
            widget_code = f'''ElevatedButton.icon(
        {indent}  onPressed: () async {{
        {indent}    // File upload logic
        {indent}  }},
        {indent}  icon: Icon(Icons.upload_file),
        {indent}  label: Text('Upload File'),
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

            cross_alignment = self._get_property_value(prop_dict, 'crossAxisAlignment', 'center')

            # Check if this is the main home column

            is_home_column = widget.widget_id == 'home_column'

            widget_code = f'''{widget.widget_type}(

        {indent}  mainAxisAlignment: MainAxisAlignment.{alignment},

        {indent}  crossAxisAlignment: CrossAxisAlignment.{cross_alignment},'''

            if widget.widget_type == 'Column' and is_home_column:
                widget_code += f'''

        {indent}  mainAxisSize: MainAxisSize.min,'''

            widget_code += f'''

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
            obscure = self._get_property_value(prop_dict, 'obscureText', False)

            # Check if this is the URL input field for Configuration screen
            is_url_input = widget.widget_id == 'url_input'

            if is_url_input:
                widget_code = f'''TextField(
{indent}  controller: _urlController,
{indent}  decoration: InputDecoration(
{indent}    hintText: '{hint}','''
            else:
                widget_code = f'''TextField(
{indent}  decoration: InputDecoration(
{indent}    hintText: '{hint}','''

            if label:
                widget_code += f"\n{indent}    labelText: '{label}',"
            widget_code += f'''
{indent}    border: OutlineInputBorder(),
{indent}  ),'''
            if obscure:
                widget_code += f"\n{indent}  obscureText: true,"
            widget_code += f"\n{indent})"

        elif widget.widget_type == 'Image':
            widget_code = self._generate_image(prop_dict)

        elif widget.widget_type == 'Icon':
            icon_name = self._get_property_value(prop_dict, 'icon', 'info')
            icon_size = self._get_property_value(prop_dict, 'size', None)
            icon_color = self._get_property_value(prop_dict, 'color', None)

            widget_code = f"Icon(Icons.{icon_name}"
            if icon_size:
                widget_code += f", size: {icon_size}"
            if icon_color:
                widget_code += f", color: Color(0xFF{icon_color.lstrip('#')})"
            widget_code += ")"

        elif widget.widget_type == 'Divider':
            height = self._get_property_value(prop_dict, 'height', None)
            thickness = self._get_property_value(prop_dict, 'thickness', None)
            color = self._get_property_value(prop_dict, 'color', None)

            widget_code = "Divider("
            params = []
            if height:
                params.append(f"height: {height}")
            if thickness:
                params.append(f"thickness: {thickness}")
            if color:
                params.append(f"color: Color(0xFF{color.lstrip('#')})")
            widget_code += ", ".join(params)
            widget_code += ")"

        elif widget.widget_type == 'Card':
            elevation = self._get_property_value(prop_dict, 'elevation', '4')
            margin = self._get_property_value(prop_dict, 'margin', None)
            color = self._get_property_value(prop_dict, 'color', None)

            widget_code = f'''Card(
{indent}  elevation: {elevation},'''
            if margin:
                widget_code += f"\n{indent}  margin: EdgeInsets.all({margin}),"
            if color:
                widget_code += f"\n{indent}  color: Color(0xFF{color.lstrip('#')}),"
            widget_code += f'''
{indent}  child: '''
            if child_widgets.exists():
                if child_widgets.count() == 1:
                    widget_code += self._generate_widget_code(child_widgets.first(), indent_level + 1)
                else:
                    widget_code += self._generate_children_column(child_widgets, indent_level + 1)
            else:
                widget_code += "Container()"
            widget_code += f",\n{indent})"

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

        elif widget.widget_type == 'ListView':
            widget_code = self._generate_list_view(widget, prop_dict, child_widgets, indent_level)

        elif widget.widget_type == 'GridView':
            widget_code = self._generate_grid_view(widget, prop_dict, child_widgets, indent_level)


        elif widget.widget_type == 'SingleChildScrollView':

            scroll_direction = self._get_property_value(prop_dict, 'scrollDirection', 'vertical')

            physics = self._get_property_value(prop_dict, 'physics', 'AlwaysScrollableScrollPhysics')

            widget_code = f'''SingleChildScrollView(

                {indent}  scrollDirection: Axis.{scroll_direction},

                {indent}  physics: {physics}(),

                {indent}  child: '''

            if child_widgets.exists():

                if child_widgets.count() == 1:

                    widget_code += self._generate_widget_code(child_widgets.first(), indent_level + 1)

                else:

                    widget_code += f'''Column(

                {indent}    mainAxisSize: MainAxisSize.min,

                {indent}    children: [

                '''

                    for child in child_widgets:
                        widget_code += f"{indent}      {self._generate_widget_code(child, indent_level + 3)},\n"

                    widget_code += f"{indent}    ],\n{indent}  )"

            else:

                widget_code += "Container()"

            widget_code += f",\n{indent})"

        elif widget.widget_type == 'PageView':

            widget_code = f'''PageView(

        {indent}  children: [

        '''

            for child in child_widgets:
                widget_code += f"{indent}    {self._generate_widget_code(child, indent_level + 2)},\n"

            widget_code += f"{indent}  ],\n{indent})"

        elif widget.widget_type == 'Stack':

            widget_code = f'''Stack(

        {indent}  children: [

        '''

            for child in child_widgets:
                widget_code += f"{indent}    {self._generate_widget_code(child, indent_level + 2)},\n"

            widget_code += f"{indent}  ],\n{indent})"

        elif widget.widget_type == 'Positioned':

            top = self._get_property_value(prop_dict, 'top', None)

            bottom = self._get_property_value(prop_dict, 'bottom', None)

            left = self._get_property_value(prop_dict, 'left', None)

            right = self._get_property_value(prop_dict, 'right', None)

            widget_code = f"Positioned("

            params = []

            if top:
                params.append(f"top: {top}")

            if bottom:
                params.append(f"bottom: {bottom}")

            if left:
                params.append(f"left: {left}")

            if right:
                params.append(f"right: {right}")

            if params:
                widget_code += ", ".join(params) + ", "

            widget_code += "child: "

            if child_widgets.exists():

                widget_code += self._generate_widget_code(child_widgets.first(), indent_level)

            else:

                widget_code += "Container()"

            widget_code += ")"

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

        elif widget.widget_type == 'Flexible':
            flex = self._get_property_value(prop_dict, 'flex', '1')
            fit = self._get_property_value(prop_dict, 'fit', 'loose')
            widget_code = f'''Flexible(
{indent}  flex: {flex},
{indent}  fit: FlexFit.{fit},
{indent}  child: '''
            if child_widgets.exists():
                widget_code += self._generate_widget_code(child_widgets.first(), indent_level + 1)
            else:
                widget_code += "Container()"
            widget_code += f",\n{indent})"

        elif widget.widget_type == 'Wrap':
            spacing = self._get_property_value(prop_dict, 'spacing', '8.0')
            runSpacing = self._get_property_value(prop_dict, 'runSpacing', '8.0')
            widget_code = f'''Wrap(
{indent}  spacing: {spacing},
{indent}  runSpacing: {runSpacing},
{indent}  children: [
'''
            for child in child_widgets:
                widget_code += f"{indent}    {self._generate_widget_code(child, indent_level + 2)},\n"
            widget_code += f"{indent}  ],\n{indent})"
        elif widget.widget_type == 'Center':
            widget_code = f"Center(child: "
            if child_widgets.exists():
                widget_code += self._generate_widget_code(child_widgets.first(), indent_level)
            else:
                widget_code += "Container()"
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

        elif widget.widget_type == 'SizedBox':
            width = self._get_property_value(prop_dict, 'width', None)
            height = self._get_property_value(prop_dict, 'height', None)
            widget_code = f"SizedBox("
            params = []
            if width:
                params.append(f"width: {width}")
            if height:
                params.append(f"height: {height}")
            if params:
                widget_code += ", ".join(params)
                if child_widgets.exists():
                    widget_code += ", "
            if child_widgets.exists():
                widget_code += f"child: {self._generate_widget_code(child_widgets.first(), indent_level)}"
            widget_code += ")"

        elif widget.widget_type == 'AspectRatio':
            ratio = self._get_property_value(prop_dict, 'aspectRatio', '1.0')
            widget_code = f'''AspectRatio(
{indent}  aspectRatio: {ratio},
{indent}  child: '''
            if child_widgets.exists():
                widget_code += self._generate_widget_code(child_widgets.first(), indent_level + 1)
            else:
                widget_code += "Container()"
            widget_code += f",\n{indent})"

        elif widget.widget_type == 'SafeArea':
            widget_code = f'''SafeArea(
{indent}  child: '''
            if child_widgets.exists():
                widget_code += self._generate_widget_code(child_widgets.first(), indent_level + 1)
            else:
                widget_code += "Container()"
            widget_code += f",\n{indent})"

        elif widget.widget_type == 'Scaffold':
            widget_code = f'''Scaffold(
{indent}  body: '''
            if child_widgets.exists():
                widget_code += self._generate_widget_code(child_widgets.first(), indent_level + 1)
            else:
                widget_code += "Container()"
            widget_code += f",\n{indent})"

        elif widget.widget_type == 'AppBar':
            title = self._escape_dart_string(self._get_property_value(prop_dict, 'title', 'App'))
            widget_code = f"AppBar(title: Text('{title}'))"

        elif widget.widget_type == 'BottomNavigationBar':
            widget_code = self._generate_bottom_nav(child_widgets, indent_level)

        elif widget.widget_type == 'TabBar':
            widget_code = self._generate_tab_bar(child_widgets, indent_level)

        elif widget.widget_type == 'Drawer':
            widget_code = f'''Drawer(
{indent}  child: '''
            if child_widgets.exists():
                widget_code += self._generate_widget_code(child_widgets.first(), indent_level + 1)
            else:
                widget_code += "Container()"
            widget_code += f",\n{indent})"

        elif widget.widget_type == 'Switch':
            value = self._get_property_value(prop_dict, 'value', False)
            action_code = self._generate_action_from_property(prop_dict.get('onChanged'))
            widget_code = f"Switch(value: {str(value).lower()}, onChanged: {action_code if action_code != 'null' else '(v) {}'})"

        elif widget.widget_type == 'Checkbox':
            value = self._get_property_value(prop_dict, 'value', False)
            action_code = self._generate_action_from_property(prop_dict.get('onChanged'))
            widget_code = f"Checkbox(value: {str(value).lower()}, onChanged: {action_code if action_code != 'null' else '(v) {}'})"

        elif widget.widget_type == 'Radio':
            value = self._get_property_value(prop_dict, 'value', '1')
            groupValue = self._get_property_value(prop_dict, 'groupValue', '1')
            action_code = self._generate_action_from_property(prop_dict.get('onChanged'))
            widget_code = f"Radio(value: '{value}', groupValue: '{groupValue}', onChanged: {action_code if action_code != 'null' else '(v) {}'})"

        elif widget.widget_type == 'Slider':
            value = self._get_property_value(prop_dict, 'value', '0.5')
            min_val = self._get_property_value(prop_dict, 'min', '0.0')
            max_val = self._get_property_value(prop_dict, 'max', '1.0')
            action_code = self._generate_action_from_property(prop_dict.get('onChanged'))
            widget_code = f"Slider(value: {value}, min: {min_val}, max: {max_val}, onChanged: {action_code if action_code != 'null' else '(v) {}'})"

        elif widget.widget_type == 'DropdownButton':
            widget_code = self._generate_dropdown(prop_dict, indent_level)

        elif widget.widget_type == 'FutureBuilder':
            widget_code = self._generate_future_builder(prop_dict, child_widgets, indent_level)

        elif widget.widget_type == 'StreamBuilder':
            widget_code = self._generate_stream_builder(prop_dict, child_widgets, indent_level)

        else:
            # For any other widget type not explicitly handled
            widget_code = f"Container(child: Text('Widget type: {widget.widget_type}'))"

        return widget_code

    # Rest of the helper methods remain the same...
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

        # First, handle Unicode normalization and smart quotes
        import unicodedata

        # Normalize Unicode characters
        try:
            text = unicodedata.normalize('NFKD', text)
        except:
            pass

        # Replace problematic Unicode characters BEFORE escaping
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
            ''': "'",  # Left single quotation mark
            ''': "'",  # Right single quotation mark
            '"': '"',  # Left double quotation mark
            '"': '"',  # Right double quotation mark
            '–': '-',  # En dash
            '—': '-',  # Em dash
            '…': '...',  # Ellipsis
            '\u2018': "'",  # Unicode left single quote
            '\u2019': "'",  # Unicode right single quote
            '\u201C': '"',  # Unicode left double quote
            '\u201D': '"',  # Unicode right double quote
        }

        for old_char, new_char in replacements.items():
            text = text.replace(old_char, new_char)

        # Remove any remaining non-printable or problematic Unicode characters
        cleaned_text = []
        for char in text:
            if ord(char) < 32 and char not in '\n\r\t':
                # Skip control characters except newline, carriage return, tab
                continue
            elif ord(char) > 126 and ord(char) < 160:
                # Skip non-printable extended ASCII
                continue
            elif ord(char) >= 160:
                # Try to convert extended characters to ASCII equivalent
                try:
                    ascii_equiv = unicodedata.normalize('NFKD', char).encode('ascii', 'ignore').decode('ascii')
                    if ascii_equiv:
                        cleaned_text.append(ascii_equiv)
                    else:
                        cleaned_text.append(' ')  # Replace with space if no equivalent
                except:
                    cleaned_text.append(' ')  # Replace with space on error
            else:
                cleaned_text.append(char)

        text = ''.join(cleaned_text)

        # Now escape for Dart strings - ORDER MATTERS!
        text = text.replace('\\', '\\\\')  # Escape backslashes FIRST
        text = text.replace("'", "\\'")  # Escape single quotes
        text = text.replace('"', '\\"')  # Escape double quotes
        text = text.replace('\n', '\\n')  # Escape newlines
        text = text.replace('\r', '\\r')  # Escape carriage returns
        text = text.replace('\t', '\\t')  # Escape tabs
        text = text.replace('$', '\\$')  # Escape dollar signs

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

        # Check for scroll direction property
        scroll_direction = self._get_property_value(prop_dict, 'scrollDirection', 'vertical')
        is_horizontal = scroll_direction == 'horizontal'

        if data_source_prop and data_source_prop.data_source_field_reference:
            # Dynamic ListView with data source
            data_source = data_source_prop.data_source_field_reference.data_source
            field = data_source_prop.data_source_field_reference

            # Determine if this is a product-related data source
            is_product_list = any(keyword in data_source.name.lower()
                                  for keyword in ['product', 'flash', 'trending', 'arrival', 'seller', 'best'])

            # For horizontal lists, use Container with fixed height
            height_wrapper_start = ""
            height_wrapper_end = ""
            if is_horizontal:
                height_wrapper_start = f"Container(height: 280, child: "
                height_wrapper_end = ")"

            return f'''{height_wrapper_start}FutureBuilder<List<dynamic>>(
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
    {indent}      scrollDirection: Axis.{'horizontal' if is_horizontal else 'vertical'},
    {indent}      shrinkWrap: {'false' if is_horizontal else 'true'},
    {indent}      physics: {'ClampingScrollPhysics()' if is_horizontal else 'NeverScrollableScrollPhysics()'},
    {indent}      primary: false,
    {indent}      itemCount: items.length,
    {indent}      itemBuilder: (context, index) {{
    {indent}        final item = items[index];
    {indent}        return {self._generate_list_item_widget(data_source.name, field.field_name, is_horizontal, is_product_list, indent_level + 3)};
    {indent}      }},
    {indent}    );
    {indent}  }},
    {indent}){height_wrapper_end}'''
        else:
            # Static ListView with child widgets
            if child_widgets.exists():
                code = f"ListView(\n{indent}  shrinkWrap: true,\n{indent}  physics: NeverScrollableScrollPhysics(),\n{indent}  primary: false,\n{indent}  children: [\n"
                for child in child_widgets:
                    code += f"{indent}    {self._generate_widget_code(child, indent_level + 2)},\n"
                code += f"{indent}  ],\n{indent})"
                return code
            else:
                return "ListView(shrinkWrap: true, physics: NeverScrollableScrollPhysics(), children: [])"

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

            # Check if this is categories grid
            is_categories = 'categor' in data_source.name.lower()

            return f'''FutureBuilder<List<dynamic>>(
    {indent}  future: _apiService.fetchData('{data_source.name}'),
    {indent}  builder: (context, snapshot) {{
    {indent}    if (snapshot.connectionState == ConnectionState.waiting) {{
    {indent}      return Container(
    {indent}        height: 200,
    {indent}        child: Center(child: CircularProgressIndicator()),
    {indent}      );
    {indent}    }}
    {indent}    if (snapshot.hasError) {{
    {indent}      return Container(
    {indent}        height: 200,
    {indent}        child: Center(child: Text('Error loading data')),
    {indent}      );
    {indent}    }}
    {indent}    final data = snapshot.data ?? [];
    {indent}    if (data.isEmpty) {{
    {indent}      return Container(
    {indent}        height: 200,
    {indent}        child: Center(child: Text('No items')),
    {indent}      );
    {indent}    }}
    {indent}    return GridView.builder(
    {indent}      shrinkWrap: true,
    {indent}      physics: NeverScrollableScrollPhysics(),
    {indent}      gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
    {indent}        crossAxisCount: {columns},
    {indent}        crossAxisSpacing: 8,
    {indent}        mainAxisSpacing: 8,
    {indent}        childAspectRatio: {('1.0' if is_categories else '0.8')},
    {indent}      ),
    {indent}      itemCount: data.length > 8 ? 8 : data.length,
    {indent}      itemBuilder: (context, index) {{
    {indent}        final item = data[index];
    {indent}        return {self._generate_category_item(indent_level + 3) if is_categories else self._generate_grid_item(field.field_name, indent_level + 3)};
    {indent}      }},
    {indent}    );
    {indent}  }},
    {indent})'''
        else:
            # Static GridView
            return f'''GridView.count(
    {indent}  crossAxisCount: {columns},
    {indent}  shrinkWrap: true,
    {indent}  physics: NeverScrollableScrollPhysics(),
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

    def _generate_bottom_nav(self, child_widgets, indent_level):
        """Generate BottomNavigationBar dynamically from child widgets"""
        indent = '  ' * indent_level

        # Generate navigation items from child widgets
        nav_items = []
        nav_actions = []

        for i, child in enumerate(child_widgets):
            # Get properties from child widget
            properties = WidgetProperty.objects.filter(widget=child)
            prop_dict = {prop.property_name: prop for prop in properties}

            icon = self._get_property_value(prop_dict, 'icon', 'home')
            label = self._get_property_value(prop_dict, 'label', f'Item {i + 1}')

            nav_items.append({
                'icon': icon,
                'label': label
            })

            # Get navigation action if exists
            if 'onTap' in prop_dict and prop_dict['onTap'].action_reference:
                action = prop_dict['onTap'].action_reference
                if action.target_screen:
                    nav_actions.append(f"Navigator.pushNamed(context, '{action.target_screen.route_name}');")
                else:
                    nav_actions.append("// No action configured")
            else:
                nav_actions.append("// No action configured")

        # Build the navigation bar
        result = f'''BottomNavigationBar(
    {indent}  type: BottomNavigationBarType.fixed,
    {indent}  currentIndex: 0,
    {indent}  selectedItemColor: Theme.of(context).primaryColor,
    {indent}  unselectedItemColor: Colors.grey,
    {indent}  onTap: (index) {{
    {indent}    switch (index) {{'''

        for i, action in enumerate(nav_actions):
            result += f'''
    {indent}      case {i}:
    {indent}        {action}
    {indent}        break;'''

        result += f'''
    {indent}    }}
    {indent}  }},
    {indent}  items: ['''

        # Generate items properly without string concatenation issues
        for i, item in enumerate(nav_items):
            result += f'''
    {indent}    BottomNavigationBarItem(
    {indent}      icon: Icon(Icons.{item['icon']}),
    {indent}      label: '{item['label']}',
    {indent}    ),'''

        result += f'''
    {indent}  ],
    {indent})'''

        return result

    def _generate_tab_bar(self, child_widgets, indent_level):
        """Generate TabBar"""
        indent = '  ' * indent_level
        # Simplified tab bar generation
        return "TabBar(tabs: [Tab(text: 'Tab 1'), Tab(text: 'Tab 2')])"

    def _generate_dropdown(self, prop_dict, indent_level):
        """Generate DropdownButton"""
        indent = '  ' * indent_level
        items = self._get_property_value(prop_dict, 'items', 'Option 1,Option 2,Option 3')
        value = self._get_property_value(prop_dict, 'value', None)

        items_list = items.split(',')
        dropdown_items = ', '.join(
            [f"DropdownMenuItem(value: '{item.strip()}', child: Text('{item.strip()}'))" for item in items_list])

        return f"DropdownButton(items: [{dropdown_items}], onChanged: (v) {{}})"

    def _generate_future_builder(self, prop_dict, child_widgets, indent_level):
        """Generate FutureBuilder"""
        indent = '  ' * indent_level
        # Simplified FutureBuilder
        return f'''FutureBuilder(
{indent}  future: Future.value(true),
{indent}  builder: (context, snapshot) {{
{indent}    if (snapshot.hasData) {{
{indent}      return Container();
{indent}    }}
{indent}    return CircularProgressIndicator();
{indent}  }},
{indent})'''

    def _generate_stream_builder(self, prop_dict, child_widgets, indent_level):
        """Generate StreamBuilder"""
        indent = '  ' * indent_level
        # Simplified StreamBuilder
        return f'''StreamBuilder(
{indent}  stream: Stream.empty(),
{indent}  builder: (context, snapshot) {{
{indent}    return Container();
{indent}  }},
{indent})'''

    def _generate_action_code(self, action):
        """Generate Dart code for actions"""
        # Handle special configuration actions
        if action.name == 'SaveConfiguration':
            return "_saveConfiguration"
        elif action.name == 'ValidateConfiguration':
            return "_validateUrl"
        elif action.name == 'LoadConfiguration':
            return "_loadSavedUrl"

        # Normal navigation
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
        elif action.action_type == 'show_snackbar':
            return f'''() {{
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(content: Text('{action.dialog_message or 'Message'}'))
              );
            }}'''
        elif action.action_type == 'api_call':
            if action.api_data_source:
                return f"() {{ _apiService.fetchData('{action.api_data_source.name}'); }}"
        elif action.action_type == 'open_url':
            return f"() {{ /* Open URL: {action.url} */ }}"
        elif action.action_type == 'share_content':
            return "() { /* Share content */ }"

        return "null"

    def _generate_services(self):
        """Generate API service - all data sources are dynamic APIs"""
        data_sources = DataSource.objects.filter(application=self.application)

        service_content = '''import 'dart:convert';
    import 'package:http/http.dart' as http;
    import 'package:shared_preferences/shared_preferences.dart';

    class ApiService {
      static final ApiService _instance = ApiService._internal();
      factory ApiService() => _instance;
      ApiService._internal();

      String? _cachedBaseUrl;

      // Get base URL - check saved configuration first, then use default
Future<String> _getBaseUrl(String defaultUrl) async {
  // Return cached URL if available
  if (_cachedBaseUrl != null && _cachedBaseUrl!.isNotEmpty) {
    return _cachedBaseUrl!;
  }

  // Always check for saved URL first
  final prefs = await SharedPreferences.getInstance();
  final savedUrl = prefs.getString('base_url');

  // Check if base URL is special marker or if we should use saved URL
  if (defaultUrl == 'LOCAL_STORAGE' || defaultUrl == 'DYNAMIC' || defaultUrl.isEmpty) {
    if (savedUrl == null || savedUrl.isEmpty) {
      throw Exception('No server URL configured. Please configure the server URL first.');
    }
    _cachedBaseUrl = savedUrl;
    return _cachedBaseUrl!;
  }

  // Use saved URL if exists, otherwise use default from database
  _cachedBaseUrl = (savedUrl != null && savedUrl.isNotEmpty) ? savedUrl : defaultUrl;
  
  if (_cachedBaseUrl == null || _cachedBaseUrl!.isEmpty) {
    throw Exception('No server URL configured. Please configure the server URL first.');
  }
  
  return _cachedBaseUrl!;
}

      // Clear cached URL when configuration changes
      void clearCache() {
        _cachedBaseUrl = null;
      }

    '''

        # Generate methods for each data source
        for data_source in data_sources:
            method_name = self._to_camel_case(data_source.name)

            service_content += f'''
      Future<List<dynamic>> fetch{self._to_pascal_case(data_source.name)}() async {{
        try {{
          final baseUrl = await _getBaseUrl('{data_source.base_url}');
          final url = '${{baseUrl}}{data_source.endpoint}';
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
            padding: padding ?? const EdgeInsets.all(16.0),
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
              const CircularProgressIndicator(),
              if (message != null) ...[
                const SizedBox(height: 16),
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
              const Icon(Icons.error_outline, size: 64, color: Colors.red),
              const SizedBox(height: 16),
              Text(message, textAlign: TextAlign.center),
              if (onRetry != null) ...[
                const SizedBox(height: 16),
                ElevatedButton(
                  onPressed: onRetry,
                  child: const Text('Retry'),
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
        # First, replace special characters with underscores
        text = re.sub(r'[&\+\-\*\/\\\|\?\!\@\#\$\%\^\(\)\[\]\{\}\<\>\,\.\;\:\'\"\`\~]', '_', text)
        # Then handle camelCase conversion
        text = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', text)
        text = re.sub(r'([a-z\d])([A-Z])', r'\1_\2', text)
        # Replace spaces and multiple underscores with single underscore
        text = text.lower().replace(' ', '_')
        text = re.sub(r'_+', '_', text)  # Replace multiple underscores with single
        text = text.strip('_')  # Remove leading/trailing underscores
        return text

    def _to_pascal_case(self, text):
        """Convert text to PascalCase"""
        import re
        # Replace special characters with spaces
        text = re.sub(r'[&\+\-\*\/\\\|\?\!\@\#\$\%\^\(\)\[\]\{\}\<\>\,\.\;\:\'\"\`\~_]', ' ', text)
        # Split by spaces and capitalize each word
        words = [word.capitalize() for word in text.split() if word]
        return ''.join(words)

    def _to_camel_case(self, text):
        """Convert text to camelCase"""
        pascal = self._to_pascal_case(text)
        if not pascal:
            return ''
        # Ensure the result starts with a lowercase letter and is a valid identifier
        result = pascal[0].lower() + pascal[1:]
        # If the result starts with a number, prefix with underscore
        if result and result[0].isdigit():
            result = '_' + result
        return result

    def _generate_list_item_widget(self, data_source_name, field_name, is_horizontal, is_product_list, indent_level):
        """Generate dynamic list item widget based on data source fields"""
        indent = '  ' * indent_level

        # Get the data source to understand available fields
        try:
            data_source = DataSource.objects.get(application=self.application, name=data_source_name)
            fields = DataSourceField.objects.filter(data_source=data_source)
            field_dict = {f.field_name: f for f in fields}
        except:
            field_dict = {}

        # Determine container width based on orientation
        width_style = "width: 150," if is_horizontal else ""

        # Build dynamic card based on available fields
        return f'''Container(
    {indent}  {width_style}
    {indent}  margin: EdgeInsets.symmetric(horizontal: 4, vertical: 4),
    {indent}  child: Card(
    {indent}    elevation: 2,
    {indent}    child: InkWell(
    {indent}      onTap: () {{
    {indent}        if (item['id'] != null) {{
    {indent}          // Navigate to detail if ID exists
    {indent}          Navigator.pushNamed(context, '/detail/${{item['id']}}');
    {indent}        }}
    {indent}      }},
    {indent}      child: {self._generate_dynamic_list_content(field_dict, indent_level + 3)},
    {indent}    ),
    {indent}  ),
    {indent})'''

    def _generate_dynamic_list_content(self, field_dict, indent_level):
        """Generate list content based on available fields"""
        indent = '  ' * indent_level

        # Check what fields are available
        has_image = any(f.field_type == 'image_url' for f in field_dict.values())
        has_title = 'name' in field_dict or 'title' in field_dict
        has_price = 'price' in field_dict
        has_description = 'description' in field_dict

        content = f'''Column(
    {indent}  crossAxisAlignment: CrossAxisAlignment.start,
    {indent}  children: ['''

        # Add image if available
        if has_image:
            image_field = next((f for f in field_dict.keys() if 'image' in f.lower()), 'image')
            content += f'''
    {indent}    Container(
    {indent}      height: 120,
    {indent}      width: double.infinity,
    {indent}      child: item['{image_field}'] != null
    {indent}        ? Image.network(
    {indent}            item['{image_field}'],
    {indent}            fit: BoxFit.cover,
    {indent}            errorBuilder: (c,e,s) => Icon(Icons.image),
    {indent}          )
    {indent}        : Icon(Icons.image, size: 50),
    {indent}    ),'''

        # Add text content
        content += f'''
    {indent}    Padding(
    {indent}      padding: EdgeInsets.all(8),
    {indent}      child: Column(
    {indent}        crossAxisAlignment: CrossAxisAlignment.start,
    {indent}        children: ['''

        # Add title
        if has_title:
            title_field = 'title' if 'title' in field_dict else 'name'
            content += f'''
    {indent}          Text(
    {indent}            item['{title_field}']?.toString() ?? '',
    {indent}            style: TextStyle(fontWeight: FontWeight.bold),
    {indent}            maxLines: 2,
    {indent}            overflow: TextOverflow.ellipsis,
    {indent}          ),'''

        # Add price if available
        if has_price:
            content += f'''
    {indent}          Text(
    {indent}            '\\$${{item['price']?.toString() ?? ''}}',
    {indent}            style: TextStyle(color: Theme.of(context).primaryColor),
    {indent}          ),'''

        # Add description if available
        if has_description:
            content += f'''
    {indent}          Text(
    {indent}            item['description']?.toString() ?? '',
    {indent}            style: TextStyle(fontSize: 12),
    {indent}            maxLines: 2,
    {indent}            overflow: TextOverflow.ellipsis,
    {indent}          ),'''

        content += f'''
    {indent}        ],
    {indent}      ),
    {indent}    ),
    {indent}  ],
    {indent})'''

        return content

    def _generate_category_item(self, indent_level):
        """Generate generic grid item"""
        indent = '  ' * indent_level
        return f'''InkWell(
    {indent}  onTap: () {{
    {indent}    if (item['id'] != null) {{
    {indent}      Navigator.pushNamed(context, '/detail/${{item['id']}}');
    {indent}    }}
    {indent}  }},
    {indent}  borderRadius: BorderRadius.circular(8),
    {indent}  child: Card(
    {indent}    child: Column(
    {indent}      mainAxisAlignment: MainAxisAlignment.center,
    {indent}      children: [
    {indent}        _buildCategoryIcon(item),
    {indent}        const SizedBox(height: 8),
    {indent}        Text(
    {indent}          item['name']?.toString() ?? item['title']?.toString() ?? '',
    {indent}          style: const TextStyle(fontSize: 12),
    {indent}          textAlign: TextAlign.center,
    {indent}          maxLines: 2,
    {indent}          overflow: TextOverflow.ellipsis,
    {indent}        ),
    {indent}      ],
    {indent}    ),
    {indent}  ),
    {indent})'''

    def _generate_grid_item(self, field_name, indent_level):
        """Generate generic grid item"""
        indent = '  ' * indent_level
        return f'''Card(
    {indent}  child: Center(
    {indent}    child: Text(item['{field_name}']?.toString() ?? ''),
    {indent}  ),
    {indent})'''