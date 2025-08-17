# File: core/services/code_generation/screens/special_screens.py
"""
Handles generation of special screens (Splash, Configuration, etc.).
"""

from typing import Any
from pathlib import Path

from ..base import GeneratorContext
from ..utils import StringUtils, DartCodeUtils
from .screen_builder import ScreenBuilder


class SpecialScreenHandler:
    """
    Handles generation of special screens with custom logic.
    """

    SPECIAL_SCREENS = ['SplashScreen', 'Configuration']

    def __init__(self):
        self.screen_builder = ScreenBuilder()

    def is_special_screen(self, screen_name: str) -> bool:
        """
        Check if a screen is a special screen.

        Args:
            screen_name: Name of the screen

        Returns:
            bool: True if special screen
        """
        return screen_name in self.SPECIAL_SCREENS

    def generate_screen(self, screen: Any, context: GeneratorContext) -> bool:
        """
        Generate a special screen.

        Args:
            screen: Screen model instance
            context: GeneratorContext

        Returns:
            bool: True if successful
        """
        if screen.name == 'SplashScreen':
            return self._generate_splash_screen(screen, context)
        elif screen.name == 'Configuration':
            return self._generate_configuration_screen(screen, context)
        else:
            # Fallback to regular screen builder
            return self.screen_builder.generate_screen(screen, context)

    def _generate_splash_screen(self, screen: Any, context: GeneratorContext) -> bool:
        """
        Generate SplashScreen with navigation logic.

        Args:
            screen: Screen model instance
            context: GeneratorContext

        Returns:
            bool: True if successful
        """
        try:
            # Find next screen to navigate to
            from core.models import Screen
            home_screen = Screen.objects.filter(
                application=context.application,
                name='Home'
            ).first()

            if not home_screen:
                home_screen = Screen.objects.filter(
                    application=context.application
                ).exclude(name='SplashScreen').exclude(name='Configuration').first()

            next_route = home_screen.route_name if home_screen else '/home'
            config_route = '/configuration' if context.has_config_screen else next_route

            # Build screen content
            content = self._build_splash_screen_content(
                screen,
                context,
                next_route,
                config_route
            )

            # Write file
            screen_file_name = StringUtils.to_snake_case(screen.name) + '_screen.dart'
            file_path = context.lib_path / 'screens' / screen_file_name

            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            context.add_generated_file(file_path)
            return True

        except Exception as e:
            context.add_error(f"Failed to generate SplashScreen: {str(e)}")
            return False

    def _build_splash_screen_content(self, screen: Any, context: GeneratorContext,
                                     next_route: str, config_route: str) -> str:
        """
        Build SplashScreen content with navigation logic.
        """
        normalized_name = screen.name.replace(' ', '')
        screen_class_name = StringUtils.to_pascal_case(normalized_name) + 'Screen'

        # Get root widgets
        from core.models import Widget
        root_widgets = list(Widget.objects.filter(
            screen=screen,
            parent_widget=None
        ).order_by('order'))

        imports = ["import 'package:flutter/material.dart';"]
        if context.has_config_screen:
            imports.append("import 'package:shared_preferences/shared_preferences.dart';")

        content = f'''{chr(10).join(imports)}

class {screen_class_name} extends StatefulWidget {{
  @override
  _{screen_class_name}State createState() => _{screen_class_name}State();
}}

class _{screen_class_name}State extends State<{screen_class_name}> {{
  @override
  void initState() {{
    super.initState();
    _checkConfigurationAndNavigate();
  }}

  Future<void> _checkConfigurationAndNavigate() async {{
    await Future.delayed(Duration(seconds: 2));

    if (!mounted) return;
'''

        if context.has_config_screen:
            content += f'''
    final prefs = await SharedPreferences.getInstance();
    final savedUrl = prefs.getString('base_url');

    if (savedUrl == null || savedUrl.isEmpty) {{
      Navigator.pushReplacementNamed(context, '{config_route}');
    }} else {{
      Navigator.pushReplacementNamed(context, '{next_route}');
    }}'''
        else:
            content += f'''
    Navigator.pushReplacementNamed(context, '{next_route}');'''

        content += '''
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: '''

        # Add body widgets
        if root_widgets:
            from ..widgets.widget_generator import WidgetGenerator
            widget_gen = WidgetGenerator()
            if len(root_widgets) == 1:
                content += widget_gen.generate_widget(root_widgets[0], context, 0)
            else:
                content += '''Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
'''
                for widget in root_widgets:
                    content += '          ' + widget_gen.generate_widget(widget, context, 2) + ',\n'
                content += '''        ],
      )'''
        else:
            content += '''Center(
        child: CircularProgressIndicator(),
      )'''

        content += '''
    );
  }
}'''

        return content

    def _generate_configuration_screen(self, screen: Any, context: GeneratorContext) -> bool:
        """
        Generate Configuration screen with server URL setup.

        Args:
            screen: Screen model instance
            context: GeneratorContext

        Returns:
            bool: True if successful
        """
        try:
            # Find home screen to navigate to after configuration
            from core.models import Screen
            home_screen = Screen.objects.filter(
                application=context.application,
                is_home_screen=True
            ).first()

            next_route = home_screen.route_name if home_screen else '/home'

            # Build screen content
            content = self._build_configuration_screen_content(screen, context, next_route)

            # Write file
            screen_file_name = StringUtils.to_snake_case(screen.name) + '_screen.dart'
            file_path = context.lib_path / 'screens' / screen_file_name

            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            context.add_generated_file(file_path)
            return True

        except Exception as e:
            context.add_error(f"Failed to generate Configuration screen: {str(e)}")
            return False

    def _build_configuration_screen_content(self, screen: Any, context: GeneratorContext,
                                            next_route: str) -> str:
        """
        Build Configuration screen content.
        """
        normalized_name = screen.name.replace(' ', '')
        screen_class_name = StringUtils.to_pascal_case(normalized_name) + 'Screen'

        content = f'''import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:http/http.dart' as http;
import '../services/api_service.dart';

class {screen_class_name} extends StatefulWidget {{
  @override
  _{screen_class_name}State createState() => _{screen_class_name}State();
}}

class _{screen_class_name}State extends State<{screen_class_name}> {{
  final ApiService _apiService = ApiService();
  final TextEditingController _urlController = TextEditingController();
  bool _isValidating = false;
  bool _isSaving = false;
  String? _errorMessage;

  @override
  void initState() {{
    super.initState();
    _loadSavedUrl();
  }}

  @override
  void dispose() {{
    _urlController.dispose();
    super.dispose();
  }}

  Future<void> _loadSavedUrl() async {{
    final prefs = await SharedPreferences.getInstance();
    final savedUrl = prefs.getString('base_url');
    if (savedUrl != null) {{
      setState(() {{
        _urlController.text = savedUrl;
      }});
    }}
  }}

  Future<void> _validateUrl() async {{
    final url = _urlController.text.trim();

    if (url.isEmpty) {{
      setState(() {{
        _errorMessage = 'Please enter a URL';
      }});
      return;
    }}

    setState(() {{
      _isValidating = true;
      _errorMessage = null;
    }});

    try {{
      String testUrl = url;
      if (!testUrl.startsWith('http://') && !testUrl.startsWith('https://')) {{
        testUrl = 'http://' + testUrl;
      }}

      final response = await http.get(
        Uri.parse('$testUrl/api/test'),
      ).timeout(Duration(seconds: 10));

      if (response.statusCode == 200) {{
        setState(() {{
          _isValidating = false;
          _errorMessage = null;
        }});
        _urlController.text = testUrl;
        _saveConfiguration();
      }} else {{
        setState(() {{
          _isValidating = false;
          _errorMessage = 'Server returned error: ${{response.statusCode}}';
        }});
      }}
    }} catch (e) {{
      setState(() {{
        _isValidating = false;
        _errorMessage = 'Connection failed: ${{e.toString()}}';
      }});
    }}
  }}

  Future<void> _saveConfiguration() async {{
    final url = _urlController.text.trim();

    setState(() {{
      _isSaving = true;
    }});

    String cleanUrl = url;
    if (cleanUrl.endsWith('/')) {{
      cleanUrl = cleanUrl.substring(0, cleanUrl.length - 1);
    }}

    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('base_url', cleanUrl);

    _apiService.clearCache();

    setState(() {{
      _isSaving = false;
    }});

    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text('Configuration saved successfully!'),
        backgroundColor: Colors.green,
      ),
    );

    await Future.delayed(Duration(seconds: 1));
    if (mounted) {{
      Navigator.pushReplacementNamed(context, '{next_route}');
    }}
  }}

  @override
  Widget build(BuildContext context) {{
    return Scaffold(
      appBar: AppBar(
        title: Text('Configuration'),
      ),
      body: Padding(
        padding: EdgeInsets.all(16),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            TextField(
              controller: _urlController,
              decoration: InputDecoration(
                hintText: 'Enter server URL',
                labelText: 'Server URL',
                prefixIcon: Icon(Icons.link),
                border: OutlineInputBorder(),
                errorText: _errorMessage,
              ),
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: (_isValidating || _isSaving) ? null : _validateUrl,
              child: _isValidating
                  ? CircularProgressIndicator(color: Colors.white)
                  : Text('Validate and Save'),
            ),
          ],
        ),
      ),
    );
  }}
}}'''

        return content