# File: core/services/code_generation/flutter/theme_generator.py
"""
Generates theme configuration for Flutter applications.
"""

from ..base import BaseGenerator, GeneratorContext


class ThemeGenerator(BaseGenerator):
    """
    Generates app theme configuration.
    """

    def _do_generate(self, context: GeneratorContext) -> bool:
        """
        Generate theme files.

        Args:
            context: GeneratorContext containing theme information

        Returns:
            bool: True if successful
        """
        try:
            content = self._build_theme_content(context)
            file_path = context.lib_path / 'theme' / 'app_theme.dart'
            return self.write_file(file_path, content, context)

        except Exception as e:
            self.add_error(f"Failed to generate theme: {str(e)}")
            return False

    def _build_theme_content(self, context: GeneratorContext) -> str:
        """
        Build the theme configuration content.

        Args:
            context: GeneratorContext containing theme information

        Returns:
            str: Theme configuration content
        """
        theme = context.theme

        content = f'''import 'package:flutter/material.dart';

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

    for (int i = 1; i < 10; i++) {{
      strengths.add(0.1 * i);
    }}

    for (var strength in strengths) {{
      final double ds = 0.5 - strength;
      swatch[(strength * 1000).round()] = Color.fromRGBO(
        ((color.r * 255).round() + ((ds < 0 ? (color.r * 255).round() : (255 - (color.r * 255).round())) * ds)).round(),
        ((color.g * 255).round() + ((ds < 0 ? (color.g * 255).round() : (255 - (color.g * 255).round())) * ds)).round(),
        ((color.b * 255).round() + ((ds < 0 ? (color.b * 255).round() : (255 - (color.b * 255).round())) * ds)).round(),
        1,
      );
    }}

    return MaterialColor(
      (((color.a * 255).round() << 24) | 
       ((color.r * 255).round() << 16) | 
       ((color.g * 255).round() << 8) | 
       ((color.b * 255).round() << 0)) & 0xFFFFFFFF, 
      swatch
    );
  }}
}}
'''
        return content