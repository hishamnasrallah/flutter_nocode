# File: core/services/code_generation/widgets/__init__.py
"""
Widget generation package.
Main widget generation system with factory pattern.
"""

from .widget_generator import WidgetGenerator, CustomWidgetGenerator
from .widget_factory import WidgetFactory

__all__ = [
    'WidgetGenerator',
    'CustomWidgetGenerator',
    'WidgetFactory'
]
