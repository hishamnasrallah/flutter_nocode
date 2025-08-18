# File: core/services/code_generation/screens/screen_generator.py
"""
Orchestrates screen generation for Flutter applications.
"""

from ..base import BaseGenerator, GeneratorContext
from .screen_builder import ScreenBuilder
from .special_screens import SpecialScreenHandler


class ScreenGenerator(BaseGenerator):
    """
    Main orchestrator for screen generation.
    """

    def __init__(self):
        super().__init__()
        self.screen_builder = ScreenBuilder()
        self.special_handler = SpecialScreenHandler()

    def _do_generate(self, context: GeneratorContext) -> bool:
        """
        Generate all screens for the application.

        Args:
            context: GeneratorContext containing screen information

        Returns:
            bool: True if all screens generated successfully
        """
        if not context.screens:
            self.add_warning("No screens to generate")
            return True

        success = True
        generated_screens = []

        for screen in context.screens:
            try:
                # Track generated screens to avoid duplicates
                if screen.name in generated_screens:
                    self.add_warning(f"Skipping duplicate screen: {screen.name}")
                    continue

                # Check if this is a special screen
                if self.special_handler.is_special_screen(screen.name):
                    # Use special handler
                    if not self.special_handler.generate_screen(screen, context):
                        self.add_error(f"Failed to generate special screen: {screen.name}")
                        success = False
                    else:
                        generated_screens.append(screen.name)
                else:
                    # Use regular screen builder
                    if not self.screen_builder.generate_screen(screen, context):
                        self.add_error(f"Failed to generate screen: {screen.name}")
                        success = False
                    else:
                        generated_screens.append(screen.name)

            except Exception as e:
                self.add_error(f"Error generating screen {screen.name}: {str(e)}")
                success = False

        # Log generated screens for debugging
        print(f"Generated {len(generated_screens)} screens: {', '.join(generated_screens)}")

        return success