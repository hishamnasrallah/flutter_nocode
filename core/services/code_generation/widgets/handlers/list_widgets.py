# File: core/services/code_generation/widgets/handlers/list_widgets.py
"""
Handlers for list and scrollable Flutter widgets.
"""

from typing import Any

from ...base import BaseWidgetHandler, GeneratorContext
from ...utils import DartCodeUtils


class ListViewHandler(BaseWidgetHandler):
    """Handler for ListView widget."""

    def can_handle(self, widget_type: str) -> bool:
        return widget_type == 'ListView'

    def generate(self, widget: Any, context: GeneratorContext, indent_level: int) -> str:
        indent = self.get_indent(indent_level)
        prop_dict = self.get_widget_properties(widget)
        child_widgets = self.get_child_widgets(widget)

        # Check for data source
        data_source_prop = prop_dict.get('dataSource')

        # Check scroll direction
        scroll_direction = self.get_property_value(prop_dict, 'scrollDirection', 'vertical')
        is_horizontal = scroll_direction == 'horizontal'

        # Check if nested in SingleChildScrollView
        physics = self._determine_physics(widget, is_horizontal)

        if data_source_prop and hasattr(data_source_prop, 'data_source_field_reference'):
            if data_source_prop.data_source_field_reference:
                return self._generate_dynamic_list(
                    widget, data_source_prop.data_source_field_reference,
                    scroll_direction, physics, context, indent_level
                )

        # Static ListView
        return self._generate_static_list(child_widgets, scroll_direction, physics, context, indent_level)

    def _determine_physics(self, widget: Any, is_horizontal: bool) -> str:
        """Determine appropriate scroll physics."""
        if is_horizontal:
            return 'AlwaysScrollableScrollPhysics()'

        # Check if nested in SingleChildScrollView
        parent = widget.parent_widget
        while parent:
            if parent.widget_type == 'SingleChildScrollView':
                return 'NeverScrollableScrollPhysics()'
            parent = parent.parent_widget

        return 'AlwaysScrollableScrollPhysics()'

    def _generate_dynamic_list(self, widget: Any, field_ref: Any, scroll_direction: str,
                               physics: str, context: GeneratorContext, indent_level: int) -> str:
        """Generate dynamic ListView with data source."""
        indent = self.get_indent(indent_level)
        prop_dict = self.get_widget_properties(widget)

        data_source = field_ref.data_source
        field = field_ref

        height = self.get_property_value(prop_dict, 'height', None)
        is_horizontal = scroll_direction == 'horizontal'

        # Wrap in container if horizontal
        height_wrapper_start = ""
        height_wrapper_end = ""
        if is_horizontal:
            list_height = height if height else '250'
            height_wrapper_start = f"Container(height: {list_height}, child: "
            height_wrapper_end = ")"

        return f'''{height_wrapper_start}FutureBuilder<List<dynamic>>(
{indent}  future: _apiService.fetchData('{data_source.name}'),
{indent}  builder: (context, snapshot) {{
{indent}    if (snapshot.connectionState == ConnectionState.waiting) {{
{indent}      return Center(child: CircularProgressIndicator());
{indent}    }}
{indent}    if (snapshot.hasError) {{
{indent}      return Center(child: Text('Error loading data'));
{indent}    }}
{indent}    final items = snapshot.data ?? [];
{indent}    if (items.isEmpty) {{
{indent}      return Center(child: Text('No items available'));
{indent}    }}
{indent}    return ListView.builder(
{indent}      scrollDirection: Axis.{scroll_direction},
{indent}      shrinkWrap: {str(not is_horizontal).lower()},
{indent}      physics: {physics},
{indent}      primary: false,
{indent}      itemCount: items.length,
{indent}      itemBuilder: (context, index) {{
{indent}        final item = items[index];
{indent}        return {self._generate_list_item(data_source.name, field.field_name, is_horizontal, indent_level + 3)};
{indent}      }},
{indent}    );
{indent}  }},
{indent}){height_wrapper_end}'''

    def _generate_static_list(self, child_widgets: list, scroll_direction: str, physics: str,
                              context: GeneratorContext, indent_level: int) -> str:
        """Generate static ListView."""
        indent = self.get_indent(indent_level)
        is_horizontal = scroll_direction == 'horizontal'

        from ..widget_generator import WidgetGenerator
        widget_gen = WidgetGenerator()

        code = f'''ListView(
{indent}  scrollDirection: Axis.{scroll_direction},
{indent}  shrinkWrap: {str(not is_horizontal).lower()},
{indent}  physics: {physics},
{indent}  primary: false,
{indent}  children: [
'''

        for child in child_widgets:
            code += f"{indent}    {widget_gen.generate_widget(child, context, indent_level + 2)},\n"

        code += f"{indent}  ],\n{indent})"

        return code

    def _generate_list_item(self, data_source_name: str, field_name: str,
                            is_horizontal: bool, indent_level: int) -> str:
        """Generate list item widget."""
        indent = self.get_indent(indent_level)

        width_style = "width: 150," if is_horizontal else ""

        return f'''Container(
{indent}  {width_style}
{indent}  margin: EdgeInsets.symmetric(horizontal: 4, vertical: 4),
{indent}  child: Card(
{indent}    elevation: 2,
{indent}    child: InkWell(
{indent}      onTap: () {{
{indent}        if (item['id'] != null) {{
{indent}          Navigator.pushNamed(context, '/detail/${{item['id']}}');
{indent}        }}
{indent}      }},
{indent}      child: Padding(
{indent}        padding: EdgeInsets.all(8),
{indent}        child: Column(
{indent}          crossAxisAlignment: CrossAxisAlignment.start,
{indent}          children: [
{indent}            if (item['image'] != null)
{indent}              Container(
{indent}                height: 120,
{indent}                width: double.infinity,
{indent}                child: Image.network(
{indent}                  item['image'],
{indent}                  fit: BoxFit.cover,
{indent}                  errorBuilder: (c,e,s) => Icon(Icons.image),
{indent}                ),
{indent}              ),
{indent}            Text(
{indent}              item['{field_name}']?.toString() ?? '',
{indent}              style: TextStyle(fontWeight: FontWeight.bold),
{indent}            ),
{indent}          ],
{indent}        ),
{indent}      ),
{indent}    ),
{indent}  ),
{indent})'''


class GridViewHandler(BaseWidgetHandler):
    """Handler for GridView widget."""

    def can_handle(self, widget_type: str) -> bool:
        return widget_type == 'GridView'

    def generate(self, widget: Any, context: GeneratorContext, indent_level: int) -> str:
        indent = self.get_indent(indent_level)
        prop_dict = self.get_widget_properties(widget)

        # Get grid properties
        columns = self.get_property_value(prop_dict, 'crossAxisCount', '2')
        scroll_direction = self.get_property_value(prop_dict, 'scrollDirection', 'vertical')
        height = self.get_property_value(prop_dict, 'height', None)
        item_limit = self.get_property_value(prop_dict, 'itemLimit', None)
        aspect_ratio = self.get_property_value(prop_dict, 'childAspectRatio', '1.0')

        # Check if nested
        physics = self._determine_physics(widget)
        is_nested = 'Never' in physics

        # Check for data source
        data_source_prop = prop_dict.get('dataSource')

        if data_source_prop and hasattr(data_source_prop, 'data_source_field_reference'):
            if data_source_prop.data_source_field_reference:
                return self._generate_dynamic_grid(
                    data_source_prop.data_source_field_reference,
                    columns, scroll_direction, height, item_limit, aspect_ratio,
                    physics, is_nested, context, indent_level
                )

        # Static GridView
        return self._generate_static_grid(
            columns, scroll_direction, aspect_ratio, physics, is_nested, indent_level
        )

    def _determine_physics(self, widget: Any) -> str:
        """Determine appropriate scroll physics for GridView."""
        parent = widget.parent_widget
        while parent:
            if parent.widget_type == 'SingleChildScrollView':
                return 'NeverScrollableScrollPhysics()'
            parent = parent.parent_widget
        return 'AlwaysScrollableScrollPhysics()'

    def _generate_dynamic_grid(self, field_ref: Any, columns: str, scroll_direction: str,
                               height: str, item_limit: str, aspect_ratio: str, physics: str,
                               is_nested: bool, context: GeneratorContext, indent_level: int) -> str:
        """Generate dynamic GridView with data source."""
        indent = self.get_indent(indent_level)

        data_source = field_ref.data_source
        field = field_ref

        # Container wrapper if height specified
        container_start = ""
        container_end = ""
        if height:
            container_start = f"Container(height: {height}, child: "
            container_end = ")"

        item_count = f"data.length" if not item_limit else f"data.length > {item_limit} ? {item_limit} : data.length"

        return f'''{container_start}FutureBuilder<List<dynamic>>(
{indent}  future: _apiService.fetchData('{data_source.name}'),
{indent}  builder: (context, snapshot) {{
{indent}    if (snapshot.connectionState == ConnectionState.waiting) {{
{indent}      return Center(child: CircularProgressIndicator());
{indent}    }}
{indent}    if (snapshot.hasError) {{
{indent}      return Center(child: Text('Error loading data'));
{indent}    }}
{indent}    final data = snapshot.data ?? [];
{indent}    if (data.isEmpty) {{
{indent}      return Center(child: Text('No items'));
{indent}    }}
{indent}    return GridView.builder(
{indent}      scrollDirection: Axis.{scroll_direction},
{indent}      shrinkWrap: {str(is_nested).lower()},
{indent}      physics: {physics},
{indent}      gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
{indent}        crossAxisCount: {columns},
{indent}        crossAxisSpacing: 8,
{indent}        mainAxisSpacing: 8,
{indent}        childAspectRatio: {aspect_ratio},
{indent}      ),
{indent}      itemCount: {item_count},
{indent}      itemBuilder: (context, index) {{
{indent}        final item = data[index];
{indent}        return {self._generate_grid_item(field, indent_level + 3)};
{indent}      }},
{indent}    );
{indent}  }},
{indent}){container_end}'''

    def _generate_static_grid(self, columns: str, scroll_direction: str, aspect_ratio: str,
                              physics: str, is_nested: bool, indent_level: int) -> str:
        """Generate static GridView."""
        indent = self.get_indent(indent_level)

        return f'''GridView.count(
{indent}  crossAxisCount: {columns},
{indent}  shrinkWrap: {str(is_nested).lower()},
{indent}  physics: {physics},
{indent}  childAspectRatio: {aspect_ratio},
{indent}  children: [],
{indent})'''

    def _generate_grid_item(self, field: Any, indent_level: int) -> str:
        """Generate grid item widget."""
        indent = self.get_indent(indent_level)

        if field.field_type == 'image_url':
            return f'''Card(
{indent}  child: Image.network(
{indent}    item['{field.field_name}'] ?? '',
{indent}    fit: BoxFit.cover,
{indent}    errorBuilder: (c,e,s) => Icon(Icons.image),
{indent}  ),
{indent})'''
        else:
            return f'''Card(
{indent}  child: Center(
{indent}    child: Padding(
{indent}      padding: EdgeInsets.all(8),
{indent}      child: Text(
{indent}        item['{field.field_name}']?.toString() ?? '',
{indent}        textAlign: TextAlign.center,
{indent}      ),
{indent}    ),
{indent}  ),
{indent})'''


class ListTileHandler(BaseWidgetHandler):
    """Handler for ListTile widget."""

    def can_handle(self, widget_type: str) -> bool:
        return widget_type == 'ListTile'

    def generate(self, widget: Any, context: GeneratorContext, indent_level: int) -> str:
        indent = self.get_indent(indent_level)
        prop_dict = self.get_widget_properties(widget)

        title = DartCodeUtils.escape_dart_string(self.get_property_value(prop_dict, 'title', 'Title'))
        subtitle = self.get_property_value(prop_dict, 'subtitle', '')

        code = f'''ListTile(
{indent}  title: Text('{title}'),'''

        if subtitle:
            subtitle = DartCodeUtils.escape_dart_string(subtitle)
            code += f"\n{indent}  subtitle: Text('{subtitle}'),"

        if 'leading' in prop_dict:
            icon = self.get_property_value(prop_dict, 'leading', 'info')
            code += f"\n{indent}  leading: Icon(Icons.{icon}),"

        if 'trailing' in prop_dict:
            icon = self.get_property_value(prop_dict, 'trailing', 'arrow_forward')
            code += f"\n{indent}  trailing: Icon(Icons.{icon}),"

        if 'onTap' in prop_dict:
            action_code = self._generate_action_code(prop_dict.get('onTap'))
            code += f"\n{indent}  onTap: {action_code},"

        code += f"\n{indent})"

        return code

    def _generate_action_code(self, prop: Any) -> str:
        """Generate action code from property."""
        if not prop:
            return 'null'

        if hasattr(prop, 'action_reference') and prop.action_reference:
            action = prop.action_reference
            if action.action_type == 'navigate' and action.target_screen:
                return f"() {{ Navigator.pushNamed(context, '{action.target_screen.route_name}'); }}"

        if hasattr(prop, 'screen_reference') and prop.screen_reference:
            return f"() {{ Navigator.pushNamed(context, '{prop.screen_reference.route_name}'); }}"

        return 'null'


class SingleChildScrollViewHandler(BaseWidgetHandler):
    """Handler for SingleChildScrollView widget."""

    def can_handle(self, widget_type: str) -> bool:
        return widget_type == 'SingleChildScrollView'

    def generate(self, widget: Any, context: GeneratorContext, indent_level: int) -> str:
        indent = self.get_indent(indent_level)
        prop_dict = self.get_widget_properties(widget)
        child_widgets = self.get_child_widgets(widget)

        scroll_direction = self.get_property_value(prop_dict, 'scrollDirection', 'vertical')
        physics = self.get_property_value(prop_dict, 'physics', 'AlwaysScrollableScrollPhysics')

        code = f'''SingleChildScrollView(
{indent}  scrollDirection: Axis.{scroll_direction},
{indent}  physics: {physics}(),
{indent}  child: '''

        if child_widgets:
            from ..widget_generator import WidgetGenerator
            widget_gen = WidgetGenerator()

            if len(child_widgets) == 1:
                code += widget_gen.generate_widget(child_widgets[0], context, indent_level + 1)
            else:
                code += f'''Column(
{indent}    mainAxisSize: MainAxisSize.min,
{indent}    children: [
'''
                for child in child_widgets:
                    code += f"{indent}      {widget_gen.generate_widget(child, context, indent_level + 3)},\n"
                code += f"{indent}    ],\n{indent}  )"
        else:
            code += "Container()"

        code += f",\n{indent})"

        return code