# File: core/services/code_generation/widgets/handlers/advanced_widgets.py
"""
Handlers for advanced Flutter widgets.
"""

from typing import Any

from ...base import BaseWidgetHandler, GeneratorContext
from ...utils import DartCodeUtils


class CardHandler(BaseWidgetHandler):
    """Handler for Card widget."""

    def can_handle(self, widget_type: str) -> bool:
        return widget_type == 'Card'

    def generate(self, widget: Any, context: GeneratorContext, indent_level: int) -> str:
        indent = self.get_indent(indent_level)
        prop_dict = self.get_widget_properties(widget)
        child_widgets = self.get_child_widgets(widget)

        elevation = self.get_property_value(prop_dict, 'elevation', '4')
        margin = self.get_property_value(prop_dict, 'margin', None)
        color = self.get_property_value(prop_dict, 'color', None)

        code = f'''Card(
{indent}  elevation: {elevation},'''

        if margin:
            code += f"\n{indent}  margin: EdgeInsets.all({margin}),"

        if color:
            code += f"\n{indent}  color: {DartCodeUtils.generate_color_code(color)},"

        code += f'''
{indent}  child: '''

        if child_widgets:
            from ..widget_generator import WidgetGenerator
            widget_gen = WidgetGenerator()

            if len(child_widgets) == 1:
                code += widget_gen.generate_widget(child_widgets[0], context, indent_level + 1)
            else:
                code += self._generate_children_column(child_widgets, context, indent_level + 1)
        else:
            code += "Container()"

        code += f",\n{indent})"

        return code

    def _generate_children_column(self, children: list, context: GeneratorContext, indent_level: int) -> str:
        """Generate Column for multiple children."""
        indent = self.get_indent(indent_level)

        from ..widget_generator import WidgetGenerator
        widget_gen = WidgetGenerator()

        code = f'''Column(
{indent}  children: [
'''
        for child in children:
            code += f"{indent}    {widget_gen.generate_widget(child, context, indent_level + 2)},\n"

        code += f"{indent}  ],\n{indent})"

        return code


class FutureBuilderHandler(BaseWidgetHandler):
    """Handler for FutureBuilder widget."""

    def can_handle(self, widget_type: str) -> bool:
        return widget_type == 'FutureBuilder'

    def generate(self, widget: Any, context: GeneratorContext, indent_level: int) -> str:
        indent = self.get_indent(indent_level)
        prop_dict = self.get_widget_properties(widget)
        child_widgets = self.get_child_widgets(widget)

        # Check if there's a data source
        data_source_prop = prop_dict.get('dataSource')

        if data_source_prop and hasattr(data_source_prop, 'data_source_field_reference'):
            if data_source_prop.data_source_field_reference:
                data_source = data_source_prop.data_source_field_reference.data_source
                return self._generate_with_data_source(data_source, child_widgets, context, indent_level)

        # Default FutureBuilder
        return self._generate_default(child_widgets, context, indent_level)

    def _generate_with_data_source(self, data_source: Any, child_widgets: list,
                                   context: GeneratorContext, indent_level: int) -> str:
        """Generate FutureBuilder with data source."""
        indent = self.get_indent(indent_level)

        code = f'''FutureBuilder<List<dynamic>>(
{indent}  future: _apiService.fetchData('{data_source.name}'),
{indent}  builder: (context, snapshot) {{
{indent}    if (snapshot.connectionState == ConnectionState.waiting) {{
{indent}      return Center(child: CircularProgressIndicator());
{indent}    }}
{indent}    if (snapshot.hasError) {{
{indent}      return Center(child: Text('Error: ${{snapshot.error}}'));
{indent}    }}
{indent}    if (!snapshot.hasData || snapshot.data!.isEmpty) {{
{indent}      return Center(child: Text('No data available'));
{indent}    }}
{indent}    return '''

        if child_widgets:
            from ..widget_generator import WidgetGenerator
            widget_gen = WidgetGenerator()
            code += widget_gen.generate_widget(child_widgets[0], context, indent_level + 2)
        else:
            code += "Container()"

        code += f''';
{indent}  }},
{indent})'''

        return code

    def _generate_default(self, child_widgets: list, context: GeneratorContext, indent_level: int) -> str:
        """Generate default FutureBuilder."""
        indent = self.get_indent(indent_level)

        code = f'''FutureBuilder(
{indent}  future: Future.value(true),
{indent}  builder: (context, snapshot) {{
{indent}    if (snapshot.hasData) {{
{indent}      return '''

        if child_widgets:
            from ..widget_generator import WidgetGenerator
            widget_gen = WidgetGenerator()
            code += widget_gen.generate_widget(child_widgets[0], context, indent_level + 3)
        else:
            code += "Container()"

        code += f''';
{indent}    }}
{indent}    return CircularProgressIndicator();
{indent}  }},
{indent})'''

        return code


class StreamBuilderHandler(BaseWidgetHandler):
    """Handler for StreamBuilder widget."""

    def can_handle(self, widget_type: str) -> bool:
        return widget_type == 'StreamBuilder'

    def generate(self, widget: Any, context: GeneratorContext, indent_level: int) -> str:
        indent = self.get_indent(indent_level)
        child_widgets = self.get_child_widgets(widget)

        code = f'''StreamBuilder(
{indent}  stream: Stream.empty(),
{indent}  builder: (context, snapshot) {{
{indent}    return '''

        if child_widgets:
            from ..widget_generator import WidgetGenerator
            widget_gen = WidgetGenerator()
            code += widget_gen.generate_widget(child_widgets[0], context, indent_level + 2)
        else:
            code += "Container()"

        code += f''';
{indent}  }},
{indent})'''

        return code


class PageViewHandler(BaseWidgetHandler):
    """Handler for PageView widget."""

    def can_handle(self, widget_type: str) -> bool:
        return widget_type == 'PageView'

    def generate(self, widget: Any, context: GeneratorContext, indent_level: int) -> str:
        indent = self.get_indent(indent_level)
        child_widgets = self.get_child_widgets(widget)

        code = f'''PageView(
{indent}  children: [
'''

        if child_widgets:
            from ..widget_generator import WidgetGenerator
            widget_gen = WidgetGenerator()

            for child in child_widgets:
                code += f"{indent}    {widget_gen.generate_widget(child, context, indent_level + 2)},\n"

        code += f"{indent}  ],\n{indent})"

        return code


class WrapHandler(BaseWidgetHandler):
    """Handler for Wrap widget."""

    def can_handle(self, widget_type: str) -> bool:
        return widget_type == 'Wrap'

    def generate(self, widget: Any, context: GeneratorContext, indent_level: int) -> str:
        indent = self.get_indent(indent_level)
        prop_dict = self.get_widget_properties(widget)
        child_widgets = self.get_child_widgets(widget)

        spacing = self.get_property_value(prop_dict, 'spacing', '8.0')
        run_spacing = self.get_property_value(prop_dict, 'runSpacing', '8.0')

        code = f'''Wrap(
{indent}  spacing: {spacing},
{indent}  runSpacing: {run_spacing},
{indent}  children: [
'''

        if child_widgets:
            from ..widget_generator import WidgetGenerator
            widget_gen = WidgetGenerator()

            for child in child_widgets:
                code += f"{indent}    {widget_gen.generate_widget(child, context, indent_level + 2)},\n"

        code += f"{indent}  ],\n{indent})"

        return code


class AspectRatioHandler(BaseWidgetHandler):
    """Handler for AspectRatio widget."""

    def can_handle(self, widget_type: str) -> bool:
        return widget_type == 'AspectRatio'

    def generate(self, widget: Any, context: GeneratorContext, indent_level: int) -> str:
        indent = self.get_indent(indent_level)
        prop_dict = self.get_widget_properties(widget)
        child_widgets = self.get_child_widgets(widget)

        ratio = self.get_property_value(prop_dict, 'aspectRatio', '1.0')

        code = f'''AspectRatio(
{indent}  aspectRatio: {ratio},
{indent}  child: '''

        if child_widgets:
            from ..widget_generator import WidgetGenerator
            widget_gen = WidgetGenerator()
            code += widget_gen.generate_widget(child_widgets[0], context, indent_level + 1)
        else:
            code += "Container()"

        code += f",\n{indent})"

        return code


class SafeAreaHandler(BaseWidgetHandler):
    """Handler for SafeArea widget."""

    def can_handle(self, widget_type: str) -> bool:
        return widget_type == 'SafeArea'

    def generate(self, widget: Any, context: GeneratorContext, indent_level: int) -> str:
        indent = self.get_indent(indent_level)
        child_widgets = self.get_child_widgets(widget)

        code = f'''SafeArea(
{indent}  child: '''

        if child_widgets:
            from ..widget_generator import WidgetGenerator
            widget_gen = WidgetGenerator()
            code += widget_gen.generate_widget(child_widgets[0], context, indent_level + 1)
        else:
            code += "Container()"

        code += f",\n{indent})"

        return code


class ScaffoldHandler(BaseWidgetHandler):
    """Handler for Scaffold widget."""

    def can_handle(self, widget_type: str) -> bool:
        return widget_type == 'Scaffold'

    def generate(self, widget: Any, context: GeneratorContext, indent_level: int) -> str:
        indent = self.get_indent(indent_level)
        child_widgets = self.get_child_widgets(widget)

        code = f'''Scaffold(
{indent}  body: '''

        if child_widgets:
            from ..widget_generator import WidgetGenerator
            widget_gen = WidgetGenerator()
            code += widget_gen.generate_widget(child_widgets[0], context, indent_level + 1)
        else:
            code += "Container()"

        code += f",\n{indent})"

        return code