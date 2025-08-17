# File: core/services/code_generation/widgets/handlers/__init__.py
"""
Widget handlers package.
Contains all specific widget type handlers.
"""

from .basic_widgets import (
    TextWidgetHandler,
    ButtonWidgetHandler,
    IconWidgetHandler,
    ImageWidgetHandler,
    DividerWidgetHandler
)

from .layout_widgets import (
    ContainerWidgetHandler,
    ColumnRowWidgetHandler,
    StackWidgetHandler,
    ExpandedFlexibleHandler,
    PaddingWidgetHandler,
    CenterWidgetHandler,
    SizedBoxWidgetHandler
)

from .list_widgets import (
    ListViewHandler,
    GridViewHandler,
    ListTileHandler,
    SingleChildScrollViewHandler
)

from .input_widgets import (
    TextFieldHandler,
    DropdownHandler,
    SwitchCheckboxRadioHandler,
    SliderHandler,
    DateTimePickerHandler
)

from .navigation_widgets import (
    BottomNavigationHandler,
    AppBarHandler,
    DrawerHandler,
    TabBarHandler
)

from .advanced_widgets import (
    CardHandler,
    FutureBuilderHandler,
    StreamBuilderHandler,
    PageViewHandler,
    WrapHandler,
    AspectRatioHandler,
    SafeAreaHandler,
    ScaffoldHandler
)

__all__ = [
    # Basic widgets
    'TextWidgetHandler',
    'ButtonWidgetHandler',
    'IconWidgetHandler',
    'ImageWidgetHandler',
    'DividerWidgetHandler',

    # Layout widgets
    'ContainerWidgetHandler',
    'ColumnRowWidgetHandler',
    'StackWidgetHandler',
    'ExpandedFlexibleHandler',
    'PaddingWidgetHandler',
    'CenterWidgetHandler',
    'SizedBoxWidgetHandler',

    # List widgets
    'ListViewHandler',
    'GridViewHandler',
    'ListTileHandler',
    'SingleChildScrollViewHandler',

    # Input widgets
    'TextFieldHandler',
    'DropdownHandler',
    'SwitchCheckboxRadioHandler',
    'SliderHandler',
    'DateTimePickerHandler',

    # Navigation widgets
    'BottomNavigationHandler',
    'AppBarHandler',
    'DrawerHandler',
    'TabBarHandler',

    # Advanced widgets
    'CardHandler',
    'FutureBuilderHandler',
    'StreamBuilderHandler',
    'PageViewHandler',
    'WrapHandler',
    'AspectRatioHandler',
    'SafeAreaHandler',
    'ScaffoldHandler'
]