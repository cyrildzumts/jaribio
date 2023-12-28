"""
Django settings for jaribio project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
from django.utils.translation import ugettext_lazy as _
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['JARIBIO_SECRET_KEY']

SITE_NAME           =  os.environ.get('JARIBIO_SITE_NAME', 'JARIBIO')

META_KEYWORDS       = _("LYSHOP Gabon, Online Shop, Shoes, Fashion, Perfumes, Electronics, Smartphones")
META_DESCRIPTION    = _("LYSHOP is an online store in Gabon. We sell shoes, perfumes, accessories and more for men, women and children. We offer deliveries to libreville and port-gentil.")
HOME_TITLE          = _("Online Quiz | JARIBIO")

CELERY_BROKER_URL   = os.environ.get('JARIBIO_CELERY_BROKER_URL')
CELERY_BACKEND      = os.environ.get('JARIBIO_CELERY_BACKEND')

CELERY_DEFAULT_QUEUE = "jaribio-default"
CELERY_DEFAULT_EXCHANGE = "jaribio-default"
CELERY_DEFAULT_ROUTING_KEY = "jaribio-default"

CELERY_OUTGOING_MAIL_QUEUE = "jaribio-outgoing-mails"
CELERY_OUTGOING_MAIL_EXCHANGE = "jaribio-mail"
CELERY_OUTGOING_MAIL_ROUTING_KEY = "jaribio.mail.outgoing"


CELERY_IDENTIFICATION_QUEUE = "jaribio-ident"
CELERY_IDENTIFICATION_EXCHANGE = "jaribio-ident"
CELERY_IDENTIFICATION_ROUTING_KEY = "jaribio.identification"
CELERY_DEFAULT_EXCHANGE_TYPE = 'direct'

CELERY_NAMESPACE = 'CELERY'
CELERY_APP_NAME = 'jaribio'

ACCOUNT_ROOT_PATH = "/accounts/"
HOME_URL = "/"
DASHBOARD_ROOT_PATH = "/dashboard/"
USER_PATH = "/users/detail/"


ALLOWED_HOSTS = [os.getenv('JARIBIO_ALLOWED_HOST')]
SITE_HOST = os.getenv('JARIBIO_HOST')

#EMAIL SETTINGS
EMAIL_HOST = os.environ.get('JARIBIO_EMAIL_HOST')
EMAIL_PORT = os.environ.get('JARIBIO_EMAIL_PORT')
EMAIL_HOST_PASSWORD = os.environ.get('JARIBIO_EMAIL_PASSWORD')
EMAIL_HOST_USER = os.environ.get('JARIBIO_EMAIL_USER')
DEFAULT_FROM_EMAIL = os.environ.get('JARIBIO_DEFAULT_FROM_EMAIL', 'JARIBIO <info@jaribio-quiz.com>')
CONTACT_MAIL =  os.environ.get('JARIBIO_CONTACT_MAIL')
ADMIN_EXTERNAL_EMAIL = os.environ.get("JARIBIO_ADMIN_EXTERNAL_EMAIL")
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_BACKEND = os.environ.get('JARIBIO_EMAIL_BACKEND')

DJANGO_EMAIL_TEMPLATE = "tags/template_email_new.html"
DJANGO_EMAIL_TO_ADMIN_TEMPLATE = "tags/admin_newuser_template_email.html"
DJANGO_EMAIL_TEMPLATE_TXT = "tags/template_email.txt"
DJANGO_WELCOME_EMAIL_TEMPLATE = "welcome_email_new.html"
DJANGO_VALIDATION_EMAIL_TEMPLATE = "validation_email_new.html"

PAY_USERNAME = os.getenv('JARIBIO_PAY_USER')
PAY_REQUEST_TOKEN = os.getenv('JARIBIO_LIPA_REQUEST_TOKEN')
PAY_REQUEST_DESCRIPTION = os.getenv('JARIBIO_PAY_DESCRIPTION', "JARIBIO PAYMENT")
JARIBIO_USER = os.getenv('JARIBIO_USER')
JARIBIO_LIPA_REQUEST_URL = os.getenv('JARIBIO_LIPA_REQUEST_URL')
JARIBIO_LIPA_API_PAYMENTS_URL = os.getenv('JARIBIO_LIPA_API_PAYMENTS_URL')
CURRENCY = os.getenv('JARIBIO_CURRENCY') 

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'api.apps.ApiConfig',
    'accounts',
    'quiz.apps.QuizConfig',
    'core.apps.CoreConfig',
    'dashboard.apps.DashboardConfig',
]

# RESTFRAMEWORK SETTINGS
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ]
}

SESSION_COOKIE_AGE = 86400

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

ROOT_URLCONF = 'jaribio.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'jaribio.context_processors.site_context',
                'accounts.context_processors.account_context',
                'core.context_processors.core_context',
                'dashboard.context_processors.dashboard_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'jaribio.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'dev': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'jaribio.db'),
    },
    'production': {
	'ENGINE':  os.environ.get('JARIBIO_DATABASE_ENGINE'),
	'NAME'	:  os.environ.get('JARIBIO_DATABASE_NAME'),
	'USER'	:  os.environ.get('JARIBIO_DATABASE_USERNAME'),
	'PASSWORD':  os.environ.get('JARIBIO_DATABASE_PW'),
	'HOST'	:  os.environ.get('JARIBIO_DATABASE_HOST') ,
	'PORT' 	:  os.environ.get('JARIBIO_DATABASE_PORT'),
    'OPTIONS' : {
        'sslmode': 'require'
    },
    'TEST'  :{
        'NAME': os.getenv('JARIBIO_TEST_DATABASE', 'test_jaribio_db'),
    },
   },

}

DEFAULT_DATABASE = os.environ.get('DJANGO_DATABASE', 'dev')
DATABASES['default'] = DATABASES[DEFAULT_DATABASE]
DEV_MODE = DEFAULT_DATABASE == 'dev'
ALLOW_GOOGLE_ANALYTICS = os.environ.get('JARIBIO_ALLOW_GOOGLE_ANALYTICS', 'false') == 'true'
#CSRF_COOKIE_SECURE = not DEV_MODE


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = DEV_MODE
#DEBUG = True

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '{asctime} {levelname} {module} {message}',
            'style': '{',
        },
        'file': {
            'format': '{asctime} {levelname} {module} {message}',
            'style': '{',
        },
        'async': {
            'format': '{module} {message}',
            'style': '{',
        },
    },

    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'file',
            'filename':'logs/jaribio.log',
            'when' : 'midnight'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        '' : {
            'level': 'DEBUG',
            'handlers': ['console', 'file'],
            'propagate': True,
        },
        'django': {
            'level': 'WARNING',
            'handlers': ['file'],
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins', 'file'],
            'level': 'WARNING',
            'propagate': False,
        },
        'django.template': {
            'handlers': ['console', 'file'],
            'level': 'WARNING',
            'propagate': True,
        },
        'PIL':{
            'handlers': ['console', 'file'],
            'level': 'WARNING',
            'propagate': False,
        }
    }
}

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'fr'
LANGUAGES = (
    ('fr',_('French')),
    ('en',_('English')),
)
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]
TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DECIMAL_SEPAROTOR='.'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "staticfiles"),
]


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
