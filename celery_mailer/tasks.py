from django.conf import settings
from django.core.mail import get_connection
from celery.task import task

from celery_mailer.serializer import deserialize


CONFIG = getattr(settings, 'CELERY_EMAIL_TASK_CONFIG', {})
BACKEND = getattr(settings, 'CELERY_EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')

TASK_CONFIG = {
    'name': 'celery_mailer_send',
    'ignore_result': True,
}

TASK_CONFIG.update(CONFIG)


@task(**TASK_CONFIG)
def send_email(message, **kwargs):

    serializer_type = getattr(settings, 'CELERY_TASK_SERIALIZER', None)
    if serializer_type == 'json':
        message = deserialize(message)

    logger = send_email.get_logger()
    conn = get_connection(backend=BACKEND, **kwargs.pop('_backend_init_kwargs', {}))

    try:
        result = conn.send_messages([message])
        logger.debug('Successfully sent email message to %r.' % message.to)
        return result

    except Exception, e:

        # Catching all exceptions b/c it could be any number of things
        # depending on the backend
        logger.warning('Failed to send email message to %r, retrying.' % message.to)

        if getattr(settings, 'USE_CELERY', True):
            send_email.retry(exc=e)
        else:
            return None
