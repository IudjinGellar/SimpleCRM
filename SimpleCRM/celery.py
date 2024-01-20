import os
from celery import Celery
from django.conf import settings
from kombu import Exchange, Queue

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'SimpleCRM.settings')

app = Celery('SimpleCRM')

app.config_from_object('django.conf:settings',
                       namespace='CELERY')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

task_exchange = Exchange('tasks', type='direct')
task_queues = [Queue('sender', task_exchange, routing_key='sender'),
               Queue('worker', task_exchange, routing_key='worker')
               ]
