import os
from celery import Celery
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'best_habr_api.settings')

app = Celery('best_habr_api')
app.config_from_object('django.conf:settings')
app.conf.beat_schedule = {
    'parse-articles': {
        'task': 'articles.tasks.parse_articles',
        'schedule': settings.CELERY_PARSE_TASK_SCHEDULE
    }
}

app.autodiscover_tasks(settings.INSTALLED_APPS)
