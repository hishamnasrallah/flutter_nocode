import os
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-this-in-production')

DEBUG = config('DEBUG', default=True, cast=bool)

CSRF_TRUSTED_ORIGINS = [
    'https://*.ngrok-free.app',
    'http://*.ngrok-free.app',
    'http://localhost:3001',
    "https://*.trycloudflare.com"

]
# Allow specific domains for CORS
CORS_ALLOWED_ORIGINS = [
    "https://businesses-hebrew-every-baltimore.trycloudflare.com",
    "http://6c75545e1be2.ngrok-free.app",
    "https://6032713a89bd.ngrok-free.app",
    "http://6032713a89bd.ngrok-free.app"
]

# Alternatively, for dev only (NOT for production):
CORS_ALLOW_ALL_ORIGINS = True


ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'colorfield',
    'corsheaders',
    'core',
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'flutter_nocode.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'flutter_nocode.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Build server configuration
BUILD_SERVER_URL = config('BUILD_SERVER_URL', default='http://localhost:8001')
BUILD_SERVER_API_KEY = config('BUILD_SERVER_API_KEY', default='your-build-server-api-key')

# File storage paths
GENERATED_CODE_PATH = BASE_DIR / 'generated_flutter_projects'
APK_STORAGE_PATH = BASE_DIR / 'media' / 'apks'
SOURCE_ZIP_STORAGE_PATH = BASE_DIR / 'media' / 'source_zips'

# Create directories if they don't exist
os.makedirs(GENERATED_CODE_PATH, exist_ok=True)
os.makedirs(APK_STORAGE_PATH, exist_ok=True)
os.makedirs(SOURCE_ZIP_STORAGE_PATH, exist_ok=True)

# Flutter SDK Configuration
FLUTTER_SDK_PATH = config('FLUTTER_SDK_PATH', default=r'C:\flutter')

# Verify Flutter exists
flutter_exe = os.path.join(FLUTTER_SDK_PATH, 'bin', 'flutter.bat' if os.name == 'nt' else 'flutter')
if os.path.exists(flutter_exe):
    print(f"✓ Flutter found at {flutter_exe}")
    FLUTTER_AVAILABLE = True
else:
    print(f"✗ Flutter NOT found at {flutter_exe}")
    FLUTTER_AVAILABLE = False

# Android SDK Path
ANDROID_SDK_PATH = config('ANDROID_SDK_PATH', default=r'C:\android-sdk')
ANDROID_CMDLINE_TOOLS = os.path.join(ANDROID_SDK_PATH, 'cmdline-tools', 'latest')

# Java path (Java 17+ required for Flutter)
JAVA_HOME = config('JAVA_HOME', default=r'C:\Program Files\Eclipse Adoptium\jdk-21.0.8.9-hotspot')

# Set environment variables for Flutter build process
os.environ['FLUTTER_ROOT'] = FLUTTER_SDK_PATH
os.environ['ANDROID_HOME'] = ANDROID_SDK_PATH
os.environ['ANDROID_SDK_ROOT'] = ANDROID_SDK_PATH
os.environ['JAVA_HOME'] = JAVA_HOME

# Build complete PATH
flutter_bin = os.path.join(FLUTTER_SDK_PATH, 'bin')
android_bin = os.path.join(ANDROID_CMDLINE_TOOLS, 'bin')
java_bin = os.path.join(JAVA_HOME, 'bin')

# Add to PATH (put Flutter first)
current_path = os.environ.get('PATH', '')
path_separator = ';' if os.name == 'nt' else ':'
os.environ['PATH'] = f"{flutter_bin}{path_separator}{android_bin}{path_separator}{java_bin}{path_separator}{current_path}"

# Build settings
BUILD_TIMEOUT = config('BUILD_TIMEOUT', default=600, cast=int)
USE_MOCK_BUILD = config('USE_MOCK_BUILD', default=False, cast=bool)

# Debug: Print configuration
if DEBUG:
    print(f"Flutter SDK Path: {FLUTTER_SDK_PATH}")
    print(f"Flutter Available: {FLUTTER_AVAILABLE}")
    print(f"Android SDK Path: {ANDROID_SDK_PATH}")
    print(f"Java Home: {JAVA_HOME}")
    print(f"Build Timeout: {BUILD_TIMEOUT} seconds")
    print(f"Use Mock Build: {USE_MOCK_BUILD}")