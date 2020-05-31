#########################
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.apps import apps
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'youtube_search.settings')

app = Celery('youtube_search')

app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])

# app.conf.beat_schedule = {
#     'fetch-every-10-seconds': {
#         'task': 'tasks.fetch',
#         'schedule': 10.0
#     },
# }

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

@app.task
def fetch_data():
    from .utils import YouTubeApi
    YouTubeApi().store_recent_data()
    return True
