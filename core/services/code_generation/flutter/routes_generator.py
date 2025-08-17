# File: core/services/code_generation/flutter/routes_generator.py
"""
Generates route configuration for Flutter applications.
"""

from ..base import BaseGenerator, GeneratorContext
from ..utils import StringUtils


class RoutesGenerator(BaseGenerator):
    """
    Generates app routes configuration.
    """

    def _do_generate(self, context: GeneratorContext) -> bool:
        """
        Generate routes configuration file.

        Args:
            context: GeneratorContext containing screen information

        Returns:
            bool: True if successful
        """
        try:
            content = self._build_routes_content(context)
            file_path = context.lib_path / 'routes' / 'app_routes.dart'
            return self.write_file(file_path, content, context)

        except Exception as e:
            self.add_error(f"Failed to generate routes: {str(e)}")
            return False

    def _build_routes_content(self, context: GeneratorContext) -> str:
        """
        Build the routes configuration content.

        Args:
            context: GeneratorContext containing screen information

        Returns:
            str: Routes configuration content
        """
        # Generate imports
        imports = self._generate_imports(context)

        # Generate route mappings
        route_mappings = self._generate_route_mappings(context)

        content = f'''import 'package:flutter/material.dart';
{imports}

class AppRoutes {{
  static Map<String, WidgetBuilder> get routes {{
    return {{
{route_mappings}
    }};
  }}
}}
'''
        return content

    def _generate_imports(self, context: GeneratorContext) -> str:
        """
        Generate import statements for all screens.

        Args:
            context: GeneratorContext containing screen information

        Returns:
            str: Import statements
        """
        imports = []

        for screen in context.screens:
            screen_file_name = StringUtils.to_snake_case(screen.name) + '_screen.dart'
            imports.append(f"import '../screens/{screen_file_name}';")

        return '\n'.join(imports)

    def _generate_route_mappings(self, context: GeneratorContext) -> str:
        """
        Generate route mapping entries.

        Args:
            context: GeneratorContext containing screen information

        Returns:
            str: Route mapping entries
        """
        mappings = []

        for screen in context.screens:
            screen_class_name = StringUtils.to_pascal_case(screen.name) + 'Screen'
            mappings.append(f"      '{screen.route_name}': (context) => {screen_class_name}(),")

        return '\n'.join(mappings)