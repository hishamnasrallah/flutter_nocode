# File: core/services/code_generation/project/__init__.py
"""
Project management package.
Handles project structure, configuration, and packaging.
"""

from .structure_manager import ProjectStructureManager
from .config_manager import ConfigurationManager
from .package_manager import PackageManager

__all__ = [
    'ProjectStructureManager',
    'ConfigurationManager',
    'PackageManager'
]