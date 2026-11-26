from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# The server's own settings.py holds the real key and DB password. This file is
# never deployed (deploy.sh skips it), so the tracked copy keeps secrets out of git.
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-laptop-only-key')

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'results.apps.ResultsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tailwind',
    'theme',
    'django_browser_reload',
    'django_filters',
    'django_fastdev',
    'import_export',
    'fontawesomefree',
    'django_quill',

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

ROOT_URLCONF = 'lab.urls'

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

TAILWIND_APP_NAME='theme'
INTERNAL_IPS=['127.0.0.1']
NPM_BIN_PATH = "/snap/bin/npm"

WSGI_APPLICATION = 'lab.wsgi.application'


#DATABASES = {
    #'default': {
   #     'ENGINE': 'django.db.backends.sqlite3',
  #      'NAME': BASE_DIR / 'db.sqlite3',
 #   }
#}

DATABASES = {
    'default':{
	'ENGINE': 'django.db.backends.postgresql_psycopg2',
	'NAME':	'supreme',
	'USER': 'sadmin',
	'PASSWORD': os.environ.get('SUPREME_DB_PASSWORD', ''),
	'HOST': 'localhost',
	'PORT': '',
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

TIME_ZONE = 'Africa/Lagos'

USE_I18N = False

USE_L10N=True

USE_THOUSAND_SEPARATOR=True

USE_TZ = True

DATE_INPUT_FORMATS = ['%d-%m-%Y'] 
DATETIME_INPUT_FORMAT=['%d-%m-%Y']

LOGIN_REDIRECT_URL = '/'
LOGIN_URL="/login/"

STATIC_URL = '/static/'
STATIC_ROOT=os.path.join(BASE_DIR,'static')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

QUILL_CONFIGS = {
    'default': {
        'theme': 'snow',
        'modules': {
            'syntax': True,
            'toolbar': [
                [
                    {'font': []},
                    {'header': []},
                    {'align': []},
                    'bold', 'italic', 'underline', 'strike', 'blockquote',
                    {'color': []},
                    {'background': []},
                    {'script': 'sub'},
                    {'script': 'super'}, 
                ],
                ['code-block', 'link'],
                ['clean'],
            ]
        }
    }
}

# Per-machine overrides (laptop DB credentials etc.). lab/local_settings.py is
# git-ignored and does not exist on the server, so the server keeps the values
# above. deploy.sh never ships this file either way.
try:
    from .local_settings import *  # noqa: F401,F403
except ImportError:
    pass
