from datetime import timedelta
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'your key'

DEBUG = True

ALLOWED_HOSTS = ["*"]

ROOT_URLCONF = 'rest.urls'

ML_ROOT_URL = 'http://127.0.0.1:5555/'

DEFAULT_AUTO_FIELD='django.db.models.AutoField'

environments = ['local', 'prod']
if 'ANALYTICS_APP_ENV' not in os.environ or not os.environ['ANALYTICS_APP_ENV'] in environments:
    #print("[-] To run this project you need to set environ ANALYTICS_APP_ENV to one of these: " + ", ".join(environments))
    print("[-] Not environ ANALYTICS_APP_ENV running in LOCAL ")
    ENVIRONMENT = 'local'
    # sys.exit(-1)
else:
    ENVIRONMENT = os.environ['ANALYTICS_APP_ENV']

if ENVIRONMENT == 'prod':
    HOST = "analytics-platform.ml"
    SWAGGER_BASE_URL = "http://%s/api" % HOST
elif ENVIRONMENT == 'local':
    HOST = "0.0.0.0:8000"
    SWAGGER_BASE_URL = "http://%s/api" % HOST

AUTHENTICATION_BACKENDS = [
    'oauth2_provider.backends.OAuth2Backend',
    'django.contrib.auth.backends.ModelBackend',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    ],
}


MINIO_SERVER = {
        "IP": "localhost",
        "PORT": 9000,
        "ACCESS_KEY": "minioadmin",
        "SECRET_KEY": "minioadmin",
}

OAUTH2_PROVIDER = {
    'SCOPES': {'read': 'Read scope', 'write': 'Write scope', 'groups': 'Access to your groups'}
}


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=50),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=10),
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=50),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=10),
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'drf_yasg',
    'accounts',
    'datasets',
    'notifications',
    'marketplace',
    'ml_studio',
    'corsheaders',
    'rest_framework',
    'oauth2_provider',
    'jupyterhub',
    'ml_models'
]

MIDDLEWARE = [
    'oauth2_provider.middleware.OAuth2TokenMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

#############################
# Tableau Settings
#############################
TABLEAU_SERVER = {
    "URL": "http://x.x.x.x:8999",
    "DEFAULT_SITE": "API",
    "ADMIN_LOGIN": "xxxxxx",
    "ADMIN_PASS": "xxxxxxx"
}


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates/')],
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

CORS_ORIGIN_ALLOW_ALL = True

WSGI_APPLICATION = 'rest.wsgi.application'

AUTH_USER_MODEL = 'accounts.CustomUser'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '.persistant/db.sqlite3'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

X_FRAME_OPTIONS = 'ALLOW-FROM http://localhost:8080'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
