"""
Django settings for kakadatabase project.

Generated by 'django-admin startproject' using Django 2.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'DO_NOT_USE_IN_PRODUCTION'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Production settings for security and geo libraries
if os.environ.get('IS_PRODUCTION') == 'True' \
   and 'DJANGO_SECRET_KEY' in os.environ:
    SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

    DEBUG = False

    ALLOWED_HOSTS = [
        '.kakadatabase.nz',
        '.orokonui.nz',
    ]

    GEOS_LIBRARY_PATH = "{}/lib/libgeos_c.so".format(
        os.environ.get('GEO_LIBRARIES_PATH')
    )
    GDAL_LIBRARY_PATH = "{}/lib/libgdal.so".format(
        os.environ.get('GEO_LIBRARIES_PATH')
    )
    PROJ4_LIBRARY_PATH = "{}/lib/libproj.so".format(
        os.environ.get('GEO_LIBRARIES_PATH')
    )
    GDAL_DATA = "{}/share/gdal/".format(os.environ.get('GEO_LIBRARIES_PATH'))

# Application definition

INSTALLED_APPS = [
    'theme',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'corsheaders',
    'rest_framework',
    'rest_framework_gis',
    'rest_framework_csv',
    'debug_toolbar',
    'leaflet',
    'birds',
    'bands',
    'locations',
    'observations',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'kakadatabase.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS':
            {
                'context_processors':
                    [
                        'django.template.context_processors.debug',
                        'django.template.context_processors.request',
                        'django.contrib.auth.context_processors.auth',
                        'django.contrib.messages.context_processors.messages',
                    ],
            },
    },
]

WSGI_APPLICATION = 'kakadatabase.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

import dj_database_url

DATABASES = {}

DATABASES['default'] = dj_database_url.config(
    default='postgres://postgres:@localhost:5432/kakadatabase',
    conn_max_age=600
)

DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
            'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
            'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
            'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
            'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-au'

TIME_ZONE = 'Pacific/Auckland'

USE_I18N = True

USE_L10N = False

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATIC_URL = '/static/'

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'

# Django REST Framework

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES':
        (
            'rest_framework.renderers.JSONRenderer',
            'rest_framework.renderers.BrowsableAPIRenderer',
            'rest_framework_csv.renderers.PaginatedCSVRenderer',
        ),
    'DEFAULT_PERMISSION_CLASSES':
        ('rest_framework.permissions.IsAuthenticatedOrReadOnly', ),
    'DEFAULT_FILTER_BACKENDS':
        (
            'django_filters.rest_framework.DjangoFilterBackend',
            'rest_framework.filters.OrderingFilter',
            'rest_framework.filters.SearchFilter',
        ),
    'DEFAULT_THROTTLE_CLASSES':
        ('rest_framework.throttling.ScopedRateThrottle', ),
    'DEFAULT_THROTTLE_RATES': {
        'report': '60/hour',
    },
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE':
        100,
}

# CORS

CORS_ORIGIN_WHITELIST = ('localhost:3000', )

if not DEBUG:
    CORS_ORIGIN_WHITELIST = (
        'beta.kakadatabase.nz',
        'www.kakadatabase.nz',
        'kakadatabase.nz',
        'kakadatabase.orokonui.nz',
    )

if os.environ.get('CORS_ALLOW_LOCALHOST') == 'True':
    CORS_ORIGIN_WHITELIST += (
        'localhost:3000',
        'localhost:8000',
    )

# Custom admin site header

ADMIN_SITE_HEADER = "Kākā Database"
ADMIN_SITE_TITLE = "Kākā Database"
ADMIN_INDEX_TITLE = "Admin"

# Production security

if not DEBUG:
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_SECONDS = 3600
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'

# Debug toolbar

if DEBUG:
    INTERNAL_IPS = ['127.0.0.1']

# Leaflet

LINZ_API_KEY = os.environ.get('LINZ_API_KEY')
MAPBOX_API_KEY = os.environ.get('MAPBOX_API_KEY')

# yapf: disable
LEAFLET_CONFIG = {
    'DEFAULT_CENTER': (-41.47, 172.72),
    'DEFAULT_ZOOM': 5,
    'MIN_ZOOM': 5,
    'MAX_ZOOM': 13,
    'RESET_VIEW': False,
    'TILES': [],
    'FORCE_IMAGE_PATH': True,
}
# yapf: enable
