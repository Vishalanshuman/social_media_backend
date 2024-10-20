import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')

app = Celery('social_media_backend')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_daily_emails_except_weekends': {
        'task': 'apps.common.tasks.send_daily_emails',
        'schedule': crontab(hour=6, minute=0, day_of_week='mon,tue,wed,thu,fri'),
    },
}


app.conf.beat_schedule = {
    'update-user-data-weekly': {
        'task': 'apps.common.tasks.upload_user_data_to_s3',
        'schedule': crontab(0, 0, day_of_week='mon'),  
    },
}


# app.conf.beat_schedule = {
#     'send-daily-emails': {
#         'task': 'apps.common.tasks.send_daily_emails',
#         'schedule': 10.0,  # Run every 10 seconds
#     },
# }
app.conf.broker_url = 'redis://localhost:6379/0'
app.conf.broker_connection_retry_on_startup = True
