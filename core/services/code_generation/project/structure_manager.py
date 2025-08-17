# File: core/services/code_generation/project/structure_manager.py
"""
Manages Flutter project structure creation.
Handles directory creation and Flutter project initialization.
"""

import os
import subprocess
import time
from pathlib import Path
from django.conf import settings

from ..base import BaseGenerator, GeneratorContext
from ..exceptions import ProjectStructureException
from ..utils import FileUtils


class ProjectStructureManager(BaseGenerator):
    """
    Manages the creation and setup of Flutter project structure.
    """

    def validate(self, context: GeneratorContext) -> bool:
        """Validate that Flutter SDK is available."""
        if not super().validate(context):
            return False

        # Check Flutter SDK availability
        flutter_exe = self._get_flutter_executable()
        if not os.path.exists(flutter_exe):
            self.add_error(f"Flutter SDK not found at {flutter_exe}")
            return False

        return True

    def _do_generate(self, context: GeneratorContext) -> bool:
        """
        Create Flutter project structure.

        Args:
            context: GeneratorContext containing project information

        Returns:
            bool: True if successful
        """
        try:
            # Clean existing project directory
            if not self._clean_project_directory(context.project_path):
                raise ProjectStructureException("Failed to clean project directory")

            # Create Flutter project
            if not self._create_flutter_project(context):
                raise ProjectStructureException("Failed to create Flutter project")

            # Create additional directories
            if not self._create_additional_directories(context):
                raise ProjectStructureException("Failed to create additional directories")

            return True

        except Exception as e:
            self.add_error(str(e))
            return False

    def _clean_project_directory(self, project_path: Path) -> bool:
        """
        Clean existing project directory with retry logic.

        Args:
            project_path: Path to project directory

        Returns:
            bool: True if successful
        """
        if not project_path.exists():
            return True

        # Try to clean with retry logic
        if not FileUtils.clean_directory(project_path, max_retries=5):
            # If cleaning fails, try to rename instead
            try:
                import datetime
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_path = project_path.parent / f"{project_path.name}_old_{timestamp}"
                project_path.rename(backup_path)

                # Schedule background deletion on Windows
                if os.name == 'nt':
                    try:
                        subprocess.Popen(
                            ['cmd', '/c', 'timeout', '/t', '10', '&&', 'rmdir', '/S', '/Q', str(backup_path)],
                            shell=True,
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL
                        )
                    except:
                        pass

                return True

            except Exception as e:
                self.add_warning(f"Could not fully clean project directory: {str(e)}")
                # Continue anyway - Flutter create might handle it
                return True

        return True

    def _create_flutter_project(self, context: GeneratorContext) -> bool:
        """
        Create Flutter project using Flutter CLI.

        Args:
            context: GeneratorContext containing project information

        Returns:
            bool: True if successful
        """
        flutter_exe = self._get_flutter_executable()

        # Ensure parent directory exists
        context.project_path.parent.mkdir(parents=True, exist_ok=True)

        # Extract package name and organization
        package_parts = context.application.package_name.split('.')
        project_name = package_parts[-1]  # e.g., 'myapp'
        org = '.'.join(package_parts[:-1]) if len(package_parts) > 1 else 'com.example'

        # Build Flutter create command
        create_command = [
            flutter_exe, 'create',
            '--project-name', project_name,
            '--org', org,
            '--platforms', 'android,ios',
            '--no-pub',  # Don't run pub get yet
            str(context.project_path)
        ]

        print(f"Creating Flutter project: {' '.join(create_command)}")

        try:
            result = subprocess.run(
                create_command,
                capture_output=True,
                text=True,
                timeout=120,
                env=os.environ.copy()
            )

            if result.returncode != 0:
                self.add_error(f"Flutter create failed: {result.stderr}")
                return False

            print(f"Flutter project created successfully at {context.project_path}")

            # Wait for files to be fully written
            time.sleep(1)

            return True

        except subprocess.TimeoutExpired:
            self.add_error("Flutter create command timed out")
            return False
        except Exception as e:
            self.add_error(f"Failed to create Flutter project: {str(e)}")
            return False

    def _create_additional_directories(self, context: GeneratorContext) -> bool:
        """
        Create additional directories for our custom structure.

        Args:
            context: GeneratorContext containing project information

        Returns:
            bool: True if successful
        """
        directories = [
            'lib/screens',
            'lib/widgets',
            'lib/widgets/handlers',
            'lib/services',
            'lib/models',
            'lib/theme',
            'lib/routes',
            'lib/utils',
            'assets/images',
            'assets/fonts',
        ]

        for directory in directories:
            dir_path = context.project_path / directory
            if not FileUtils.ensure_directory(dir_path):
                self.add_warning(f"Could not create directory: {directory}")

        return True

    def _get_flutter_executable(self) -> str:
        """
        Get the Flutter executable path.

        Returns:
            str: Path to Flutter executable
        """
        flutter_exe = os.path.join(
            settings.FLUTTER_SDK_PATH,
            'bin',
            'flutter.bat' if os.name == 'nt' else 'flutter'
        )
        return flutter_exe