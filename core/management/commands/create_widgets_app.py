from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import (
    Application, Theme, Screen, Widget, WidgetProperty, Action
)


class Command(BaseCommand):
    help = 'Create a Widgets App that showcases all supported widgets and properties'

    def add_arguments(self, parser):
        parser.add_argument('--name', type=str, default='Widgets App', help='Application name')
        parser.add_argument('--package', type=str, default='com.example.widgets_app', help='Package name')

    def handle(self, *args, **options):
        app_name = options['name']
        package_name = options['package']

        try:
            with transaction.atomic():
                app = self._create_app(app_name, package_name)
                actions_map = {}

                # Create Home screen
                home = Screen.objects.create(
                    application=app,
                    name='Home',
                    route_name='/',
                    is_home_screen=True,
                    app_bar_title='Widgets Showcase',
                    show_app_bar=True,
                    show_back_button=False
                )

                # Screens map (label -> builder function)
                screens = {
                    'Container': self._build_container_screen,
                    'Column': self._build_column_screen,
                    'Row': self._build_row_screen,
                    'Stack': self._build_stack_screen,
                    'Center': self._build_center_screen,
                    'Padding': self._build_padding_screen,
                    'SizedBox': self._build_sizedbox_screen,
                    'Expanded & Flexible': self._build_expand_flexible_screen,
                    'Align': self._build_align_screen,
                    'Positioned': self._build_positioned_screen,
                    'SingleChildScrollView': self._build_scrollview_screen,
                    'PageView': self._build_pageview_screen,
                    'SafeArea': self._build_safearea_screen,
                    'Future/Stream': self._build_future_stream_screen,
                    'Text': self._build_text_screen,
                    'Image': self._build_image_screen,
                    'Icon': self._build_icon_screen,
                    'TextField': self._build_textfield_screen,
                    'TextButton': self._build_textbutton_screen,
                    'OutlinedButton': self._build_outlinedbutton_screen,
                    'IconButton': self._build_iconbutton_screen,
                    'FloatingActionButton': self._build_fab_only_screen,
                    'Switch': self._build_switch_screen,
                    'Checkbox': self._build_checkbox_screen,
                    'Radio': self._build_radio_screen,
                    'Slider': self._build_slider_screen,
                    'DropdownButton': self._build_dropdown_screen,
                    'Tooltip': self._build_tooltip_screen,
                    'Divider': self._build_divider_screen,
                    'Card': self._build_card_screen,
                    'ListTile': self._build_listtile_screen,
                    'ListView': self._build_listview_screen,
                    'GridView': self._build_gridview_screen,
                    'BottomNavigationBar': self._build_bottomnav_screen,
                    'TabBar': self._build_tabs_screen,
                    'Drawer': self._build_drawer_screen,
                    'Scaffold': self._build_scaffold_screen,
                    'AspectRatio & Wrap': self._build_aspect_wrap_screen,
                    'SnackBar': self._build_snackbar_screen,
                    'Dialog/AlertDialog': self._build_dialog_screen,
                }

                # Create screens and actions
                screen_refs = {}
                for idx, (label, builder) in enumerate(screens.items()):
                    route = f"/{label.lower().replace(' ', '-').replace('&', 'and')}"
                    screen = Screen.objects.create(
                        application=app,
                        name=label,
                        route_name=route,
                        is_home_screen=False,
                        app_bar_title=label,
                        show_app_bar=True,
                        show_back_button=True
                    )
                    screen_refs[label] = screen
                    # Build screen widgets
                    builder(app, screen)
                    # Property editor FAB is injected by the screen generator globally per screen

                # Create navigation actions from Home
                for label, screen in screen_refs.items():
                    action = Action.objects.create(
                        application=app,
                        name=f"Open {label}",
                        action_type='navigate',
                        target_screen=screen
                    )
                    actions_map[label] = action

                # Build Home content: scrollable list of buttons
                home_col = Widget.objects.create(screen=home, widget_type='Column', order=0, widget_id='home_col')

                # Title
                title = Widget.objects.create(screen=home, widget_type='Text', parent_widget=home_col, order=0, widget_id='home_title')
                WidgetProperty.objects.create(widget=title, property_name='text', property_type='string', string_value='Widgets Showcase')
                WidgetProperty.objects.create(widget=title, property_name='fontSize', property_type='integer', integer_value=22)
                WidgetProperty.objects.create(widget=title, property_name='fontWeight', property_type='string', string_value='bold')

                # Buttons list
                buttons_list = Widget.objects.create(screen=home, widget_type='ListView', parent_widget=home_col, order=1, widget_id='home_buttons_list')
                WidgetProperty.objects.create(widget=buttons_list, property_name='padding', property_type='integer', integer_value=8)

                # Create a button per screen
                order = 0
                for label, action in actions_map.items():
                    btn = Widget.objects.create(screen=home, widget_type='ElevatedButton', parent_widget=buttons_list, order=order, widget_id=f"btn_{order}")
                    WidgetProperty.objects.create(widget=btn, property_name='text', property_type='string', string_value=label)
                    WidgetProperty.objects.create(widget=btn, property_name='onPressed', property_type='action_reference', action_reference=action)
                    WidgetProperty.objects.create(widget=btn, property_name='padding', property_type='integer', integer_value=12)
                    order += 1

                self.stdout.write(self.style.SUCCESS(f"Successfully created Widgets App: {app.name}"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error creating Widgets App: {str(e)}"))

    def _create_app(self, name: str, package: str):
        theme = Theme.objects.create(
            name='Widgets Theme',
            primary_color='#1976D2',
            accent_color='#E91E63',
            background_color='#FAFAFA',
            text_color='#212121',
            font_family='Roboto',
            is_dark_mode=False,
        )
        app = Application.objects.create(
            name=name,
            description='Showcase of all widgets and properties',
            package_name=package,
            version='1.0.0',
            theme=theme,
        )
        return app

    def _add_properties_fab(self, app: Application, screen: Screen, title: str, message: str):
        # Build a page-specific bottom sheet editor launcher
        fab = Widget.objects.create(screen=screen, widget_type='FloatingActionButton', order=999, widget_id=f"fab_{screen.name.lower().replace(' ','_')}")
        WidgetProperty.objects.create(widget=fab, property_name='icon', property_type='string', string_value='edit')

    # ---- Screen builders ----
    def _build_container_screen(self, app: Application, screen: Screen):
        cont = Widget.objects.create(screen=screen, widget_type='Container', order=0, widget_id='container_demo')
        # Size, spacing
        WidgetProperty.objects.create(widget=cont, property_name='width', property_type='integer', integer_value=320)
        WidgetProperty.objects.create(widget=cont, property_name='height', property_type='integer', integer_value=160)
        WidgetProperty.objects.create(widget=cont, property_name='padding', property_type='integer', integer_value=16)
        WidgetProperty.objects.create(widget=cont, property_name='margin', property_type='integer', integer_value=12)
        # Decoration and alignment
        WidgetProperty.objects.create(widget=cont, property_name='color', property_type='color', color_value='#F5F5F5')
        WidgetProperty.objects.create(widget=cont, property_name='alignment', property_type='alignment', alignment_value='center')
        WidgetProperty.objects.create(widget=cont, property_name='borderRadius', property_type='integer', integer_value=12)
        WidgetProperty.objects.create(widget=cont, property_name='borderColor', property_type='color', color_value='#1976D2')
        WidgetProperty.objects.create(widget=cont, property_name='borderWidth', property_type='integer', integer_value=2)
        WidgetProperty.objects.create(widget=cont, property_name='boxShadowColor', property_type='color', color_value='#55000000')
        WidgetProperty.objects.create(widget=cont, property_name='boxShadowBlur', property_type='integer', integer_value=8)
        WidgetProperty.objects.create(widget=cont, property_name='boxShadowSpread', property_type='integer', integer_value=1)
        WidgetProperty.objects.create(widget=cont, property_name='boxShadowOffsetX', property_type='integer', integer_value=0)
        WidgetProperty.objects.create(widget=cont, property_name='boxShadowOffsetY', property_type='integer', integer_value=2)
        WidgetProperty.objects.create(widget=cont, property_name='gradientStart', property_type='color', color_value='#1976D2')
        WidgetProperty.objects.create(widget=cont, property_name='gradientEnd', property_type='color', color_value='#E91E63')
        # Constraints
        WidgetProperty.objects.create(widget=cont, property_name='minWidth', property_type='integer', integer_value=200)
        WidgetProperty.objects.create(widget=cont, property_name='maxWidth', property_type='integer', integer_value=360)
        WidgetProperty.objects.create(widget=cont, property_name='minHeight', property_type='integer', integer_value=120)
        WidgetProperty.objects.create(widget=cont, property_name='maxHeight', property_type='integer', integer_value=180)
        # Child
        txt = Widget.objects.create(screen=screen, widget_type='Text', parent_widget=cont, order=0, widget_id='container_text')
        WidgetProperty.objects.create(widget=txt, property_name='text', property_type='string', string_value='Container with decoration, constraints, padding, margin')
        WidgetProperty.objects.create(widget=txt, property_name='fontSize', property_type='integer', integer_value=14)

    def _build_column_screen(self, app: Application, screen: Screen):
        col = Widget.objects.create(screen=screen, widget_type='Column', order=0, widget_id='column_demo')
        WidgetProperty.objects.create(widget=col, property_name='mainAxisAlignment', property_type='string', string_value='spaceBetween')
        WidgetProperty.objects.create(widget=col, property_name='crossAxisAlignment', property_type='string', string_value='center')
        WidgetProperty.objects.create(widget=col, property_name='spacing', property_type='integer', integer_value=12)
        WidgetProperty.objects.create(widget=col, property_name='padding', property_type='integer', integer_value=16)
        # Children
        for i in range(3):
            b = Widget.objects.create(screen=screen, widget_type='ElevatedButton', parent_widget=col, order=i, widget_id=f'col_btn_{i}')
            WidgetProperty.objects.create(widget=b, property_name='text', property_type='string', string_value=f'Button {i+1}')

    def _build_row_screen(self, app: Application, screen: Screen):
        row = Widget.objects.create(screen=screen, widget_type='Row', order=0, widget_id='row_demo')
        WidgetProperty.objects.create(widget=row, property_name='mainAxisAlignment', property_type='string', string_value='spaceAround')
        WidgetProperty.objects.create(widget=row, property_name='crossAxisAlignment', property_type='string', string_value='center')
        WidgetProperty.objects.create(widget=row, property_name='spacing', property_type='integer', integer_value=16)
        for i in range(3):
            t = Widget.objects.create(screen=screen, widget_type='Text', parent_widget=row, order=i, widget_id=f'row_text_{i}')
            WidgetProperty.objects.create(widget=t, property_name='text', property_type='string', string_value=f'Item {i+1}')

    def _build_stack_screen(self, app: Application, screen: Screen):
        stack = Widget.objects.create(screen=screen, widget_type='Stack', order=0, widget_id='stack_demo')
        base = Widget.objects.create(screen=screen, widget_type='Container', parent_widget=stack, order=0, widget_id='stack_base')
        WidgetProperty.objects.create(widget=base, property_name='width', property_type='integer', integer_value=300)
        WidgetProperty.objects.create(widget=base, property_name='height', property_type='integer', integer_value=160)
        WidgetProperty.objects.create(widget=base, property_name='color', property_type='color', color_value='#BBDEFB')
        pos = Widget.objects.create(screen=screen, widget_type='Positioned', parent_widget=stack, order=1, widget_id='stack_pos')
        WidgetProperty.objects.create(widget=pos, property_name='top', property_type='integer', integer_value=16)
        WidgetProperty.objects.create(widget=pos, property_name='left', property_type='integer', integer_value=16)
        WidgetProperty.objects.create(widget=pos, property_name='width', property_type='integer', integer_value=120)
        WidgetProperty.objects.create(widget=pos, property_name='height', property_type='integer', integer_value=80)
        inner = Widget.objects.create(screen=screen, widget_type='Container', parent_widget=pos, order=0, widget_id='stack_inner')
        WidgetProperty.objects.create(widget=inner, property_name='color', property_type='color', color_value='#1976D2')

    def _build_center_screen(self, app: Application, screen: Screen):
        c = Widget.objects.create(screen=screen, widget_type='Center', order=0, widget_id='center_demo')
        WidgetProperty.objects.create(widget=c, property_name='widthFactor', property_type='decimal', decimal_value=1.2)
        WidgetProperty.objects.create(widget=c, property_name='heightFactor', property_type='decimal', decimal_value=1.2)
        t = Widget.objects.create(screen=screen, widget_type='Text', parent_widget=c, order=0, widget_id='center_text')
        WidgetProperty.objects.create(widget=t, property_name='text', property_type='string', string_value='Centered content with factors')

    def _build_padding_screen(self, app: Application, screen: Screen):
        p = Widget.objects.create(screen=screen, widget_type='Padding', order=0, widget_id='padding_demo')
        WidgetProperty.objects.create(widget=p, property_name='padding', property_type='integer', integer_value=24)
        t = Widget.objects.create(screen=screen, widget_type='Text', parent_widget=p, order=0, widget_id='padding_text')
        WidgetProperty.objects.create(widget=t, property_name='text', property_type='string', string_value='Padding applied')

    def _build_sizedbox_screen(self, app: Application, screen: Screen):
        s = Widget.objects.create(screen=screen, widget_type='SizedBox', order=0, widget_id='sized_demo')
        WidgetProperty.objects.create(widget=s, property_name='width', property_type='integer', integer_value=220)
        WidgetProperty.objects.create(widget=s, property_name='height', property_type='integer', integer_value=60)

    def _build_expand_flexible_screen(self, app: Application, screen: Screen):
        row = Widget.objects.create(screen=screen, widget_type='Row', order=0, widget_id='expand_row')
        exp = Widget.objects.create(screen=screen, widget_type='Expanded', parent_widget=row, order=0, widget_id='expanded_demo')
        WidgetProperty.objects.create(widget=exp, property_name='flex', property_type='integer', integer_value=2)
        Widget.objects.create(screen=screen, widget_type='Text', parent_widget=exp, order=0, widget_id='expanded_text')
        flx = Widget.objects.create(screen=screen, widget_type='Flexible', parent_widget=row, order=1, widget_id='flexible_demo')
        WidgetProperty.objects.create(widget=flx, property_name='flex', property_type='integer', integer_value=1)
        WidgetProperty.objects.create(widget=flx, property_name='fit', property_type='string', string_value='tight')
        Widget.objects.create(screen=screen, widget_type='Text', parent_widget=flx, order=0, widget_id='flexible_text')

    def _build_align_screen(self, app: Application, screen: Screen):
        al = Widget.objects.create(screen=screen, widget_type='Align', order=0, widget_id='align_demo')
        WidgetProperty.objects.create(widget=al, property_name='alignment', property_type='alignment', alignment_value='bottomRight')
        Widget.objects.create(screen=screen, widget_type='Text', parent_widget=al, order=0, widget_id='align_text')

    def _build_positioned_screen(self, app: Application, screen: Screen):
        self._build_stack_screen(app, screen)

    def _build_scrollview_screen(self, app: Application, screen: Screen):
        sc = Widget.objects.create(screen=screen, widget_type='SingleChildScrollView', order=0, widget_id='scsv_demo')
        WidgetProperty.objects.create(widget=sc, property_name='padding', property_type='integer', integer_value=12)
        col = Widget.objects.create(screen=screen, widget_type='Column', parent_widget=sc, order=0, widget_id='scsv_col')
        for i in range(10):
            t = Widget.objects.create(screen=screen, widget_type='Text', parent_widget=col, order=i, widget_id=f'scsv_t_{i}')
            WidgetProperty.objects.create(widget=t, property_name='text', property_type='string', string_value=f'Item {i+1}')

    def _build_pageview_screen(self, app: Application, screen: Screen):
        pv = Widget.objects.create(screen=screen, widget_type='PageView', order=0, widget_id='pageview_demo')
        for i, color in enumerate(['#FFCDD2', '#C8E6C9', '#BBDEFB']):
            c = Widget.objects.create(screen=screen, widget_type='Container', parent_widget=pv, order=i, widget_id=f'pv_{i}')
            WidgetProperty.objects.create(widget=c, property_name='color', property_type='color', color_value=color)
            t = Widget.objects.create(screen=screen, widget_type='Text', parent_widget=c, order=0, widget_id=f'pv_t_{i}')
            WidgetProperty.objects.create(widget=t, property_name='text', property_type='string', string_value=f'Page {i+1}')

    def _build_safearea_screen(self, app: Application, screen: Screen):
        sa = Widget.objects.create(screen=screen, widget_type='SafeArea', order=0, widget_id='safearea_demo')
        t = Widget.objects.create(screen=screen, widget_type='Text', parent_widget=sa, order=0, widget_id='sa_text')
        WidgetProperty.objects.create(widget=t, property_name='text', property_type='string', string_value='Safe area content')

    def _build_future_stream_screen(self, app: Application, screen: Screen):
        fb = Widget.objects.create(screen=screen, widget_type='FutureBuilder', order=0, widget_id='fb_placeholder')
        Widget.objects.create(screen=screen, widget_type='StreamBuilder', order=1, widget_id='sb_placeholder')

    def _build_text_screen(self, app: Application, screen: Screen):
        t = Widget.objects.create(screen=screen, widget_type='Text', order=0, widget_id='text_demo')
        WidgetProperty.objects.create(widget=t, property_name='text', property_type='string', string_value='Styled Text Example')
        WidgetProperty.objects.create(widget=t, property_name='fontSize', property_type='integer', integer_value=20)
        WidgetProperty.objects.create(widget=t, property_name='fontWeight', property_type='string', string_value='bold')
        WidgetProperty.objects.create(widget=t, property_name='fontStyle', property_type='string', string_value='italic')
        WidgetProperty.objects.create(widget=t, property_name='color', property_type='color', color_value='#1976D2')
        WidgetProperty.objects.create(widget=t, property_name='fontFamily', property_type='string', string_value='Roboto')
        WidgetProperty.objects.create(widget=t, property_name='letterSpacing', property_type='decimal', decimal_value=1.2)
        WidgetProperty.objects.create(widget=t, property_name='wordSpacing', property_type='decimal', decimal_value=2.0)
        WidgetProperty.objects.create(widget=t, property_name='height', property_type='decimal', decimal_value=1.3)
        WidgetProperty.objects.create(widget=t, property_name='decoration', property_type='string', string_value='underline')
        WidgetProperty.objects.create(widget=t, property_name='decorationColor', property_type='color', color_value='#E91E63')
        WidgetProperty.objects.create(widget=t, property_name='decorationStyle', property_type='string', string_value='dashed')
        WidgetProperty.objects.create(widget=t, property_name='decorationThickness', property_type='decimal', decimal_value=2.0)
        WidgetProperty.objects.create(widget=t, property_name='textAlign', property_type='string', string_value='center')
        WidgetProperty.objects.create(widget=t, property_name='softWrap', property_type='boolean', boolean_value=True)
        WidgetProperty.objects.create(widget=t, property_name='overflow', property_type='string', string_value='ellipsis')
        WidgetProperty.objects.create(widget=t, property_name='maxLines', property_type='integer', integer_value=2)

    def _build_richtext_screen(self, app: Application, screen: Screen):
        rt = Widget.objects.create(screen=screen, widget_type='RichText', order=0, widget_id='richtext_demo')
        WidgetProperty.objects.create(widget=rt, property_name='text', property_type='string', string_value='RichText demo content')

    def _build_image_screen(self, app: Application, screen: Screen):
        im = Widget.objects.create(screen=screen, widget_type='Image', order=0, widget_id='image_demo')
        WidgetProperty.objects.create(widget=im, property_name='imageUrl', property_type='url', url_value='https://picsum.photos/400/200')
        WidgetProperty.objects.create(widget=im, property_name='width', property_type='integer', integer_value=300)
        WidgetProperty.objects.create(widget=im, property_name='height', property_type='integer', integer_value=150)
        WidgetProperty.objects.create(widget=im, property_name='fit', property_type='string', string_value='cover')
        WidgetProperty.objects.create(widget=im, property_name='alignment', property_type='alignment', alignment_value='center')
        WidgetProperty.objects.create(widget=im, property_name='repeat', property_type='string', string_value='noRepeat')
        WidgetProperty.objects.create(widget=im, property_name='opacity', property_type='decimal', decimal_value=0.95)
        WidgetProperty.objects.create(widget=im, property_name='colorBlendMode', property_type='string', string_value='srcOver')
        WidgetProperty.objects.create(widget=im, property_name='scale', property_type='decimal', decimal_value=1.0)

    def _build_icon_screen(self, app: Application, screen: Screen):
        ic = Widget.objects.create(screen=screen, widget_type='Icon', order=0, widget_id='icon_demo')
        WidgetProperty.objects.create(widget=ic, property_name='icon', property_type='string', string_value='home')
        WidgetProperty.objects.create(widget=ic, property_name='size', property_type='integer', integer_value=48)
        WidgetProperty.objects.create(widget=ic, property_name='color', property_type='color', color_value='#FF5722')

    def _build_textfield_screen(self, app: Application, screen: Screen):
        tf = Widget.objects.create(screen=screen, widget_type='TextField', order=0, widget_id='textfield_demo')
        WidgetProperty.objects.create(widget=tf, property_name='labelText', property_type='string', string_value='Email')
        WidgetProperty.objects.create(widget=tf, property_name='hintText', property_type='string', string_value='enter your email')
        WidgetProperty.objects.create(widget=tf, property_name='obscureText', property_type='boolean', boolean_value=False)
        # Extras (editor shows but backend may ignore gracefully)
        WidgetProperty.objects.create(widget=tf, property_name='prefixIcon', property_type='string', string_value='email')
        WidgetProperty.objects.create(widget=tf, property_name='filled', property_type='boolean', boolean_value=True)
        WidgetProperty.objects.create(widget=tf, property_name='fillColor', property_type='color', color_value='#FFFDE7')
        WidgetProperty.objects.create(widget=tf, property_name='borderRadius', property_type='integer', integer_value=8)
        WidgetProperty.objects.create(widget=tf, property_name='helperText', property_type='string', string_value='We will not share your email.')

    def _build_textbutton_screen(self, app: Application, screen: Screen):
        b = Widget.objects.create(screen=screen, widget_type='TextButton', order=0, widget_id='textbutton_demo')
        WidgetProperty.objects.create(widget=b, property_name='text', property_type='string', string_value='TextButton')
        WidgetProperty.objects.create(widget=b, property_name='foregroundColor', property_type='color', color_value='#1976D2')
        WidgetProperty.objects.create(widget=b, property_name='padding', property_type='integer', integer_value=12)

    def _build_outlinedbutton_screen(self, app: Application, screen: Screen):
        b = Widget.objects.create(screen=screen, widget_type='OutlinedButton', order=0, widget_id='outlinedbutton_demo')
        WidgetProperty.objects.create(widget=b, property_name='text', property_type='string', string_value='OutlinedButton')
        WidgetProperty.objects.create(widget=b, property_name='borderColor', property_type='color', color_value='#1976D2')
        WidgetProperty.objects.create(widget=b, property_name='borderWidth', property_type='integer', integer_value=2)
        WidgetProperty.objects.create(widget=b, property_name='borderRadius', property_type='integer', integer_value=8)

    def _build_iconbutton_screen(self, app: Application, screen: Screen):
        ib = Widget.objects.create(screen=screen, widget_type='IconButton', order=0, widget_id='iconbutton_demo')
        WidgetProperty.objects.create(widget=ib, property_name='icon', property_type='string', string_value='favorite')
        WidgetProperty.objects.create(widget=ib, property_name='color', property_type='color', color_value='#E91E63')
        WidgetProperty.objects.create(widget=ib, property_name='size', property_type='integer', integer_value=28)
        WidgetProperty.objects.create(widget=ib, property_name='splashRadius', property_type='integer', integer_value=22)

    def _build_fab_only_screen(self, app: Application, screen: Screen):
        fb = Widget.objects.create(screen=screen, widget_type='FloatingActionButton', order=0, widget_id='fab_demo')
        WidgetProperty.objects.create(widget=fb, property_name='icon', property_type='string', string_value='add')
        WidgetProperty.objects.create(widget=fb, property_name='backgroundColor', property_type='color', color_value='#1976D2')
        WidgetProperty.objects.create(widget=fb, property_name='foregroundColor', property_type='color', color_value='#FFFFFF')
        # Use either mini or extended, not both (extended doesn't support mini)
        WidgetProperty.objects.create(widget=fb, property_name='extended', property_type='boolean', boolean_value=True)
        WidgetProperty.objects.create(widget=fb, property_name='label', property_type='string', string_value='Create')

    def _build_switch_screen(self, app: Application, screen: Screen):
        sw = Widget.objects.create(screen=screen, widget_type='Switch', order=0, widget_id='switch_demo')
        WidgetProperty.objects.create(widget=sw, property_name='value', property_type='boolean', boolean_value=True)

    def _build_checkbox_screen(self, app: Application, screen: Screen):
        cb = Widget.objects.create(screen=screen, widget_type='Checkbox', order=0, widget_id='checkbox_demo')
        WidgetProperty.objects.create(widget=cb, property_name='value', property_type='boolean', boolean_value=True)

    def _build_radio_screen(self, app: Application, screen: Screen):
        rd = Widget.objects.create(screen=screen, widget_type='Radio', order=0, widget_id='radio_demo')
        WidgetProperty.objects.create(widget=rd, property_name='value', property_type='string', string_value='A')
        WidgetProperty.objects.create(widget=rd, property_name='groupValue', property_type='string', string_value='A')

    def _build_slider_screen(self, app: Application, screen: Screen):
        sl = Widget.objects.create(screen=screen, widget_type='Slider', order=0, widget_id='slider_demo')
        WidgetProperty.objects.create(widget=sl, property_name='value', property_type='decimal', decimal_value=0.5)
        WidgetProperty.objects.create(widget=sl, property_name='min', property_type='decimal', decimal_value=0.0)
        WidgetProperty.objects.create(widget=sl, property_name='max', property_type='decimal', decimal_value=1.0)

    def _build_dropdown_screen(self, app: Application, screen: Screen):
        dd = Widget.objects.create(screen=screen, widget_type='DropdownButton', order=0, widget_id='dropdown_demo')
        WidgetProperty.objects.create(widget=dd, property_name='items', property_type='string', string_value='Red,Green,Blue')
        WidgetProperty.objects.create(widget=dd, property_name='value', property_type='string', string_value='Green')

    def _build_divider_screen(self, app: Application, screen: Screen):
        d = Widget.objects.create(screen=screen, widget_type='Divider', order=0, widget_id='divider_demo')
        WidgetProperty.objects.create(widget=d, property_name='height', property_type='integer', integer_value=24)
        WidgetProperty.objects.create(widget=d, property_name='thickness', property_type='integer', integer_value=2)
        WidgetProperty.objects.create(widget=d, property_name='indent', property_type='integer', integer_value=16)
        WidgetProperty.objects.create(widget=d, property_name='endIndent', property_type='integer', integer_value=16)
        WidgetProperty.objects.create(widget=d, property_name='color', property_type='color', color_value='#9E9E9E')

        t = Widget.objects.create(screen=screen, widget_type='Text', order=1, widget_id='divider_note')
        WidgetProperty.objects.create(widget=t, property_name='text', property_type='string', string_value='Divider above has height, thickness, indent, endIndent and color')

    def _build_card_screen(self, app: Application, screen: Screen):
        c = Widget.objects.create(screen=screen, widget_type='Card', order=0, widget_id='card_demo')
        WidgetProperty.objects.create(widget=c, property_name='elevation', property_type='integer', integer_value=6)
        WidgetProperty.objects.create(widget=c, property_name='margin', property_type='integer', integer_value=12)
        WidgetProperty.objects.create(widget=c, property_name='color', property_type='color', color_value='#FFF3E0')
        WidgetProperty.objects.create(widget=c, property_name='shadowColor', property_type='color', color_value='#FF9800')
        WidgetProperty.objects.create(widget=c, property_name='borderRadius', property_type='integer', integer_value=12)
        inner = Widget.objects.create(screen=screen, widget_type='Text', parent_widget=c, order=0, widget_id='card_text')
        WidgetProperty.objects.create(widget=inner, property_name='text', property_type='string', string_value='Card with color, elevation, borderRadius and padding')
        WidgetProperty.objects.create(widget=c, property_name='padding', property_type='integer', integer_value=16)

    def _build_listtile_screen(self, app: Application, screen: Screen):
        lt = Widget.objects.create(screen=screen, widget_type='ListTile', order=0, widget_id='listtile_demo')
        WidgetProperty.objects.create(widget=lt, property_name='title', property_type='string', string_value='ListTile Title')
        WidgetProperty.objects.create(widget=lt, property_name='subtitle', property_type='string', string_value='Subtitle text')
        WidgetProperty.objects.create(widget=lt, property_name='leading', property_type='string', string_value='star')
        WidgetProperty.objects.create(widget=lt, property_name='trailing', property_type='string', string_value='chevron_right')
        WidgetProperty.objects.create(widget=lt, property_name='tileColor', property_type='color', color_value='#E0F7FA')
        WidgetProperty.objects.create(widget=lt, property_name='contentPadding', property_type='integer', integer_value=12)

    def _build_listview_screen(self, app: Application, screen: Screen):
        lv = Widget.objects.create(screen=screen, widget_type='ListView', order=0, widget_id='listview_demo')
        WidgetProperty.objects.create(widget=lv, property_name='scrollDirection', property_type='string', string_value='vertical')
        WidgetProperty.objects.create(widget=lv, property_name='padding', property_type='integer', integer_value=8)
        for i in range(5):
            t = Widget.objects.create(screen=screen, widget_type='Text', parent_widget=lv, order=i, widget_id=f'lv_t_{i}')
            WidgetProperty.objects.create(widget=t, property_name='text', property_type='string', string_value=f'List item {i+1}')

    def _build_gridview_screen(self, app: Application, screen: Screen):
        gv = Widget.objects.create(screen=screen, widget_type='GridView', order=0, widget_id='gridview_demo')
        WidgetProperty.objects.create(widget=gv, property_name='crossAxisCount', property_type='integer', integer_value=3)
        WidgetProperty.objects.create(widget=gv, property_name='childAspectRatio', property_type='decimal', decimal_value=1.0)
        WidgetProperty.objects.create(widget=gv, property_name='padding', property_type='integer', integer_value=8)

    def _build_tooltip_screen(self, app: Application, screen: Screen):
        tp = Widget.objects.create(screen=screen, widget_type='Tooltip', order=0, widget_id='tooltip_demo')
        WidgetProperty.objects.create(widget=tp, property_name='message', property_type='string', string_value='Tooltip message')
        WidgetProperty.objects.create(widget=tp, property_name='padding', property_type='integer', integer_value=8)
        WidgetProperty.objects.create(widget=tp, property_name='margin', property_type='integer', integer_value=8)
        btn = Widget.objects.create(screen=screen, widget_type='ElevatedButton', parent_widget=tp, order=0, widget_id='tooltip_btn')
        WidgetProperty.objects.create(widget=btn, property_name='text', property_type='string', string_value='Hover me')

    def _build_bottomnav_screen(self, app: Application, screen: Screen):
        # Build BottomNavigationBar with 3 items
        bnav = Widget.objects.create(screen=screen, widget_type='BottomNavigationBar', order=0, widget_id='bottomnav_demo')
        WidgetProperty.objects.create(widget=bnav, property_name='currentIndex', property_type='integer', integer_value=0)
        WidgetProperty.objects.create(widget=bnav, property_name='backgroundColor', property_type='color', color_value='#FFFFFF')
        WidgetProperty.objects.create(widget=bnav, property_name='selectedItemColor', property_type='color', color_value='#1976D2')
        WidgetProperty.objects.create(widget=bnav, property_name='unselectedItemColor', property_type='color', color_value='#9E9E9E')
        WidgetProperty.objects.create(widget=bnav, property_name='iconSize', property_type='integer', integer_value=22)
        WidgetProperty.objects.create(widget=bnav, property_name='elevation', property_type='integer', integer_value=8)
        for i, (icon, label) in enumerate([('home', 'Home'), ('search', 'Search'), ('person', 'Profile')]):
            item = Widget.objects.create(screen=screen, widget_type='Container', parent_widget=bnav, order=i, widget_id=f'bn_item_{i}')
            WidgetProperty.objects.create(widget=item, property_name='icon', property_type='string', string_value=icon)
            WidgetProperty.objects.create(widget=item, property_name='label', property_type='string', string_value=label)

    def _build_tabs_screen(self, app: Application, screen: Screen):
        tabs = Widget.objects.create(screen=screen, widget_type='TabBar', order=0, widget_id='tabbar_demo')
        for i in range(3):
            tab = Widget.objects.create(screen=screen, widget_type='Text', parent_widget=tabs, order=i, widget_id=f'tab_{i}')
            WidgetProperty.objects.create(widget=tab, property_name='text', property_type='string', string_value=f'Tab {i+1}')
        tbv = Widget.objects.create(screen=screen, widget_type='TabBarView', order=1, widget_id='tabbarview_demo')
        for i in range(3):
            cont = Widget.objects.create(screen=screen, widget_type='Container', parent_widget=tbv, order=i, widget_id=f'tbv_c_{i}')
            WidgetProperty.objects.create(widget=cont, property_name='height', property_type='integer', integer_value=200)
            WidgetProperty.objects.create(widget=cont, property_name='color', property_type='color', color_value=['#FFCDD2', '#C8E6C9', '#BBDEFB'][i])
            txt = Widget.objects.create(screen=screen, widget_type='Text', parent_widget=cont, order=0, widget_id=f'tbv_t_{i}')
            WidgetProperty.objects.create(widget=txt, property_name='text', property_type='string', string_value=f'Content of Tab {i+1}')

    def _build_dialog_screen(self, app: Application, screen: Screen):
        col = Widget.objects.create(screen=screen, widget_type='Column', order=0, widget_id='dialog_col')
        btn = Widget.objects.create(screen=screen, widget_type='ElevatedButton', parent_widget=col, order=0, widget_id='dialog_btn')
        WidgetProperty.objects.create(widget=btn, property_name='text', property_type='string', string_value='Open Dialog')
        act = Action.objects.create(
            application=app,
            name=f"Dialog on {screen.name}",
            action_type='show_dialog',
            dialog_title='Demo Dialog',
            dialog_message='This is a demo dialog'
        )
        WidgetProperty.objects.create(widget=btn, property_name='onPressed', property_type='action_reference', action_reference=act)

    def _build_snackbar_screen(self, app: Application, screen: Screen):
        col = Widget.objects.create(screen=screen, widget_type='Column', order=0, widget_id='snack_col')
        btn = Widget.objects.create(screen=screen, widget_type='ElevatedButton', parent_widget=col, order=0, widget_id='snack_btn')
        WidgetProperty.objects.create(widget=btn, property_name='text', property_type='string', string_value='Show SnackBar')
        act = Action.objects.create(application=app, name=f"Snack on {screen.name}", action_type='show_snackbar', dialog_message='Hello SnackBar', parameters='{"backgroundColor":"#323232","durationMs":1500,"padding":8,"margin":8}')
        WidgetProperty.objects.create(widget=btn, property_name='onPressed', property_type='action_reference', action_reference=act)

    def _build_drawer_screen(self, app: Application, screen: Screen):
        dr = Widget.objects.create(screen=screen, widget_type='Drawer', order=0, widget_id='drawer_demo')
        WidgetProperty.objects.create(widget=dr, property_name='width', property_type='integer', integer_value=280)
        WidgetProperty.objects.create(widget=dr, property_name='backgroundColor', property_type='color', color_value='#FFFFFF')
        for i in range(3):
            lt = Widget.objects.create(screen=screen, widget_type='ListTile', parent_widget=dr, order=i, widget_id=f'dr_lt_{i}')
            WidgetProperty.objects.create(widget=lt, property_name='title', property_type='string', string_value=f'Item {i+1}')
            WidgetProperty.objects.create(widget=lt, property_name='leading', property_type='string', string_value='chevron_right')

    def _build_scaffold_screen(self, app: Application, screen: Screen):
        sc = Widget.objects.create(screen=screen, widget_type='Scaffold', order=0, widget_id='scaffold_demo')
        WidgetProperty.objects.create(widget=sc, property_name='backgroundColor', property_type='color', color_value='#FAFAFA')
        body = Widget.objects.create(screen=screen, widget_type='Text', parent_widget=sc, order=0, widget_id='sc_body_text')
        WidgetProperty.objects.create(widget=body, property_name='text', property_type='string', string_value='Scaffold body content')

    def _build_aspect_wrap_screen(self, app: Application, screen: Screen):
        ar = Widget.objects.create(screen=screen, widget_type='AspectRatio', order=0, widget_id='aspect_demo')
        WidgetProperty.objects.create(widget=ar, property_name='aspectRatio', property_type='decimal', decimal_value=1.5)
        wr = Widget.objects.create(screen=screen, widget_type='Wrap', order=1, widget_id='wrap_demo')
        WidgetProperty.objects.create(widget=wr, property_name='spacing', property_type='integer', integer_value=8)
        WidgetProperty.objects.create(widget=wr, property_name='runSpacing', property_type='integer', integer_value=8)
        WidgetProperty.objects.create(widget=wr, property_name='direction', property_type='string', string_value='horizontal')
        WidgetProperty.objects.create(widget=wr, property_name='alignment', property_type='string', string_value='center')
        WidgetProperty.objects.create(widget=wr, property_name='runAlignment', property_type='string', string_value='center')
        WidgetProperty.objects.create(widget=wr, property_name='crossAxisAlignment', property_type='string', string_value='center')
        for i in range(6):
            b = Widget.objects.create(screen=screen, widget_type='ElevatedButton', parent_widget=wr, order=i, widget_id=f'wrap_btn_{i}')
            WidgetProperty.objects.create(widget=b, property_name='text', property_type='string', string_value=f'Chip {i+1}')

    def _build_picker_screen(self, app: Application, screen: Screen):
        col = Widget.objects.create(screen=screen, widget_type='Column', order=0, widget_id='picker_col')
        d = Widget.objects.create(screen=screen, widget_type='DatePicker', parent_widget=col, order=0, widget_id='date_picker')
        t = Widget.objects.create(screen=screen, widget_type='TimePicker', parent_widget=col, order=1, widget_id='time_picker')


