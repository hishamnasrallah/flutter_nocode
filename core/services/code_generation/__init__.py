# File: core/services/code_generation/__init__.py
"""
Flutter Code Generation Package.
Main entry point for the code generation system.
"""

from .generator import FlutterCodeGenerator
from .base import GeneratorContext, BaseGenerator, BaseWidgetHandler
from .exceptions import (
    CodeGenerationException,
    ProjectStructureException,
    ConfigurationException,
    ScreenGenerationException,
    WidgetGenerationException,
    ServiceGenerationException,
    ValidationException,
    FileSystemException,
    DartSyntaxException,
    TemplateException
)

__all__ = [
    'FlutterCodeGenerator',
    'GeneratorContext',
    'BaseGenerator',
    'BaseWidgetHandler',
    'CodeGenerationException',
    'ProjectStructureException',
    'ConfigurationException',
    'ScreenGenerationException',
    'WidgetGenerationException',
    'ServiceGenerationException',
    'ValidationException',
    'FileSystemException',
    'DartSyntaxException',
    'TemplateException'
]