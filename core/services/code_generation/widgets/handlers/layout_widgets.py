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

        if 'color' in prop_dict:
            color = self.get_property_value(prop_dict, 'color')
            if color:
                code += f"{indent}  decoration: BoxDecoration(color: {DartCodeUtils.generate_color_code(color)}),\n"

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

        code = f'''{widget.widget_type}(
{indent}  mainAxisAlignment: MainAxisAlignment.{main_axis},
{indent}  crossAxisAlignment: CrossAxisAlignment.{cross_axis},'''

        # Check if this is a special home column
        if widget.widget_type == 'Column' and widget.widget_id == 'home_column':
            code += f'''
{indent}  mainAxisSize: MainAxisSize.min,'''

        code += f'''
{indent}  children: ['''

        if child_widgets:
            from ..widget_generator import WidgetGenerator
            widget_gen = WidgetGenerator()

            for i, child in enumerate(child_widgets):
                child_code = widget_gen.generate_widget(child, context, indent_level + 2)
                code += f'''
{indent}    {child_code}'''
                if i < len(child_widgets) - 1:
                    code += ','

        code += f'''
{indent}  ],
{indent})'''

        return code


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

        from ..widget_generator import WidgetGenerator
        widget_gen = WidgetGenerator()

        code = f'''Stack(
{indent}  children: [
'''
        for child in children:
            code += f"{indent}    {widget_gen.generate_widget(child, context, indent_level + 2)},\n"

        code += f"{indent}  ],\n{indent})"

        return code

    def _generate_positioned(self, prop_dict: dict, children: list, context: GeneratorContext,
                             indent_level: int) -> str:
        top = self.get_property_value(prop_dict, 'top', None)
        bottom = self.get_property_value(prop_dict, 'bottom', None)
        left = self.get_property_value(prop_dict, 'left', None)
        right = self.get_property_value(prop_dict, 'right', None)

        params = []
        if top:
            params.append(f"top: {top}")
        if bottom:
            params.append(f"bottom: {bottom}")
        if left:
            params.append(f"left: {left}")
        if right:
            params.append(f"right: {right}")

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
        child_widgets = self.get_child_widgets(widget)

        code = "Center(child: "

        if child_widgets:
            from ..widget_generator import WidgetGenerator
            widget_gen = WidgetGenerator()
            code += widget_gen.generate_widget(child_widgets[0], context, indent_level)
        else:
            code += "Container()"

        code += ")"
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