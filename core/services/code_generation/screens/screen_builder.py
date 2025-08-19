# File: core/services/code_generation/screens/screen_builder.py
"""
Builds regular screens for Flutter applications.
"""

from typing import Any, List
from pathlib import Path

from ..base import GeneratorContext
from ..utils import StringUtils, DartCodeUtils
from ..widgets.widget_generator import WidgetGenerator


class ScreenBuilder:
    """
    Builds regular (non-special) screens.
    """

    def __init__(self):
        self.widget_generator = WidgetGenerator()

    def generate_screen(self, screen: Any, context: GeneratorContext) -> bool:
        """
        Generate a single screen file.

        Args:
            screen: Screen model instance
            context: GeneratorContext containing project information

        Returns:
            bool: True if successful
        """
        try:
            # Generate screen content
            content = self._build_screen_content(screen, context)

            # Determine file path - ensure consistent naming
            screen_file_name = StringUtils.to_snake_case(screen.name) + '_screen.dart'
            file_path = context.lib_path / 'screens' / screen_file_name

            # Write file
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            context.add_generated_file(file_path)

            # Log successful generation
            print(f"Generated screen: {screen.name} -> {screen_file_name}")

            return True

        except Exception as e:
            context.add_error(f"Failed to generate screen {screen.name}: {str(e)}")
            print(f"Error generating screen {screen.name}: {str(e)}")
            return False

    def _build_screen_content(self, screen: Any, context: GeneratorContext) -> str:
        """
        Build the content for a screen file.

        Args:
            screen: Screen model instance
            context: GeneratorContext containing project information

        Returns:
            str: Screen file content
        """
        # Normalize screen name - handle spaces and special cases
        normalized_name = screen.name.replace(' ', '').replace('&', 'And')
        # Remove any non-alphanumeric characters
        import re
        normalized_name = re.sub(r'[^a-zA-Z0-9]', '', normalized_name)
        screen_class_name = StringUtils.to_pascal_case(normalized_name) + 'Screen'

        # Get root widgets for this screen - excluding BottomNavigationBar
        root_widgets = self._get_root_widgets_excluding_navigation(screen)

        # Check if any widget uses FutureBuilder
        has_future_builder = self._check_for_future_builder(root_widgets)

        # Build imports
        imports = self._build_imports(screen, context)

        # Build class definition - AVOIDING F-STRING ISSUES WITH UNDERSCORES
        content = imports + '\n\n'
        content += 'class ' + screen_class_name + ' extends StatefulWidget {\n'
        content += '  @override\n'
        content += '  _' + screen_class_name + 'State createState() => _' + screen_class_name + 'State();\n'
        content += '}\n\n'
        content += 'class _' + screen_class_name + 'State extends State<' + screen_class_name + '> {\n'
        content += '  final ApiService _apiService = ApiService();\n'
        content += '  final Map<String, TextEditingController> _controllers = {};\n'
        content += '  final Map<String, dynamic> _stateVariables = {\n'
        content += '    // Initialize state variables for interactive widgets\n'
        content += '    "notifications_switch": true,\n'
        content += '    "auto_refresh_switch": true,\n'
        content += '    "dark_mode_switch": false,\n'
        content += '  };\n'
        content += '  int _selectedIndex = 0;\n\n'
        content += '  @override\n'
        content += '  void dispose() {\n'
        content += '    _controllers.forEach((key, controller) => controller.dispose());\n'
        content += '    super.dispose();\n'
        content += '  }\n\n'
        content += '  @override\n'
        content += '  Widget build(BuildContext context) {\n'
        content += '    return Scaffold(\n'

        # Add AppBar if needed
        if screen.show_app_bar:
            app_bar_title = DartCodeUtils.escape_dart_string(screen.app_bar_title or screen.name)
            content += '      appBar: AppBar(\n'
            content += f"        title: Text('{app_bar_title}'),\n"
            content += f"        automaticallyImplyLeading: {str(screen.show_back_button).lower()},\n"
            content += '      ),\n'

        # Add body
        content += '      body: '

        if root_widgets:
            if len(root_widgets) == 1:
                content += self.widget_generator.generate_widget(root_widgets[0], context, 0)
            else:
                content += self._generate_multiple_widgets(root_widgets, context)
        else:
            content += "Center(child: Text('No content configured for this screen'))"

        # Handle bottom navigation if exists
        bottom_nav = self._get_bottom_navigation(screen)
        if bottom_nav:
            content += ',\n      bottomNavigationBar: '
            content += self.widget_generator.generate_widget(bottom_nav, context, 0)

        content += '\n    );\n'
        content += '  }\n'

        # Add helper methods if FutureBuilder is used
        if has_future_builder:
            content += '''

      Widget _buildSingleItemView(Map<String, dynamic> data) {
        return Container(
          padding: EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: data.entries.map((entry) {
              return Padding(
                padding: EdgeInsets.symmetric(vertical: 4),
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      '${entry.key}: ',
                      style: TextStyle(fontWeight: FontWeight.bold),
                    ),
                    Expanded(
                      child: Text(
                        '${entry.value}',
                        softWrap: true,
                      ),
                    ),
                  ],
                ),
              );
            }).toList(),
          ),
        );
      }

      Widget _buildListView(List<dynamic> items) {
        return ListView.builder(
          shrinkWrap: true,
          itemCount: items.length,
          itemBuilder: (context, index) {
            final item = items[index];
            if (item is Map<String, dynamic>) {
              return Card(
                margin: EdgeInsets.all(8),
                child: _buildSingleItemView(item),
              );
            } else {
              return ListTile(
                title: Text('$item'),
              );
            }
          },
        );
      }'''

        content += '\n}'

        return content

    def _build_imports(self, screen: Any, context: GeneratorContext) -> str:
        """
        Build import statements for a screen.

        Args:
            screen: Screen model instance
            context: GeneratorContext containing project information

        Returns:
            str: Import statements
        """
        imports = [
            "import 'package:flutter/material.dart';",
            "import '../services/api_service.dart';",
            "import '../models/app_models.dart';"
        ]

        # Check if screen uses GridView with categories
        from core.models import Widget
        uses_grid = Widget.objects.filter(
            screen=screen,
            widget_type='GridView'
        ).exists()

        if uses_grid:
            # Add any additional imports needed for grid views
            pass

        return '\n'.join(imports)

    def _get_root_widgets(self, screen: Any) -> List[Any]:
        """
        Get root widgets for a screen.

        Args:
            screen: Screen model instance

        Returns:
            List: Root widgets ordered by position
        """
        from core.models import Widget
        return list(Widget.objects.filter(
            screen=screen,
            parent_widget=None
        ).order_by('order'))

    def _get_bottom_navigation(self, screen: Any) -> Any:
        """
        Get bottom navigation widget for a screen if exists.

        Args:
            screen: Screen model instance

        Returns:
            Widget instance or None
        """
        from core.models import Widget
        return Widget.objects.filter(
            screen=screen,
            widget_type='BottomNavigationBar'
        ).first()

    def _generate_multiple_widgets(self, widgets: List[Any], context: GeneratorContext) -> str:
        """
        Generate code for multiple root widgets wrapped in a Column.

        Args:
            widgets: List of widget instances
            context: GeneratorContext

        Returns:
            str: Generated Dart code
        """
        code = '''Column(
        children: [
'''
        for widget in widgets:
            code += '          ' + self.widget_generator.generate_widget(widget, context, 2) + ',\n'

        code += '''        ],
      )'''

        return code

    def _get_root_widgets_excluding_navigation(self, screen: Any) -> List[Any]:
        """
        Get root widgets for a screen, excluding navigation widgets.

        Args:
            screen: Screen model instance

        Returns:
            List: Root widgets ordered by position, excluding BottomNavigationBar
        """
        from core.models import Widget
        return list(Widget.objects.filter(
            screen=screen,
            parent_widget=None
        ).exclude(
            widget_type__in=['BottomNavigationBar', 'AppBar', 'Drawer']
        ).order_by('order'))

    def _check_for_future_builder(self, widgets: List[Any]) -> bool:
        """
        Check if any widget in the tree is a FutureBuilder.

        Args:
            widgets: List of widgets to check

        Returns:
            bool: True if FutureBuilder found
        """
        from core.models import Widget

        for widget in widgets:
            if widget.widget_type == 'FutureBuilder':
                return True
            # Check children recursively
            children = Widget.objects.filter(parent_widget=widget)
            if children and self._check_for_future_builder(list(children)):
                return True
        return False