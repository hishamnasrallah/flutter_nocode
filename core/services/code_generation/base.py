# File: core/services/code_generation/base.py
"""
Base classes and interfaces for the Flutter code generation system.
Provides abstract base classes and common interfaces for all generators.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Optional, List
from dataclasses import dataclass


@dataclass
class GeneratorContext:
    """Context object passed between generators containing shared state."""
    application: Any  # Application model instance
    project_path: Path
    lib_path: Path
    screens: List[Any]  # List of Screen model instances
    data_sources: List[Any]  # List of DataSource model instances
    theme: Any  # Theme model instance
    custom_widgets: List[Any]  # List of CustomPubDevWidget instances

    # Additional context data
    uses_dynamic_url: bool = False
    has_config_screen: bool = False
    initial_route: str = '/home'

    # Metadata for tracking generation progress
    generated_files: List[Path] = None
    errors: List[str] = None
    warnings: List[str] = None

    def __post_init__(self):
        if self.generated_files is None:
            self.generated_files = []
        if self.errors is None:
            self.errors = []
        if self.warnings is None:
            self.warnings = []

    def add_generated_file(self, file_path: Path):
        """Track a generated file."""
        self.generated_files.append(file_path)

    def add_error(self, error: str):
        """Add an error message."""
        self.errors.append(error)

    def add_warning(self, warning: str):
        """Add a warning message."""
        self.warnings.append(warning)


class GeneratorInterface(ABC):
    """Interface that all generators must implement."""

    @abstractmethod
    def generate(self, context: GeneratorContext) -> bool:
        """
        Generate code based on the provided context.

        Args:
            context: GeneratorContext containing all necessary data

        Returns:
            bool: True if generation successful, False otherwise
        """
        pass

    @abstractmethod
    def validate(self, context: GeneratorContext) -> bool:
        """
        Validate that generation can proceed.

        Args:
            context: GeneratorContext to validate

        Returns:
            bool: True if validation passes, False otherwise
        """
        pass


class BaseGenerator(GeneratorInterface):
    """
    Base class for all code generators.
    Provides common functionality and template method pattern.
    """

    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def generate(self, context: GeneratorContext) -> bool:
        """
        Template method for generation process.

        Args:
            context: GeneratorContext containing all necessary data

        Returns:
            bool: True if generation successful, False otherwise
        """
        try:
            # Validate before generation
            if not self.validate(context):
                return False

            # Pre-generation hook
            self._pre_generate(context)

            # Actual generation (implemented by subclasses)
            result = self._do_generate(context)

            # Post-generation hook
            if result:
                self._post_generate(context)

            return result

        except Exception as e:
            self.add_error(f"Generation failed: {str(e)}")
            context.add_error(f"{self.__class__.__name__}: {str(e)}")
            return False

    @abstractmethod
    def _do_generate(self, context: GeneratorContext) -> bool:
        """
        Actual generation logic implemented by subclasses.

        Args:
            context: GeneratorContext containing all necessary data

        Returns:
            bool: True if generation successful, False otherwise
        """
        pass

    def validate(self, context: GeneratorContext) -> bool:
        """
        Basic validation that can be overridden by subclasses.

        Args:
            context: GeneratorContext to validate

        Returns:
            bool: True if validation passes, False otherwise
        """
        if not context.application:
            self.add_error("No application provided in context")
            return False

        if not context.project_path:
            self.add_error("No project path provided in context")
            return False

        return True

    def _pre_generate(self, context: GeneratorContext):
        """Hook called before generation. Can be overridden by subclasses."""
        pass

    def _post_generate(self, context: GeneratorContext):
        """Hook called after successful generation. Can be overridden by subclasses."""
        pass

    def add_error(self, error: str):
        """Add an error message."""
        self.errors.append(error)

    def add_warning(self, warning: str):
        """Add a warning message."""
        self.warnings.append(warning)

    def get_errors(self) -> List[str]:
        """Get all error messages."""
        return self.errors

    def get_warnings(self) -> List[str]:
        """Get all warning messages."""
        return self.warnings

    def clear_messages(self):
        """Clear all error and warning messages."""
        self.errors.clear()
        self.warnings.clear()

    def write_file(self, file_path: Path, content: str, context: GeneratorContext) -> bool:
        """
        Write content to a file with error handling.

        Args:
            file_path: Path to write to
            content: Content to write
            context: GeneratorContext for tracking

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Ensure parent directory exists
            file_path.parent.mkdir(parents=True, exist_ok=True)

            # Write content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            # Track generated file
            context.add_generated_file(file_path)

            return True

        except Exception as e:
            self.add_error(f"Failed to write {file_path}: {str(e)}")
            return False


class BaseWidgetHandler(ABC):
    """Base class for all widget handlers."""

    @abstractmethod
    def can_handle(self, widget_type: str) -> bool:
        """
        Check if this handler can handle the given widget type.

        Args:
            widget_type: Type of widget to check

        Returns:
            bool: True if this handler can handle the widget type
        """
        pass

    @abstractmethod
    def generate(self, widget: Any, context: GeneratorContext, indent_level: int) -> str:
        """
        Generate Dart code for the widget.

        Args:
            widget: Widget model instance
            context: GeneratorContext containing all necessary data
            indent_level: Current indentation level

        Returns:
            str: Generated Dart code
        """
        pass

    def get_indent(self, level: int) -> str:
        """Get indentation string for the given level."""
        return '  ' * level

    def get_widget_properties(self, widget: Any) -> Dict[str, Any]:
        """
        Get properties for a widget as a dictionary.

        Args:
            widget: Widget model instance

        Returns:
            Dict: Property name to WidgetProperty mapping
        """
        from core.models import WidgetProperty
        properties = WidgetProperty.objects.filter(widget=widget)
        return {prop.property_name: prop for prop in properties}

    def get_child_widgets(self, widget: Any) -> List[Any]:
        """
        Get child widgets for a parent widget.

        Args:
            widget: Parent widget model instance

        Returns:
            List: Ordered list of child widgets
        """
        from core.models import Widget
        return Widget.objects.filter(parent_widget=widget).order_by('order')

    def get_property_value(self, prop_dict: Dict[str, Any], property_name: str, default_value: Any = '') -> Any:
        """
        Get property value from property dictionary.

        Args:
            prop_dict: Dictionary of properties
            property_name: Name of property to get
            default_value: Default value if property not found

        Returns:
            Property value or default
        """
        if property_name in prop_dict:
            prop = prop_dict[property_name]
            value = prop.get_value()
            if value is not None and value != '':
                return value
        return default_value