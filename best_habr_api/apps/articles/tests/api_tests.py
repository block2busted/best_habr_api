import os
from collections import OrderedDict

import pytest
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse as api_reverse
from rest_framework import status

from articles.models import Article


class ArticleAPITestCase(APITestCase):
    def setUp(self) -> None:
        article_1 = Article.objects.create(
            title='First article.',
            url='https://github.com',
            content='First article content.'
        )
        article_1.save()
        article_2 = Article.objects.create(
            title='Second article.',
            url='https://habr.com/ru',
            content='Second article content.'
        )
        article_2.save()

    def test_created_articles(self):
        qs = Article.objects.all()
        self.assertEqual(qs.count(), 2)

    def test_article_detail_api(self):
        endpoint = api_reverse('articles-api:article-detail', kwargs={'pk': 1})
        parameters = {'pk': 1}
        response = self.client.get(endpoint, parameters, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_response_data = {
            'title': 'First article.',
            'url': 'https://github.com',
            'content': 'First article content.'
        }
        self.assertEqual(response.data, expected_response_data)

    def test_article_detail_api_fail(self):
        endpoint = api_reverse('articles-api:article-detail', kwargs={'pk': 3})
        parameters = {'pk': 3}
        response = self.client.get(endpoint, parameters, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        expected_response_data = {
            'detail': ErrorDetail(string='Не найдено.', code='not_found')
        }
        self.assertEqual(response.data, expected_response_data)

    def test_article_list_api(self):
        endpoint = api_reverse('articles-api:articles')
        response = self.client.get(endpoint, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_response_data = OrderedDict(
            [
                ('count', 2),
                ('next', None),
                ('previous', None),
                ('results', [
                    OrderedDict(
                        [
                            ('title', 'Second article.'),
                            ('content', 'Second article content.')
                        ]
                    ),
                    OrderedDict(
                        [
                            ('title', 'First article.'),
                            ('content', 'First article content.')
                        ]
                    )
                ]
                 )
            ]
        )
        self.assertEqual(response.data, expected_response_data)
