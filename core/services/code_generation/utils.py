# File: core/services/code_generation/utils.py
"""
Utility functions for Flutter code generation.
Provides string manipulation, validation, and helper functions.
"""

import re
import unicodedata
from typing import Optional, Dict, Any, List


class StringUtils:
    """Utility class for string manipulation."""

    @staticmethod
    def to_snake_case(text: str) -> str:
        """
        Convert text to snake_case.

        Args:
            text: Input text

        Returns:
            str: Text in snake_case
        """
        # Replace ampersand with 'and'
        text = text.replace('&', '_and_')
        # Replace special characters with underscores
        text = re.sub(r'[&\+\-\*\/\\\|\?\!\@\#\$\%\^\(\)\[\]\{\}\<\>\,\.\;\:\'\"\`\~]', '_', text)
        # Handle camelCase conversion
        text = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', text)
        text = re.sub(r'([a-z\d])([A-Z])', r'\1_\2', text)
        # Replace spaces and multiple underscores with single underscore
        text = text.lower().replace(' ', '_')
        text = re.sub(r'_+', '_', text)
        text = text.strip('_')

        # Ensure valid Dart identifier
        if text and text[0].isdigit():
            text = '_' + text

        return text

    @staticmethod
    def to_pascal_case(text: str) -> str:
        """
        Convert text to PascalCase.

        Args:
            text: Input text

        Returns:
            str: Text in PascalCase
        """
        # Replace special characters with spaces
        text = re.sub(r'[&\+\-\*\/\\\|\?\!\@\#\$\%\^\(\)\[\]\{\}\<\>\,\.\;\:\'\"\`\~_]', ' ', text)
        # Split by spaces and capitalize each word
        words = [word.capitalize() for word in text.split() if word]
        return ''.join(words)

    @staticmethod
    def to_camel_case(text: str) -> str:
        """
        Convert text to camelCase.

        Args:
            text: Input text

        Returns:
            str: Text in camelCase
        """
        pascal = StringUtils.to_pascal_case(text)
        if not pascal:
            return ''
        # Ensure the result starts with a lowercase letter
        result = pascal[0].lower() + pascal[1:]
        # If the result starts with a number, prefix with underscore
        if result and result[0].isdigit():
            result = '_' + result
        return result


class DartCodeUtils:
    """Utility class for Dart code generation and validation."""

    @staticmethod
    def escape_dart_string(text: str) -> str:
        """
        Escape string for Dart code and handle special characters.

        Args:
            text: Input text

        Returns:
            str: Properly escaped Dart string
        """
        if not text:
            return ''

        # Normalize Unicode characters
        try:
            text = unicodedata.normalize('NFKD', text)
        except:
            pass

        # Replace problematic Unicode characters
        replacements = {
            '🔴': '[RED]',
            '🟢': '[GREEN]',
            '🔵': '[BLUE]',
            '🟡': '[YELLOW]',
            '⚠️': '[WARNING]',
            '❌': '[X]',
            '✅': '[CHECK]',
            '📱': '[PHONE]',
            '🛒': '[CART]',
            '📰': '[NEWS]',
            ''': "'",
            ''': "'",
            '"': '"',
            '"': '"',
            '–': '-',
            '—': '-',
            '…': '...',
            '\u2018': "'",
            '\u2019': "'",
            '\u201C': '"',
            '\u201D': '"',
        }

        for old_char, new_char in replacements.items():
            text = text.replace(old_char, new_char)

        # Remove non-printable characters
        cleaned_text = []
        for char in text:
            if ord(char) < 32 and char not in '\n\r\t':
                continue
            elif ord(char) > 126 and ord(char) < 160:
                continue
            elif ord(char) >= 160:
                try:
                    ascii_equiv = unicodedata.normalize('NFKD', char).encode('ascii', 'ignore').decode('ascii')
                    if ascii_equiv:
                        cleaned_text.append(ascii_equiv)
                    else:
                        cleaned_text.append(' ')
                except:
                    cleaned_text.append(' ')
            else:
                cleaned_text.append(char)

        text = ''.join(cleaned_text)

        # Escape for Dart strings
        text = text.replace('\\', '\\\\')
        text = text.replace("'", "\\'")
        text = text.replace('"', '\\"')
        text = text.replace('\n', '\\n')
        text = text.replace('\r', '\\r')
        text = text.replace('\t', '\\t')
        text = text.replace('$', '\\$')

        return text

    @staticmethod
    def validate_dart_syntax(code: str) -> tuple[bool, Optional[str]]:
        """
        Validate basic Dart syntax (balanced brackets, parentheses, etc.).

        Args:
            code: Dart code to validate

        Returns:
            tuple: (is_valid, error_message)
        """
        if not code:
            return True, None

        # Count brackets and parentheses
        open_parens = code.count('(')
        close_parens = code.count(')')
        open_brackets = code.count('[')
        close_brackets = code.count(']')
        open_braces = code.count('{')
        close_braces = code.count('}')

        errors = []

        if open_parens != close_parens:
            errors.append(f"Unbalanced parentheses: {open_parens} open, {close_parens} close")

        if open_brackets != close_brackets:
            errors.append(f"Unbalanced brackets: {open_brackets} open, {close_brackets} close")

        if open_braces != close_braces:
            errors.append(f"Unbalanced braces: {open_braces} open, {close_braces} close")

        if errors:
            return False, "; ".join(errors)

        return True, None

    @staticmethod
    def fix_dart_syntax(code: str) -> str:
        """
        Attempt to fix common Dart syntax issues.

        Args:
            code: Dart code to fix

        Returns:
            str: Fixed Dart code
        """
        if not code:
            return code

        # Count and fix unbalanced delimiters
        open_parens = code.count('(')
        close_parens = code.count(')')
        open_brackets = code.count('[')
        close_brackets = code.count(']')
        open_braces = code.count('{')
        close_braces = code.count('}')

        # Add missing closing delimiters
        if open_parens > close_parens:
            code += ')' * (open_parens - close_parens)

        if open_brackets > close_brackets:
            code += ']' * (open_brackets - close_brackets)

        if open_braces > close_braces:
            code += '}' * (open_braces - close_braces)

        return code

    @staticmethod
    def generate_color_code(hex_color: str) -> str:
        """
        Generate Dart Color code from hex string.

        Args:
            hex_color: Hex color string (with or without #)

        Returns:
            str: Dart Color code
        """
        if not hex_color:
            return "Colors.grey"

        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 6:
            return f"Color(0xFF{hex_color.upper()})"
        else:
            return "Colors.grey"

    @staticmethod
    def generate_edge_insets(value: Any, type: str = "all") -> str:
        """
        Generate EdgeInsets code.

        Args:
            value: Padding value(s)
            type: Type of EdgeInsets (all, symmetric, only)

        Returns:
            str: EdgeInsets code
        """
        if not value:
            return "EdgeInsets.zero"

        if type == "all":
            return f"EdgeInsets.all({value})"
        elif type == "symmetric":
            if isinstance(value, dict):
                h = value.get('horizontal', 0)
                v = value.get('vertical', 0)
                return f"EdgeInsets.symmetric(horizontal: {h}, vertical: {v})"
            return f"EdgeInsets.symmetric(horizontal: {value}, vertical: {value})"
        elif type == "only":
            if isinstance(value, dict):
                parts = []
                for side in ['top', 'right', 'bottom', 'left']:
                    if side in value:
                        parts.append(f"{side}: {value[side]}")
                return f"EdgeInsets.only({', '.join(parts)})"

        return "EdgeInsets.zero"


class FileUtils:
    """Utility class for file operations."""

    @staticmethod
    def ensure_directory(path) -> bool:
        """
        Ensure a directory exists, creating it if necessary.

        Args:
            path: Directory path

        Returns:
            bool: True if successful
        """
        try:
            path.mkdir(parents=True, exist_ok=True)
            return True
        except Exception:
            return False

    @staticmethod
    def clean_directory(path, max_retries: int = 3) -> bool:
        """
        Clean a directory with retry logic for locked files.

        Args:
            path: Directory path to clean
            max_retries: Maximum number of retry attempts

        Returns:
            bool: True if successful
        """
        import shutil
        import time
        import subprocess
        import os

        for attempt in range(max_retries):
            try:
                if path.exists():
                    # On Windows, try to kill locking processes
                    if os.name == 'nt' and attempt > 0:
                        processes = ['java.exe', 'gradle.exe', 'dart.exe', 'flutter.bat']
                        for process in processes:
                            try:
                                subprocess.run(['taskkill', '/F', '/IM', process],
                                               capture_output=True, shell=True, timeout=5)
                            except:
                                pass
                        time.sleep(2)

                    shutil.rmtree(path, ignore_errors=False)
                    return True
                return True

            except Exception:
                if attempt < max_retries - 1:
                    time.sleep(2)
                else:
                    # Try with ignore_errors as last resort
                    try:
                        shutil.rmtree(path, ignore_errors=True)
                    except:
                        pass
                    return False

        return False


class WidgetPropertyUtils:
    """Utility class for widget property handling."""

    @staticmethod
    def extract_properties(widget_properties: List[Any]) -> Dict[str, Any]:
        """
        Extract properties from widget property list.

        Args:
            widget_properties: List of WidgetProperty instances

        Returns:
            Dict: Property name to value mapping
        """
        props = {}
        for prop in widget_properties:
            value = prop.get_value()
            if value is not None and value != '':
                props[prop.property_name] = value
        return props

    @staticmethod
    def get_text_style_properties(prop_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract text style properties from property dictionary.

        Args:
            prop_dict: Property dictionary

        Returns:
            Dict: Text style properties
        """
        style_props = {}

        if 'color' in prop_dict:
            style_props['color'] = prop_dict['color'].get_value()

        if 'fontSize' in prop_dict:
            style_props['fontSize'] = prop_dict['fontSize'].get_value()

        if 'fontWeight' in prop_dict:
            style_props['fontWeight'] = prop_dict['fontWeight'].get_value()

        if 'fontStyle' in prop_dict:
            style_props['fontStyle'] = prop_dict['fontStyle'].get_value()

        # Additional text style properties
        if 'fontFamily' in prop_dict:
            style_props['fontFamily'] = prop_dict['fontFamily'].get_value()
        if 'letterSpacing' in prop_dict:
            style_props['letterSpacing'] = prop_dict['letterSpacing'].get_value()
        if 'wordSpacing' in prop_dict:
            style_props['wordSpacing'] = prop_dict['wordSpacing'].get_value()
        if 'height' in prop_dict:
            style_props['height'] = prop_dict['height'].get_value()
        if 'decoration' in prop_dict:
            style_props['decoration'] = prop_dict['decoration'].get_value()
        if 'decorationColor' in prop_dict:
            style_props['decorationColor'] = prop_dict['decorationColor'].get_value()
        if 'decorationStyle' in prop_dict:
            style_props['decorationStyle'] = prop_dict['decorationStyle'].get_value()
        if 'decorationThickness' in prop_dict:
            style_props['decorationThickness'] = prop_dict['decorationThickness'].get_value()

        return style_props

    @staticmethod
    def generate_text_style(style_props: Dict[str, Any]) -> str:
        """
        Generate TextStyle code from properties.

        Args:
            style_props: Style properties

        Returns:
            str: TextStyle code or empty string
        """
        if not style_props:
            return ''

        parts = []

        if 'color' in style_props and style_props['color']:
            color_code = DartCodeUtils.generate_color_code(style_props['color'])
            parts.append(f"color: {color_code}")

        if 'fontSize' in style_props and style_props['fontSize']:
            parts.append(f"fontSize: {style_props['fontSize']}")

        if 'fontWeight' in style_props and style_props['fontWeight']:
            weight_value = style_props['fontWeight']
            # Map common weight names to Flutter values
            weight_map = {
                'thin': 'w100',
                'light': 'w300',
                'regular': 'w400',
                'medium': 'w500',
                'semibold': 'w600',
                'bold': 'w700',
                'black': 'w900'
            }

            # Convert if it's a named weight
            if weight_value in weight_map:
                weight_value = weight_map[weight_value]

            # Ensure it starts with 'w' for weight values
            if weight_value and not weight_value.startswith('FontWeight.'):
                if not weight_value.startswith('w'):
                    weight_value = 'w500'  # Default to medium
                parts.append(f"fontWeight: FontWeight.{weight_value}")
            else:
                parts.append(f"fontWeight: {weight_value}")

        if 'fontStyle' in style_props and style_props['fontStyle']:
            parts.append(f"fontStyle: FontStyle.{style_props['fontStyle']}")

        if 'fontFamily' in style_props and style_props['fontFamily']:
            ff = DartCodeUtils.escape_dart_string(style_props['fontFamily'])
            parts.append(f"fontFamily: '{ff}'")
        if 'letterSpacing' in style_props and style_props['letterSpacing']:
            parts.append(f"letterSpacing: {style_props['letterSpacing']}")
        if 'wordSpacing' in style_props and style_props['wordSpacing']:
            parts.append(f"wordSpacing: {style_props['wordSpacing']}")
        if 'height' in style_props and style_props['height']:
            parts.append(f"height: {style_props['height']}")
        if 'decoration' in style_props and style_props['decoration']:
            parts.append(f"decoration: TextDecoration.{style_props['decoration']}")
        if 'decorationColor' in style_props and style_props['decorationColor']:
            parts.append(f"decorationColor: {DartCodeUtils.generate_color_code(style_props['decorationColor'])}")
        if 'decorationStyle' in style_props and style_props['decorationStyle']:
            parts.append(f"decorationStyle: TextDecorationStyle.{style_props['decorationStyle']}")
        if 'decorationThickness' in style_props and style_props['decorationThickness']:
            parts.append(f"decorationThickness: {style_props['decorationThickness']}")

        if parts:
            return f", style: TextStyle({', '.join(parts)})"

        return ''