from django.core import mail

import celery_mailer
from celery_mailer.tasks import send_email


def test_sending_email(settings):
    results = mail.send_mail('test', 'Testing with Celery! w00t!!', 'from@example.com',
                             ['to@example.com'])

    for result in results:
        result.get()

    assert len(mail.outbox) == 1
    assert mail.outbox[0].subject == 'test'


def test_sending_mass_email(settings):
    emails = (
        ('mass 1', 'mass message 1', 'from@example.com', ['to@example.com']),
        ('mass 2', 'mass message 2', 'from@example.com', ['to@example.com']),
    )
    results = mail.send_mass_mail(emails)

    for result in results:
        result.get()

    assert len(mail.outbox) == 2
    assert len(results) == 2
    assert mail.outbox[0].subject == 'mass 1'
    assert mail.outbox[1].subject == 'mass 2'


def test_setting_extra_configs(settings):
    assert send_email.queue == 'django_email'
    assert send_email.delivery_mode == 1
    assert send_email.rate_limit == '50/m'


def test_backend_parameters(settings):
    default_backend = celery_mailer.tasks.BACKEND

    celery_mailer.tasks.BACKEND = 'tests.conftest.TestBackend'

    results = mail.send_mail('test', 'Testing with Celery! w00t!!', 'from@example.com',
                             ['to@example.com'], auth_user='username', auth_password='password')

    for result in results:
        assert result.get() == {'username': 'username', 'password': 'password'}

    celery_mailer.tasks.BACKEND = default_backend
