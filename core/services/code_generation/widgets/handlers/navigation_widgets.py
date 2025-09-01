# File: core/services/code_generation/widgets/handlers/navigation_widgets.py
"""
Handlers for navigation Flutter widgets.
"""

from typing import Any, List

from ...base import BaseWidgetHandler, GeneratorContext
from ...utils import DartCodeUtils


class BottomNavigationHandler(BaseWidgetHandler):
    """Handler for BottomNavigationBar widget."""

    def can_handle(self, widget_type: str) -> bool:
        return widget_type == 'BottomNavigationBar'

    def generate(self, widget: Any, context: GeneratorContext, indent_level: int) -> str:
        indent = self.get_indent(indent_level)
        prop_dict = self.get_widget_properties(widget)
        child_widgets = self.get_child_widgets(widget)

        # Generate navigation items and actions from child widgets
        nav_items = []
        nav_actions = []

        for i, child in enumerate(child_widgets):
            # Get properties from child widget
            child_props = self.get_widget_properties(child)

            icon = self.get_property_value(child_props, 'icon', 'home')
            label = self.get_property_value(child_props, 'label', f'Item {i + 1}')
            label = DartCodeUtils.escape_dart_string(label)

            nav_items.append({'icon': icon, 'label': label})

            # Get navigation action if exists
            if 'onTap' in child_props:
                action_prop = child_props['onTap']
                if hasattr(action_prop, 'action_reference') and action_prop.action_reference:
                    action = action_prop.action_reference
                    if action.target_screen:
                        nav_actions.append(f"Navigator.pushNamed(context, '{action.target_screen.route_name}');")
                    else:
                        nav_actions.append("// No action configured")
                elif hasattr(action_prop, 'screen_reference') and action_prop.screen_reference:
                    nav_actions.append(f"Navigator.pushNamed(context, '{action_prop.screen_reference.route_name}');")
                else:
                    nav_actions.append("// No action configured")
            else:
                nav_actions.append("// No action configured")

        # Build the navigation bar
        current_index = self.get_property_value(prop_dict, 'currentIndex', '0')
        bg = self.get_property_value(prop_dict, 'backgroundColor', None)
        sel = self.get_property_value(prop_dict, 'selectedItemColor', None)
        unsel = self.get_property_value(prop_dict, 'unselectedItemColor', None)
        icon_size = self.get_property_value(prop_dict, 'iconSize', None)
        elevation = self.get_property_value(prop_dict, 'elevation', None)

        code = f'''BottomNavigationBar(
{indent}  type: BottomNavigationBarType.fixed,
{indent}  currentIndex: {current_index},'''

        if bg:
            code += f"\n{indent}  backgroundColor: {DartCodeUtils.generate_color_code(bg)},"
        if sel:
            code += f"\n{indent}  selectedItemColor: {DartCodeUtils.generate_color_code(sel)},"
        else:
            code += f"\n{indent}  selectedItemColor: Theme.of(context).primaryColor,"
        if unsel:
            code += f"\n{indent}  unselectedItemColor: {DartCodeUtils.generate_color_code(unsel)},"
        else:
            code += f"\n{indent}  unselectedItemColor: Colors.grey,"
        if icon_size:
            code += f"\n{indent}  iconSize: {icon_size},"
        if elevation:
            code += f"\n{indent}  elevation: {elevation},"

        code += f'''
{indent}  onTap: (index) {{
{indent}    switch (index) {{'''

        for i, action in enumerate(nav_actions):
            code += f'''
{indent}      case {i}:
{indent}        {action}
{indent}        break;'''

        code += f'''
{indent}    }}
{indent}  }},
{indent}  items: ['''

        for item in nav_items:
            code += f'''
{indent}    BottomNavigationBarItem(
{indent}      icon: Icon(Icons.{item['icon']}),
{indent}      label: '{item['label']}',
{indent}    ),'''

        code += f'''
{indent}  ],
{indent})'''

        return code


class AppBarHandler(BaseWidgetHandler):
    """Handler for AppBar widget."""

    def can_handle(self, widget_type: str) -> bool:
        return widget_type == 'AppBar'

    def generate(self, widget: Any, context: GeneratorContext, indent_level: int) -> str:
        indent = self.get_indent(indent_level)
        prop_dict = self.get_widget_properties(widget)

        title = self.get_property_value(prop_dict, 'title', 'App')
        title = DartCodeUtils.escape_dart_string(title)

        # Optional properties
        background_color = self.get_property_value(prop_dict, 'backgroundColor', None)
        foreground_color = self.get_property_value(prop_dict, 'foregroundColor', None)
        elevation = self.get_property_value(prop_dict, 'elevation', None)
        toolbar_height = self.get_property_value(prop_dict, 'toolbarHeight', None)
        icon_theme_color = (
            self.get_property_value(prop_dict, 'iconTheme.color', None)
            or self.get_property_value(prop_dict, 'iconColor', None)
        )

        params = [f"title: Text('{title}')"]
        if background_color:
            params.append(f"backgroundColor: {DartCodeUtils.generate_color_code(background_color)}")
        if foreground_color:
            params.append(f"foregroundColor: {DartCodeUtils.generate_color_code(foreground_color)}")
        if elevation:
            params.append(f"elevation: {elevation}")
        if toolbar_height:
            params.append(f"toolbarHeight: {toolbar_height}")
        if icon_theme_color:
            params.append(f"iconTheme: IconThemeData(color: {DartCodeUtils.generate_color_code(icon_theme_color)})")

        return 'AppBar(' + ', '.join(params) + ')'


class DrawerHandler(BaseWidgetHandler):
    """Handler for Drawer widget."""

    def can_handle(self, widget_type: str) -> bool:
        return widget_type == 'Drawer'

    def generate(self, widget: Any, context: GeneratorContext, indent_level: int) -> str:
        indent = self.get_indent(indent_level)
        prop_dict = self.get_widget_properties(widget)
        child_widgets = self.get_child_widgets(widget)

        width = self.get_property_value(prop_dict, 'width', None)
        bg = self.get_property_value(prop_dict, 'backgroundColor', None)

        code = f'''Drawer('''

        if width:
            code += f"\n{indent}  width: {width},"
        if bg:
            code += f"\n{indent}  backgroundColor: {DartCodeUtils.generate_color_code(bg)},"

        code += f"\n{indent}  child: "

        if child_widgets:
            from ..widget_generator import WidgetGenerator
            widget_gen = WidgetGenerator()

            if len(child_widgets) == 1:
                code += widget_gen.generate_widget(child_widgets[0], context, indent_level + 1)
            else:
                # Wrap multiple children in ListView
                code += f'''ListView(
{indent}    padding: EdgeInsets.zero,
{indent}    children: ['''

                for child in child_widgets:
                    code += f'''
{indent}      {widget_gen.generate_widget(child, context, indent_level + 3)},'''

                code += f'''
{indent}    ],
{indent}  )'''
        else:
            code += "Container()"

        code += f",\n{indent})"

        return code


class TabBarHandler(BaseWidgetHandler):
    """Handler for TabBar widget."""

    def can_handle(self, widget_type: str) -> bool:
        return widget_type == 'TabBar'

    def generate(self, widget: Any, context: GeneratorContext, indent_level: int) -> str:
        indent = self.get_indent(indent_level)
        prop_dict = self.get_widget_properties(widget)
        child_widgets = self.get_child_widgets(widget)

        # Generate tabs from child widgets or use defaults
        tabs = []

        if child_widgets:
            for child in child_widgets:
                child_props = self.get_widget_properties(child)
                text = self.get_property_value(child_props, 'text', 'Tab')
                text = DartCodeUtils.escape_dart_string(text)
                tabs.append(text)
        else:
            tabs = ['Tab 1', 'Tab 2']

        label_color = self.get_property_value(prop_dict, 'labelColor', None)
        unselected_label_color = self.get_property_value(prop_dict, 'unselectedLabelColor', None)
        indicator_color = self.get_property_value(prop_dict, 'indicatorColor', None)
        padding_val = self.get_property_value(prop_dict, 'padding', None)
        indicator_padding_val = self.get_property_value(prop_dict, 'indicatorPadding', None)

        code = f'''TabBar('''

        if label_color:
            code += f"\n{indent}  labelColor: {DartCodeUtils.generate_color_code(label_color)},"
        if unselected_label_color:
            code += f"\n{indent}  unselectedLabelColor: {DartCodeUtils.generate_color_code(unselected_label_color)},"
        if indicator_color:
            code += f"\n{indent}  indicatorColor: {DartCodeUtils.generate_color_code(indicator_color)},"
        if padding_val:
            code += f"\n{indent}  padding: EdgeInsets.all({padding_val}),"
        if indicator_padding_val:
            code += f"\n{indent}  indicatorPadding: EdgeInsets.all({indicator_padding_val}),"

        code += f"\n{indent}  tabs: ["""

        for tab_text in tabs:
            code += f'''
{indent}    Tab(text: '{tab_text}'),'''

        code += f'''
{indent}  ],
{indent})'''

        return code