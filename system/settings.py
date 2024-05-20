import os
from environ import environ, Env
from pathlib import Path


env: Env = environ.Env(
    DEBUG=(bool, False)
)

BASE_DIR = Path(__file__).resolve().parent.parent

env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = env('DJANGO_SECRET_KEY', cast=str, default='')

DEBUG = env('DJANGO_DEBUG', cast=bool, default=False)

ALLOWED_HOSTS = env('DJANGO_ALLOWED_HOSTS', cast=list, default=[])

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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
        'NAME': env('DATABASE_NAME', cast=str, default=''),
        'USER': env('DATABASE_USERNAME', cast=str, default=''),
        'PASSWORD': env('DATABASE_PASSWORD', cast=str, default=''),
        'HOST': env('DATABASE_HOST', cast=str, default=''),
        'PORT': env('DATABASE_PORT', cast=str, default=''),
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

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'

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

EMAIL_HOST = env('EMAIL_HOST', cast=str, default='')
EMAIL_PORT = env('EMAIL_PORT', cast=int, default=587)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', cast=str, default='')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', cast=str, default='')
EMAIL_USE_TLS = env('EMAIL_USE_TLS', cast=bool, default=True)

# Message storage

MESSAGE_STORAGE = "django.contrib.messages.storage.cookie.CookieStorage"
