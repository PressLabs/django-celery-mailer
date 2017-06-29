import sys

import django
from django.conf import settings


settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
        }
    },
    INSTALLED_APPS=('django.contrib.auth',
                    'django.contrib.contenttypes',
                    'django.contrib.sessions',
                    'django.contrib.admin',
                    'celery_mailer',),
    CELERY_ALWAYS_EAGER=True,
    CELERY_EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
    EMAIL_BACKEND='celery_mailer.backends.CeleryEmailBackend',

    # for tests
    CELERY_EMAIL_TASK_CONFIG = {
        'queue' : 'django_email',
        'delivery_mode' : 1, # non persistent
        'rate_limit' : '50/m', # 50 emails per minute
    }
)


django.setup()
