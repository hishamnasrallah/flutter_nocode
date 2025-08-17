# File: core/services/code_generation/generator.py
"""
Main orchestrator for Flutter code generation.
Coordinates all generation components and manages the overall workflow.
"""

from pathlib import Path
from typing import Tuple, Optional
from django.conf import settings

from .base import GeneratorContext
from .exceptions import CodeGenerationException
from .project.structure_manager import ProjectStructureManager
from .project.config_manager import ConfigurationManager
from .project.package_manager import PackageManager
from .flutter.main_generator import MainDartGenerator
from .flutter.theme_generator import ThemeGenerator
from .flutter.routes_generator import RoutesGenerator
from .screens.screen_generator import ScreenGenerator
from .services.api_service_generator import ApiServiceGenerator
from .services.model_generator import ModelGenerator
from .widgets.widget_generator import CustomWidgetGenerator


class FlutterCodeGenerator:
    """
    Main orchestrator class for Flutter project generation.
    Coordinates all generation components and manages the workflow.
    """

    def __init__(self, application):
        """
        Initialize the Flutter code generator.

        Args:
            application: Application model instance
        """
        self.application = application
        self.project_path = settings.GENERATED_CODE_PATH / f"{application.package_name.replace('.', '_')}"
        self.lib_path = self.project_path / 'lib'

        # Initialize context
        self.context = self._create_context()

        # Initialize all generators
        self.structure_manager = ProjectStructureManager()
        self.config_manager = ConfigurationManager()
        self.package_manager = PackageManager()
        self.main_generator = MainDartGenerator()
        self.theme_generator = ThemeGenerator()
        self.routes_generator = RoutesGenerator()
        self.screen_generator = ScreenGenerator()
        self.api_service_generator = ApiServiceGenerator()
        self.model_generator = ModelGenerator()
        self.custom_widget_generator = CustomWidgetGenerator()

    def generate_project(self) -> Tuple[bool, str]:
        """
        Generate complete Flutter project.

        Returns:
            Tuple[bool, str]: (success, message)
        """
        try:
            # Step 1: Create project structure
            if not self._create_project_structure():
                return False, self._get_error_message("Failed to create project structure")

            # Step 2: Configure project
            if not self._configure_project():
                return False, self._get_error_message("Failed to configure project")

            # Step 3: Generate main Dart files
            if not self._generate_flutter_core():
                return False, self._get_error_message("Failed to generate Flutter core files")

            # Step 4: Generate screens
            if not self._generate_screens():
                return False, self._get_error_message("Failed to generate screens")

            # Step 5: Generate services
            if not self._generate_services():
                return False, self._get_error_message("Failed to generate services")

            # Step 6: Generate custom widgets
            if not self._generate_custom_widgets():
                return False, self._get_error_message("Failed to generate custom widgets")

            # Step 7: Package source code
            zip_path = self._package_source_code()
            if not zip_path:
                return False, self._get_error_message("Failed to package source code")

            # Update application with generated files
            self._update_application(zip_path)

            # Check for warnings
            if self.context.warnings:
                warnings_msg = f" Warnings: {'; '.join(self.context.warnings)}"
            else:
                warnings_msg = ""

            return True, f"Flutter project generated successfully at {self.project_path}{warnings_msg}"

        except CodeGenerationException as e:
            return False, f"Code generation error: {str(e)}"
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"Error details:\n{error_details}")
            return False, f"Unexpected error: {str(e)}"

    def _create_context(self) -> GeneratorContext:
        """
        Create the generator context with all necessary data.

        Returns:
            GeneratorContext: Initialized context
        """
        from core.models import Screen, DataSource, CustomPubDevWidget

        # Load all necessary data
        screens = list(Screen.objects.filter(application=self.application))
        data_sources = list(DataSource.objects.filter(application=self.application))
        custom_widgets = list(CustomPubDevWidget.objects.filter(
            application=self.application,
            is_active=True
        ))

        # Check for configuration screen
        has_config_screen = any(screen.name == 'Configuration' for screen in screens)

        # Check if any data source uses dynamic URL
        uses_dynamic_url = any(ds.use_dynamic_base_url for ds in data_sources) or has_config_screen

        # Determine initial route
        splash_screen = next((s for s in screens if s.name == 'SplashScreen'), None)
        if splash_screen:
            initial_route = splash_screen.route_name
        else:
            home_screen = next((s for s in screens if s.name == 'Home' or s.is_home_screen), None)
            initial_route = home_screen.route_name if home_screen else '/home'

        return GeneratorContext(
            application=self.application,
            project_path=self.project_path,
            lib_path=self.lib_path,
            screens=screens,
            data_sources=data_sources,
            theme=self.application.theme,
            custom_widgets=custom_widgets,
            uses_dynamic_url=uses_dynamic_url,
            has_config_screen=has_config_screen,
            initial_route=initial_route
        )

    def _create_project_structure(self) -> bool:
        """Create Flutter project structure."""
        return self.structure_manager.generate(self.context)

    def _configure_project(self) -> bool:
        """Configure project files (pubspec.yaml, gradle, etc.)."""
        return self.config_manager.generate(self.context)

    def _generate_flutter_core(self) -> bool:
        """Generate core Flutter files (main.dart, theme, routes)."""
        # Generate main.dart
        if not self.main_generator.generate(self.context):
            return False

        # Generate theme
        if not self.theme_generator.generate(self.context):
            return False

        # Generate routes
        if not self.routes_generator.generate(self.context):
            return False

        return True

    def _generate_screens(self) -> bool:
        """Generate all screens."""
        return self.screen_generator.generate(self.context)

    def _generate_services(self) -> bool:
        """Generate service layer (API, models)."""
        # Generate API service
        if not self.api_service_generator.generate(self.context):
            return False

        # Generate models
        if not self.model_generator.generate(self.context):
            return False

        return True

    def _generate_custom_widgets(self) -> bool:
        """Generate custom widget components."""
        return self.custom_widget_generator.generate(self.context)

    def _package_source_code(self) -> Optional[Path]:
        """
        Package source code into ZIP file.

        Returns:
            Optional[Path]: Path to ZIP file or None if failed
        """
        result = self.package_manager.generate(self.context)
        if result:
            return self.package_manager.get_zip_path()
        return None

    def _update_application(self, zip_path: Path):
        """
        Update application model with generated files.

        Args:
            zip_path: Path to generated ZIP file
        """
        self.application.source_code_zip.name = f"source_zips/{self.application.package_name}_source.zip"
        self.application.save()

    def _get_error_message(self, base_message: str) -> str:
        """
        Get detailed error message including context errors.

        Args:
            base_message: Base error message

        Returns:
            str: Detailed error message
        """
        if self.context.errors:
            details = "; ".join(self.context.errors)
            return f"{base_message}: {details}"
        return base_message