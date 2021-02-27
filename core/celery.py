import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.development')

app = Celery('core')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    # Executes every 5 minutes
    'send_req_5': {
        'task': 'records.tasks.send_request', 
        'schedule': crontab(minute='*/120'),
        
    },
    'send_req_6': {
        'task' : 'records.tasks.send_request_cfscrape',
        'schedule': crontab(minute='*/120')
    },
    'send_req_7': {
        'task': 'records.tasks.delete_old_history',
        'schedule': crontab(minute='*/1440')
    }
}

