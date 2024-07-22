import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bicycle_sharing.settings')
app = Celery('bicycle_sharing')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
