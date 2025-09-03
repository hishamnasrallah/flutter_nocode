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
        shadow_color = self.get_property_value(prop_dict, 'shadowColor', None)
        border_radius = self.get_property_value(prop_dict, 'borderRadius', None)
        padding_val = self.get_property_value(prop_dict, 'padding', None)

        code = f'''Card(
{indent}  elevation: {elevation},'''

        if margin:
            code += f"\n{indent}  margin: EdgeInsets.all({margin}),"

        if color:
            code += f"\n{indent}  color: {DartCodeUtils.generate_color_code(color)},"
        if shadow_color:
            code += f"\n{indent}  shadowColor: {DartCodeUtils.generate_color_code(shadow_color)},"
        if border_radius:
            code += f"\n{indent}  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular({border_radius})),"

        code += f'''
{indent}  child: '''

        if child_widgets:
            from ..widget_generator import WidgetGenerator
            widget_gen = WidgetGenerator()

            inner = None
            if len(child_widgets) == 1:
                inner = widget_gen.generate_widget(child_widgets[0], context, indent_level + 1)
            else:
                inner = self._generate_children_column(child_widgets, context, indent_level + 1)

            if padding_val:
                code += f"Padding(\n{indent}    padding: EdgeInsets.all({padding_val}),\n{indent}    child: {inner}\n{indent}  )"
            else:
                code += inner
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
        """Generate FutureBuilder with data source - fully dynamic."""
        indent = self.get_indent(indent_level)
        from ...utils import StringUtils

        # Always use dynamic type and handle both Map and List at runtime
        code = f'''FutureBuilder<dynamic>(
    {indent}  future: _apiService.fetch{StringUtils.to_pascal_case(data_source.name)}(),
    {indent}  builder: (context, snapshot) {{
    {indent}    if (snapshot.connectionState == ConnectionState.waiting) {{
    {indent}      return Center(child: CircularProgressIndicator());
    {indent}    }}
    {indent}    if (snapshot.hasError) {{
    {indent}      return Center(child: Text('Error: ${{snapshot.error}}'));
    {indent}    }}
    {indent}    if (!snapshot.hasData) {{
    {indent}      return Center(child: Text('No data available'));
    {indent}    }}
    {indent}    
    {indent}    final rawData = snapshot.data;
    {indent}    
    {indent}    // Handle both single objects and lists dynamically
    {indent}    if (rawData is Map<String, dynamic>) {{
    {indent}      // Single object - display its fields
    {indent}      return _buildSingleItemView(rawData);
    {indent}    }} else if (rawData is List) {{
    {indent}      // List of items
    {indent}      if (rawData.isEmpty) {{
    {indent}        return Center(child: Text('No items available'));
    {indent}      }}
    {indent}      return _buildListView(rawData);
    {indent}    }} else {{
    {indent}      return Center(child: Text('Unexpected data format'));
    {indent}    }}
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


class TabBarViewHandler(BaseWidgetHandler):
    """Handler for TabBarView widget (renders children in pages)."""

    def can_handle(self, widget_type: str) -> bool:
        return widget_type == 'TabBarView'

    def generate(self, widget: Any, context: GeneratorContext, indent_level: int) -> str:
        indent = self.get_indent(indent_level)
        child_widgets = self.get_child_widgets(widget)

        code = f'''TabBarView(
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
        direction = self.get_property_value(prop_dict, 'direction', None)
        alignment = self.get_property_value(prop_dict, 'alignment', None)
        run_alignment = self.get_property_value(prop_dict, 'runAlignment', None)
        cross_axis_alignment = self.get_property_value(prop_dict, 'crossAxisAlignment', None)

        code = f'''Wrap(
{indent}  spacing: {spacing},
{indent}  runSpacing: {run_spacing},'''

        # Optional alignment params
        if direction:
            code += f"\n{indent}  direction: Axis.{direction},"
        if alignment:
            code += f"\n{indent}  alignment: WrapAlignment.{alignment},"
        if run_alignment:
            code += f"\n{indent}  runAlignment: WrapAlignment.{run_alignment},"
        if cross_axis_alignment:
            code += f"\n{indent}  crossAxisAlignment: WrapCrossAlignment.{cross_axis_alignment},"

        code += f"\n{indent}  children: [\n"

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
        prop_dict = self.get_widget_properties(widget)

        # Optional properties
        background_color = self.get_property_value(prop_dict, 'backgroundColor', None)

        # Start building Scaffold
        code = f'''Scaffold('''

        # backgroundColor if provided
        if background_color:
            code += f"\n{indent}  backgroundColor: {DartCodeUtils.generate_color_code(background_color)},"

        code += f"\n{indent}  body: "

        if child_widgets:
            from ..widget_generator import WidgetGenerator
            widget_gen = WidgetGenerator()
            code += widget_gen.generate_widget(child_widgets[0], context, indent_level + 1)
        else:
            code += "Container()"

        code += f",\n{indent})"

        return code


class TooltipHandler(BaseWidgetHandler):
    """Handler for Tooltip widget."""

    def can_handle(self, widget_type: str) -> bool:
        return widget_type == 'Tooltip'

    def generate(self, widget: Any, context: GeneratorContext, indent_level: int) -> str:
        indent = self.get_indent(indent_level)
        prop_dict = self.get_widget_properties(widget)
        child_widgets = self.get_child_widgets(widget)

        message = self.get_property_value(prop_dict, 'message', 'Info')
        message = DartCodeUtils.escape_dart_string(message)
        padding_val = self.get_property_value(prop_dict, 'padding', None)
        margin_val = self.get_property_value(prop_dict, 'margin', None)
        text_style = self.get_property_value(prop_dict, 'textStyle', None)
        deco_color = self.get_property_value(prop_dict, 'decoration.color', None)
        deco_radius = self.get_property_value(prop_dict, 'decoration.borderRadius', None)
        show_duration = self.get_property_value(prop_dict, 'showDurationMs', None)
        wait_duration = self.get_property_value(prop_dict, 'waitDurationMs', None)

        code = f"""Tooltip(
{indent}  message: '{message}',"""

        if padding_val:
            code += f"\n{indent}  padding: EdgeInsets.all({padding_val}),"
        if margin_val:
            code += f"\n{indent}  margin: EdgeInsets.all({margin_val}),"
        if text_style:
            code += f"\n{indent}  textStyle: TextStyle(color: Colors.white)"
        if deco_color or deco_radius:
            deco_parts = []
            if deco_color:
                deco_parts.append(f"color: {DartCodeUtils.generate_color_code(deco_color)}")
            if deco_radius:
                deco_parts.append(f"borderRadius: BorderRadius.circular({deco_radius})")
            code += f"\n{indent}  decoration: BoxDecoration({', '.join(deco_parts)}),"
        if show_duration:
            code += f"\n{indent}  showDuration: Duration(milliseconds: {show_duration}),"
        if wait_duration:
            code += f"\n{indent}  waitDuration: Duration(milliseconds: {wait_duration}),"

        code += f"\n{indent}  child: "

        if child_widgets:
            from ..widget_generator import WidgetGenerator
            widget_gen = WidgetGenerator()
            code += widget_gen.generate_widget(child_widgets[0], context, indent_level + 1)
        else:
            code += "Icon(Icons.info)"

        code += f",\n{indent})"
        return code


class RichTextHandler(BaseWidgetHandler):
    """Basic handler for RichText using a single TextSpan from 'text'."""

    def can_handle(self, widget_type: str) -> bool:
        return widget_type == 'RichText'

    def generate(self, widget: Any, context: GeneratorContext, indent_level: int) -> str:
        prop_dict = self.get_widget_properties(widget)

        text_value = self.get_property_value(prop_dict, 'text', 'Rich Text')
        text_value = DartCodeUtils.escape_dart_string(text_value)

        return f"RichText(text: TextSpan(text: '{text_value}', style: DefaultTextStyle.of(context).style))"


class ChipHandler(BaseWidgetHandler):
    """Handler for Chip widget."""

    def can_handle(self, widget_type: str) -> bool:
        return widget_type == 'Chip'

    def generate(self, widget: Any, context: GeneratorContext, indent_level: int) -> str:
        indent = self.get_indent(indent_level)
        prop_dict = self.get_widget_properties(widget)

        label = self.get_property_value(prop_dict, 'label', 'Chip')
        label = DartCodeUtils.escape_dart_string(label)
        bg = self.get_property_value(prop_dict, 'backgroundColor', None)
        padding_val = self.get_property_value(prop_dict, 'padding', None)
        elevation = self.get_property_value(prop_dict, 'elevation', None)

        params = [f"label: Text('{label}')"]
        if bg:
            params.append(f"backgroundColor: {DartCodeUtils.generate_color_code(bg)}")
        if padding_val:
            params.append(f"labelPadding: EdgeInsets.all({padding_val})")
        if elevation:
            params.append(f"elevation: {elevation}")

        return 'Chip(' + ', '.join(params) + ')'


class AvatarHandler(BaseWidgetHandler):
    """Handler for Avatar widget (CircleAvatar)."""

    def can_handle(self, widget_type: str) -> bool:
        return widget_type == 'Avatar'

    def generate(self, widget: Any, context: GeneratorContext, indent_level: int) -> str:
        prop_dict = self.get_widget_properties(widget)

        radius = self.get_property_value(prop_dict, 'radius', None)
        bg = self.get_property_value(prop_dict, 'backgroundColor', None)
        fg = self.get_property_value(prop_dict, 'foregroundColor', None)
        image = self.get_property_value(prop_dict, 'backgroundImage', None)
        text = self.get_property_value(prop_dict, 'text', None)

        params = []
        if radius:
            params.append(f"radius: {radius}")
        if bg:
            params.append(f"backgroundColor: {DartCodeUtils.generate_color_code(bg)}")
        if fg:
            params.append(f"foregroundColor: {DartCodeUtils.generate_color_code(fg)}")
        if image:
            img = DartCodeUtils.escape_dart_string(image)
            # Use NetworkImage if URL-like, else AssetImage
            if image.startswith('http'):
                params.append(f"backgroundImage: NetworkImage('{img}')")
            else:
                params.append(f"backgroundImage: AssetImage('{img}')")

        if text and not image:
            t = DartCodeUtils.escape_dart_string(text)
            params.append(f"child: Text('{t}')")

        return 'CircleAvatar(' + ', '.join(params) + ')'


class BottomSheetHandler(BaseWidgetHandler):
    """Handler for BottomSheet-like container (as a widget snippet)."""

    def can_handle(self, widget_type: str) -> bool:
        return widget_type == 'BottomSheet'

    def generate(self, widget: Any, context: GeneratorContext, indent_level: int) -> str:
        indent = self.get_indent(indent_level)
        prop_dict = self.get_widget_properties(widget)
        child_widgets = self.get_child_widgets(widget)

        height = self.get_property_value(prop_dict, 'height', None)
        bg = self.get_property_value(prop_dict, 'backgroundColor', None)
        handle = self.get_property_value(prop_dict, 'handle', None)

        # Build inner content
        from ..widget_generator import WidgetGenerator
        widget_gen = WidgetGenerator()
        inner = "Container()"
        if child_widgets:
            if len(child_widgets) == 1:
                inner = widget_gen.generate_widget(child_widgets[0], context, indent_level + 2)
            else:
                inner_children = []
                for child in child_widgets:
                    inner_children.append(widget_gen.generate_widget(child, context, indent_level + 3))
                inner = f"Column(\n{indent}    mainAxisSize: MainAxisSize.min,\n{indent}    children: [\n{indent}      " + f",\n{indent}      ".join(inner_children) + f"\n{indent}    ],\n{indent}  )"

        # Outer container representing bottom sheet body
        params = []
        if height:
            params.append(f"height: {height}")
        if bg:
            params.append(f"color: {DartCodeUtils.generate_color_code(bg)}")

        content = inner
        if handle and str(handle).lower() == 'true':
            # Add a small header handle
            content = f"Column(\n{indent}    mainAxisSize: MainAxisSize.min,\n{indent}    children: [\n{indent}      Container(width: 40, height: 4, margin: EdgeInsets.only(top: 8, bottom: 12), decoration: BoxDecoration(color: Colors.grey[400], borderRadius: BorderRadius.circular(2))),\n{indent}      {inner}\n{indent}    ],\n{indent}  )"

        container = "Container("
        if params:
            container += ", ".join(params) + ", "
        container += f"child: {content})"

        return container


class DialogHandler(BaseWidgetHandler):
    """Handler snippet to produce an in-place AlertDialog widget tree."""

    def can_handle(self, widget_type: str) -> bool:
        return widget_type in ['Dialog', 'AlertDialog']

    def generate(self, widget: Any, context: GeneratorContext, indent_level: int) -> str:
        indent = self.get_indent(indent_level)
        prop_dict = self.get_widget_properties(widget)
        child_widgets = self.get_child_widgets(widget)

        title_text = self.get_property_value(prop_dict, 'title', 'Dialog Title')
        content_text = self.get_property_value(prop_dict, 'content', 'Dialog content goes here.')
        bg = self.get_property_value(prop_dict, 'backgroundColor', None)
        elevation = self.get_property_value(prop_dict, 'elevation', None)
        border_radius = self.get_property_value(prop_dict, 'borderRadius', None)
        padding_val = self.get_property_value(prop_dict, 'padding', None)

        params = []
        if bg:
            params.append(f"backgroundColor: {DartCodeUtils.generate_color_code(bg)}")
        if elevation:
            params.append(f"elevation: {elevation}")
        if border_radius:
            params.append(f"shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular({border_radius}))")

        # Title
        if title_text:
            tt = DartCodeUtils.escape_dart_string(title_text)
            params.append(f"title: Text('{tt}')")

        # Content
        content_code = ""
        if child_widgets:
            from ..widget_generator import WidgetGenerator
            widget_gen = WidgetGenerator()
            if len(child_widgets) == 1:
                content_code = widget_gen.generate_widget(child_widgets[0], context, indent_level + 1)
            else:
                inner = []
                for child in child_widgets:
                    inner.append(widget_gen.generate_widget(child, context, indent_level + 2))
                content_code = f"Column(\n{indent}    mainAxisSize: MainAxisSize.min,\n{indent}    children: [\n{indent}      " + f",\n{indent}      ".join(inner) + f"\n{indent}    ],\n{indent}  )"
        else:
            ct = DartCodeUtils.escape_dart_string(content_text)
            content_code = f"Text('{ct}')"

        if padding_val:
            content_code = f"Padding(padding: EdgeInsets.all({padding_val}), child: {content_code})"

        params.append(f"content: {content_code}")

        # Default action
        params.append(f"actions: [TextButton(onPressed: () => Navigator.pop(context), child: Text('OK'))]")

        return 'AlertDialog(' + ', '.join(params) + ')'


class BadgeHandler(BaseWidgetHandler):
    """Simple Badge handler using a Container overlay approach."""

    def can_handle(self, widget_type: str) -> bool:
        return widget_type == 'Badge'

    def generate(self, widget: Any, context: GeneratorContext, indent_level: int) -> str:
        indent = self.get_indent(indent_level)
        prop_dict = self.get_widget_properties(widget)
        child_widgets = self.get_child_widgets(widget)

        count = self.get_property_value(prop_dict, 'count', None)
        color = self.get_property_value(prop_dict, 'color', '#F44336')
        text_color = self.get_property_value(prop_dict, 'textColor', '#FFFFFF')
        visible = self.get_property_value(prop_dict, 'visibility', True)

        if not child_widgets:
            base = "Icon(Icons.notifications)"
        else:
            from ..widget_generator import WidgetGenerator
            widget_gen = WidgetGenerator()
            base = widget_gen.generate_widget(child_widgets[0], context, indent_level + 1)

        badge = f"""Positioned(
{indent}    right: 0,
{indent}    top: 0,
{indent}    child: Container(
{indent}      padding: EdgeInsets.symmetric(horizontal: 6, vertical: 2),
{indent}      decoration: BoxDecoration(
{indent}        color: {DartCodeUtils.generate_color_code(color)},
{indent}        borderRadius: BorderRadius.circular(10),
{indent}      ),
{indent}      constraints: BoxConstraints(minWidth: 18, minHeight: 18),
{indent}      child: Text(
{indent}        '{str(count) if count is not None else ''}',
{indent}        style: TextStyle(color: {DartCodeUtils.generate_color_code(text_color)}, fontSize: 12),
{indent}        textAlign: TextAlign.center,
{indent}      ),
{indent}    ),
{indent}  )"""

        if visible and str(visible).lower() != 'false':
            overlay = badge
        else:
            overlay = f"SizedBox.shrink()"

        return f"Stack(children: [{base}, {overlay}])"