import os

from django.contrib import admin
from django.http import HttpResponse, JsonResponse
from django.urls import path
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from flutter_nocode import settings
from .models import (
    Theme, Application, DataSource, DataSourceField, Screen, 
    Widget, WidgetProperty, Action, BuildHistory, CustomPubDevWidget
)
from .services.code_generator import FlutterCodeGenerator
from .services.build_service import BuildService
import json


class DataSourceFieldInline(admin.TabularInline):
    model = DataSourceField
    extra = 1
    fields = ('field_name', 'field_type', 'display_name', 'is_required')


class WidgetPropertyInline(admin.StackedInline):
    model = WidgetProperty
    extra = 0
    fields = (
        'property_name', 'property_type',
        'string_value', 'integer_value', 'decimal_value', 'boolean_value',
        'color_value', 'alignment_value', 'url_value', 'json_value',
        'action_reference', 'data_source_field_reference', 'screen_reference'
    )
    
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        
        # Filter references based on the widget's screen's application
        if obj and obj.screen:
            application = obj.screen.application
            
            # Filter actions to only show actions from the same application
            formset.form.base_fields['action_reference'].queryset = Action.objects.filter(
                application=application
            )
            
            # Filter data source fields to only show fields from the same application
            formset.form.base_fields['data_source_field_reference'].queryset = DataSourceField.objects.filter(
                data_source__application=application
            )
            
            # Filter screens to only show screens from the same application
            formset.form.base_fields['screen_reference'].queryset = Screen.objects.filter(
                application=application
            )
        
        return formset


class WidgetInline(admin.StackedInline):
    model = Widget
    extra = 0
    fields = ('widget_type', 'parent_widget', 'order', 'widget_id')
    ordering = ('order',)


class ScreenInline(admin.StackedInline):
    model = Screen
    extra = 1
    fields = (
        'name', 'route_name', 'is_home_screen',
        'show_app_bar', 'app_bar_title', 'show_back_button',
        'background_color'
    )


class ActionInline(admin.TabularInline):
    model = Action
    extra = 0
    fields = (
        'name', 'action_type', 'target_screen', 'api_data_source',
        'dialog_title', 'dialog_message', 'url'
    )


class BuildHistoryInline(admin.TabularInline):
    model = BuildHistory
    extra = 0
    readonly_fields = (
        'build_id', 'status', 'build_start_time', 'build_end_time',
        'duration_seconds', 'apk_size_mb'
    )
    fields = readonly_fields
    can_delete = False
    
    def has_add_permission(self, request, obj=None):
        return False


class CustomPubDevWidgetInline(admin.TabularInline):
    model = CustomPubDevWidget
    extra = 0
    fields = ('package_name', 'package_version', 'widget_class_name', 'import_statement', 'is_active')


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ('name', 'primary_color', 'accent_color', 'is_dark_mode', 'created_at')
    list_filter = ('is_dark_mode', 'created_at')
    search_fields = ('name',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('name',)
        }),
        ('Colors', {
            'fields': ('primary_color', 'accent_color', 'background_color', 'text_color'),
            'description': 'Choose the color scheme for your app'
        }),
        ('Typography', {
            'fields': ('font_family',)
        }),
        ('Mode', {
            'fields': ('is_dark_mode',)
        }),
    )


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'package_name', 'version', 'theme', 'build_status', 'updated_at')
    list_filter = ('build_status', 'theme', 'created_at')
    search_fields = ('name', 'package_name', 'description')
    readonly_fields = ('build_status', 'created_at', 'updated_at')
    
    fieldsets = (
        ('App Information', {
            'fields': ('name', 'description', 'package_name', 'version'),
            'description': 'Basic information about your Flutter application'
        }),
        ('Styling', {
            'fields': ('theme',),
            'description': 'Choose how your app looks'
        }),
        ('Build Status', {
            'fields': ('build_status',),
            'classes': ('collapse',)
        }),
        ('Generated Files', {
            'fields': ('apk_file', 'source_code_zip'),
            'classes': ('collapse',),
            'description': 'Download your built app and source code'
        }),
    )
    
    inlines = [ScreenInline, ActionInline, CustomPubDevWidgetInline, BuildHistoryInline]

    actions = ['generate_flutter_code', 'build_apk', 'clean_project_directory', 'create_sample_ecommerce',
               'create_sample_social_media', 'create_sample_news', 'create_full_marketplace']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:app_id>/download-apk/', self.admin_site.admin_view(self.download_apk), name='download_apk'),
            path('<int:app_id>/download-source/', self.admin_site.admin_view(self.download_source), name='download_source'),
            path('<int:app_id>/build-status/', self.admin_site.admin_view(self.build_status), name='build_status'),
        ]
        return custom_urls + urls

    def clean_project_directory(self, request, queryset):
        """Manually clean project directories"""
        import subprocess
        import shutil
        import time

        for app in queryset:
            project_path = settings.GENERATED_CODE_PATH / f"{app.package_name.replace('.', '_')}"

            if project_path.exists():
                try:
                    # Kill processes on Windows
                    if os.name == 'nt':
                        subprocess.run(['taskkill', '/F', '/IM', 'java.exe'], capture_output=True, shell=True)
                        subprocess.run(['taskkill', '/F', '/IM', 'gradle.exe'], capture_output=True, shell=True)
                        subprocess.run(['taskkill', '/F', '/IM', 'dart.exe'], capture_output=True, shell=True)
                        time.sleep(2)

                    # Remove directory
                    shutil.rmtree(project_path, ignore_errors=True)
                    self.message_user(request, f"Cleaned project directory for {app.name}")
                except Exception as e:
                    self.message_user(request, f"Error cleaning {app.name}: {str(e)}", level=messages.ERROR)
            else:
                self.message_user(request, f"No project directory found for {app.name}")

    clean_project_directory.short_description = "🧹 Clean Project Directory"

    def generate_flutter_code(self, request, queryset):
        """Generate Flutter source code for selected applications"""
        for app in queryset:
            try:
                generator = FlutterCodeGenerator(app)
                success, message = generator.generate_project()
                
                if success:
                    self.message_user(request, f"Flutter code generated successfully for {app.name}: {message}")
                else:
                    self.message_user(request, f"Failed to generate code for {app.name}: {message}", level=messages.ERROR)
            except Exception as e:
                self.message_user(request, f"Error generating code for {app.name}: {str(e)}", level=messages.ERROR)
    
    generate_flutter_code.short_description = "🔧 Generate Flutter Source Code"
    
    def build_apk(self, request, queryset):
        """Build APK for selected applications"""
        for app in queryset:
            try:
                build_service = BuildService()
                success, message = build_service.start_build(app)
                
                if success:
                    self.message_user(request, f"Build started for {app.name}: {message}")
                else:
                    self.message_user(request, f"Failed to start build for {app.name}: {message}", level=messages.ERROR)
            except Exception as e:
                self.message_user(request, f"Error starting build for {app.name}: {str(e)}", level=messages.ERROR)
    
    build_apk.short_description = "📱 Build APK File"
    
    def create_sample_ecommerce(self, request, queryset):
        """Create a sample e-commerce application"""
        from .management.commands.create_sample_app import create_ecommerce_app
        
        for app in queryset:
            try:
                create_ecommerce_app(app)
                self.message_user(request, f"Sample e-commerce structure created for {app.name}")
            except Exception as e:
                self.message_user(request, f"Error creating e-commerce sample for {app.name}: {str(e)}", level=messages.ERROR)
    
    create_sample_ecommerce.short_description = "🛒 Create E-commerce Sample"
    
    def create_sample_social_media(self, request, queryset):
        """Create a sample social media application"""
        from .management.commands.create_sample_app import create_social_media_app
        
        for app in queryset:
            try:
                create_social_media_app(app)
                self.message_user(request, f"Sample social media structure created for {app.name}")
            except Exception as e:
                self.message_user(request, f"Error creating social media sample for {app.name}: {str(e)}", level=messages.ERROR)
    
    create_sample_social_media.short_description = "📱 Create Social Media Sample"

    def create_sample_news(self, request, queryset):
        """Create a sample news application"""
        from .management.commands.create_sample_app import create_news_app

        for app in queryset:
            try:
                create_news_app(app)
                self.message_user(request, f"Sample news app structure created for {app.name}")
            except Exception as e:
                self.message_user(request, f"Error creating news sample for {app.name}: {str(e)}", level=messages.ERROR)

    create_sample_news.short_description = "📰 Create News App Sample"

    def create_full_marketplace(self, request, queryset):
        """Create a complete marketplace application"""
        from django.core.management import call_command

        for app in queryset:
            try:
                # Call the management command with the app's details
                call_command('create_full_marketplace',
                             name=app.name,
                             package=app.package_name)
                self.message_user(request, f"Full marketplace created for {app.name}")
            except Exception as e:
                self.message_user(request, f"Error creating marketplace: {str(e)}", level=messages.ERROR)

    create_full_marketplace.short_description = "🛍️ Create Full Marketplace"
    
    def download_apk(self, request, app_id):
        """Download APK file"""
        app = get_object_or_404(Application, id=app_id)
        if app.apk_file:
            response = HttpResponse(app.apk_file.read(), content_type='application/vnd.android.package-archive')
            response['Content-Disposition'] = f'attachment; filename="{app.name}.apk"'
            return response
        else:
            messages.error(request, "No APK file available. Please build the app first.")
            return redirect('admin:core_application_change', app_id)
    
    def download_source(self, request, app_id):
        """Download source code ZIP"""
        app = get_object_or_404(Application, id=app_id)
        if app.source_code_zip:
            response = HttpResponse(app.source_code_zip.read(), content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename="{app.name}_source.zip"'
            return response
        else:
            messages.error(request, "No source code available. Please generate code first.")
            return redirect('admin:core_application_change', app_id)
    
    def build_status(self, request, app_id):
        """Get build status as JSON"""
        app = get_object_or_404(Application, id=app_id)
        latest_build = app.build_history.first()
        
        data = {
            'status': app.build_status,
            'latest_build': None
        }
        
        if latest_build:
            data['latest_build'] = {
                'id': str(latest_build.build_id),
                'status': latest_build.status,
                'start_time': latest_build.build_start_time.isoformat(),
                'end_time': latest_build.build_end_time.isoformat() if latest_build.build_end_time else None,
                'duration': latest_build.duration_seconds,
                'error_message': latest_build.error_message,
                'apk_available': bool(latest_build.apk_file),
                'source_available': bool(latest_build.source_code_zip),
            }
        
        return JsonResponse(data)


@admin.register(DataSource)
class DataSourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'application', 'data_source_type', 'method', 'created_at')
    list_filter = ('data_source_type', 'method', 'application')
    search_fields = ('name', 'base_url', 'endpoint')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('application', 'name')
        }),
        ('API Configuration', {
            'fields': ('base_url', 'endpoint', 'method', 'headers'),
            'description': 'Configuration for REST API data sources'
        }),
    )
    
    inlines = [DataSourceFieldInline]


@admin.register(Screen)
class ScreenAdmin(admin.ModelAdmin):
    list_display = ('name', 'application', 'route_name', 'is_home_screen', 'show_app_bar')
    list_filter = ('application', 'is_home_screen', 'show_app_bar')
    search_fields = ('name', 'route_name', 'app_bar_title')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('application', 'name', 'route_name', 'is_home_screen')
        }),
        ('Top Bar Configuration', {
            'fields': ('show_app_bar', 'app_bar_title', 'show_back_button')
        }),
        ('Styling', {
            'fields': ('background_color',)
        }),
    )
    
    inlines = [WidgetInline]


@admin.register(Widget)
class WidgetAdmin(admin.ModelAdmin):
    list_display = ('widget_type', 'screen', 'parent_widget', 'order', 'widget_id')
    list_filter = ('widget_type', 'screen__application', 'screen')
    search_fields = ('widget_type', 'widget_id', 'screen__name')
    ordering = ('screen', 'order')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('screen', 'widget_type', 'widget_id')
        }),
        ('Layout', {
            'fields': ('parent_widget', 'order')
        }),
    )
    
    inlines = [WidgetPropertyInline]
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        
        # Filter parent_widget to only show widgets from the same screen
        if obj and obj.screen:
            form.base_fields['parent_widget'].queryset = Widget.objects.filter(
                screen=obj.screen
            ).exclude(id=obj.id if obj.id else None)
        
        return form


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ('name', 'application', 'action_type', 'target_screen', 'created_at')
    list_filter = ('action_type', 'application')
    search_fields = ('name', 'dialog_title', 'dialog_message')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('application', 'name', 'action_type')
        }),
        ('Navigation', {
            'fields': ('target_screen',),
            'description': 'For navigation actions'
        }),
        ('API Calls', {
            'fields': ('api_data_source',),
            'description': 'For API call actions'
        }),
        ('Dialogs and Messages', {
            'fields': ('dialog_title', 'dialog_message'),
            'description': 'For popup and message actions'
        }),
        ('URLs and External Actions', {
            'fields': ('url',),
            'description': 'For URL-based actions'
        }),
        ('Advanced', {
            'fields': ('parameters',),
            'classes': ('collapse',)
        }),
    )
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        
        # Filter target_screen and api_data_source based on application
        if obj and obj.application:
            form.base_fields['target_screen'].queryset = Screen.objects.filter(
                application=obj.application
            )
            form.base_fields['api_data_source'].queryset = DataSource.objects.filter(
                application=obj.application
            )
        
        return form


@admin.register(BuildHistory)
class BuildHistoryAdmin(admin.ModelAdmin):
    list_display = ('application', 'build_id_short', 'status', 'build_start_time', 'duration_display', 'apk_size_mb')
    list_filter = ('status', 'application', 'build_start_time')
    search_fields = ('application__name', 'build_id', 'error_message')
    readonly_fields = (
        'build_id', 'build_start_time', 'build_end_time', 'duration_seconds',
        'apk_size_mb', 'log_output', 'error_message'
    )
    ordering = ('-build_start_time',)
    
    fieldsets = (
        ('Build Information', {
            'fields': ('application', 'build_id', 'status')
        }),
        ('Timing', {
            'fields': ('build_start_time', 'build_end_time', 'duration_seconds')
        }),
        ('Results', {
            'fields': ('apk_file', 'source_code_zip', 'apk_size_mb')
        }),
        ('Logs and Errors', {
            'fields': ('log_output', 'error_message'),
            'classes': ('collapse',)
        }),
    )
    
    def build_id_short(self, obj):
        return obj.build_id.hex[:8]
    build_id_short.short_description = 'Build ID'
    
    def duration_display(self, obj):
        if obj.duration_seconds:
            minutes = int(obj.duration_seconds // 60)
            seconds = int(obj.duration_seconds % 60)
            return f"{minutes}m {seconds}s"
        return "-"
    duration_display.short_description = 'Duration'
    
    def has_add_permission(self, request):
        return False


@admin.register(CustomPubDevWidget)
class CustomPubDevWidgetAdmin(admin.ModelAdmin):
    list_display = ('widget_class_name', 'application', 'package_name', 'package_version', 'is_active')
    list_filter = ('application', 'is_active')
    search_fields = ('package_name', 'widget_class_name', 'description')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('application', 'widget_class_name', 'description')
        }),
        ('Package Details', {
            'fields': ('package_name', 'package_version', 'import_statement')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )


# Customize admin site
admin.site.site_header = "Flutter App Builder - Admin Panel"
admin.site.site_title = "Flutter App Builder"
admin.site.index_title = "Welcome to Flutter App Builder"