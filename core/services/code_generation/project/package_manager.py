# File: core/services/code_generation/project/package_manager.py
"""
Manages source code packaging.
Creates ZIP files of generated Flutter projects.
"""

import zipfile
from pathlib import Path
from django.conf import settings

from ..base import BaseGenerator, GeneratorContext
from ..exceptions import FileSystemException


class PackageManager(BaseGenerator):
    """
    Manages packaging of generated source code into ZIP files.
    """

    def __init__(self):
        super().__init__()
        self.zip_path = None

    def _do_generate(self, context: GeneratorContext) -> bool:
        """
        Create ZIP file of the generated source code.

        Args:
            context: GeneratorContext containing project information

        Returns:
            bool: True if successful
        """
        try:
            # Determine ZIP file path
            self.zip_path = settings.SOURCE_ZIP_STORAGE_PATH / f"{context.application.package_name}_source.zip"

            # Ensure storage directory exists
            self.zip_path.parent.mkdir(parents=True, exist_ok=True)

            # Create ZIP file
            if not self._create_zip_file(context):
                raise FileSystemException("Failed to create ZIP file")

            return True

        except Exception as e:
            self.add_error(str(e))
            return False

    def _create_zip_file(self, context: GeneratorContext) -> bool:
        """
        Create ZIP file of the project directory.

        Args:
            context: GeneratorContext containing project information

        Returns:
            bool: True if successful
        """
        try:
            with zipfile.ZipFile(self.zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Walk through project directory
                for root, dirs, files in context.project_path.walk():
                    # Skip certain directories
                    dirs[:] = [d for d in dirs if not self._should_skip_directory(d)]

                    for file in files:
                        # Skip certain files
                        if self._should_skip_file(file):
                            continue

                        file_path = Path(root) / file
                        arcname = file_path.relative_to(context.project_path)
                        zipf.write(file_path, arcname)

            print(f"Created source ZIP at: {self.zip_path}")
            return True

        except Exception as e:
            self.add_error(f"Failed to create ZIP file: {str(e)}")
            return False

    def _should_skip_directory(self, directory_name: str) -> bool:
        """
        Check if a directory should be skipped when creating ZIP.

        Args:
            directory_name: Name of the directory

        Returns:
            bool: True if should skip
        """
        skip_dirs = {
            '.git',
            '.gradle',
            '.dart_tool',
            'build',
            '.idea',
            '__pycache__'
        }
        return directory_name in skip_dirs

    def _should_skip_file(self, file_name: str) -> bool:
        """
        Check if a file should be skipped when creating ZIP.

        Args:
            file_name: Name of the file

        Returns:
            bool: True if should skip
        """
        skip_extensions = {
            '.pyc',
            '.pyo',
            '.class',
            '.iml'
        }

        skip_files = {
            '.DS_Store',
            'Thumbs.db',
            'desktop.ini'
        }

        # Check file extension
        for ext in skip_extensions:
            if file_name.endswith(ext):
                return True

        # Check specific files
        return file_name in skip_files

    def get_zip_path(self) -> Path:
        """
        Get the path to the created ZIP file.

        Returns:
            Path: Path to ZIP file or None if not created
        """
        return self.zip_path