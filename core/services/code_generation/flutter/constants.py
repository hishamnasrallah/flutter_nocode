# File: core/services/code_generation/flutter/constants.py
"""
Flutter-specific constants used throughout the code generation system.
"""

# Flutter SDK requirements
FLUTTER_MIN_SDK_VERSION = '3.0.0'
FLUTTER_MAX_SDK_VERSION = '4.0.0'

# Default dependency versions
DEFAULT_DEPENDENCIES = {
    'http': '^1.1.0',
    'shared_preferences': '^2.2.2',
    'url_launcher': '^6.2.1',
    'image_picker': '^1.0.4',
    'path_provider': '^2.1.1',
}

# Development dependencies
DEV_DEPENDENCIES = {
    'flutter_test': {'sdk': 'flutter'},
    'flutter_lints': '^3.0.0'
}

# Android configuration
ANDROID_MIN_SDK_VERSION = 21
ANDROID_TARGET_SDK_VERSION = 33
ANDROID_COMPILE_SDK_VERSION = 33
ANDROID_NDK_VERSION = '27.0.12077973'

# iOS configuration
IOS_DEPLOYMENT_TARGET = '11.0'

# Default widget properties
DEFAULT_WIDGET_PROPERTIES = {
    'Container': {
        'padding': 8.0,
        'margin': 0.0,
    },
    'Text': {
        'fontSize': 14.0,
        'color': '000000',
    },
    'Card': {
        'elevation': 4.0,
    },
    'GridView': {
        'crossAxisCount': 2,
        'childAspectRatio': 1.0,
        'crossAxisSpacing': 8.0,
        'mainAxisSpacing': 8.0,
    },
    'ListView': {
        'scrollDirection': 'vertical',
        'shrinkWrap': False,
    },
}

# Material Design Icons mapping
MATERIAL_ICONS = {
    'home': 'Icons.home',
    'settings': 'Icons.settings',
    'person': 'Icons.person',
    'search': 'Icons.search',
    'add': 'Icons.add',
    'edit': 'Icons.edit',
    'delete': 'Icons.delete',
    'save': 'Icons.save',
    'close': 'Icons.close',
    'menu': 'Icons.menu',
    'more': 'Icons.more_vert',
    'back': 'Icons.arrow_back',
    'forward': 'Icons.arrow_forward',
    'up': 'Icons.arrow_upward',
    'down': 'Icons.arrow_downward',
    'refresh': 'Icons.refresh',
    'share': 'Icons.share',
    'favorite': 'Icons.favorite',
    'star': 'Icons.star',
    'info': 'Icons.info',
    'warning': 'Icons.warning',
    'error': 'Icons.error',
    'check': 'Icons.check',
    'camera': 'Icons.camera',
    'image': 'Icons.image',
    'file': 'Icons.insert_drive_file',
    'folder': 'Icons.folder',
    'link': 'Icons.link',
    'location': 'Icons.location_on',
    'map': 'Icons.map',
    'phone': 'Icons.phone',
    'email': 'Icons.email',
    'message': 'Icons.message',
    'notifications': 'Icons.notifications',
    'calendar': 'Icons.calendar_today',
    'clock': 'Icons.access_time',
    'shopping_cart': 'Icons.shopping_cart',
    'category': 'Icons.category',
    'filter': 'Icons.filter_list',
    'sort': 'Icons.sort',
}

# Flutter widget categories
WIDGET_CATEGORIES = {
    'basic': [
        'Text', 'Button', 'Icon', 'Image', 'Divider'
    ],
    'layout': [
        'Container', 'Row', 'Column', 'Stack', 'Positioned',
        'Expanded', 'Flexible', 'Padding', 'Center', 'SizedBox',
        'AspectRatio', 'Wrap'
    ],
    'scrollable': [
        'ListView', 'GridView', 'SingleChildScrollView', 'PageView'
    ],
    'input': [
        'TextField', 'Checkbox', 'Radio', 'Switch', 'Slider',
        'DropdownButton', 'DatePicker', 'TimePicker', 'FileUpload'
    ],
    'navigation': [
        'AppBar', 'BottomNavigationBar', 'Drawer', 'TabBar'
    ],
    'advanced': [
        'Card', 'ListTile', 'FutureBuilder', 'StreamBuilder',
        'SafeArea', 'Scaffold'
    ]
}

# Button types mapping
BUTTON_TYPES = {
    'elevated': 'ElevatedButton',
    'text': 'TextButton',
    'outlined': 'OutlinedButton',
    'icon': 'IconButton',
    'floating': 'FloatingActionButton',
}

# Text style weights
FONT_WEIGHTS = {
    'thin': 'FontWeight.w100',
    'light': 'FontWeight.w300',
    'regular': 'FontWeight.w400',
    'medium': 'FontWeight.w500',
    'bold': 'FontWeight.w700',
    'black': 'FontWeight.w900',
}

# Common screen names that might need special handling
SPECIAL_SCREENS = [
    'SplashScreen',
    'Configuration',
    'Login',
    'Register',
    'Home',
    'Settings',
    'Profile'
]

# HTTP methods
HTTP_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']

# Default headers for API calls
DEFAULT_API_HEADERS = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
}

# File extensions for different asset types
ASSET_EXTENSIONS = {
    'images': ['.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg'],
    'fonts': ['.ttf', '.otf', '.woff', '.woff2'],
    'data': ['.json', '.xml', '.yaml', '.yml'],
}

# Default animation durations (in milliseconds)
ANIMATION_DURATIONS = {
    'fast': 200,
    'normal': 300,
    'slow': 500,
}

# Default border radius values
BORDER_RADIUS = {
    'none': 0,
    'small': 4,
    'medium': 8,
    'large': 16,
    'circular': 999,
}