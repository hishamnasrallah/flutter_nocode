# File: core/services/code_generation/flutter/main_generator.py
"""
Generates the main.dart file for Flutter applications.
"""

from ..base import BaseGenerator, GeneratorContext
from ..utils import StringUtils


class MainDartGenerator(BaseGenerator):
    """
    Generates the main.dart entry point for Flutter applications.
    """

    def _do_generate(self, context: GeneratorContext) -> bool:
        """
        Generate main.dart file.

        Args:
            context: GeneratorContext containing project information

        Returns:
            bool: True if successful
        """
        try:
            content = self._build_main_dart_content(context)
            file_path = context.lib_path / 'main.dart'
            return self.write_file(file_path, content, context)

        except Exception as e:
            self.add_error(f"Failed to generate main.dart: {str(e)}")
            return False

    def _build_main_dart_content(self, context: GeneratorContext) -> str:
        """
        Build the content for main.dart.

        Args:
            context: GeneratorContext containing project information

        Returns:
            str: main.dart content
        """
        # Generate imports
        imports = self._generate_imports(context)

        # Determine theme mode
        theme_mode = 'ThemeMode.dark' if context.theme.is_dark_mode else 'ThemeMode.light'

        content = f'''import 'package:flutter/material.dart';
import 'theme/app_theme.dart';
import 'routes/app_routes.dart';
{imports}

void main() {{
  runApp(MyApp());
}}

class MyApp extends StatelessWidget {{
  @override
  Widget build(BuildContext context) {{
    return MaterialApp(
      title: '{context.application.name}',
      theme: AppTheme.lightTheme,
      darkTheme: AppTheme.darkTheme,
      themeMode: {theme_mode},
      initialRoute: '{context.initial_route}',
      routes: AppRoutes.routes,
      debugShowCheckedModeBanner: false,
    );
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
            imports.append(f"import 'screens/{screen_file_name}';")

        return '\n'.join(imports)