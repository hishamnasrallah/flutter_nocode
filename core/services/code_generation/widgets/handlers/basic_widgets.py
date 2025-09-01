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
        
        # Additional text parameters
        params = ''
        text_align = self.get_property_value(prop_dict, 'textAlign', None)
        if text_align:
            params += f", textAlign: TextAlign.{text_align}"
        soft_wrap = self.get_property_value(prop_dict, 'softWrap', None)
        if soft_wrap is not None and soft_wrap != '':
            # Accept boolean or string boolean
            soft_wrap_val = str(soft_wrap).lower() if isinstance(soft_wrap, bool) or isinstance(soft_wrap, str) else 'true'
            params += f", softWrap: {soft_wrap_val}"
        overflow = self.get_property_value(prop_dict, 'overflow', None)
        if overflow:
            params += f", overflow: TextOverflow.{overflow}"
        max_lines = self.get_property_value(prop_dict, 'maxLines', None)
        if max_lines:
            params += f", maxLines: {max_lines}"

        return f"Text('{text_value}'{style_code}{params})"


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

        # Style properties (support both top-level and style.* aliases)
        bg = self.get_property_value(prop_dict, 'backgroundColor', None) or self.get_property_value(prop_dict, 'style.backgroundColor', None)
        fg = self.get_property_value(prop_dict, 'foregroundColor', None) or self.get_property_value(prop_dict, 'style.foregroundColor', None)
        padding = self.get_property_value(prop_dict, 'padding', None) or self.get_property_value(prop_dict, 'style.padding', None)
        width = self.get_property_value(prop_dict, 'width', None)
        height = self.get_property_value(prop_dict, 'height', None)
        margin = self.get_property_value(prop_dict, 'margin', None)
        radius = self.get_property_value(prop_dict, 'borderRadius', None)
        elevation = self.get_property_value(prop_dict, 'elevation', None)
        border_color = self.get_property_value(prop_dict, 'borderColor', None)
        border_width = self.get_property_value(prop_dict, 'borderWidth', None)

        # Button style builder using *.styleFrom
        style_args = []
        if bg:
            style_args.append(f"backgroundColor: {DartCodeUtils.generate_color_code(bg)}")
        if fg:
            style_args.append(f"foregroundColor: {DartCodeUtils.generate_color_code(fg)}")
        if padding:
            style_args.append(f"padding: EdgeInsets.all({padding})")
        if elevation:
            style_args.append(f"elevation: {elevation}")
        if radius:
            style_args.append(f"shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular({radius}))")
        # OutlinedButton borders
        if widget.widget_type == 'OutlinedButton' and (border_color or border_width):
            color_expr = DartCodeUtils.generate_color_code(border_color) if border_color else 'Colors.grey'
            width_expr = border_width if border_width else '1.0'
            style_args.append(f"side: BorderSide(color: {color_expr}, width: {width_expr})")

        style_code = f"style: {widget.widget_type}.styleFrom({', '.join(style_args)})" if style_args else ''

        # Size/margin wrappers
        inner = f"{widget.widget_type}(\n{indent}  onPressed: {action_code},\n{indent}  child: Text('{text}')" + (f",\n{indent}  {style_code}" if style_code else '') + f"\n{indent})"
        if width or height:
            size_params = []
            if width:
                size_params.append(f"width: {width}")
            if height:
                size_params.append(f"height: {height}")
            inner = f"SizedBox({', '.join(size_params)}, child: {inner})"
        if margin:
            inner = f"Padding(padding: EdgeInsets.all({margin}), child: {inner})"

        return inner

        # If no action defined, create a default action based on button text
        if action_code == 'null':
            # Generic handler for all buttons
            action_code = '''() {
              // Button action for: ''' + text + '''
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(content: Text("''' + text + ''' clicked")),
              );
            }'''

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
        splash_radius = self.get_property_value(prop_dict, 'splashRadius', None)

        icon_code = f"Icon(Icons.{icon}"
        if color:
            icon_code += f", color: {DartCodeUtils.generate_color_code(color)}"
        if size:
            icon_code += f", size: {size}"
        icon_code += ")"

        return f'''IconButton(
{indent}  icon: {icon_code},
{indent}  onPressed: {action_code},
{indent}{'  splashRadius: ' + str(splash_radius) + ',' if splash_radius else ''}
{indent})'''

    def _generate_fab(self, widget: Any, prop_dict: dict, indent_level: int) -> str:
        indent = self.get_indent(indent_level)

        icon = self.get_property_value(prop_dict, 'icon', 'add')
        action_code = self._generate_action_code(prop_dict.get('onPressed'))
        bg = self.get_property_value(prop_dict, 'backgroundColor', None)
        fg = self.get_property_value(prop_dict, 'foregroundColor', None)
        mini = self.get_property_value(prop_dict, 'mini', None)
        extended = self.get_property_value(prop_dict, 'extended', None)
        label = self.get_property_value(prop_dict, 'label', None)
        params = [f"onPressed: {action_code}"]
        if bg:
            params.append(f"backgroundColor: {DartCodeUtils.generate_color_code(bg)}")
        if fg:
            params.append(f"foregroundColor: {DartCodeUtils.generate_color_code(fg)}")
        # Only allow mini for the regular FAB, not the extended variant
        is_extended = extended and str(extended).lower() == 'true'
        if (mini and str(mini).lower() == 'true') and not is_extended:
            params.append("mini: true")

        if is_extended:
            lbl = DartCodeUtils.escape_dart_string(label or 'Action')
            return f"FloatingActionButton.extended({', '.join(params)}, label: Text('{lbl}'), icon: Icon(Icons.{icon}))"
        else:
            return f"FloatingActionButton({', '.join(params)}, child: Icon(Icons.{icon}))"

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
            elif action.action_type == 'show_snackbar':
                message = DartCodeUtils.escape_dart_string(action.dialog_message or 'Done')
                # Try to parse parameters as JSON for styling
                try:
                    import json
                    params = json.loads(action.parameters) if action.parameters else {}
                except Exception:
                    params = {}
                bg = params.get('backgroundColor')
                duration_ms = params.get('durationMs')
                padding = params.get('padding')
                margin = params.get('margin')
                parts = [f"content: Text('{message}')"]
                if bg:
                    parts.append(f"backgroundColor: {DartCodeUtils.generate_color_code(bg)}")
                if duration_ms:
                    parts.append(f"duration: Duration(milliseconds: {duration_ms})")
                if padding:
                    parts.append(f"padding: EdgeInsets.all({padding})")
                if margin:
                    parts.append(f"margin: EdgeInsets.all({margin})")
                return "() { ScaffoldMessenger.of(context).showSnackBar(SnackBar(" + ', '.join(parts) + ")); }"
            elif action.action_type == 'api_call' and action.api_data_source:
                from ...utils import StringUtils
                method_name = 'fetch' + StringUtils.to_pascal_case(action.api_data_source.name)
                return f"() async {{ try {{ await _apiService.{method_name}(); ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Success'))); }} catch (e) {{ ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Error'))); }} }}"
            elif action.action_type == 'open_url' and action.url:
                return f"() {{ /* TODO: open URL {action.url} */ }}"

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

        # Common optional params
        width = self.get_property_value(prop_dict, 'width', None)
        height = self.get_property_value(prop_dict, 'height', None)
        fit = self.get_property_value(prop_dict, 'fit', None)
        fit_expr = f"BoxFit.{fit}" if fit else "BoxFit.cover"
        alignment = self.get_property_value(prop_dict, 'alignment', None)
        repeat = self.get_property_value(prop_dict, 'repeat', None)
        opacity = self.get_property_value(prop_dict, 'opacity', None)
        color_blend_mode = self.get_property_value(prop_dict, 'colorBlendMode', None)
        scale = self.get_property_value(prop_dict, 'scale', None)

        size_params = []
        if width:
            size_params.append(f"width: {width}")
        if height:
            size_params.append(f"height: {height}")
        size_params_str = (', ' + ', '.join(size_params)) if size_params else ''

        extra_params = []
        if alignment:
            extra_params.append(f"alignment: Alignment.{alignment}")
        if repeat:
            extra_params.append(f"repeat: ImageRepeat.{repeat}")
        if color_blend_mode:
            extra_params.append(f"colorBlendMode: BlendMode.{color_blend_mode}")
        if scale:
            extra_params.append(f"scale: {scale}")

        if url_prop:
            url = url_prop.get_value()
            if url and url.startswith('http'):
                base = f"Image.network('{url}', fit: {fit_expr}{size_params_str}"
            elif url:
                base = f"Image.asset('{url}', fit: {fit_expr}{size_params_str}"
            else:
                base = None

            if base:
                if extra_params:
                    base += ", " + ", ".join(extra_params)
                # Opacity wrapper if requested
                code = base + (", errorBuilder: (c,e,s) => Icon(Icons.image))" if url and url.startswith('http') else ")")
                if opacity:
                    return f"Opacity(opacity: {opacity}, child: {code})"
                return code

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
        indent_val = self.get_property_value(prop_dict, 'indent', None)
        end_indent_val = self.get_property_value(prop_dict, 'endIndent', None)

        params = []
        if height:
            params.append(f"height: {height}")
        if thickness:
            params.append(f"thickness: {thickness}")
        if color:
            params.append(f"color: {DartCodeUtils.generate_color_code(color)}")
        if indent_val:
            params.append(f"indent: {indent_val}")
        if end_indent_val:
            params.append(f"endIndent: {end_indent_val}")

        if params:
            return f"Divider({', '.join(params)})"

        return "Divider()"