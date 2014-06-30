from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend

from celery_mailer.tasks import send_email
from celery_mailer.serializer import serialize


class CeleryEmailBackend(BaseEmailBackend):

    def __init__(self, fail_silently=False, **kwargs):
        super(CeleryEmailBackend, self).__init__(fail_silently)
        self.init_kwargs = kwargs

    def send_messages(self, email_messages, **kwargs):
        results = []
        kwargs['_backend_init_kwargs'] = self.init_kwargs

        for msg in email_messages:
            if getattr(settings, 'USE_CELERY', True):
                results.append(send_email.delay(serialize(msg), **kwargs))
            else:
                result = send_email(serialize(msg), **kwargs)
                if result:
                    results.append(result)

        return results
