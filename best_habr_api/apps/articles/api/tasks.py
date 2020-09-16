from celery import shared_task

from .services import parse_and_create_articles

@shared_task
def test_task():
    parse_and_create_articles()
