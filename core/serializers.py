from rest_framework import serializers
from .models import (
    Theme, Application, DataSource, DataSourceField,
    Screen, Widget, WidgetProperty, Action, BuildHistory,
    CustomPubDevWidget
)
from django.contrib.auth.models import User
import json


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'is_active')
        read_only_fields = ('id', 'date_joined')


class ThemeSerializer(serializers.ModelSerializer):
    applications_count = serializers.SerializerMethodField()

    class Meta:
        model = Theme
        fields = ('id', 'name', 'primary_color', 'accent_color', 'background_color',
                  'text_color', 'font_family', 'is_dark_mode', 'created_at',
                  'updated_at', 'applications_count')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def get_applications_count(self, obj):
        return obj.application_set.count()


class DataSourceFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSourceField
        fields = ('id', 'data_source', 'field_name', 'field_type', 'display_name',
                  'is_required', 'created_at')
        read_only_fields = ('id', 'created_at')


class DataSourceSerializer(serializers.ModelSerializer):
    fields = DataSourceFieldSerializer(many=True, read_only=True)
    fields_count = serializers.SerializerMethodField()

    class Meta:
        model = DataSource
        fields = ('id', 'application', 'name', 'data_source_type', 'base_url',
                  'endpoint', 'method', 'headers', 'use_dynamic_base_url',
                  'created_at', 'updated_at', 'fields', 'fields_count')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def get_fields_count(self, obj):
        return obj.fields.count()


class ActionSerializer(serializers.ModelSerializer):
    target_screen_name = serializers.SerializerMethodField()
    api_data_source_name = serializers.SerializerMethodField()

    class Meta:
        model = Action
        fields = ('id', 'application', 'name', 'action_type', 'target_screen',
                  'target_screen_name', 'api_data_source', 'api_data_source_name',
                  'parameters', 'dialog_title', 'dialog_message', 'url',
                  'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def get_target_screen_name(self, obj):
        return obj.target_screen.name if obj.target_screen else None

    def get_api_data_source_name(self, obj):
        return obj.api_data_source.name if obj.api_data_source else None


class WidgetPropertySerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()

    class Meta:
        model = WidgetProperty
        fields = ('id', 'widget', 'property_name', 'property_type', 'string_value',
                  'integer_value', 'decimal_value', 'boolean_value', 'color_value',
                  'alignment_value', 'url_value', 'json_value', 'action_reference',
                  'data_source_field_reference', 'screen_reference', 'created_at', 'value')
        read_only_fields = ('id', 'created_at')

    def get_value(self, obj):
        return obj.get_value()

    def validate(self, data):
        property_type = data.get('property_type')

        # Clear all value fields first
        value_fields = ['string_value', 'integer_value', 'decimal_value', 'boolean_value',
                        'color_value', 'alignment_value', 'url_value', 'json_value',
                        'action_reference', 'data_source_field_reference', 'screen_reference']

        # Validate that only the correct value field is set
        if property_type == 'string' and not data.get('string_value'):
            raise serializers.ValidationError("String value is required for string property type")
        elif property_type == 'integer' and data.get('integer_value') is None:
            raise serializers.ValidationError("Integer value is required for integer property type")
        elif property_type == 'decimal' and data.get('decimal_value') is None:
            raise serializers.ValidationError("Decimal value is required for decimal property type")
        elif property_type == 'boolean' and data.get('boolean_value') is None:
            raise serializers.ValidationError("Boolean value is required for boolean property type")
        elif property_type == 'color' and not data.get('color_value'):
            raise serializers.ValidationError("Color value is required for color property type")
        elif property_type == 'alignment' and not data.get('alignment_value'):
            raise serializers.ValidationError("Alignment value is required for alignment property type")
        elif property_type == 'url' and not data.get('url_value'):
            raise serializers.ValidationError("URL value is required for URL property type")
        elif property_type == 'json' and not data.get('json_value'):
            raise serializers.ValidationError("JSON value is required for JSON property type")
        elif property_type == 'action_reference' and not data.get('action_reference'):
            raise serializers.ValidationError("Action reference is required for action property type")
        elif property_type == 'data_source_field_reference' and not data.get('data_source_field_reference'):
            raise serializers.ValidationError("Data source field reference is required")
        elif property_type == 'screen_reference' and not data.get('screen_reference'):
            raise serializers.ValidationError("Screen reference is required for screen property type")

        return data


class WidgetSerializer(serializers.ModelSerializer):
    properties = WidgetPropertySerializer(many=True, read_only=True)
    child_widgets = serializers.SerializerMethodField()
    can_have_children = serializers.SerializerMethodField()

    class Meta:
        model = Widget
        fields = ('id', 'screen', 'widget_type', 'parent_widget', 'order',
                  'widget_id', 'properties', 'child_widgets', 'can_have_children',
                  'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def get_child_widgets(self, obj):
        children = obj.child_widgets.all().order_by('order')
        return WidgetSerializer(children, many=True).data

    def get_can_have_children(self, obj):
        container_widgets = ['Column', 'Row', 'Container', 'Stack', 'ListView',
                             'GridView', 'Wrap', 'Expanded', 'Flexible', 'Padding',
                             'Center', 'Card', 'Scaffold', 'SingleChildScrollView']
        return obj.widget_type in container_widgets


class ScreenSerializer(serializers.ModelSerializer):
    widgets = serializers.SerializerMethodField()
    widgets_count = serializers.SerializerMethodField()

    class Meta:
        model = Screen
        fields = ('id', 'application', 'name', 'route_name', 'is_home_screen',
                  'app_bar_title', 'show_app_bar', 'show_back_button',
                  'background_color', 'widgets', 'widgets_count',
                  'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def get_widgets(self, obj):
        root_widgets = obj.widgets.filter(parent_widget=None).order_by('order')
        return WidgetSerializer(root_widgets, many=True).data

    def get_widgets_count(self, obj):
        return obj.widgets.count()


class ApplicationListSerializer(serializers.ModelSerializer):
    theme_name = serializers.SerializerMethodField()
    screens_count = serializers.SerializerMethodField()
    last_build = serializers.SerializerMethodField()

    class Meta:
        model = Application
        fields = ('id', 'name', 'description', 'package_name', 'version',
                  'theme', 'theme_name', 'build_status', 'screens_count',
                  'last_build', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at', 'build_status')

    def get_theme_name(self, obj):
        return obj.theme.name if obj.theme else None

    def get_screens_count(self, obj):
        return obj.screens.count()

    def get_last_build(self, obj):
        last_build = obj.build_history.first()
        if last_build:
            return {
                'id': last_build.id,
                'status': last_build.status,
                'date': last_build.build_start_time
            }
        return None


class ApplicationDetailSerializer(serializers.ModelSerializer):
    theme = ThemeSerializer(read_only=True)
    theme_id = serializers.PrimaryKeyRelatedField(
        queryset=Theme.objects.all(),
        source='theme',
        write_only=True
    )
    screens = ScreenSerializer(many=True, read_only=True)
    data_sources = DataSourceSerializer(many=True, read_only=True)
    actions = ActionSerializer(many=True, read_only=True)
    custom_widgets = serializers.SerializerMethodField()
    statistics = serializers.SerializerMethodField()

    class Meta:
        model = Application
        fields = ('id', 'name', 'description', 'package_name', 'version', 'theme',
                  'theme_id', 'build_status', 'apk_file', 'source_code_zip',
                  'screens', 'data_sources', 'actions', 'custom_widgets',
                  'statistics', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at', 'build_status',
                            'apk_file', 'source_code_zip')

    def get_custom_widgets(self, obj):
        from .serializers import CustomPubDevWidgetSerializer
        return CustomPubDevWidgetSerializer(obj.custom_widgets.filter(is_active=True), many=True).data

    def get_statistics(self, obj):
        return {
            'screens_count': obj.screens.count(),
            'widgets_count': Widget.objects.filter(screen__application=obj).count(),
            'data_sources_count': obj.data_sources.count(),
            'actions_count': obj.actions.count(),
            'builds_count': obj.build_history.count(),
            'successful_builds': obj.build_history.filter(status='success').count()
        }


class BuildHistorySerializer(serializers.ModelSerializer):
    duration_seconds = serializers.ReadOnlyField()
    duration_display = serializers.SerializerMethodField()

    class Meta:
        model = BuildHistory
        fields = ('id', 'application', 'build_id', 'status', 'build_start_time',
                  'build_end_time', 'duration_seconds', 'duration_display',
                  'log_output', 'error_message', 'apk_file', 'source_code_zip',
                  'apk_size_mb')
        read_only_fields = ('id', 'build_id', 'build_start_time')

    def get_duration_display(self, obj):
        if obj.duration_seconds:
            minutes = int(obj.duration_seconds // 60)
            seconds = int(obj.duration_seconds % 60)
            return f"{minutes}m {seconds}s"
        return None


class CustomPubDevWidgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomPubDevWidget
        fields = ('id', 'application', 'package_name', 'package_version',
                  'widget_class_name', 'import_statement', 'description',
                  'is_active', 'created_at')
        read_only_fields = ('id', 'created_at')


class CloneApplicationSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, required=True)
    package_name = serializers.CharField(max_length=100, required=True)
    clone_screens = serializers.BooleanField(default=True)
    clone_data_sources = serializers.BooleanField(default=True)
    clone_actions = serializers.BooleanField(default=True)
    clone_theme = serializers.BooleanField(default=False)

    def validate_package_name(self, value):
        if Application.objects.filter(package_name=value).exists():
            raise serializers.ValidationError("Package name already exists")
        return value


class BuildApplicationSerializer(serializers.Serializer):
    build_type = serializers.ChoiceField(choices=['debug', 'release'], default='debug')
    clean_build = serializers.BooleanField(default=False)
    generate_source_only = serializers.BooleanField(default=False)


class WidgetTreeSerializer(serializers.Serializer):
    widget_type = serializers.CharField(max_length=50)
    parent_widget = serializers.IntegerField(required=False, allow_null=True)
    order = serializers.IntegerField(default=0)
    widget_id = serializers.CharField(max_length=100, required=False, allow_blank=True)
    properties = serializers.ListField(
        child=serializers.DictField(),
        required=False,
        default=list
    )
    children = serializers.ListField(
        child=serializers.DictField(),
        required=False,
        default=list
    )


class BulkWidgetCreateSerializer(serializers.Serializer):
    screen_id = serializers.IntegerField()
    widgets = serializers.ListField(
        child=WidgetTreeSerializer()
    )


class TemplateApplicationSerializer(serializers.Serializer):
    template_type = serializers.ChoiceField(
        choices=['ecommerce', 'social_media', 'news', 'recipe', 'weather', 'marketplace']
    )
    name = serializers.CharField(max_length=100)
    package_name = serializers.CharField(max_length=100)

    def validate_package_name(self, value):
        if Application.objects.filter(package_name=value).exists():
            raise serializers.ValidationError("Package name already exists")
        return value