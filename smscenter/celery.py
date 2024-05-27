import os

from celery import Celery
from celery.schedules import crontab


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smscenter.settings')

app = Celery('smscenter')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


# Define Celery Beat schedule
app.conf.beat_schedule = {
    'run-task-every-hour': {
        'task': 'provider.tasks.execute_work',  # Path to your Celery task
        'schedule': crontab(minute=0, hour='*/1'),  # Run task every hour
    },
}