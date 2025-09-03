# File: core/services/code_generation/widgets/handlers/input_widgets.py
"""
Handlers for input Flutter widgets.
"""

from typing import Any

from ...base import BaseWidgetHandler, GeneratorContext
from ...utils import DartCodeUtils


class TextFieldHandler(BaseWidgetHandler):
    """Handler for TextField widget."""

    def can_handle(self, widget_type: str) -> bool:
        return widget_type == 'TextField'

    def generate(self, widget: Any, context: GeneratorContext, indent_level: int) -> str:
        indent = self.get_indent(indent_level)
        prop_dict = self.get_widget_properties(widget)

        hint = DartCodeUtils.escape_dart_string(self.get_property_value(prop_dict, 'hintText', 'Enter text...'))
        label = DartCodeUtils.escape_dart_string(self.get_property_value(prop_dict, 'labelText', ''))
        obscure = self.get_property_value(prop_dict, 'obscureText', False)

        # Check if this is a special URL input field
        is_url_input = widget.widget_id == 'url_input' and widget.screen.name == 'Configuration'

        if is_url_input:
            return f'''TextField(
{indent}  controller: _urlController,
{indent}  decoration: InputDecoration(
{indent}    hintText: '{hint}',
{indent}    labelText: 'Server URL',
{indent}    prefixIcon: Icon(Icons.link),
{indent}    border: OutlineInputBorder(),
{indent}  ),
{indent})'''

        # Regular TextField
        code = f'''TextField(
{indent}  decoration: InputDecoration(
{indent}    hintText: '{hint}','''

        if label:
            code += f"\n{indent}    labelText: '{label}',"

        code += f'''
{indent}    border: OutlineInputBorder(),
{indent}  ),'''

        if obscure and str(obscure).lower() == 'true':
            code += f"\n{indent}  obscureText: true,"

        code += f"\n{indent})"

        return code


class DropdownHandler(BaseWidgetHandler):
    """Handler for DropdownButton widget."""

    def can_handle(self, widget_type: str) -> bool:
        return widget_type == 'DropdownButton'

    def generate(self, widget: Any, context: GeneratorContext, indent_level: int) -> str:
        indent = self.get_indent(indent_level)
        prop_dict = self.get_widget_properties(widget)

        items = self.get_property_value(prop_dict, 'items', 'Option 1,Option 2,Option 3')
        value = self.get_property_value(prop_dict, 'value', None)
        icon = self.get_property_value(prop_dict, 'icon', None)
        item_height = self.get_property_value(prop_dict, 'itemHeight', None)
        is_dense = self.get_property_value(prop_dict, 'isDense', None)
        is_expanded = self.get_property_value(prop_dict, 'isExpanded', None)
        padding_val = self.get_property_value(prop_dict, 'padding', None)

        items_list = items.split(',')

        params = [f"value: {'\"' + value + '\"' if value else 'null'}"]

        # Build items
        items_code = f"{indent}  items: ["
        for item in items_list:
            item_text = DartCodeUtils.escape_dart_string(item.strip())
            items_code += f"\n{indent}    DropdownMenuItem(value: '{item_text}', child: Text('{item_text}')),"
        items_code += f"\n{indent}  ]"

        extras = []
        if icon:
            extras.append(f"icon: Icon(Icons.{icon})")
        if item_height:
            extras.append(f"itemHeight: {item_height}")
        if is_dense is not None and str(is_dense) != '':
            extras.append(f"isDense: {str(is_dense).lower()}")
        if is_expanded is not None and str(is_expanded) != '':
            extras.append(f"isExpanded: {str(is_expanded).lower()}")

        base = f"DropdownButton<String>(\n{indent}  " + ",\n{indent}  ".join([params[0], items_code, "onChanged: (String? newValue) {}"] + extras) + f"\n{indent})"

        if padding_val:
            return f"Padding(\n{indent}  padding: EdgeInsets.all({padding_val}),\n{indent}  child: {base}\n{indent})"
        return base


class SwitchCheckboxRadioHandler(BaseWidgetHandler):
    """Handler for Switch, Checkbox, and Radio widgets."""

    def can_handle(self, widget_type: str) -> bool:
        return widget_type in ['Switch', 'Checkbox', 'Radio']

    def generate(self, widget: Any, context: GeneratorContext, indent_level: int) -> str:
        prop_dict = self.get_widget_properties(widget)

        if widget.widget_type == 'Switch':
            return self._generate_switch(prop_dict)
        elif widget.widget_type == 'Checkbox':
            return self._generate_checkbox(prop_dict)
        elif widget.widget_type == 'Radio':
            return self._generate_radio(prop_dict)

        return "Container()"

    def _generate_switch(self, prop_dict: dict) -> str:
        """Generate Switch widget."""
        value = self.get_property_value(prop_dict, 'value', True)
        active_color = self.get_property_value(prop_dict, 'activeColor', None)
        inactive_thumb_color = self.get_property_value(prop_dict, 'inactiveColor', None)
        inactive_track_color = self.get_property_value(prop_dict, 'inactiveTrackColor', None)

        # For stateful widgets, use state variable
        widget_id = self.get_property_value(prop_dict, 'widget_id', 'switch')
        parts = [
            f"value: _stateVariables['{widget_id}'] ?? {str(value).lower()}",
            "onChanged: (bool value) { setState(() { _stateVariables['" + widget_id + "'] = value; }); }"
        ]
        if active_color:
            parts.append(f"activeColor: {DartCodeUtils.generate_color_code(active_color)}")
        if inactive_thumb_color:
            parts.append(f"inactiveThumbColor: {DartCodeUtils.generate_color_code(inactive_thumb_color)}")
        if inactive_track_color:
            parts.append(f"inactiveTrackColor: {DartCodeUtils.generate_color_code(inactive_track_color)}")
        return "Switch(" + ', '.join(parts) + ")"

    def _generate_checkbox(self, prop_dict: dict) -> str:
        """Generate Checkbox widget."""
        value = self.get_property_value(prop_dict, 'value', False)
        action_code = self._generate_action_code(prop_dict.get('onChanged'))
        active_color = self.get_property_value(prop_dict, 'activeColor', None)
        check_color = self.get_property_value(prop_dict, 'checkColor', None)
        shape = self.get_property_value(prop_dict, 'shape', None)

        value_str = str(value).lower() if isinstance(value, bool) else 'false'
        on_changed = action_code if action_code != 'null' else '(bool? v) {}'
        parts = [f"value: {value_str}", f"onChanged: {on_changed}"]
        if active_color:
            parts.append(f"activeColor: {DartCodeUtils.generate_color_code(active_color)}")
        if check_color:
            parts.append(f"checkColor: {DartCodeUtils.generate_color_code(check_color)}")
        if shape:
            parts.append("shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(" + str(shape) + "))")
        return "Checkbox(" + ', '.join(parts) + ")"

    def _generate_radio(self, prop_dict: dict) -> str:
        """Generate Radio widget."""
        value = self.get_property_value(prop_dict, 'value', '1')
        group_value = self.get_property_value(prop_dict, 'groupValue', '1')
        action_code = self._generate_action_code(prop_dict.get('onChanged'))
        active_color = self.get_property_value(prop_dict, 'activeColor', None)

        on_changed = action_code if action_code != 'null' else '(v) {}'
        parts = [f"value: '{value}'", f"groupValue: '{group_value}'", f"onChanged: {on_changed}"]
        if active_color:
            parts.append(f"activeColor: {DartCodeUtils.generate_color_code(active_color)}")
        return "Radio(" + ', '.join(parts) + ")"

    def _generate_action_code(self, prop: Any) -> str:
        """Generate action code for change events."""
        # For input widgets, we typically just return a function signature
        return 'null'


class SliderHandler(BaseWidgetHandler):
    """Handler for Slider widget."""

    def can_handle(self, widget_type: str) -> bool:
        return widget_type == 'Slider'

    def generate(self, widget: Any, context: GeneratorContext, indent_level: int) -> str:
        prop_dict = self.get_widget_properties(widget)

        value = self.get_property_value(prop_dict, 'value', '0.5')
        min_val = self.get_property_value(prop_dict, 'min', '0.0')
        max_val = self.get_property_value(prop_dict, 'max', '1.0')
        active_color = self.get_property_value(prop_dict, 'activeColor', None)
        inactive_color = self.get_property_value(prop_dict, 'inactiveColor', None)
        thumb_color = self.get_property_value(prop_dict, 'thumbColor', None)

        parts = [f"value: {value}", f"min: {min_val}", f"max: {max_val}", "onChanged: (double v) {}"]
        if active_color:
            parts.append(f"activeColor: {DartCodeUtils.generate_color_code(active_color)}")
        if inactive_color:
            parts.append(f"inactiveColor: {DartCodeUtils.generate_color_code(inactive_color)}")
        if thumb_color:
            parts.append(f"thumbColor: {DartCodeUtils.generate_color_code(thumb_color)}")
        return "Slider(" + ', '.join(parts) + ")"


class DateTimePickerHandler(BaseWidgetHandler):
    """Handler for DatePicker and TimePicker widgets."""

    def can_handle(self, widget_type: str) -> bool:
        return widget_type in ['DatePicker', 'TimePicker', 'FileUpload']

    def generate(self, widget: Any, context: GeneratorContext, indent_level: int) -> str:
        indent = self.get_indent(indent_level)

        if widget.widget_type == 'DatePicker':
            return self._generate_date_picker(indent_level)
        elif widget.widget_type == 'TimePicker':
            return self._generate_time_picker(indent_level)
        elif widget.widget_type == 'FileUpload':
            return self._generate_file_upload(indent_level)

        return "Container()"

    def _generate_date_picker(self, indent_level: int) -> str:
        """Generate DatePicker widget."""
        indent = self.get_indent(indent_level)

        return f'''TextButton(
{indent}  onPressed: () async {{
{indent}    final date = await showDatePicker(
{indent}      context: context,
{indent}      initialDate: DateTime.now(),
{indent}      firstDate: DateTime(2020),
{indent}      lastDate: DateTime(2030),
{indent}    );
{indent}  }},
{indent}  child: Text('Select Date'),
{indent})'''

    def _generate_time_picker(self, indent_level: int) -> str:
        """Generate TimePicker widget."""
        indent = self.get_indent(indent_level)

        return f'''TextButton(
{indent}  onPressed: () async {{
{indent}    final time = await showTimePicker(
{indent}      context: context,
{indent}      initialTime: TimeOfDay.now(),
{indent}    );
{indent}  }},
{indent}  child: Text('Select Time'),
{indent})'''

    def _generate_file_upload(self, indent_level: int) -> str:
        """Generate FileUpload widget."""
        indent = self.get_indent(indent_level)

        return f'''ElevatedButton.icon(
{indent}  onPressed: () async {{
{indent}    // File upload logic
{indent}  }},
{indent}  icon: Icon(Icons.upload_file),
{indent}  label: Text('Upload File'),
{indent})'''