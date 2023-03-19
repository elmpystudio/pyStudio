from datetime import timedelta
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'your key'
DEBUG = True

JUPYTERHUB_CLIENT_ID = 'QmS4c2KSGvU$45OwlYV2JshEuUG0TO0XTzr1hB3E7'

ALLOWED_HOSTS = ["*"]

ROOT_URLCONF = 'rest.urls'

ML_ROOT_URL = 'http://localhost:5000/'

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
    "ACCESS_KEY": "minio",
    "SECRET_KEY": "yourPassword",
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
    'oauth2_provider',
    'corsheaders',
    'rest_framework',
    'drf_yasg',

    # MAIN APPS
    'users',
    'datasets',
    'ml_models',
    'notifications',
    'marketplace',
    'jupyterhub',
    'ml_studio',
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

AUTH_USER_MODEL = 'users.User'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, './db.sqlite3'),
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
