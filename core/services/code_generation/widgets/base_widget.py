# File: core/services/code_generation/widgets/handlers/basic_widgets.py
"""
Handlers for basic Flutter widgets.
"""

from typing import Any

from ...base import BaseWidgetHandler, GeneratorContext
from ...utils import DartCodeUtils, WidgetPropertyUtils


class TextWidgetHandler(BaseWidgetHandler):
    """Handler for Text widgets."""

    def can_handle(self, widget_type: str) -> bool:
        return widget_type == 'Text'

    def generate(self, widget: Any, context: GeneratorContext, indent_level: int) -> str:
        prop_dict = self.get_widget_properties(widget)

        text_value = self.get_property_value(prop_dict, 'text', 'Text')
        text_value = DartCodeUtils.escape_dart_string(text_value)

        # Generate text style if properties exist
        style_props = WidgetPropertyUtils.get_text_style_properties(prop_dict)
        style_code = WidgetPropertyUtils.generate_text_style(style_props)

        return f"Text('{text_value}'{style_code})"


class ButtonWidgetHandler(BaseWidgetHandler):
    """Handler for Button widgets (ElevatedButton, TextButton, OutlinedButton, IconButton)."""

    def can_handle(self, widget_type: str) -> bool:
        return widget_type in ['ElevatedButton', 'TextButton', 'OutlinedButton', 'IconButton', 'FloatingActionButton']

    def generate(self, widget: Any, context: GeneratorContext, indent_level: int) -> str:
        indent = self.get_indent(indent_level)
        prop_dict = self.get_widget_properties(widget)

        if widget.widget_type == 'IconButton':
            return self._generate_icon_button(widget, prop_dict, indent_level)
        elif widget.widget_type == 'FloatingActionButton':
            return self._generate_fab(widget, prop_dict, indent_level)
        else:
            return self._generate_regular_button(widget, prop_dict, indent_level)

    def _generate_regular_button(self, widget: Any, prop_dict: dict, indent_level: int) -> str:
        indent = self.get_indent(indent_level)

        text = self.get_property_value(prop_dict, 'text', 'Button')
        text = DartCodeUtils.escape_dart_string(text)
        action_code = self._generate_action_code(prop_dict.get('onPressed'))

        return f'''{widget.widget_type}(
{indent}  onPressed: {action_code},
{indent}  child: Text('{text}'),
{indent})'''

    def _generate_icon_button(self, widget: Any, prop_dict: dict, indent_level: int) -> str:
        indent = self.get_indent(indent_level)

        icon = self.get_property_value(prop_dict, 'icon', 'add')
        action_code = self._generate_action_code(prop_dict.get('onPressed'))
        color = self.get_property_value(prop_dict, 'color', None)
        size = self.get_property_value(prop_dict, 'size', None)

        icon_code = f"Icon(Icons.{icon}"
        if color:
            icon_code += f", color: {DartCodeUtils.generate_color_code(color)}"
        if size:
            icon_code += f", size: {size}"
        icon_code += ")"

        return f'''IconButton(
{indent}  icon: {icon_code},
{indent}  onPressed: {action_code},
{indent})'''

    def _generate_fab(self, widget: Any, prop_dict: dict, indent_level: int) -> str:
        indent = self.get_indent(indent_level)

        icon = self.get_property_value(prop_dict, 'icon', 'add')
        action_code = self._generate_action_code(prop_dict.get('onPressed'))

        return f'''FloatingActionButton(
{indent}  onPressed: {action_code},
{indent}  child: Icon(Icons.{icon}),
{indent})'''

    def _generate_action_code(self, prop: Any) -> str:
        """Generate action code from property."""
        if not prop:
            return 'null'

        if hasattr(prop, 'action_reference') and prop.action_reference:
            action = prop.action_reference
            if action.action_type == 'navigate' and action.target_screen:
                return f"() {{ Navigator.pushNamed(context, '{action.target_screen.route_name}'); }}"
            elif action.action_type == 'navigate_back':
                return "() { Navigator.pop(context); }"
            elif action.action_type == 'show_dialog':
                title = DartCodeUtils.escape_dart_string(action.dialog_title or 'Alert')
                message = DartCodeUtils.escape_dart_string(action.dialog_message or 'Message')
                return f'''() {{
          showDialog(
            context: context,
            builder: (context) => AlertDialog(
              title: Text('{title}'),
              content: Text('{message}'),
              actions: [
                TextButton(
                  onPressed: () => Navigator.pop(context),
                  child: Text('OK'),
                ),
              ],
            ),
          );
        }}'''

        if hasattr(prop, 'screen_reference') and prop.screen_reference:
            return f"() {{ Navigator.pushNamed(context, '{prop.screen_reference.route_name}'); }}"

        return 'null'


class IconWidgetHandler(BaseWidgetHandler):
    """Handler for Icon widget."""

    def can_handle(self, widget_type: str) -> bool:
        return widget_type == 'Icon'

    def generate(self, widget: Any, context: GeneratorContext, indent_level: int) -> str:
        prop_dict = self.get_widget_properties(widget)

        icon_name = self.get_property_value(prop_dict, 'icon', 'info')
        icon_size = self.get_property_value(prop_dict, 'size', None)
        icon_color = self.get_property_value(prop_dict, 'color', None)

        code = f"Icon(Icons.{icon_name}"

        params = []
        if icon_size:
            params.append(f"size: {icon_size}")
        if icon_color:
            params.append(f"color: {DartCodeUtils.generate_color_code(icon_color)}")

        if params:
            code += f", {', '.join(params)}"

        code += ")"
        return code


class ImageWidgetHandler(BaseWidgetHandler):
    """Handler for Image widget."""

    def can_handle(self, widget_type: str) -> bool:
        return widget_type == 'Image'

    def generate(self, widget: Any, context: GeneratorContext, indent_level: int) -> str:
        prop_dict = self.get_widget_properties(widget)

        # Try different property names for image URL
        url_prop = None
        for prop_name in ['imageUrl', 'url', 'src', 'source']:
            if prop_name in prop_dict:
                url_prop = prop_dict[prop_name]
                break

        if url_prop:
            url = url_prop.get_value()
            if url and url.startswith('http'):
                return f"Image.network('{url}', fit: BoxFit.cover, errorBuilder: (c,e,s) => Icon(Icons.image))"
            elif url:
                return f"Image.asset('{url}', fit: BoxFit.cover)"

        return "Icon(Icons.image, size: 50)"


class DividerWidgetHandler(BaseWidgetHandler):
    """Handler for Divider widget."""

    def can_handle(self, widget_type: str) -> bool:
        return widget_type == 'Divider'

    def generate(self, widget: Any, context: GeneratorContext, indent_level: int) -> str:
        prop_dict = self.get_widget_properties(widget)

        height = self.get_property_value(prop_dict, 'height', None)
        thickness = self.get_property_value(prop_dict, 'thickness', None)
        color = self.get_property_value(prop_dict, 'color', None)

        params = []
        if height:
            params.append(f"height: {height}")
        if thickness:
            params.append(f"thickness: {thickness}")
        if color:
            params.append(f"color: {DartCodeUtils.generate_color_code(color)}")

        if params:
            return f"Divider({', '.join(params)})"

        return "Divider()"