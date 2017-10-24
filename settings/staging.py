from base import *
import dj_database_url

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
# Load the ClearDB connection details from the environment variable
DATABASES = {
    'default': dj_database_url.config('CLEARDB_DATABASE_URL')
}


# PayPal Settings
PAYPAL_NOTIFY_URL = 'spss-online.herokuapp.com/a-very-hard-to-guess-url/'
PAYPAL_RECEIVER_EMAIL = 'irene.g5555-easySPSS1@gmail.com'

SITE_URL = 'https://spss-online.herokuapp.com'
ALLOWED_HOSTS.append('spss-online.herokuapp.com')

# Log DEBUG information to the console
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
        },
    },
}



