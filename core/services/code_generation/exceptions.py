# File: core/services/code_generation/exceptions.py
"""
Custom exceptions for the Flutter code generation system.
"""


class CodeGenerationException(Exception):
    """Base exception for all code generation errors."""
    pass


class ProjectStructureException(CodeGenerationException):
    """Exception raised when project structure creation fails."""
    pass


class ConfigurationException(CodeGenerationException):
    """Exception raised when configuration generation fails."""
    pass


class ScreenGenerationException(CodeGenerationException):
    """Exception raised when screen generation fails."""
    pass


class WidgetGenerationException(CodeGenerationException):
    """Exception raised when widget generation fails."""
    pass


class ServiceGenerationException(CodeGenerationException):
    """Exception raised when service generation fails."""
    pass


class ValidationException(CodeGenerationException):
    """Exception raised when validation fails."""
    pass


class FileSystemException(CodeGenerationException):
    """Exception raised when file system operations fail."""
    pass


class DartSyntaxException(CodeGenerationException):
    """Exception raised when generated Dart code has syntax issues."""
    pass


class TemplateException(CodeGenerationException):
    """Exception raised when template processing fails."""
    pass