# File: core/services/code_generation/widgets/widget_generator.py
"""
Main widget generation orchestrator.
Coordinates widget code generation using factory pattern.
"""

from typing import Any

from ..base import BaseGenerator, GeneratorContext
from ..utils import DartCodeUtils
from .widget_factory import WidgetFactory


class WidgetGenerator:
    """
    Main orchestrator for widget code generation.
    """

    def __init__(self):
        self.factory = WidgetFactory()

    def generate_widget(self, widget: Any, context: GeneratorContext, indent_level: int) -> str:
        """
        Generate Dart code for a widget.

        Args:
            widget: Widget model instance
            context: GeneratorContext
            indent_level: Current indentation level

        Returns:
            str: Generated Dart code
        """
        try:
            # Get appropriate handler from factory
            handler = self.factory.get_handler(widget.widget_type)

            if handler:
                # Generate widget code using handler
                code = handler.generate(widget, context, indent_level)
            else:
                # Fallback for unknown widget types
                code = self._generate_fallback(widget, indent_level)

            # Validate and fix syntax if needed
            code = DartCodeUtils.fix_dart_syntax(code)

            return code

        except Exception as e:
            context.add_warning(f"Error generating widget {widget.widget_type}: {str(e)}")
            return self._generate_error_widget(widget, indent_level)

    def _generate_fallback(self, widget: Any, indent_level: int) -> str:
        """
        Generate fallback code for unknown widget types.

        Args:
            widget: Widget model instance
            indent_level: Indentation level

        Returns:
            str: Fallback widget code
        """
        indent = '  ' * indent_level
        return f"Container(child: Text('Unsupported widget: {widget.widget_type}'))"

    def _generate_error_widget(self, widget: Any, indent_level: int) -> str:
        """
        Generate error widget for failed generation.

        Args:
            widget: Widget model instance
            indent_level: Indentation level

        Returns:
            str: Error widget code
        """
        indent = '  ' * indent_level
        return f"Container(child: Text('Error generating: {widget.widget_type}'))"


class CustomWidgetGenerator(BaseGenerator):
    """
    Generates custom widget components file.
    """

    def _do_generate(self, context: GeneratorContext) -> bool:
        """
        Generate custom widgets file.

        Args:
            context: GeneratorContext

        Returns:
            bool: True if successful
        """
        try:
            content = self._build_custom_widgets_content(context)
            file_path = context.lib_path / 'widgets' / 'custom_widgets.dart'
            return self.write_file(file_path, content, context)

        except Exception as e:
            self.add_error(f"Failed to generate custom widgets: {str(e)}")
            return False

    def _build_custom_widgets_content(self, context: GeneratorContext) -> str:
        """
        Build custom widgets file content.

        Args:
            context: GeneratorContext

        Returns:
            str: Custom widgets file content
        """
        content = '''import 'package:flutter/material.dart';

// Custom widgets for the application

class AppCard extends StatelessWidget {
  final Widget child;
  final EdgeInsets? padding;
  final Color? backgroundColor;

  const AppCard({
    super.key,
    required this.child,
    this.padding,
    this.backgroundColor,
  });

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

  const LoadingWidget({super.key, this.message});

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
    super.key,
    required this.message,
    this.onRetry,
  });

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

class EmptyStateWidget extends StatelessWidget {
  final String message;
  final IconData? icon;

  const EmptyStateWidget({
    super.key,
    required this.message,
    this.icon,
  });

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          if (icon != null)
            Icon(icon, size: 64, color: Colors.grey),
          const SizedBox(height: 16),
          Text(
            message,
            style: const TextStyle(color: Colors.grey),
            textAlign: TextAlign.center,
          ),
        ],
      ),
    );
  }
}
'''
        return content