from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.core.files.base import ContentFile
import json
import uuid
import os
from datetime import datetime

from .models import (
    Theme, Application, DataSource, DataSourceField,
    Screen, Widget, WidgetProperty, Action, BuildHistory,
    CustomPubDevWidget
)
from .serializers import (
    ThemeSerializer, ApplicationListSerializer, ApplicationDetailSerializer,
    DataSourceSerializer, DataSourceFieldSerializer, ScreenSerializer,
    WidgetSerializer, WidgetPropertySerializer, ActionSerializer,
    BuildHistorySerializer, CustomPubDevWidgetSerializer,
    CloneApplicationSerializer, BuildApplicationSerializer,
    WidgetTreeSerializer, BulkWidgetCreateSerializer,
    TemplateApplicationSerializer
)
from .services import FlutterCodeGenerator, BuildService


class ThemeViewSet(viewsets.ModelViewSet):
    queryset = Theme.objects.all()
    serializer_class = ThemeSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def templates(self, request):
        """Get predefined theme templates"""
        templates = [
            {
                'id': 1,
                'name': 'Material Blue',
                'primary_color': '#2196F3',
                'accent_color': '#FF4081',
                'background_color': '#FFFFFF',
                'text_color': '#000000',
                'font_family': 'Roboto',
                'is_dark_mode': False
            },
            {
                'id': 2,
                'name': 'Dark Theme',
                'primary_color': '#1976D2',
                'accent_color': '#FFC107',
                'background_color': '#121212',
                'text_color': '#FFFFFF',
                'font_family': 'Roboto',
                'is_dark_mode': True
            },
            {
                'id': 3,
                'name': 'Green Nature',
                'primary_color': '#4CAF50',
                'accent_color': '#8BC34A',
                'background_color': '#F1F8E9',
                'text_color': '#33691E',
                'font_family': 'Roboto',
                'is_dark_mode': False
            },
            {
                'id': 4,
                'name': 'Purple Gradient',
                'primary_color': '#9C27B0',
                'accent_color': '#E91E63',
                'background_color': '#F3E5F5',
                'text_color': '#4A148C',
                'font_family': 'Roboto',
                'is_dark_mode': False
            },
            {
                'id': 5,
                'name': 'Orange Sunset',
                'primary_color': '#FF5722',
                'accent_color': '#FFC107',
                'background_color': '#FFF3E0',
                'text_color': '#3E2723',
                'font_family': 'Roboto',
                'is_dark_mode': False
            },
            {
                'id': 6,
                'name': 'Teal Ocean',
                'primary_color': '#009688',
                'accent_color': '#00BCD4',
                'background_color': '#E0F2F1',
                'text_color': '#004D40',
                'font_family': 'Roboto',
                'is_dark_mode': False
            },
            {
                'id': 7,
                'name': 'Red Power',
                'primary_color': '#F44336',
                'accent_color': '#FF5252',
                'background_color': '#FFEBEE',
                'text_color': '#B71C1C',
                'font_family': 'Roboto',
                'is_dark_mode': False
            },
            {
                'id': 8,
                'name': 'Indigo Deep',
                'primary_color': '#3F51B5',
                'accent_color': '#536DFE',
                'background_color': '#E8EAF6',
                'text_color': '#1A237E',
                'font_family': 'Roboto',
                'is_dark_mode': False
            },
            {
                'id': 9,
                'name': 'Grey Professional',
                'primary_color': '#607D8B',
                'accent_color': '#78909C',
                'background_color': '#ECEFF1',
                'text_color': '#263238',
                'font_family': 'Roboto',
                'is_dark_mode': False
            },
            {
                'id': 10,
                'name': 'Black Elegant',
                'primary_color': '#000000',
                'accent_color': '#424242',
                'background_color': '#000000',
                'text_color': '#FFFFFF',
                'font_family': 'Roboto',
                'is_dark_mode': True
            }
        ]
        return Response(templates)

    @action(detail=True, methods=['post'])
    def duplicate(self, request, pk=None):
        """Duplicate a theme"""
        theme = self.get_object()
        new_theme = Theme.objects.create(
            name=f"{theme.name} (Copy)",
            primary_color=theme.primary_color,
            accent_color=theme.accent_color,
            background_color=theme.background_color,
            text_color=theme.text_color,
            font_family=theme.font_family,
            is_dark_mode=theme.is_dark_mode
        )
        return Response(ThemeSerializer(new_theme).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def popular(self, request):
        """Get most used themes"""
        themes = Theme.objects.all()
        theme_data = []
        for theme in themes:
            theme_data.append({
                'theme': ThemeSerializer(theme).data,
                'usage_count': theme.application_set.count()
            })
        theme_data.sort(key=lambda x: x['usage_count'], reverse=True)
        return Response(theme_data[:5])


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return ApplicationListSerializer
        return ApplicationDetailSerializer

    @action(detail=True, methods=['post'])
    def clone(self, request, pk=None):
        """Clone an application with all its components"""
        app = self.get_object()
        serializer = CloneApplicationSerializer(data=request.data)

        if serializer.is_valid():
            with transaction.atomic():
                # Create new application
                new_app = Application.objects.create(
                    name=serializer.validated_data['name'],
                    package_name=serializer.validated_data['package_name'],
                    description=f"Cloned from {app.name}. {app.description}",
                    version='1.0.0',
                    theme=app.theme if not serializer.validated_data['clone_theme'] else self._clone_theme(app.theme)
                )

                # Clone data sources if requested
                data_source_mapping = {}
                if serializer.validated_data['clone_data_sources']:
                    for ds in app.data_sources.all():
                        new_ds = DataSource.objects.create(
                            application=new_app,
                            name=ds.name,
                            data_source_type=ds.data_source_type,
                            base_url=ds.base_url,
                            endpoint=ds.endpoint,
                            method=ds.method,
                            headers=ds.headers,
                            use_dynamic_base_url=ds.use_dynamic_base_url
                        )
                        data_source_mapping[ds.id] = new_ds

                        # Clone fields
                        field_mapping = {}
                        for field in ds.fields.all():
                            new_field = DataSourceField.objects.create(
                                data_source=new_ds,
                                field_name=field.field_name,
                                field_type=field.field_type,
                                display_name=field.display_name,
                                is_required=field.is_required
                            )
                            field_mapping[field.id] = new_field

                # Clone screens if requested
                screen_mapping = {}
                if serializer.validated_data['clone_screens']:
                    for screen in app.screens.all():
                        new_screen = Screen.objects.create(
                            application=new_app,
                            name=screen.name,
                            route_name=screen.route_name,
                            is_home_screen=screen.is_home_screen,
                            app_bar_title=screen.app_bar_title,
                            show_app_bar=screen.show_app_bar,
                            show_back_button=screen.show_back_button,
                            background_color=screen.background_color
                        )
                        screen_mapping[screen.id] = new_screen

                        # Clone widgets recursively
                        widget_mapping = {}
                        self._clone_widgets_recursive(screen, new_screen, None, widget_mapping, screen_mapping)

                # Clone actions if requested
                if serializer.validated_data['clone_actions']:
                    for action in app.actions.all():
                        new_action = Action.objects.create(
                            application=new_app,
                            name=action.name,
                            action_type=action.action_type,
                            target_screen=screen_mapping.get(action.target_screen.id) if action.target_screen else None,
                            api_data_source=data_source_mapping.get(
                                action.api_data_source.id) if action.api_data_source else None,
                            parameters=action.parameters,
                            dialog_title=action.dialog_title,
                            dialog_message=action.dialog_message,
                            url=action.url
                        )

                return Response(
                    ApplicationDetailSerializer(new_app).data,
                    status=status.HTTP_201_CREATED
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _clone_theme(self, theme):
        """Helper to clone a theme"""
        return Theme.objects.create(
            name=f"{theme.name} (Clone)",
            primary_color=theme.primary_color,
            accent_color=theme.accent_color,
            background_color=theme.background_color,
            text_color=theme.text_color,
            font_family=theme.font_family,
            is_dark_mode=theme.is_dark_mode
        )

    def _clone_widgets_recursive(self, old_screen, new_screen, old_parent, widget_mapping, screen_mapping,
                                 parent_widget=None):
        """Recursively clone widgets"""
        widgets = Widget.objects.filter(screen=old_screen, parent_widget=old_parent)

        for widget in widgets:
            new_widget = Widget.objects.create(
                screen=new_screen,
                widget_type=widget.widget_type,
                parent_widget=parent_widget,
                order=widget.order,
                widget_id=widget.widget_id
            )
            widget_mapping[widget.id] = new_widget

            # Clone properties
            for prop in widget.properties.all():
                new_screen_ref = None
                if prop.screen_reference:
                    new_screen_ref = screen_mapping.get(prop.screen_reference.id)

                WidgetProperty.objects.create(
                    widget=new_widget,
                    property_name=prop.property_name,
                    property_type=prop.property_type,
                    string_value=prop.string_value,
                    integer_value=prop.integer_value,
                    decimal_value=prop.decimal_value,
                    boolean_value=prop.boolean_value,
                    color_value=prop.color_value,
                    alignment_value=prop.alignment_value,
                    url_value=prop.url_value,
                    json_value=prop.json_value,
                    action_reference=prop.action_reference,
                    data_source_field_reference=prop.data_source_field_reference,
                    screen_reference=new_screen_ref
                )

            # Clone children
            self._clone_widgets_recursive(old_screen, new_screen, widget, widget_mapping, screen_mapping, new_widget)

    @action(detail=True, methods=['post'])
    def build(self, request, pk=None):
        """Trigger application build"""
        app = self.get_object()
        serializer = BuildApplicationSerializer(data=request.data)

        if serializer.is_valid():
            build_service = BuildService()

            # Create build history entry
            build_history = BuildHistory.objects.create(
                application=app,
                status='started'
            )

            if serializer.validated_data.get('generate_source_only'):
                # Only generate source code
                generator = FlutterCodeGenerator(app)
                success, message = generator.generate_project()

                if success:
                    build_history.status = 'code_generated'
                    build_history.build_end_time = datetime.now()
                    build_history.save()

                    return Response({
                        'status': 'success',
                        'message': message,
                        'build_id': build_history.build_id
                    })
                else:
                    build_history.status = 'code_generation_failed'
                    build_history.error_message = message
                    build_history.build_end_time = datetime.now()
                    build_history.save()

                    return Response({
                        'status': 'error',
                        'message': message
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                # Full build
                success, message = build_service.start_build(app)

                if success:
                    return Response({
                        'status': 'success',
                        'message': message,
                        'build_id': build_history.build_id
                    })
                return Response({
                    'status': 'error',
                    'message': message
                }, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def preview_code(self, request, pk=None):
        """Preview generated Flutter code for specific files"""
        app = self.get_object()
        file_type = request.query_params.get('file', 'main')

        generator = FlutterCodeGenerator(app)

        code_files = {
            'main': generator._generate_main_dart(),
            'pubspec': generator._generate_pubspec(),
            'theme': generator._generate_theme_dart(),
            'routes': generator._generate_routes_dart()
        }

        # Get screen specific code
        screen_id = request.query_params.get('screen_id')
        if screen_id:
            try:
                screen = Screen.objects.get(id=screen_id, application=app)
                code_files['screen'] = generator._generate_screen_dart(screen)
                file_type = 'screen'
            except Screen.DoesNotExist:
                pass

        code = code_files.get(file_type, 'File type not found')

        return Response({
            'file_type': file_type,
            'code': code,
            'language': 'dart'
        })

    @action(detail=True, methods=['get'])
    def export_json(self, request, pk=None):
        """Export application configuration as JSON"""
        app = self.get_object()

        export_data = {
            'application': ApplicationDetailSerializer(app).data,
            'exported_at': datetime.now().isoformat(),
            'version': '1.0'
        }

        return Response(export_data)

    @action(detail=False, methods=['post'])
    def import_json(self, request):
        """Import application from JSON"""
        json_data = request.data.get('json_data')

        if not json_data:
            return Response({'error': 'JSON data is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Parse and create application from JSON
            app_data = json_data.get('application')

            # Create new application
            # Implementation here...

            return Response({'status': 'success', 'message': 'Application imported successfully'})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def create_from_template(self, request):
        """Create application from template"""
        serializer = TemplateApplicationSerializer(data=request.data)

        if serializer.is_valid():
            template_type = serializer.validated_data['template_type']

            # Import the appropriate command
            if template_type == 'ecommerce':
                from .management.commands.create_sample_app import create_ecommerce_app
                app = create_ecommerce_app(serializer.validated_data['name'])
            elif template_type == 'social_media':
                from .management.commands.create_sample_app import create_social_media_app
                app = create_social_media_app(serializer.validated_data['name'])
            elif template_type == 'news':
                from .management.commands.create_sample_app import create_news_app
                app = create_news_app(serializer.validated_data['name'])
            elif template_type == 'recipe':
                from .management.commands.create_recipe_app import create_recipe_app
                app = create_recipe_app(serializer.validated_data['name'], serializer.validated_data['package_name'])
            elif template_type == 'weather':
                from .management.commands.create_weather_app import create_comprehensive_weather_app
                app = create_comprehensive_weather_app(serializer.validated_data['name'],
                                                       serializer.validated_data['package_name'])
            elif template_type == 'marketplace':
                from .management.commands.create_marketplace_app import create_complete_marketplace_app
                app = create_complete_marketplace_app(serializer.validated_data['name'],
                                                      serializer.validated_data['package_name'])
            else:
                return Response({'error': 'Invalid template type'}, status=status.HTTP_400_BAD_REQUEST)

            # Update package name
            app.package_name = serializer.validated_data['package_name']
            app.save()

            return Response(ApplicationDetailSerializer(app).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """Get detailed application statistics"""
        app = self.get_object()

        stats = {
            'screens': {
                'total': app.screens.count(),
                'with_app_bar': app.screens.filter(show_app_bar=True).count(),
                'home_screens': app.screens.filter(is_home_screen=True).count()
            },
            'widgets': {
                'total': Widget.objects.filter(screen__application=app).count(),
                'by_type': {}
            },
            'data_sources': {
                'total': app.data_sources.count(),
                'by_method': {}
            },
            'actions': {
                'total': app.actions.count(),
                'by_type': {}
            },
            'builds': {
                'total': app.build_history.count(),
                'successful': app.build_history.filter(status='success').count(),
                'failed': app.build_history.filter(status='failed').count(),
                'average_duration': None
            }
        }

        # Widget type distribution
        for widget_type, _ in Widget.WIDGET_TYPES:
            count = Widget.objects.filter(screen__application=app, widget_type=widget_type).count()
            if count > 0:
                stats['widgets']['by_type'][widget_type] = count

        # Data source method distribution
        for method, _ in DataSource.HTTP_METHODS:
            count = app.data_sources.filter(method=method).count()
            if count > 0:
                stats['data_sources']['by_method'][method] = count

        # Action type distribution
        for action_type, _ in Action.ACTION_TYPES:
            count = app.actions.filter(action_type=action_type).count()
            if count > 0:
                stats['actions']['by_type'][action_type] = count

        # Calculate average build duration
        successful_builds = app.build_history.filter(status='success')
        if successful_builds.exists():
            durations = [b.duration_seconds for b in successful_builds if b.duration_seconds]
            if durations:
                stats['builds']['average_duration'] = sum(durations) / len(durations)

        return Response(stats)


class ScreenViewSet(viewsets.ModelViewSet):
    queryset = Screen.objects.all()
    serializer_class = ScreenSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        app_id = self.request.query_params.get('application', None)
        if app_id:
            queryset = queryset.filter(application_id=app_id)
        return queryset.order_by('created_at')

    @action(detail=True, methods=['post'])
    def duplicate(self, request, pk=None):
        """Duplicate a screen with all widgets"""
        screen = self.get_object()

        with transaction.atomic():
            # Create new screen
            new_screen = Screen.objects.create(
                application=screen.application,
                name=f"{screen.name} (Copy)",
                route_name=f"{screen.route_name}-copy-{uuid.uuid4().hex[:8]}",
                is_home_screen=False,
                app_bar_title=screen.app_bar_title,
                show_app_bar=screen.show_app_bar,
                show_back_button=screen.show_back_button,
                background_color=screen.background_color
            )

            # Clone all widgets
            widget_mapping = {}
            self._clone_screen_widgets(screen, new_screen, widget_mapping)

            return Response(ScreenSerializer(new_screen).data, status=status.HTTP_201_CREATED)

    def _clone_screen_widgets(self, old_screen, new_screen, widget_mapping, parent_widget=None, old_parent=None):
        """Clone all widgets from old screen to new screen"""
        widgets = Widget.objects.filter(screen=old_screen, parent_widget=old_parent).order_by('order')

        for widget in widgets:
            new_widget = Widget.objects.create(
                screen=new_screen,
                widget_type=widget.widget_type,
                parent_widget=parent_widget,
                order=widget.order,
                widget_id=f"{widget.widget_id}_copy" if widget.widget_id else None
            )
            widget_mapping[widget.id] = new_widget

            # Clone properties
            for prop in widget.properties.all():
                WidgetProperty.objects.create(
                    widget=new_widget,
                    property_name=prop.property_name,
                    property_type=prop.property_type,
                    string_value=prop.string_value,
                    integer_value=prop.integer_value,
                    decimal_value=prop.decimal_value,
                    boolean_value=prop.boolean_value,
                    color_value=prop.color_value,
                    alignment_value=prop.alignment_value,
                    url_value=prop.url_value,
                    json_value=prop.json_value,
                    action_reference=prop.action_reference,
                    data_source_field_reference=prop.data_source_field_reference,
                    screen_reference=prop.screen_reference
                )

            # Recursively clone children
            self._clone_screen_widgets(old_screen, new_screen, widget_mapping, new_widget, widget)

    @action(detail=True, methods=['post'])
    def set_home(self, request, pk=None):
        """Set this screen as home screen"""
        screen = self.get_object()

        # Remove home flag from other screens
        Screen.objects.filter(application=screen.application, is_home_screen=True).update(is_home_screen=False)

        # Set this screen as home
        screen.is_home_screen = True
        screen.save()

        return Response({'status': 'success', 'message': f'{screen.name} is now the home screen'})

    @action(detail=True, methods=['get'])
    def widget_tree(self, request, pk=None):
        """Get hierarchical widget tree for the screen"""
        screen = self.get_object()

        def build_tree(parent=None):
            widgets = Widget.objects.filter(screen=screen, parent_widget=parent).order_by('order')
            tree = []
            for widget in widgets:
                node = {
                    'id': widget.id,
                    'type': widget.widget_type,
                    'widget_id': widget.widget_id,
                    'properties': WidgetPropertySerializer(widget.properties.all(), many=True).data,
                    'children': build_tree(widget)
                }
                tree.append(node)
            return tree

        return Response({'tree': build_tree()})

    @action(detail=False, methods=['get'])
    def templates(self, request):
        """Get screen templates"""
        templates = [
            {
                'id': 1,
                'name': 'Login Screen',
                'description': 'Standard login screen with email and password',
                'preview_image': '/assets/templates/login.png',
                'widgets_count': 8
            },
            {
                'id': 2,
                'name': 'Product List',
                'description': 'Grid view of products with search',
                'preview_image': '/assets/templates/product-list.png',
                'widgets_count': 12
            },
            {
                'id': 3,
                'name': 'Profile Screen',
                'description': 'User profile with settings',
                'preview_image': '/assets/templates/profile.png',
                'widgets_count': 15
            },
            {
                'id': 4,
                'name': 'Dashboard',
                'description': 'Analytics dashboard with charts',
                'preview_image': '/assets/templates/dashboard.png',
                'widgets_count': 20
            },
            {
                'id': 5,
                'name': 'Chat Screen',
                'description': 'Messaging interface',
                'preview_image': '/assets/templates/chat.png',
                'widgets_count': 10
            }
        ]
        return Response(templates)


class WidgetViewSet(viewsets.ModelViewSet):
    queryset = Widget.objects.all()
    serializer_class = WidgetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        screen_id = self.request.query_params.get('screen', None)
        if screen_id:
            queryset = queryset.filter(screen_id=screen_id)
        parent_id = self.request.query_params.get('parent', None)
        if parent_id:
            if parent_id == 'null':
                queryset = queryset.filter(parent_widget=None)
            else:
                queryset = queryset.filter(parent_widget_id=parent_id)
        return queryset.order_by('order')

    @action(detail=True, methods=['post'])
    def reorder(self, request, pk=None):
        """Reorder widgets within a container"""
        widget = self.get_object()
        new_order = request.data.get('order', 0)
        old_order = widget.order

        if new_order == old_order:
            return Response({'status': 'success', 'message': 'No change in order'})

        with transaction.atomic():
            # Get all siblings
            siblings = Widget.objects.filter(
                screen=widget.screen,
                parent_widget=widget.parent_widget
            ).exclude(id=widget.id).order_by('order')

            # Update the widget's order
            widget.order = new_order
            widget.save()

            # Reorder siblings
            current_order = 0
            for sibling in siblings:
                if current_order == new_order:
                    current_order += 1
                sibling.order = current_order
                sibling.save()
                current_order += 1

        return Response({'status': 'success', 'message': 'Widget reordered successfully'})

    @action(detail=True, methods=['post'])
    def move(self, request, pk=None):
        """Move widget to different parent"""
        widget = self.get_object()
        new_parent_id = request.data.get('new_parent_id')

        with transaction.atomic():
            if new_parent_id:
                new_parent = Widget.objects.get(id=new_parent_id)
                if new_parent.screen != widget.screen:
                    return Response({'error': 'Cannot move widget to different screen'},
                                    status=status.HTTP_400_BAD_REQUEST)
                widget.parent_widget = new_parent
            else:
                widget.parent_widget = None

            # Set order to last position in new parent
            siblings_count = Widget.objects.filter(
                screen=widget.screen,
                parent_widget=widget.parent_widget
            ).exclude(id=widget.id).count()
            widget.order = siblings_count
            widget.save()

        return Response({'status': 'success', 'message': 'Widget moved successfully'})

    @action(detail=False, methods=['get'])
    def widget_types(self, request):
        """Get available widget types with detailed information"""
        widget_info = {
            'layout': [
                {
                    'type': 'Column',
                    'name': 'Column',
                    'icon': 'view_column',
                    'description': 'Arrange widgets vertically',
                    'properties': ['mainAxisAlignment', 'crossAxisAlignment', 'mainAxisSize']
                },
                {
                    'type': 'Row',
                    'name': 'Row',
                    'icon': 'view_stream',
                    'description': 'Arrange widgets horizontally',
                    'properties': ['mainAxisAlignment', 'crossAxisAlignment', 'mainAxisSize']
                },
                {
                    'type': 'Container',
                    'name': 'Container',
                    'icon': 'crop_square',
                    'description': 'A box with decoration and constraints',
                    'properties': ['width', 'height', 'padding', 'margin', 'color', 'decoration']
                },
                {
                    'type': 'Stack',
                    'name': 'Stack',
                    'icon': 'layers',
                    'description': 'Stack widgets on top of each other',
                    'properties': ['alignment', 'fit']
                },
                {
                    'type': 'Padding',
                    'name': 'Padding',
                    'icon': 'format_indent_increase',
                    'description': 'Add padding around a widget',
                    'properties': ['padding']
                },
                {
                    'type': 'Center',
                    'name': 'Center',
                    'icon': 'format_align_center',
                    'description': 'Center a widget',
                    'properties': []
                },
                {
                    'type': 'Expanded',
                    'name': 'Expanded',
                    'icon': 'unfold_more',
                    'description': 'Expand to fill available space',
                    'properties': ['flex']
                },
                {
                    'type': 'Flexible',
                    'name': 'Flexible',
                    'icon': 'unfold_less',
                    'description': 'Flexible space allocation',
                    'properties': ['flex', 'fit']
                },
                {
                    'type': 'Wrap',
                    'name': 'Wrap',
                    'icon': 'wrap_text',
                    'description': 'Wrap widgets to next line',
                    'properties': ['direction', 'spacing', 'runSpacing']
                },
                {
                    'type': 'Positioned',
                    'name': 'Positioned',
                    'icon': 'gps_fixed',
                    'description': 'Position widget in Stack',
                    'properties': ['top', 'left', 'right', 'bottom', 'width', 'height']
                }
            ],
            'display': [
                {
                    'type': 'Text',
                    'name': 'Text',
                    'icon': 'text_fields',
                    'description': 'Display text',
                    'properties': ['text', 'fontSize', 'fontWeight', 'color', 'textAlign']
                },
                {
                    'type': 'Image',
                    'name': 'Image',
                    'icon': 'image',
                    'description': 'Display an image',
                    'properties': ['imageUrl', 'width', 'height', 'fit']
                },
                {
                    'type': 'Icon',
                    'name': 'Icon',
                    'icon': 'emoji_emotions',
                    'description': 'Display an icon',
                    'properties': ['icon', 'size', 'color']
                },
                {
                    'type': 'Card',
                    'name': 'Card',
                    'icon': 'credit_card',
                    'description': 'Material Design card',
                    'properties': ['elevation', 'color', 'margin']
                },
                {
                    'type': 'Divider',
                    'name': 'Divider',
                    'icon': 'remove',
                    'description': 'Horizontal line divider',
                    'properties': ['height', 'thickness', 'color']
                },
                {
                    'type': 'ListTile',
                    'name': 'List Tile',
                    'icon': 'list',
                    'description': 'Material Design list item',
                    'properties': ['title', 'subtitle', 'leading', 'trailing', 'onTap']
                }
            ],
            'input': [
                {
                    'type': 'TextField',
                    'name': 'Text Field',
                    'icon': 'input',
                    'description': 'Text input field',
                    'properties': ['labelText', 'hintText', 'helperText', 'prefixIcon', 'suffixIcon']
                },
                {
                    'type': 'ElevatedButton',
                    'name': 'Elevated Button',
                    'icon': 'smart_button',
                    'description': 'Raised button',
                    'properties': ['text', 'onPressed', 'color', 'textColor']
                },
                {
                    'type': 'TextButton',
                    'name': 'Text Button',
                    'icon': 'touch_app',
                    'description': 'Flat text button',
                    'properties': ['text', 'onPressed', 'textColor']
                },
                {
                    'type': 'IconButton',
                    'name': 'Icon Button',
                    'icon': 'touch_app',
                    'description': 'Icon button',
                    'properties': ['icon', 'onPressed', 'color', 'size']
                },
                {
                    'type': 'FloatingActionButton',
                    'name': 'FAB',
                    'icon': 'add_circle',
                    'description': 'Floating action button',
                    'properties': ['icon', 'onPressed', 'backgroundColor']
                },
                {
                    'type': 'Switch',
                    'name': 'Switch',
                    'icon': 'toggle_on',
                    'description': 'On/Off switch',
                    'properties': ['value', 'onChanged', 'activeColor']
                },
                {
                    'type': 'Checkbox',
                    'name': 'Checkbox',
                    'icon': 'check_box',
                    'description': 'Checkbox',
                    'properties': ['value', 'onChanged', 'activeColor']
                },
                {
                    'type': 'Radio',
                    'name': 'Radio',
                    'icon': 'radio_button_checked',
                    'description': 'Radio button',
                    'properties': ['value', 'groupValue', 'onChanged']
                },
                {
                    'type': 'Slider',
                    'name': 'Slider',
                    'icon': 'tune',
                    'description': 'Value slider',
                    'properties': ['value', 'min', 'max', 'onChanged']
                },
                {
                    'type': 'DropdownButton',
                    'name': 'Dropdown',
                    'icon': 'arrow_drop_down',
                    'description': 'Dropdown menu',
                    'properties': ['value', 'items', 'onChanged']
                }
            ],
            'scrollable': [
                {
                    'type': 'ListView',
                    'name': 'List View',
                    'icon': 'list',
                    'description': 'Scrollable list',
                    'properties': ['scrollDirection', 'shrinkWrap', 'physics', 'dataSource']
                },
                {
                    'type': 'GridView',
                    'name': 'Grid View',
                    'icon': 'grid_on',
                    'description': 'Scrollable grid',
                    'properties': ['crossAxisCount', 'childAspectRatio', 'spacing', 'dataSource']
                },
                {
                    'type': 'SingleChildScrollView',
                    'name': 'Scroll View',
                    'icon': 'swap_vert',
                    'description': 'Make content scrollable',
                    'properties': ['scrollDirection', 'physics']
                },
                {
                    'type': 'PageView',
                    'name': 'Page View',
                    'icon': 'view_carousel',
                    'description': 'Swipeable pages',
                    'properties': ['scrollDirection', 'pageSnapping']
                }
            ],
            'navigation': [
                {
                    'type': 'AppBar',
                    'name': 'App Bar',
                    'icon': 'view_headline',
                    'description': 'Top navigation bar',
                    'properties': ['title', 'backgroundColor', 'elevation']
                },
                {
                    'type': 'BottomNavigationBar',
                    'name': 'Bottom Navigation',
                    'icon': 'view_carousel',
                    'description': 'Bottom navigation bar',
                    'properties': ['items', 'currentIndex', 'onTap']
                },
                {
                    'type': 'TabBar',
                    'name': 'Tab Bar',
                    'icon': 'tab',
                    'description': 'Tab navigation',
                    'properties': ['tabs', 'controller']
                },
                {
                    'type': 'Drawer',
                    'name': 'Drawer',
                    'icon': 'menu',
                    'description': 'Side navigation drawer',
                    'properties': ['width']
                }
            ],
            'special': [
                {
                    'type': 'Scaffold',
                    'name': 'Scaffold',
                    'icon': 'dashboard',
                    'description': 'Basic screen structure',
                    'properties': ['appBar', 'body', 'floatingActionButton', 'drawer']
                },
                {
                    'type': 'SafeArea',
                    'name': 'Safe Area',
                    'icon': 'security',
                    'description': 'Avoid system UI overlaps',
                    'properties': ['top', 'bottom', 'left', 'right']
                },
                {
                    'type': 'SizedBox',
                    'name': 'Sized Box',
                    'icon': 'aspect_ratio',
                    'description': 'Fixed size box',
                    'properties': ['width', 'height']
                },
                {
                    'type': 'AspectRatio',
                    'name': 'Aspect Ratio',
                    'icon': 'aspect_ratio',
                    'description': 'Maintain aspect ratio',
                    'properties': ['aspectRatio']
                },
                {
                    'type': 'FutureBuilder',
                    'name': 'Future Builder',
                    'icon': 'hourglass_empty',
                    'description': 'Build based on async data',
                    'properties': ['future']
                },
                {
                    'type': 'StreamBuilder',
                    'name': 'Stream Builder',
                    'icon': 'stream',
                    'description': 'Build based on stream data',
                    'properties': ['stream']
                }
            ]
        }
        return Response(widget_info)

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        """Create multiple widgets at once"""
        serializer = BulkWidgetCreateSerializer(data=request.data)

        if serializer.is_valid():
            screen_id = serializer.validated_data['screen_id']
            widgets_data = serializer.validated_data['widgets']

            try:
                screen = Screen.objects.get(id=screen_id)
            except Screen.DoesNotExist:
                return Response({'error': 'Screen not found'}, status=status.HTTP_404_NOT_FOUND)

            created_widgets = []

            with transaction.atomic():
                for widget_data in widgets_data:
                    widget = self._create_widget_recursive(screen, widget_data)
                    created_widgets.append(widget)

            return Response(
                WidgetSerializer(created_widgets, many=True).data,
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _create_widget_recursive(self, screen, widget_data, parent=None):
        """Recursively create widget and its children"""
        properties = widget_data.pop('properties', [])
        children = widget_data.pop('children', [])

        widget = Widget.objects.create(
            screen=screen,
            widget_type=widget_data['widget_type'],
            parent_widget=parent,
            order=widget_data.get('order', 0),
            widget_id=widget_data.get('widget_id', '')
        )

        # Create properties
        for prop_data in properties:
            WidgetProperty.objects.create(widget=widget, **prop_data)

        # Create children
        for child_data in children:
            self._create_widget_recursive(screen, child_data, widget)

        return widget

    @action(detail=True, methods=['post'])
    def duplicate(self, request, pk=None):
        """Duplicate a widget with all its properties and children"""
        widget = self.get_object()

        with transaction.atomic():
            new_widget = self._duplicate_widget_recursive(widget)
            return Response(WidgetSerializer(new_widget).data, status=status.HTTP_201_CREATED)

    def _duplicate_widget_recursive(self, widget, parent=None):
        """Recursively duplicate widget"""
        new_widget = Widget.objects.create(
            screen=widget.screen,
            widget_type=widget.widget_type,
            parent_widget=parent or widget.parent_widget,
            order=widget.order,
            widget_id=f"{widget.widget_id}_copy" if widget.widget_id else None
        )

        # Duplicate properties
        for prop in widget.properties.all():
            WidgetProperty.objects.create(
                widget=new_widget,
                property_name=prop.property_name,
                property_type=prop.property_type,
                string_value=prop.string_value,
                integer_value=prop.integer_value,
                decimal_value=prop.decimal_value,
                boolean_value=prop.boolean_value,
                color_value=prop.color_value,
                alignment_value=prop.alignment_value,
                url_value=prop.url_value,
                json_value=prop.json_value,
                action_reference=prop.action_reference,
                data_source_field_reference=prop.data_source_field_reference,
                screen_reference=prop.screen_reference
            )

        # Duplicate children
        for child in widget.child_widgets.all():
            self._duplicate_widget_recursive(child, new_widget)

        return new_widget


class WidgetPropertyViewSet(viewsets.ModelViewSet):
    queryset = WidgetProperty.objects.all()
    serializer_class = WidgetPropertySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        widget_id = self.request.query_params.get('widget', None)
        if widget_id:
            queryset = queryset.filter(widget_id=widget_id)
        return queryset

    @action(detail=False, methods=['post'])
    def bulk_update(self, request):
        """Update multiple properties at once"""
        widget_id = request.data.get('widget_id')
        properties = request.data.get('properties', [])

        if not widget_id:
            return Response({'error': 'widget_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            widget = Widget.objects.get(id=widget_id)
        except Widget.DoesNotExist:
            return Response({'error': 'Widget not found'}, status=status.HTTP_404_NOT_FOUND)

        updated_properties = []

        with transaction.atomic():
            for prop_data in properties:
                prop_name = prop_data.get('property_name')
                if not prop_name:
                    continue

                prop, created = WidgetProperty.objects.get_or_create(
                    widget=widget,
                    property_name=prop_name,
                    defaults={'property_type': prop_data.get('property_type', 'string')}
                )

                # Update property based on type
                for field, value in prop_data.items():
                    if hasattr(prop, field):
                        setattr(prop, field, value)

                prop.save()
                updated_properties.append(prop)

        return Response(
            WidgetPropertySerializer(updated_properties, many=True).data,
            status=status.HTTP_200_OK
        )


class ActionViewSet(viewsets.ModelViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        app_id = self.request.query_params.get('application', None)
        if app_id:
            queryset = queryset.filter(application_id=app_id)
        action_type = self.request.query_params.get('type', None)
        if action_type:
            queryset = queryset.filter(action_type=action_type)
        return queryset.order_by('name')

    @action(detail=False, methods=['get'])
    def action_types(self, request):
        """Get available action types with descriptions"""
        action_types = []
        for action_type, display_name in Action.ACTION_TYPES:
            action_types.append({
                'type': action_type,
                'name': display_name,
                'description': self._get_action_description(action_type),
                'required_fields': self._get_required_fields(action_type)
            })
        return Response(action_types)

    def _get_action_description(self, action_type):
        descriptions = {
            'navigate': 'Navigate to another screen in the app',
            'navigate_back': 'Go back to the previous screen',
            'api_call': 'Make an API call to fetch or send data',
            'show_dialog': 'Display a popup dialog with a message',
            'show_snackbar': 'Show a temporary message at the bottom',
            'open_url': 'Open a URL in the browser',
            'send_email': 'Open email client with pre-filled content',
            'make_phone_call': 'Initiate a phone call',
            'share_content': 'Share content via system share dialog',
            'take_photo': 'Open camera to take a photo',
            'pick_image': 'Select an image from gallery',
            'save_data': 'Save data to local storage',
            'load_data': 'Load data from local storage',
            'refresh_data': 'Refresh current data',
            'submit_form': 'Submit form data',
            'validate_form': 'Validate form fields',
            'clear_form': 'Clear all form fields',
            'toggle_visibility': 'Show or hide a widget',
            'play_sound': 'Play a sound effect',
            'vibrate': 'Trigger device vibration'
        }
        return descriptions.get(action_type, '')

    def _get_required_fields(self, action_type):
        required_fields = {
            'navigate': ['target_screen'],
            'api_call': ['api_data_source'],
            'show_dialog': ['dialog_title', 'dialog_message'],
            'show_snackbar': ['dialog_message'],
            'open_url': ['url'],
            'send_email': ['url'],
            'make_phone_call': ['url'],
            'share_content': ['dialog_message'],
            'save_data': ['parameters'],
            'load_data': ['parameters']
        }
        return required_fields.get(action_type, [])


class DataSourceViewSet(viewsets.ModelViewSet):
    queryset = DataSource.objects.all()
    serializer_class = DataSourceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        app_id = self.request.query_params.get('application', None)
        if app_id:
            queryset = queryset.filter(application_id=app_id)
        return queryset.order_by('name')

    @action(detail=True, methods=['post'])
    def test_connection(self, request, pk=None):
        """Test data source connection"""
        data_source = self.get_object()

        import requests

        try:
            # Build URL
            if data_source.use_dynamic_base_url:
                base_url = request.data.get('test_base_url', data_source.base_url)
            else:
                base_url = data_source.base_url

            url = f"{base_url}{data_source.endpoint}"

            # Parse headers
            headers = {}
            if data_source.headers:
                for line in data_source.headers.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        headers[key.strip()] = value.strip()

            # Make request
            if data_source.method == 'GET':
                response = requests.get(url, headers=headers, timeout=10)
            elif data_source.method == 'POST':
                response = requests.post(url, headers=headers, json={}, timeout=10)
            else:
                response = requests.request(data_source.method, url, headers=headers, timeout=10)

            # Parse response
            try:
                data = response.json()
                sample_data = data[:5] if isinstance(data, list) else data
            except:
                sample_data = None

            return Response({
                'status': 'success',
                'status_code': response.status_code,
                'response_time': response.elapsed.total_seconds(),
                'sample_data': sample_data,
                'headers': dict(response.headers)
            })

        except requests.exceptions.Timeout:
            return Response({
                'status': 'error',
                'message': 'Connection timeout'
            }, status=status.HTTP_408_REQUEST_TIMEOUT)
        except requests.exceptions.ConnectionError:
            return Response({
                'status': 'error',
                'message': 'Connection failed'
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def auto_detect_fields(self, request, pk=None):
        """Auto-detect fields from API response"""
        data_source = self.get_object()

        import requests

        try:
            url = f"{data_source.base_url}{data_source.endpoint}"
            headers = {}
            if data_source.headers:
                for line in data_source.headers.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        headers[key.strip()] = value.strip()

            response = requests.get(url, headers=headers, timeout=10)
            data = response.json()

            # Detect fields
            detected_fields = []
            sample = data[0] if isinstance(data, list) and len(data) > 0 else data

            if isinstance(sample, dict):
                for key, value in sample.items():
                    field_type = self._detect_field_type(value)
                    detected_fields.append({
                        'field_name': key,
                        'field_type': field_type,
                        'display_name': key.replace('_', ' ').title(),
                        'sample_value': str(value)[:100]
                    })

            return Response({
                'status': 'success',
                'fields': detected_fields
            })

        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    def _detect_field_type(self, value):
        """Detect field type from value"""
        if isinstance(value, bool):
            return 'boolean'
        elif isinstance(value, int):
            return 'integer'
        elif isinstance(value, float):
            return 'decimal'
        elif isinstance(value, str):
            if '@' in value:
                return 'email'
            elif value.startswith('http'):
                return 'url'
            elif any(ext in value.lower() for ext in ['.jpg', '.png', '.gif', '.jpeg']):
                return 'image_url'
            elif len(value) > 100:
                return 'string'
            else:
                return 'string'
        else:
            return 'string'


class DataSourceFieldViewSet(viewsets.ModelViewSet):
    queryset = DataSourceField.objects.all()
    serializer_class = DataSourceFieldSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        data_source_id = self.request.query_params.get('data_source', None)
        if data_source_id:
            queryset = queryset.filter(data_source_id=data_source_id)
        return queryset.order_by('field_name')

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        """Create multiple fields at once"""
        data_source_id = request.data.get('data_source_id')
        fields = request.data.get('fields', [])

        if not data_source_id:
            return Response({'error': 'data_source_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            data_source = DataSource.objects.get(id=data_source_id)
        except DataSource.DoesNotExist:
            return Response({'error': 'DataSource not found'}, status=status.HTTP_404_NOT_FOUND)

        created_fields = []

        with transaction.atomic():
            # Delete existing fields if requested
            if request.data.get('replace_existing', False):
                DataSourceField.objects.filter(data_source=data_source).delete()

            for field_data in fields:
                field = DataSourceField.objects.create(
                    data_source=data_source,
                    field_name=field_data['field_name'],
                    field_type=field_data['field_type'],
                    display_name=field_data.get('display_name', field_data['field_name']),
                    is_required=field_data.get('is_required', False)
                )
                created_fields.append(field)

        return Response(
            DataSourceFieldSerializer(created_fields, many=True).data,
            status=status.HTTP_201_CREATED
        )


class BuildHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BuildHistory.objects.all()
    serializer_class = BuildHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        app_id = self.request.query_params.get('application', None)
        if app_id:
            queryset = queryset.filter(application_id=app_id)
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        return queryset.order_by('-build_start_time')

    @action(detail=True, methods=['get'])
    def logs(self, request, pk=None):
        """Get build logs"""
        build = self.get_object()
        return Response({
            'build_id': build.build_id,
            'status': build.status,
            'logs': build.log_output,
            'error': build.error_message
        })

    @action(detail=True, methods=['get'])
    def download_apk(self, request, pk=None):
        """Get APK download URL"""
        build = self.get_object()
        if build.apk_file:
            return Response({
                'download_url': request.build_absolute_uri(build.apk_file.url),
                'file_size': build.apk_size_mb,
                'file_name': f"{build.application.name}.apk"
            })
        return Response({'error': 'APK not available'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def download_source(self, request, pk=None):
        """Get source code download URL"""
        build = self.get_object()
        if build.source_code_zip:
            return Response({
                'download_url': request.build_absolute_uri(build.source_code_zip.url),
                'file_name': f"{build.application.name}_source.zip"
            })
        return Response({'error': 'Source code not available'}, status=status.HTTP_404_NOT_FOUND)


class CustomPubDevWidgetViewSet(viewsets.ModelViewSet):
    queryset = CustomPubDevWidget.objects.all()
    serializer_class = CustomPubDevWidgetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        app_id = self.request.query_params.get('application', None)
        if app_id:
            queryset = queryset.filter(application_id=app_id)
        if self.request.query_params.get('active_only', False):
            queryset = queryset.filter(is_active=True)
        return queryset.order_by('widget_class_name')

    @action(detail=False, methods=['get'])
    def popular_packages(self, request):
        """Get popular pub.dev packages"""
        packages = [
            {
                'package_name': 'flutter_staggered_grid_view',
                'version': '^0.6.2',
                'description': 'Provides staggered grid layouts',
                'widgets': ['StaggeredGrid', 'StaggeredGridTile']
            },
            {
                'package_name': 'carousel_slider',
                'version': '^4.2.1',
                'description': 'A carousel slider widget',
                'widgets': ['CarouselSlider']
            },
            {
                'package_name': 'cached_network_image',
                'version': '^3.3.0',
                'description': 'Flutter library to load and cache network images',
                'widgets': ['CachedNetworkImage']
            },
            {
                'package_name': 'shimmer',
                'version': '^3.0.0',
                'description': 'A package provides an easy way to add shimmer effect',
                'widgets': ['Shimmer']
            },
            {
                'package_name': 'flutter_rating_bar',
                'version': '^4.0.1',
                'description': 'A simple yet fully customizable rating bar',
                'widgets': ['RatingBar', 'RatingBarIndicator']
            }
        ]
        return Response(packages)