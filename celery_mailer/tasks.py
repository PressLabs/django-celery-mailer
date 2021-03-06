from django.conf import settings
from django.core.mail import get_connection
from django.core.mail.message import EmailMessage

from celery import Celery
from celery.utils.log import get_task_logger


CONFIG = getattr(settings, 'CELERY_EMAIL_TASK_CONFIG', {})
BACKEND = getattr(settings, 'CELERY_EMAIL_BACKEND',
                  'django.core.mail.backends.smtp.EmailBackend')
TASK_CONFIG = {
    'name': 'celery_mailer_send',
    'ignore_result': True,
}

TASK_CONFIG.update(CONFIG)

celery = Celery('celery_mailer')
celery.config_from_object(settings)
logger = get_task_logger(TASK_CONFIG['name'])


@celery.task(**TASK_CONFIG)
def send_email(msg, **kwargs):
    message = EmailMessage()
    for field in msg:
        setattr(message, field, msg[field])

    conn = get_connection(backend=BACKEND, **kwargs.pop('_backend_init_kwargs', {}))
    try:
        result = conn.send_messages([message])
        logger.debug('Successfully sent email message to %r.' % message.to)
        return result
    except Exception as e:
        # Catching all exceptions b/c it could be any number of things
        # depending on the backend
        logger.warning('Failed to send email message to %r, retrying.' % message.to)

        if getattr(settings, 'USE_CELERY', True):
            send_email.retry(exc=e)
        else:
            return None
