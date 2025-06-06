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

AZURE_ACCOUNT_NAME = env.str('AZURE_ACCOUNT_NAME') or os.getenv('AZURE_ACCOUNT_NAME')
AZURE_ACCOUNT_KEY = env.str('AZURE_ACCOUNT_KEY') or os.getenv('AZURE_ACCOUNT_KEY')
AZURE_CONNECTION_STRING = env.str('AZURE_CONNECTION_STRING') or os.getenv('AZURE_CONNECTION_STRING')

AZURE_CONTAINER_STATIC = env.str('AZURE_CONTAINER_STATIC') or os.getenv('AZURE_CONTAINER_STATIC')

AZURE_CONTAINER_MEDIA = env.str('AZURE_CONTAINER_MEDIA') or os.getenv('AZURE_CONTAINER_MEDIA')

STATIC_URL = f"https://{AZURE_ACCOUNT_NAME}.blob.core.windows.net/{AZURE_CONTAINER_STATIC}/"

MEDIA_URL = f"https://{AZURE_ACCOUNT_NAME}.blob.core.windows.net/{AZURE_CONTAINER_MEDIA}/"

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