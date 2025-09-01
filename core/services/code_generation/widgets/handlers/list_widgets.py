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

        # Static ListView with optional padding
        padding_val = self.get_property_value(prop_dict, 'padding', None)
        list_code = self._generate_static_list(child_widgets, scroll_direction, physics, context, indent_level)
        if padding_val:
            list_code = list_code.replace("children: [", f"padding: EdgeInsets.all({padding_val}),\n{indent}  children: [")
        return list_code

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
            from ...utils import StringUtils

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

            return f'''{height_wrapper_start}FutureBuilder<dynamic>(
    {indent}  future: _apiService.fetch{StringUtils.to_pascal_case(data_source.name)}(),
    {indent}  builder: (context, snapshot) {{
    {indent}    if (snapshot.connectionState == ConnectionState.waiting) {{
    {indent}      return Center(child: CircularProgressIndicator());
    {indent}    }}
    {indent}    if (snapshot.hasError) {{
    {indent}      return Center(child: Text('Error loading data'));
    {indent}    }}
    {indent}    
    {indent}    final rawData = snapshot.data;
    {indent}    List<dynamic> items = [];
    {indent}    
    {indent}    // Handle different response formats dynamically
    {indent}    if (rawData is List) {{
    {indent}      items = rawData;
    {indent}    }} else if (rawData is Map) {{
    {indent}      // Check for common data keys
    {indent}      final possibleKeys = ['data', 'items', 'results', 'content', 'list'];
    {indent}      for (String key in possibleKeys) {{
    {indent}        if (rawData.containsKey(key) && rawData[key] is List) {{
    {indent}          items = rawData[key];
    {indent}          break;
    {indent}        }}
    {indent}      }}
    {indent}      // If no list found, check all values for first list
    {indent}      if (items.isEmpty) {{
    {indent}        for (var value in rawData.values) {{
    {indent}          if (value is List) {{
    {indent}            items = value;
    {indent}            break;
    {indent}          }}
    {indent}        }}
    {indent}      }}
    {indent}      // If still no list, treat the map as a single item
    {indent}      if (items.isEmpty) {{
    {indent}        items = [rawData];
    {indent}      }}
    {indent}    }}
    {indent}    
    {indent}    if (items.isEmpty) {{
    {indent}      return Center(child: Text('No items available'));
    {indent}    }}
    {indent}    
    {indent}    return ListView.builder(
    {indent}      scrollDirection: Axis.{scroll_direction},
    {indent}      shrinkWrap: {str(not is_horizontal).lower()},
    {indent}      physics: {physics},
    {indent}      primary: false,
    {indent}      itemCount: items.length,
    {indent}      itemBuilder: (context, index) {{
    {indent}        final item = items[index];
    {indent}        return {self._generate_dynamic_list_item(field.field_name, is_horizontal, indent_level + 3)};
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

    def _generate_dynamic_list_item(self, primary_field: str, is_horizontal: bool, indent_level: int) -> str:
        """Generate list item widget that works with any data structure."""
        indent = self.get_indent(indent_level)

        width_style = "width: 150," if is_horizontal else ""

        return f'''Container(
{indent}  {width_style}
{indent}  margin: EdgeInsets.symmetric(horizontal: 4, vertical: 4),
{indent}  child: Card(
{indent}    elevation: 2,
{indent}    child: InkWell(
{indent}      onTap: () {{
{indent}        // Navigation if ID exists
{indent}        if (item is Map && item.containsKey('id')) {{
{indent}          // Navigate with item data
{indent}        }}
{indent}      }},
{indent}      child: Padding(
{indent}        padding: EdgeInsets.all(8),
{indent}        child: item is Map ? Column(
{indent}          crossAxisAlignment: CrossAxisAlignment.start,
{indent}          children: [
{indent}            // Display image if exists
{indent}            if (item.containsKey('image') || item.containsKey('imageUrl') || item.containsKey('avatar'))
{indent}              Container(
{indent}                height: 120,
{indent}                width: double.infinity,
{indent}                child: Image.network(
{indent}                  item['image'] ?? item['imageUrl'] ?? item['avatar'] ?? '',
{indent}                  fit: BoxFit.cover,
{indent}                  errorBuilder: (c,e,s) => Icon(Icons.image),
{indent}                ),
{indent}              ),
{indent}            // Display primary field
{indent}            if (item.containsKey('{primary_field}'))
{indent}              Text(
{indent}                item['{primary_field}']?.toString() ?? '',
{indent}                style: TextStyle(fontWeight: FontWeight.bold),
{indent}                maxLines: 2,
{indent}                overflow: TextOverflow.ellipsis,
{indent}              ),
{indent}            // Try common field names if primary field doesn't exist
{indent}            if (!item.containsKey('{primary_field}'))
{indent}              Text(
{indent}                item['name'] ?? item['title'] ?? item['label'] ?? item.values.first?.toString() ?? '',
{indent}                style: TextStyle(fontWeight: FontWeight.bold),
{indent}                maxLines: 2,
{indent}                overflow: TextOverflow.ellipsis,
{indent}              ),
{indent}            // Display secondary info if exists
{indent}            if (item.containsKey('description') || item.containsKey('subtitle'))
{indent}              Text(
{indent}                item['description'] ?? item['subtitle'] ?? '',
{indent}                style: TextStyle(fontSize: 12, color: Colors.grey),
{indent}                maxLines: 2,
{indent}                overflow: TextOverflow.ellipsis,
{indent}              ),
{indent}          ],
{indent}        ) : Text(item?.toString() ?? ''),
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
        padding_val = self.get_property_value(prop_dict, 'padding', None)

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
        grid_code = self._generate_static_grid(
            columns, scroll_direction, aspect_ratio, physics, is_nested, indent_level
        )
        if padding_val:
            grid_code = grid_code.replace("children: [],", f"padding: EdgeInsets.all({padding_val}),\n{indent}  children: [],")
        return grid_code

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
        from ...utils import StringUtils

        data_source = field_ref.data_source
        field = field_ref

        # Container wrapper if height specified
        container_start = ""
        container_end = ""
        if height:
            container_start = f"Container(height: {height}, child: "
            container_end = ")"

        item_count_calc = f"items.length" if not item_limit else f"items.length > {item_limit} ? {item_limit} : items.length"

        return f'''{container_start}FutureBuilder<dynamic>(
{indent}  future: _apiService.fetch{StringUtils.to_pascal_case(data_source.name)}(),
{indent}  builder: (context, snapshot) {{
{indent}    if (snapshot.connectionState == ConnectionState.waiting) {{
{indent}      return Center(child: CircularProgressIndicator());
{indent}    }}
{indent}    if (snapshot.hasError) {{
{indent}      return Center(child: Text('Error loading data'));
{indent}    }}
{indent}    
{indent}    final rawData = snapshot.data;
{indent}    List<dynamic> items = [];
{indent}    
{indent}    // Handle different response formats dynamically
{indent}    if (rawData is List) {{
{indent}      items = rawData;
{indent}    }} else if (rawData is Map) {{
{indent}      // Check for common data keys
{indent}      final possibleKeys = ['data', 'items', 'results', 'content', 'list'];
{indent}      for (String key in possibleKeys) {{
{indent}        if (rawData.containsKey(key) && rawData[key] is List) {{
{indent}          items = rawData[key];
{indent}          break;
{indent}        }}
{indent}      }}
{indent}      // If no list found, check all values for first list
{indent}      if (items.isEmpty) {{
{indent}        for (var value in rawData.values) {{
{indent}          if (value is List) {{
{indent}            items = value;
{indent}            break;
{indent}          }}
{indent}        }}
{indent}      }}
{indent}      // If still no list, treat the map as a single item
{indent}      if (items.isEmpty) {{
{indent}        items = [rawData];
{indent}      }}
{indent}    }}
{indent}    
{indent}    if (items.isEmpty) {{
{indent}      return Center(child: Text('No items'));
{indent}    }}
{indent}    
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
{indent}      itemCount: {item_count_calc},
{indent}      itemBuilder: (context, index) {{
{indent}        final item = items[index];
{indent}        return {self._generate_dynamic_grid_item(field, indent_level + 3)};
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

    def _generate_dynamic_grid_item(self, field: Any, indent_level: int) -> str:
        """Generate grid item widget that works with any data structure."""
        indent = self.get_indent(indent_level)

        return f'''Card(
{indent}  child: InkWell(
{indent}    onTap: () {{
{indent}      // Handle tap if needed
{indent}    }},
{indent}    child: item is Map ? Column(
{indent}      mainAxisAlignment: MainAxisAlignment.center,
{indent}      children: [
{indent}        // Display image if exists
{indent}        if (item.containsKey('image') || item.containsKey('imageUrl') || item.containsKey('icon'))
{indent}          Expanded(
{indent}            child: item.containsKey('icon') 
{indent}              ? Icon(Icons.image, size: 40)
{indent}              : Image.network(
{indent}                  item['image'] ?? item['imageUrl'] ?? '',
{indent}                  fit: BoxFit.cover,
{indent}                  errorBuilder: (c,e,s) => Icon(Icons.image),
{indent}                ),
{indent}          ),
{indent}        // Display text
{indent}        Padding(
{indent}          padding: EdgeInsets.all(8),
{indent}          child: Text(
{indent}            item['{field.field_name}'] ?? 
{indent}            item['name'] ?? 
{indent}            item['title'] ?? 
{indent}            item['label'] ?? 
{indent}            item.values.first?.toString() ?? '',
{indent}            textAlign: TextAlign.center,
{indent}            maxLines: 2,
{indent}            overflow: TextOverflow.ellipsis,
{indent}          ),
{indent}        ),
{indent}      ],
{indent}    ) : Center(
{indent}      child: Text(
{indent}        item?.toString() ?? '',
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

        # Optional styling
        if 'contentPadding' in prop_dict:
            padding = self.get_property_value(prop_dict, 'contentPadding', None)
            if padding:
                code += f"\n{indent}  contentPadding: EdgeInsets.all({padding}),"
        if 'tileColor' in prop_dict:
            tile_color = self.get_property_value(prop_dict, 'tileColor', None)
            if tile_color:
                code += f"\n{indent}  tileColor: {DartCodeUtils.generate_color_code(tile_color)},"

        if 'onTap' in prop_dict:
            action_code = self._generate_action_code(prop_dict.get('onTap'))
            code += f"\n{indent}  onTap: {action_code},"

        if 'onLongPress' in prop_dict:
            action_code = self._generate_action_code(prop_dict.get('onLongPress'))
            code += f"\n{indent}  onLongPress: {action_code},"

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
        padding_val = self.get_property_value(prop_dict, 'padding', None)

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
                inner = f'''Column(
{indent}    mainAxisSize: MainAxisSize.min,
{indent}    children: [
'''
                for child in child_widgets:
                    inner += f"{indent}      {widget_gen.generate_widget(child, context, indent_level + 3)},\n"
                inner += f"{indent}    ],\n{indent}  )"
                if padding_val:
                    code += f"Padding(\n{indent}    padding: EdgeInsets.all({padding_val}),\n{indent}    child: {inner}\n{indent}  )"
                else:
                    code += inner
        else:
            content = "Container()"
            if padding_val:
                code += f"Padding(\n{indent}    padding: EdgeInsets.all({padding_val}),\n{indent}    child: {content}\n{indent}  )"
            else:
                code += content

        code += f",\n{indent})"

        return code