"""
Django settings for skip_base project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import boto3


def get_secret(secret_name):
    secrets_manager = boto3.client('secretsmanager', region_name='us-west-2')
    return secrets_manager.get_secret_value(SecretId=secret_name)['SecretString']


def get_rds_db(db_instance_id):
    rds = boto3.client('rds', region_name='us-west-2')
    resp = rds.describe_db_instances(Filters=[
        {'Name': 'db-instance-id', 'Values': [db_instance_id]},
    ])
    return resp['DBInstances'][0]


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 't8oh)-ej%uc!&!p&0ugyy8oxgu3=w(yy$68++hc7we#g@j7m+c'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'django_extensions',
    'django_filters',
    'skip',
    'django.contrib.postgres',
    'skip_dpd',
    'django_plotly_dash.apps.DjangoPlotlyDashConfig',
    'bootstrap4'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'skip_base.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'skip_base.wsgi.application'

CORS_ORIGIN_ALLOW_ALL = True


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

rds_db = get_rds_db('skip-postgres')
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django.contrib.gis.db.backends.postgis'),
        'NAME': rds_db['DBName'],
        'USER': rds_db['MasterUsername'],
        'PASSWORD': get_secret('skip-db-password'),
        'HOST': rds_db['Endpoint']['Address'],
        'PORT': rds_db['Endpoint']['Port'],
    },
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, '_static')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',

    'django_plotly_dash.finders.DashAssetFinder',
    'django_plotly_dash.finders.DashComponentFinder',
    'django_plotly_dash.finders.DashAppDirectoryFinder',
]

# Django REST Framework configuration

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'skip.pagination.SkipPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # TODO: BasicAuthentication has not been included--it may need to be included for running tests
        # TODO: TokenAuthentication may need to be restricted for certain views, and same for SessionAuthentication
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    )
}

# Hopskotch Consumer Configuration

HOPSKOTCH_SERVER = os.getenv('HOPSKOTCH_SERVER', 'dev.hop.scimma.org')
HOPSKOTCH_PORT = os.getenv('HOPSKOTCH_PORT', '9092')

HOPSKOTCH_CONSUMER_CONFIGURATION = {
    'bootstrap.servers': f'{HOPSKOTCH_SERVER}:{HOPSKOTCH_PORT}',
    'group.id': os.getenv('HOPSKOTCH_GROUP', 'skip-test'),
    'auto.offset.reset': 'latest',
    'security.protocol': 'sasl_ssl',
    'sasl.mechanism': 'PLAIN',
    'sasl.username': 'test',
    'sasl.password': get_secret('dev-skip-hopcreds'),

    # system dependency: ssl.ca.location may need to be set
    # this does not seem to be necessary on Ubuntu. However,
    # for example on centos7: 'ssl.ca.location': '/etc/ssl/certs/ca-bundle.crt',
}

HOPSKOTCH_TOPICS = ['gcn', 'lvc-counterpart', 'tns']

# TODO: PARSERS should be renamed to <NAMESPACING>_PARSERS
PARSERS = {
    'gcn': [
        'skip.parsers.gcn_parser.GCNParser',
        'skip.parsers.lvc_counterpart_parser.LVCCounterpartParser',
        'skip.parsers.base_parser.DefaultParser'
    ],
    'lvc-counterpart': [
        'skip.parsers.lvc_counterpart_parser.LVCCounterpartParser',
        'skip.parsers.base_parser.DefaultParser'
    ],
    'tns': [
        'skip.parsers.tns_parser.TNSParser',
        'skip.parsers.base_parser.DefaultParser'
    ]
}

SKIP_API_CLIENT = 'skip.skip_api_client.SkipORMClient'
SKIP_API_KEY = os.getenv('SKIP_API_KEY', '')
X_FRAME_OPTIONS = 'SAMEORIGIN'

PLOTLY_COMPONENTS = [
    # Common components
    'dash_core_components',
    'dash_html_components',
    'dash_renderer',

    # django-plotly-dash components
    'dpd_components',
    # static support if serving local assets
    'dpd_static_support',

    # Other components, as needed
    'dash_bootstrap_components',
    'dash_table'
]


try:
    from local_settings import *  # noqa
except ImportError:
    pass
