from celery import shared_task

from .parsers import HabrParser


@shared_task
def parse_articles():
    """Parse and create best articles from https://habr.com/ru every days.
    """
    parser = HabrParser()
    parser.parse_and_create_articles()
