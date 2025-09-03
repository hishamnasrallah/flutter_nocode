# File: core/services/code_generation/widgets/widget_factory.py
"""
Factory pattern implementation for widget handler creation.
"""

from typing import Optional

from ..base import BaseWidgetHandler
from .handlers.basic_widgets import (
    TextWidgetHandler,
    ButtonWidgetHandler,
    IconWidgetHandler,
    ImageWidgetHandler,
    DividerWidgetHandler
)
from .handlers.layout_widgets import (
    ContainerWidgetHandler,
    ColumnRowWidgetHandler,
    StackWidgetHandler,
    ExpandedFlexibleHandler,
    PaddingWidgetHandler,
    CenterWidgetHandler,
    SizedBoxWidgetHandler,
    AlignWidgetHandler
)
from .handlers.list_widgets import (
    ListViewHandler,
    GridViewHandler,
    ListTileHandler,
    SingleChildScrollViewHandler
)
from .handlers.input_widgets import (
    TextFieldHandler,
    DropdownHandler,
    SwitchCheckboxRadioHandler,
    SliderHandler,
    DateTimePickerHandler
)
from .handlers.navigation_widgets import (
    BottomNavigationHandler,
    AppBarHandler,
    DrawerHandler,
    TabBarHandler
)
from .handlers.advanced_widgets import (
    CardHandler,
    FutureBuilderHandler,
    StreamBuilderHandler,
    PageViewHandler,
    TabBarViewHandler,
    ScaffoldHandler,
    SafeAreaHandler,
    TooltipHandler,
    RichTextHandler,
    ChipHandler,
    AvatarHandler,
    BottomSheetHandler,
    DialogHandler,
    BadgeHandler
)
from .handlers.custom_widgets import CustomPubDevWidgetHandler


class WidgetFactory:
    """
    Factory for creating appropriate widget handlers based on widget type.
    """

    def __init__(self):
        # Initialize all handlers
        self.handlers = self._initialize_handlers()

    def _initialize_handlers(self) -> list:
        """
        Initialize all available widget handlers.

        Returns:
            list: List of handler instances
        """
        return [
            # Basic widgets
            TextWidgetHandler(),
            ButtonWidgetHandler(),
            IconWidgetHandler(),
            ImageWidgetHandler(),
            DividerWidgetHandler(),

            # Layout widgets
            ContainerWidgetHandler(),
            ColumnRowWidgetHandler(),
            StackWidgetHandler(),
            ExpandedFlexibleHandler(),
            PaddingWidgetHandler(),
            CenterWidgetHandler(),
            SizedBoxWidgetHandler(),
            AlignWidgetHandler(),

            # List widgets
            ListViewHandler(),
            GridViewHandler(),
            ListTileHandler(),
            SingleChildScrollViewHandler(),

            # Input widgets
            TextFieldHandler(),
            DropdownHandler(),
            SwitchCheckboxRadioHandler(),
            SliderHandler(),
            DateTimePickerHandler(),

            # Navigation widgets
            BottomNavigationHandler(),
            AppBarHandler(),
            DrawerHandler(),
            TabBarHandler(),

            # Advanced widgets
            CardHandler(),
            FutureBuilderHandler(),
            StreamBuilderHandler(),
            PageViewHandler(),
            TabBarViewHandler(),
            ScaffoldHandler(),
            SafeAreaHandler(),
            TooltipHandler(),
            RichTextHandler(),
            ChipHandler(),
            AvatarHandler(),
            BottomSheetHandler(),
            DialogHandler(),
            BadgeHandler(),
            # Custom pub.dev widgets
            CustomPubDevWidgetHandler(),
        ]

    def get_handler(self, widget_type: str) -> Optional[BaseWidgetHandler]:
        """
        Get the appropriate handler for a widget type.

        Args:
            widget_type: Type of widget

        Returns:
            Optional[BaseWidgetHandler]: Handler instance or None
        """
        for handler in self.handlers:
            if handler.can_handle(widget_type):
                return handler

        return None

    def register_handler(self, handler: BaseWidgetHandler):
        """
        Register a new handler.

        Args:
            handler: Handler instance to register
        """
        self.handlers.append(handler)

    def unregister_handler(self, handler: BaseWidgetHandler):
        """
        Unregister a handler.

        Args:
            handler: Handler instance to unregister
        """
        if handler in self.handlers:
            self.handlers.remove(handler)