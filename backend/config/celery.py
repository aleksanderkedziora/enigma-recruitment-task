# celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config', include=['apps.orders.tasks'])
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.enable_utc = False

app.conf.update(timezone='Europe/Warsaw')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-payment-reminder': {
        'task': 'send_payment_remind_email',
        'schedule': crontab(hour='00', minute='00'),  # Run daily at midnight
    },
}

