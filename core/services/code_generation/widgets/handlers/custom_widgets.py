# File: core/services/code_generation/widgets/handlers/custom_widgets.py
"""
Handlers for custom and third-party widgets from pub.dev.
"""

from typing import Any, Dict, Optional

from ...base import BaseWidgetHandler, GeneratorContext
from ...utils import DartCodeUtils


class CustomPubDevWidgetHandler(BaseWidgetHandler):
    """
    Handler for custom widgets from pub.dev packages.
    Dynamically generates code based on widget configuration.
    """

    def __init__(self):
        # Map of known pub.dev packages and their widget patterns
        self.package_widgets = {
            'carousel_slider': CarouselSliderHandler(),
            'flutter_rating_bar': RatingBarHandler(),
            'shimmer': ShimmerHandler(),
            'cached_network_image': CachedNetworkImageHandler(),
            'lottie': LottieHandler(),
            'charts_flutter': ChartsHandler(),
            'qr_flutter': QRCodeHandler(),
            'flutter_spinkit': SpinKitHandler(),
            'flutter_svg': SvgHandler(),
            'video_player': VideoPlayerHandler(),
        }

    def can_handle(self, widget_type: str) -> bool:
        """Check if this is a custom widget we can handle."""
        # Check if it's a known custom widget type
        return widget_type.startswith('Custom_') or widget_type in self.package_widgets

    def generate(self, widget: Any, context: GeneratorContext, indent_level: int) -> str:
        """Generate code for custom widget."""
        # Extract package name from widget type if it's a custom widget
        if widget.widget_type.startswith('Custom_'):
            package_name = widget.widget_type.replace('Custom_', '').lower()

            # Check if we have a specific handler for this package
            if package_name in self.package_widgets:
                handler = self.package_widgets[package_name]
                return handler.generate(widget, context, indent_level)

        # Fallback to generic custom widget generation
        return self._generate_generic_custom(widget, context, indent_level)

    def _generate_generic_custom(self, widget: Any, context: GeneratorContext, indent_level: int) -> str:
        """Generate generic custom widget code."""
        indent = self.get_indent(indent_level)
        prop_dict = self.get_widget_properties(widget)
        child_widgets = self.get_child_widgets(widget)

        # Try to determine the widget class name
        widget_class = widget.widget_type
        if widget_class.startswith('Custom_'):
            widget_class = widget_class.replace('Custom_', '')

        # Build properties map
        props = []
        for prop_name, prop in prop_dict.items():
            value = prop.get_value()
            if value is not None and value != '':
                props.append(f"{prop_name}: {self._format_value(value)}")

        # Handle children/child mapping dynamically via property or heuristic
        if child_widgets:
            children_param = None
            # If user provided an explicit param name via a special property
            if 'childrenParam' in prop_dict:
                children_param = prop_dict['childrenParam'].get_value()
            # Heuristic: if more than one child, prefer 'children', else 'child'
            if not children_param:
                children_param = 'children' if len(child_widgets) > 1 else 'child'

            from ..widget_generator import WidgetGenerator
            widget_gen = WidgetGenerator()

            if children_param == 'children' or children_param == 'items':
                items = []
                for ch in child_widgets:
                    items.append(widget_gen.generate_widget(ch, context, indent_level + 2))
                list_str = ',\n' + indent + '  ' + (',\n' + indent + '  ').join(items) + '\n' + indent
                props.append(f"{children_param}: [{list_str}]")
            elif children_param == 'child':
                child_code = widget_gen.generate_widget(child_widgets[0], context, indent_level + 1)
                props.append(f"child: {child_code}")

        code = f"{widget_class}("
        if props:
            code += f"\n{indent}  {f',{chr(10)}{indent}  '.join(props)},\n{indent}"
        code += ")"

        return code

    def _format_value(self, value: Any) -> str:
        """Format a value for Dart code."""
        if isinstance(value, bool):
            return str(value).lower()
        elif isinstance(value, str):
            if value.startswith('Icons.'):
                return value
            elif value.startswith('Colors.'):
                return value
            else:
                return f"'{DartCodeUtils.escape_dart_string(value)}'"
        else:
            return str(value)


class CarouselSliderHandler(BaseWidgetHandler):
    """Handler for carousel_slider package widgets."""

    def can_handle(self, widget_type: str) -> bool:
        return 'carousel' in widget_type.lower()

    def generate(self, widget: Any, context: GeneratorContext, indent_level: int) -> str:
        indent = self.get_indent(indent_level)
        prop_dict = self.get_widget_properties(widget)
        child_widgets = self.get_child_widgets(widget)

        # Get carousel properties
        auto_play = self.get_property_value(prop_dict, 'autoPlay', True)
        height = self.get_property_value(prop_dict, 'height', 200)
        enlarge = self.get_property_value(prop_dict, 'enlargeCenterPage', True)

        # Build items from children if present; else leave placeholder
        items_code = ''
        if child_widgets:
            from ..widget_generator import WidgetGenerator
            widget_gen = WidgetGenerator()
            items = []
            for ch in child_widgets:
                items.append(widget_gen.generate_widget(ch, context, indent_level + 2))
            items_code = f"\n{indent}  items: [\n" + f"{indent}    " + f",\n{indent}    ".join(items) + f"\n{indent}  ],"
        else:
            items_code = f"\n{indent}  items: [\n{indent}    // TODO: Add slides here\n{indent}  ],"

        code = f'''CarouselSlider(
{indent}  options: CarouselOptions(
{indent}    height: {height},
{indent}    autoPlay: {str(auto_play).lower()},
{indent}    enlargeCenterPage: {str(enlarge).lower()},
{indent}    autoPlayInterval: Duration(seconds: 3),
{indent}    autoPlayAnimationDuration: Duration(milliseconds: 800),
{indent}  ),{items_code}
{indent})'''

        return code


class RatingBarHandler(BaseWidgetHandler):
    """Handler for flutter_rating_bar package widgets."""

    def can_handle(self, widget_type: str) -> bool:
        return 'rating' in widget_type.lower()

    def generate(self, widget: Any, context: GeneratorContext, indent_level: int) -> str:
        indent = self.get_indent(indent_level)
        prop_dict = self.get_widget_properties(widget)

        initial_rating = self.get_property_value(prop_dict, 'initialRating', 3.0)
        min_rating = self.get_property_value(prop_dict, 'minRating', 1)
        allow_half = self.get_property_value(prop_dict, 'allowHalfRating', True)
        item_count = self.get_property_value(prop_dict, 'itemCount', 5)

        code = f'''RatingBar.builder(
{indent}  initialRating: {initial_rating},
{indent}  minRating: {min_rating},
{indent}  allowHalfRating: {str(allow_half).lower()},
{indent}  itemCount: {item_count},
{indent}  itemBuilder: (context, _) => Icon(
{indent}    Icons.star,
{indent}    color: Colors.amber,
{indent}  ),
{indent}  onRatingUpdate: (rating) {{
{indent}    // Handle rating update
{indent}  }},
{indent})'''

        return code


class ShimmerHandler(BaseWidgetHandler):
    """Handler for shimmer package widgets."""

    def can_handle(self, widget_type: str) -> bool:
        return 'shimmer' in widget_type.lower()

    def generate(self, widget: Any, context: GeneratorContext, indent_level: int) -> str:
        indent = self.get_indent(indent_level)
        prop_dict = self.get_widget_properties(widget)
        child_widgets = self.get_child_widgets(widget)

        base_color = self.get_property_value(prop_dict, 'baseColor', 'Colors.grey[300]')
        highlight_color = self.get_property_value(prop_dict, 'highlightColor', 'Colors.grey[100]')

        code = f'''Shimmer.fromColors(
{indent}  baseColor: {base_color}!,
{indent}  highlightColor: {highlight_color}!,
{indent}  child: '''

        if child_widgets:
            from ..widget_generator import WidgetGenerator
            widget_gen = WidgetGenerator()
            code += widget_gen.generate_widget(child_widgets[0], context, indent_level + 1)
        else:
            code += f'''Container(
{indent}    width: double.infinity,
{indent}    height: 100,
{indent}    color: Colors.white,
{indent}  )'''

        code += f",\n{indent})"

        return code


class CachedNetworkImageHandler(BaseWidgetHandler):
    """Handler for cached_network_image package widgets."""

    def can_handle(self, widget_type: str) -> bool:
        return 'cachednetworkimage' in widget_type.lower().replace('_', '')

    def generate(self, widget: Any, context: GeneratorContext, indent_level: int) -> str:
        indent = self.get_indent(indent_level)
        prop_dict = self.get_widget_properties(widget)

        image_url = self.get_property_value(prop_dict, 'imageUrl', '')

        code = f'''CachedNetworkImage(
{indent}  imageUrl: '{image_url}',
{indent}  placeholder: (context, url) => CircularProgressIndicator(),
{indent}  errorWidget: (context, url, error) => Icon(Icons.error),
{indent}  fit: BoxFit.cover,
{indent})'''

        return code


class LottieHandler(BaseWidgetHandler):
    """Handler for lottie package widgets."""

    def can_handle(self, widget_type: str) -> bool:
        return 'lottie' in widget_type.lower()

    def generate(self, widget: Any, context: GeneratorContext, indent_level: int) -> str:
        indent = self.get_indent(indent_level)
        prop_dict = self.get_widget_properties(widget)

        asset_path = self.get_property_value(prop_dict, 'asset', 'assets/animations/loading.json')
        repeat = self.get_property_value(prop_dict, 'repeat', True)
        animate = self.get_property_value(prop_dict, 'animate', True)

        code = f'''Lottie.asset(
{indent}  '{asset_path}',
{indent}  repeat: {str(repeat).lower()},
{indent}  animate: {str(animate).lower()},
{indent})'''

        return code


class ChartsHandler(BaseWidgetHandler):
    """Handler for charts_flutter package widgets."""

    def can_handle(self, widget_type: str) -> bool:
        return 'chart' in widget_type.lower()

    def generate(self, widget: Any, context: GeneratorContext, indent_level: int) -> str:
        indent = self.get_indent(indent_level)
        prop_dict = self.get_widget_properties(widget)

        chart_type = self.get_property_value(prop_dict, 'chartType', 'bar')
        animate = self.get_property_value(prop_dict, 'animate', True)

        if chart_type == 'bar':
            return self._generate_bar_chart(indent, animate)
        elif chart_type == 'line':
            return self._generate_line_chart(indent, animate)
        elif chart_type == 'pie':
            return self._generate_pie_chart(indent, animate)
        else:
            return "Container(child: Text('Unsupported chart type'))"

    def _generate_bar_chart(self, indent: str, animate: bool) -> str:
        return f'''charts.BarChart(
{indent}  _createSampleData(),
{indent}  animate: {str(animate).lower()},
{indent})'''

    def _generate_line_chart(self, indent: str, animate: bool) -> str:
        return f'''charts.LineChart(
{indent}  _createSampleData(),
{indent}  animate: {str(animate).lower()},
{indent})'''

    def _generate_pie_chart(self, indent: str, animate: bool) -> str:
        return f'''charts.PieChart(
{indent}  _createSampleData(),
{indent}  animate: {str(animate).lower()},
{indent})'''


class QRCodeHandler(BaseWidgetHandler):
    """Handler for qr_flutter package widgets."""

    def can_handle(self, widget_type: str) -> bool:
        return 'qr' in widget_type.lower()

    def generate(self, widget: Any, context: GeneratorContext, indent_level: int) -> str:
        indent = self.get_indent(indent_level)
        prop_dict = self.get_widget_properties(widget)

        data = self.get_property_value(prop_dict, 'data', 'https://example.com')
        size = self.get_property_value(prop_dict, 'size', 200)

        code = f'''QrImage(
{indent}  data: '{data}',
{indent}  version: QrVersions.auto,
{indent}  size: {size},
{indent})'''

        return code


class SpinKitHandler(BaseWidgetHandler):
    """Handler for flutter_spinkit package widgets."""

    def can_handle(self, widget_type: str) -> bool:
        return 'spinkit' in widget_type.lower()

    def generate(self, widget: Any, context: GeneratorContext, indent_level: int) -> str:
        indent = self.get_indent(indent_level)
        prop_dict = self.get_widget_properties(widget)

        spinner_type = self.get_property_value(prop_dict, 'type', 'FadingCircle')
        color = self.get_property_value(prop_dict, 'color', 'Theme.of(context).primaryColor')
        size = self.get_property_value(prop_dict, 'size', 50.0)

        code = f'''SpinKit{spinner_type}(
{indent}  color: {color},
{indent}  size: {size},
{indent})'''

        return code


class SvgHandler(BaseWidgetHandler):
    """Handler for flutter_svg package widgets."""

    def can_handle(self, widget_type: str) -> bool:
        return 'svg' in widget_type.lower()

    def generate(self, widget: Any, context: GeneratorContext, indent_level: int) -> str:
        indent = self.get_indent(indent_level)
        prop_dict = self.get_widget_properties(widget)

        asset_path = self.get_property_value(prop_dict, 'asset', '')
        width = self.get_property_value(prop_dict, 'width', None)
        height = self.get_property_value(prop_dict, 'height', None)

        code = f"SvgPicture.asset(\n{indent}  '{asset_path}'"

        if width:
            code += f",\n{indent}  width: {width}"
        if height:
            code += f",\n{indent}  height: {height}"

        code += f",\n{indent})"

        return code


class VideoPlayerHandler(BaseWidgetHandler):
    """Handler for video_player package widgets."""

    def can_handle(self, widget_type: str) -> bool:
        return 'video' in widget_type.lower()

    def generate(self, widget: Any, context: GeneratorContext, indent_level: int) -> str:
        indent = self.get_indent(indent_level)
        prop_dict = self.get_widget_properties(widget)

        aspect_ratio = self.get_property_value(prop_dict, 'aspectRatio', '16 / 9')

        code = f'''AspectRatio(
{indent}  aspectRatio: {aspect_ratio},
{indent}  child: VideoPlayer(_controller),
{indent})'''

        return code