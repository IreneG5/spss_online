from base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Application definition
INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Debug Toolbar
INTERNAL_IPS = ('127.0.0.1',)

ALLOWED_HOSTS = ['127.0.0.1', 'ff980d67.ngrok.io']

# PayPal Settings
SITE_URL = 'http://ff980d67.ngrok.io'
PAYPAL_NOTIFY_URL = 'http://ff980d67.ngrok.io/a-very-hard-to-guess-url/'
PAYPAL_RECEIVER_EMAIL = 'irene.g5555-easySPSS1@gmail.com'

