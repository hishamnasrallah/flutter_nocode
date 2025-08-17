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
        code = f'''BottomNavigationBar(
{indent}  type: BottomNavigationBarType.fixed,
{indent}  currentIndex: 0,
{indent}  selectedItemColor: Theme.of(context).primaryColor,
{indent}  unselectedItemColor: Colors.grey,
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
        prop_dict = self.get_widget_properties(widget)

        title = self.get_property_value(prop_dict, 'title', 'App')
        title = DartCodeUtils.escape_dart_string(title)

        return f"AppBar(title: Text('{title}'))"


class DrawerHandler(BaseWidgetHandler):
    """Handler for Drawer widget."""

    def can_handle(self, widget_type: str) -> bool:
        return widget_type == 'Drawer'

    def generate(self, widget: Any, context: GeneratorContext, indent_level: int) -> str:
        indent = self.get_indent(indent_level)
        child_widgets = self.get_child_widgets(widget)

        code = f'''Drawer(
{indent}  child: '''

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

        code = f'''TabBar(
{indent}  tabs: ['''

        for tab_text in tabs:
            code += f'''
{indent}    Tab(text: '{tab_text}'),'''

        code += f'''
{indent}  ],
{indent})'''

        return code