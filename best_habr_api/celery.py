from __future__ import absolute_import

import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'best_habr_api.settings')

app = Celery('best_habr_api')
app.config_from_object('django.conf:settings')
app.conf.beat_schedule = {
    'test-task': {
        'task': 'articles.api.tasks.parse_articles',
        'schedule': crontab(minute=0, hour=0),
    },
}
app.autodiscover_tasks(settings.INSTALLED_APPS)