from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import viewsets

router = DefaultRouter()
router.register(r'themes', viewsets.ThemeViewSet, basename='theme')
router.register(r'applications', viewsets.ApplicationViewSet, basename='application')
router.register(r'screens', viewsets.ScreenViewSet, basename='screen')
router.register(r'widgets', viewsets.WidgetViewSet, basename='widget')
router.register(r'widget-properties', viewsets.WidgetPropertyViewSet, basename='widgetproperty')
router.register(r'actions', viewsets.ActionViewSet, basename='action')
router.register(r'data-sources', viewsets.DataSourceViewSet, basename='datasource')
router.register(r'data-source-fields', viewsets.DataSourceFieldViewSet, basename='datasourcefield')
router.register(r'build-history', viewsets.BuildHistoryViewSet, basename='buildhistory')
router.register(r'custom-widgets', viewsets.CustomPubDevWidgetViewSet, basename='custompubdevwidget')
router.register(r'app-icons', viewsets.AppIconViewSet, basename='appicon')
router.register(r'assets', viewsets.AssetViewSet, basename='asset')
router.register(r'pubspec-dependencies', viewsets.PubspecDependencyViewSet, basename='pubspecdependency')

urlpatterns = router.urls