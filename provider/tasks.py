from celery import shared_task
import time
from provider.models import SMS
from provider.views import update_sms_statuses

@shared_task
def execute_work():
    update_sms_statuses()
    