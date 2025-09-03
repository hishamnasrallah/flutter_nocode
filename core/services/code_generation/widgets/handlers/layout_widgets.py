# File: core/services/code_generation/widgets/handlers/layout_widgets.py
"""
Handlers for layout Flutter widgets.
"""

from typing import Any

from ...base import BaseWidgetHandler, GeneratorContext
from ...utils import DartCodeUtils


class ContainerWidgetHandler(BaseWidgetHandler):
    """Handler for Container widget."""

    def can_handle(self, widget_type: str) -> bool:
        return widget_type == 'Container'

    def generate(self, widget: Any, context: GeneratorContext, indent_level: int) -> str:
        indent = self.get_indent(indent_level)
        prop_dict = self.get_widget_properties(widget)
        child_widgets = self.get_child_widgets(widget)

        code = "Container(\n"

        # Add properties
        if 'width' in prop_dict:
            width = self.get_property_value(prop_dict, 'width')
            if width:
                code += f"{indent}  width: {width},\n"

        if 'height' in prop_dict:
            height = self.get_property_value(prop_dict, 'height')
            if height:
                code += f"{indent}  height: {height},\n"

        if 'padding' in prop_dict:
            padding = self.get_property_value(prop_dict, 'padding')
            if padding:
                code += f"{indent}  padding: EdgeInsets.all({padding}),\n"

        if 'margin' in prop_dict:
            margin = self.get_property_value(prop_dict, 'margin')
            if margin:
                code += f"{indent}  margin: EdgeInsets.all({margin}),\n"

        # Decoration build: color, borderRadius, border, boxShadow, gradient
        dec_color = self.get_property_value(prop_dict, 'color') or self.get_property_value(prop_dict, 'decoration.color')
        br = self.get_property_value(prop_dict, 'borderRadius') or self.get_property_value(prop_dict, 'decoration.borderRadius')
        border_color = self.get_property_value(prop_dict, 'borderColor') or self.get_property_value(prop_dict, 'decoration.border.color')
        border_width = self.get_property_value(prop_dict, 'borderWidth') or self.get_property_value(prop_dict, 'decoration.border.width')
        shadow_color = self.get_property_value(prop_dict, 'boxShadowColor') or self.get_property_value(prop_dict, 'decoration.boxShadow.color')
        shadow_blur = self.get_property_value(prop_dict, 'boxShadowBlur') or self.get_property_value(prop_dict, 'decoration.boxShadow.blurRadius')
        shadow_spread = self.get_property_value(prop_dict, 'boxShadowSpread') or self.get_property_value(prop_dict, 'decoration.boxShadow.spreadRadius')
        shadow_offset_x = self.get_property_value(prop_dict, 'boxShadowOffsetX') or self.get_property_value(prop_dict, 'decoration.boxShadow.offsetX')
        shadow_offset_y = self.get_property_value(prop_dict, 'boxShadowOffsetY') or self.get_property_value(prop_dict, 'decoration.boxShadow.offsetY')
        grad_value = self.get_property_value(prop_dict, 'gradient') or self.get_property_value(prop_dict, 'decoration.gradient')

        decoration_parts = []
        if dec_color:
            decoration_parts.append(f"color: {DartCodeUtils.generate_color_code(dec_color)}")
        if br:
            decoration_parts.append(f"borderRadius: BorderRadius.circular({br})")
        if border_color or border_width:
            color_expr = DartCodeUtils.generate_color_code(border_color) if border_color else 'Colors.black'
            width_expr = border_width if border_width else '1.0'
            decoration_parts.append(f"border: Border.all(color: {color_expr}, width: {width_expr})")
        # Single shadow support
        box_shadow_parts = []
        if shadow_color:
            box_shadow_parts.append(f"color: {DartCodeUtils.generate_color_code(shadow_color)}")
        if shadow_blur:
            box_shadow_parts.append(f"blurRadius: {shadow_blur}")
        if shadow_spread:
            box_shadow_parts.append(f"spreadRadius: {shadow_spread}")
        if shadow_offset_x or shadow_offset_y:
            ox = shadow_offset_x if shadow_offset_x else '0'
            oy = shadow_offset_y if shadow_offset_y else '0'
            box_shadow_parts.append(f"offset: Offset({ox}, {oy})")
        if box_shadow_parts:
            decoration_parts.append(f"boxShadow: [BoxShadow({', '.join(box_shadow_parts)})]")
        # Gradient: accept two colors via 'gradientStart'/'gradientEnd' or comma-separated string or JSON array
        grad_start = self.get_property_value(prop_dict, 'gradientStart') or self.get_property_value(prop_dict, 'decoration.gradient.startColor')
        grad_end = self.get_property_value(prop_dict, 'gradientEnd') or self.get_property_value(prop_dict, 'decoration.gradient.endColor')
        grad_code = None
        if grad_start and grad_end:
            c1 = DartCodeUtils.generate_color_code(grad_start)
            c2 = DartCodeUtils.generate_color_code(grad_end)
            grad_code = f"LinearGradient(colors: [{c1}, {c2}])"
        elif grad_value:
            try:
                # Try to parse as comma-separated colors
                colors = [c.strip() for c in str(grad_value).split(',') if c.strip()]
                if len(colors) >= 2:
                    c_list = ', '.join([DartCodeUtils.generate_color_code(c) for c in colors[:4]])
                    grad_code = f"LinearGradient(colors: [{c_list}])"
            except Exception:
                pass
        if grad_code:
            decoration_parts.append(f"gradient: {grad_code}")

        if decoration_parts:
            code += f"{indent}  decoration: BoxDecoration({', '.join(decoration_parts)}),\n"

        # Transform and clipBehavior
        transform = self.get_property_value(prop_dict, 'transform', None)
        if transform:
            # Support simple transforms: rotate, scale, translate as dict
            try:
                if isinstance(transform, dict):
                    if 'rotate' in transform:
                        code += f"{indent}  transform: Matrix4.rotationZ({transform['rotate']}),\n"
                    elif 'scale' in transform:
                        code += f"{indent}  transform: Matrix4.identity()..scale({transform['scale']}),\n"
                    elif 'translateX' in transform or 'translateY' in transform:
                        tx = transform.get('translateX', 0)
                        ty = transform.get('translateY', 0)
                        code += f"{indent}  transform: Matrix4.translationValues({tx}, {ty}, 0),\n"
            except Exception:
                pass
        clip_behavior = self.get_property_value(prop_dict, 'clipBehavior', None)
        if clip_behavior:
            code += f"{indent}  clipBehavior: Clip.{clip_behavior},\n"

        # Alignment
        if 'alignment' in prop_dict:
            alignment = self.get_property_value(prop_dict, 'alignment')
            if alignment:
                code += f"{indent}  alignment: Alignment.{alignment},\n"

        # Constraints (min/max)
        min_w = self.get_property_value(prop_dict, 'minWidth', None)
        max_w = self.get_property_value(prop_dict, 'maxWidth', None)
        min_h = self.get_property_value(prop_dict, 'minHeight', None)
        max_h = self.get_property_value(prop_dict, 'maxHeight', None)
        constraints_parts = []
        if any([min_w, max_w, min_h, max_h]):
            if min_w:
                constraints_parts.append(f"minWidth: {min_w}")
            if max_w:
                constraints_parts.append(f"maxWidth: {max_w}")
            if min_h:
                constraints_parts.append(f"minHeight: {min_h}")
            if max_h:
                constraints_parts.append(f"maxHeight: {max_h}")
            code += f"{indent}  constraints: BoxConstraints({', '.join(constraints_parts)}),\n"

        # Add child if exists
        if child_widgets:
            code += f"{indent}  child: "

            # Import WidgetGenerator to handle children
            from ..widget_generator import WidgetGenerator
            widget_gen = WidgetGenerator()

            if len(child_widgets) == 1:
                code += widget_gen.generate_widget(child_widgets[0], context, indent_level + 1)
            else:
                code += self._generate_children_column(child_widgets, context, indent_level + 1)
            code += ",\n"

        code += f"{indent})"
        return code

    def _generate_children_column(self, children: list, context: GeneratorContext, indent_level: int) -> str:
        """Generate Column for multiple children."""
        indent = self.get_indent(indent_level)

        from ..widget_generator import WidgetGenerator
        widget_gen = WidgetGenerator()

        code = f"Column(\n{indent}  children: [\n"
        for child in children:
            code += f"{indent}    {widget_gen.generate_widget(child, context, indent_level + 2)},\n"
        code += f"{indent}  ],\n{indent})"

        return code


class ColumnRowWidgetHandler(BaseWidgetHandler):
    """Handler for Column and Row widgets."""

    def can_handle(self, widget_type: str) -> bool:
        return widget_type in ['Column', 'Row']

    def generate(self, widget: Any, context: GeneratorContext, indent_level: int) -> str:
        indent = self.get_indent(indent_level)
        prop_dict = self.get_widget_properties(widget)
        child_widgets = self.get_child_widgets(widget)

        main_axis = self.get_property_value(prop_dict, 'mainAxisAlignment', 'start')
        cross_axis = self.get_property_value(prop_dict, 'crossAxisAlignment', 'center')

        spacing = self.get_property_value(prop_dict, 'spacing', None)
        padding_val = self.get_property_value(prop_dict, 'padding', None)
        bg_color = self.get_property_value(prop_dict, 'backgroundColor', None)
        radius = self.get_property_value(prop_dict, 'borderRadius', None)
        elevation = self.get_property_value(prop_dict, 'elevation', None)

        inner = f'''{widget.widget_type}(
{indent}  mainAxisAlignment: MainAxisAlignment.{main_axis},
{indent}  crossAxisAlignment: CrossAxisAlignment.{cross_axis},'''

        # Check if this is a special home column
        if widget.widget_type == 'Column' and widget.widget_id == 'home_column':
            code += f'''
{indent}  mainAxisSize: MainAxisSize.min,'''

        inner += f'''
{indent}  children: ['''

        if child_widgets:
            from ..widget_generator import WidgetGenerator
            widget_gen = WidgetGenerator()

            for i, child in enumerate(child_widgets):
                child_code = widget_gen.generate_widget(child, context, indent_level + 2)
                inner += f'''
{indent}    {child_code}'''
                # Insert spacing as SizedBox between children if provided
                if spacing and i < len(child_widgets) - 1:
                    inner += f''',
{indent}    SizedBox({ 'height' if widget.widget_type == 'Column' else 'width' }: {spacing}),'''
                elif i < len(child_widgets) - 1:
                    inner += ','

        inner += f'''
{indent}  ],
{indent})'''

        # Optional visual wrappers: padding, background with radius/elevation
        widget_code = inner
        if bg_color or radius or elevation:
            deco_parts = []
            if bg_color:
                deco_parts.append(f"color: {DartCodeUtils.generate_color_code(bg_color)}")
            if radius:
                deco_parts.append(f"borderRadius: BorderRadius.circular({radius})")
            if elevation:
                deco_parts.append(f"boxShadow: [BoxShadow(color: Colors.black26, blurRadius: {elevation})]")
            widget_code = f"Container(\n{indent}  decoration: BoxDecoration({', '.join(deco_parts)}),\n{indent}  child: {inner}\n{indent})"
        if padding_val:
            widget_code = f"Padding(\n{indent}  padding: EdgeInsets.all({padding_val}),\n{indent}  child: {widget_code}\n{indent})"

        return widget_code


class StackWidgetHandler(BaseWidgetHandler):
    """Handler for Stack and Positioned widgets."""

    def can_handle(self, widget_type: str) -> bool:
        return widget_type in ['Stack', 'Positioned']

    def generate(self, widget: Any, context: GeneratorContext, indent_level: int) -> str:
        indent = self.get_indent(indent_level)
        prop_dict = self.get_widget_properties(widget)
        child_widgets = self.get_child_widgets(widget)

        if widget.widget_type == 'Stack':
            return self._generate_stack(child_widgets, context, indent_level)
        else:  # Positioned
            return self._generate_positioned(prop_dict, child_widgets, context, indent_level)

    def _generate_stack(self, children: list, context: GeneratorContext, indent_level: int) -> str:
        indent = self.get_indent(indent_level)
        # Try to read visuals from a pseudo property on parent child (not provided here). Keep simple.
        from ..widget_generator import WidgetGenerator
        widget_gen = WidgetGenerator()
        body = f"""[
"""
        for child in children:
            body += f"{indent}    {widget_gen.generate_widget(child, context, indent_level + 2)},\n"
        body += f"{indent}  ]"
        return f"Stack(\n{indent}  children: {body},\n{indent})"

    def _generate_positioned(self, prop_dict: dict, children: list, context: GeneratorContext,
                             indent_level: int) -> str:
        top = self.get_property_value(prop_dict, 'top', None)
        bottom = self.get_property_value(prop_dict, 'bottom', None)
        left = self.get_property_value(prop_dict, 'left', None)
        right = self.get_property_value(prop_dict, 'right', None)
        width = self.get_property_value(prop_dict, 'width', None)
        height = self.get_property_value(prop_dict, 'height', None)

        params = []
        if top:
            params.append(f"top: {top}")
        if bottom:
            params.append(f"bottom: {bottom}")
        if left:
            params.append(f"left: {left}")
        if right:
            params.append(f"right: {right}")
        if width:
            params.append(f"width: {width}")
        if height:
            params.append(f"height: {height}")

        code = "Positioned("
        if params:
            code += ", ".join(params) + ", "

        code += "child: "

        if children:
            from ..widget_generator import WidgetGenerator
            widget_gen = WidgetGenerator()
            code += widget_gen.generate_widget(children[0], context, indent_level)
        else:
            code += "Container()"

        code += ")"
        return code


class ExpandedFlexibleHandler(BaseWidgetHandler):
    """Handler for Expanded and Flexible widgets."""

    def can_handle(self, widget_type: str) -> bool:
        return widget_type in ['Expanded', 'Flexible']

    def generate(self, widget: Any, context: GeneratorContext, indent_level: int) -> str:
        indent = self.get_indent(indent_level)
        prop_dict = self.get_widget_properties(widget)
        child_widgets = self.get_child_widgets(widget)

        flex = self.get_property_value(prop_dict, 'flex', '1')

        code = f'''{widget.widget_type}(
{indent}  flex: {flex},'''

        if widget.widget_type == 'Flexible':
            fit = self.get_property_value(prop_dict, 'fit', 'loose')
            code += f'''
{indent}  fit: FlexFit.{fit},'''

        code += f'''
{indent}  child: '''

        if child_widgets:
            from ..widget_generator import WidgetGenerator
            widget_gen = WidgetGenerator()
            code += widget_gen.generate_widget(child_widgets[0], context, indent_level + 1)
        else:
            code += "Container()"

        code += f",\n{indent})"

        return code


class PaddingWidgetHandler(BaseWidgetHandler):
    """Handler for Padding widget."""

    def can_handle(self, widget_type: str) -> bool:
        return widget_type == 'Padding'

    def generate(self, widget: Any, context: GeneratorContext, indent_level: int) -> str:
        indent = self.get_indent(indent_level)
        prop_dict = self.get_widget_properties(widget)
        child_widgets = self.get_child_widgets(widget)

        padding = self.get_property_value(prop_dict, 'padding', '8.0')

        code = f'''Padding(
{indent}  padding: EdgeInsets.all({padding}),
{indent}  child: '''

        if child_widgets:
            from ..widget_generator import WidgetGenerator
            widget_gen = WidgetGenerator()
            code += widget_gen.generate_widget(child_widgets[0], context, indent_level + 1)
        else:
            code += "Container()"

        code += f",\n{indent})"

        return code


class CenterWidgetHandler(BaseWidgetHandler):
    """Handler for Center widget."""

    def can_handle(self, widget_type: str) -> bool:
        return widget_type == 'Center'

    def generate(self, widget: Any, context: GeneratorContext, indent_level: int) -> str:
        prop_dict = self.get_widget_properties(widget)
        child_widgets = self.get_child_widgets(widget)

        width_factor = self.get_property_value(prop_dict, 'widthFactor', None)
        height_factor = self.get_property_value(prop_dict, 'heightFactor', None)

        params = []
        if width_factor:
            params.append(f"widthFactor: {width_factor}")
        if height_factor:
            params.append(f"heightFactor: {height_factor}")

        code = "Center("
        if params:
            code += ", ".join(params) + ", "
        code += "child: "

        if child_widgets:
            from ..widget_generator import WidgetGenerator
            widget_gen = WidgetGenerator()
            code += widget_gen.generate_widget(child_widgets[0], context, indent_level)
        else:
            code += "Container()"

        code += ")"
        return code


class AlignWidgetHandler(BaseWidgetHandler):
    """Handler for Align widget."""

    def can_handle(self, widget_type: str) -> bool:
        return widget_type == 'Align'

    def generate(self, widget: Any, context: GeneratorContext, indent_level: int) -> str:
        indent = self.get_indent(indent_level)
        prop_dict = self.get_widget_properties(widget)
        child_widgets = self.get_child_widgets(widget)

        alignment = self.get_property_value(prop_dict, 'alignment', 'center')

        code = f"""Align(
{indent}  alignment: Alignment.{alignment},
{indent}  child: """

        if child_widgets:
            from ..widget_generator import WidgetGenerator
            widget_gen = WidgetGenerator()
            code += widget_gen.generate_widget(child_widgets[0], context, indent_level + 1)
        else:
            code += "Container()"

        code += f",\n{indent})"

        return code


class SizedBoxWidgetHandler(BaseWidgetHandler):
    """Handler for SizedBox widget."""

    def can_handle(self, widget_type: str) -> bool:
        return widget_type == 'SizedBox'

    def generate(self, widget: Any, context: GeneratorContext, indent_level: int) -> str:
        prop_dict = self.get_widget_properties(widget)
        child_widgets = self.get_child_widgets(widget)

        width = self.get_property_value(prop_dict, 'width', None)
        height = self.get_property_value(prop_dict, 'height', None)

        code = "SizedBox("
        params = []

        if width:
            params.append(f"width: {width}")
        if height:
            params.append(f"height: {height}")

        if params:
            code += ", ".join(params)
            if child_widgets:
                code += ", "

        if child_widgets:
            from ..widget_generator import WidgetGenerator
            widget_gen = WidgetGenerator()
            code += f"child: {widget_gen.generate_widget(child_widgets[0], context, indent_level)}"

        code += ")"
        return code