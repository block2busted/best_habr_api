import pytest
from unittest import TestCase

import requests
from typic import URL as url_type

from articles.api.services import create_article_object
from articles.models import Article


class CreateArticleObjectTestCase(TestCase):
    def setUp(self) -> None:
        create_article_object(
            title='Article title.',
            url=url_type('https://habr.com/ru/'),
            content='Some article content.'
        )

    @pytest.mark.django_db
    def test_created(self):
        qs = Article.objects.all()
        self.assertEqual(qs.count(), 1)

    @pytest.mark.django_db
    def test_NetworkAddressValueError_handler(self):
        try:
            create_article_object(
                title='Article title.',
                url='not valid https://url.com/',
                content='Some article content.'
            )
        except requests.exceptions.InvalidSchema:
            raise
