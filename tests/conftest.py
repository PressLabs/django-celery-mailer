import pytest

from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend


def pytest_configure():
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
                        'celery_mailer',),
        CELERY_ALWAYS_EAGER=True,
        CELERY_EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',

        CELERY_EMAIL_TASK_CONFIG={
            'queue' : 'django_email',
            'delivery_mode' : 1, # non persistent
            'rate_limit' : '50/m', # 50 emails per minute
        }
    )


@pytest.fixture(autouse=True)
def override_settings(settings):
    settings.USE_CELERY = True

    settings.EMAIL_BACKEND = 'celery_mailer.backends.CeleryEmailBackend'

    settings.CELERY_TASK_SERIALIZER = 'json'
    settings.CELERY_RESULT_SERIALIZER = 'json'
    settings.CELERY_ACCEPT_CONTENT = ['json']
    settings.BROKER_URL = 'redis://localhost:6379/1'
    settings.CELERY_RESULT_BACKEND = 'redis://localhost:6379/2'


class TestBackend(BaseEmailBackend):
    def __init__(self, username=None, password=None, fail_silently=False, **kwargs):
        self.username = username
        self.password = password

    def send_messages(self, email_messages):
        return {'username': self.username, 'password': self.password}
