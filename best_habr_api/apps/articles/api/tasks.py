from celery import shared_task

from .services import parse_and_create_articles


@shared_task
def parse_articles():
    """Parse and create best articles from https://habr.com/ru every days."""
    parse_and_create_articles()