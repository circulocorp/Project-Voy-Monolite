import os
from environ import environ, Env
from pathlib import Path
from storages.backends.azure_storage import AzureStorage


DEVELOPMENT_MODE = False

env: Env = environ.Env(
    DEBUG=(bool, False)
)

BASE_DIR = Path(__file__).resolve().parent.parent

env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = env('DJANGO_SECRET_KEY', cast=str, default='') if DEVELOPMENT_MODE else os.getenv('DJANGO_SECRET_KEY')

DEBUG = env('DJANGO_DEBUG', cast=bool, default=False) if DEVELOPMENT_MODE else os.getenv('DJANGO_DEBUG')

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third party apps
    'storages',
    # Custom apps
    'apps.users.apps.UsersConfig',
    'apps.devices.apps.DevicesConfig',
    'apps.vehicles.apps.VehiclesConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'system.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
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

WSGI_APPLICATION = 'system.wsgi.application'

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('DATABASE_NAME', cast=str, default='') if DEVELOPMENT_MODE else os.getenv('DATABASE_NAME'),
        'USER': env('DATABASE_USERNAME', cast=str, default='') if DEVELOPMENT_MODE else os.getenv('DATABASE_USERNAME'),
        'PASSWORD': env('DATABASE_PASSWORD', cast=str, default='') if DEVELOPMENT_MODE else os.getenv('DATABASE_PASSWORD'),
        'HOST': env('DATABASE_HOST', cast=str, default='') if DEVELOPMENT_MODE else os.getenv('DATABASE_HOST'),
        'PORT': env('DATABASE_PORT', cast=str, default='') if DEVELOPMENT_MODE else os.getenv('DATABASE_PORT'),
        'OPTIONS': {'sslmode': 'prefer'}
    }
}

# Password validation

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

# Internationalization

LANGUAGE_CODE = 'es-mx'

TIME_ZONE = 'America/Mexico_City'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)


STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

STATIC_LOCATION = "static"

AZURE_STORAGE_ACCOUNT_NAME = env('AZURE_STORAGE_ACCOUNT_NAME', cast=str, default='') if DEVELOPMENT_MODE else os.getenv('AZURE_STORAGE_ACCOUNT_NAME')

if DEVELOPMENT_MODE:
    STATIC_URL = 'static/'
else:
    STATIC_URL = f"https://{AZURE_STORAGE_ACCOUNT_NAME}.blob.core.windows.net/{STATIC_LOCATION}/"

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom user model

AUTH_USER_MODEL = 'users.User'

# Login settings

LOGIN_URL = 'users:login'

LOGIN_REDIRECT_URL = 'users:dashboard'

LOGOUT_REDIRECT_URL = 'users:login'

# Email settings

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = env('EMAIL_HOST', cast=str, default='') if DEVELOPMENT_MODE else os.getenv('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT', cast=int, default=587) if DEVELOPMENT_MODE else os.getenv('EMAIL_PORT')
EMAIL_HOST_USER = env('EMAIL_HOST_USER', cast=str, default='') if DEVELOPMENT_MODE else os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', cast=str, default='') if DEVELOPMENT_MODE else os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = env('EMAIL_USE_TLS', cast=bool, default=True) if DEVELOPMENT_MODE else os.getenv('EMAIL_USE_TLS')

DEFAULT_FROM_EMAIL = 'notificaciones@circulocorp.com' 
# Message storage

MESSAGE_STORAGE = "django.contrib.messages.storage.cookie.CookieStorage"

# Azure storage settings

AZURE_ACCOUNT_NAME = env('AZURE_STORAGE_ACCOUNT_NAME', cast=str, default='') if DEVELOPMENT_MODE else os.getenv("AZURE_STORAGE_ACCOUNT_NAME")

AZURE_ACCOUNT_KEY = env('AZURE_STORAGE_ACCOUNT_KEY', cast=str, default='') if DEVELOPMENT_MODE else os.getenv("AZURE_STORAGE_ACCOUNT_KEY")

AZURE_CUSTOM_DOMAIN = f"{AZURE_ACCOUNT_NAME}.blob.core.windows.net"

AZURE_CONTAINER = STATIC_LOCATION

AZURE_CONNECTION_STRING = env('AZURE_STORAGE_CONNECTION_STRING', cast=str, default='') if DEVELOPMENT_MODE else os.getenv("AZURE_STORAGE_CONNECTION_STRING")

AZURE_CONTAINER_STATIC = "voy-static"

AZURE_CONTAINER_MEDIA = "voy-media"

STATIC_ROOT = f"https://{AZURE_ACCOUNT_NAME}.blob.core.windows.net/{AZURE_CONTAINER_STATIC}?sp=r&st=2025-03-26T19:39:21Z&se=2026-03-27T03:39:21Z&sv=2024-11-04&sr=c&sig=FW%2Bel95Ykm78gGO47okj14oc63FzRaG4Vi7US2cHGGw%3D/"

MEDIA_URL = f"https://{AZURE_ACCOUNT_NAME}.blob.core.windows.net/{AZURE_CONTAINER_MEDIA}?sp=r&st=2025-03-26T19:39:21Z&se=2026-03-27T03:39:21Z&sv=2024-11-04&sr=c&sig=FW%2Bel95Ykm78gGO47okj14oc63FzRaG4Vi7US2cHGGw%3D/"

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.azure_storage.AzureStorage",
        "OPTIONS": {
            "azure_container": AZURE_CONTAINER_MEDIA,
            "account_name": AZURE_ACCOUNT_NAME,
            "account_key": AZURE_ACCOUNT_KEY,
            "connection_string": AZURE_CONNECTION_STRING,
        },
    },
    "staticfiles": {
        "BACKEND": "storages.backends.azure_storage.AzureStorage",
        "OPTIONS": {
            "azure_container": AZURE_CONTAINER_STATIC,
            "account_name": AZURE_ACCOUNT_NAME,
            "account_key": AZURE_ACCOUNT_KEY,
            "connection_string": AZURE_CONNECTION_STRING,
        }
    }
}