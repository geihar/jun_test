from newsBoard.settings.base import *


SECRET_KEY = "development"

DEBUG = True

INTERNAL_IPS = ["*"]

ALLOWED_HOSTS = ["*"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}