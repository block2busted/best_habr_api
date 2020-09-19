import os
from collections import OrderedDict
import py
import pytest
import requests
import responses
from django.test import TestCase
from rest_framework import status
from typic import URL as url_type
from rest_framework.reverse import reverse as api_reverse

from articles.parsers import HabrParser
from articles.models import Article

_dir = os.path.dirname(os.path.realpath(__file__))

FIXTURE_DIR = py.path.local(_dir)


class GetDataMethodTestCase(TestCase):
    @pytest.mark.datafiles(FIXTURE_DIR/'html_body/article_list_body.html')
    def setUp(self) -> None:
        with open(FIXTURE_DIR/'html_body/article_list_body_page_1.html') as html_body_file:
            html_body = ''.join(html_body_file.readlines())
        responses.add(
            responses.Response(
                method='GET',
                url='https://habr.com/ru/',
                body=html_body,
                status=200,

            )
        )
        responses.add(
            responses.Response(
                method='GET',
                url='https://habr.com/ru/connection_error/',
                status=502,
            )
        )
        self.habr_parser = HabrParser()
        self.URL = url_type('https://habr.com/ru/')

    @responses.activate
    def test_connection(self):
        r = requests.get('https://habr.com/ru/')
        self.assertEqual(r.text[:15], '<!DOCTYPE html>')
        self.assertEqual(r.status_code, 200)

    @responses.activate
    def test_method(self):
        data = self.habr_parser.get_data(self.URL)
        self.assertEqual(type(data), requests.models.Response)

    @responses.activate
    def test_NetworkAddressValueError_handler(self):
        try:
            return HabrParser().get_data('it is https://not_url_type.com')
        except requests.exceptions.InvalidSchema:
            raise

    @responses.activate
    def test_RequestException_handler(self):
        try:
            return self.habr_parser.get_data('https://habr.com/ru/connection_error/')
        except requests.exceptions.RequestException:
            raise


class GetPagesCountMethodTestCase(TestCase):
    @pytest.mark.datafiles(
        FIXTURE_DIR/'html_body/article_list_passed_pagination_body.html',
        FIXTURE_DIR/'html_body/article_list_body_page_1.html'
    )
    def setUp(self) -> None:
        with open(FIXTURE_DIR/'html_body/article_list_body_page_1.html') as body_with_pagination_file:
            body_with_pagination = ''.join(body_with_pagination_file.readlines())
        responses.add(
            responses.Response(
                method='GET',
                url='https://habr.com/ru/',
                body=body_with_pagination,
                status=200,
            )
        )

        with open(FIXTURE_DIR/'html_body/article_list_passed_pagination_body.html') as body_passed_pagination_file:
            body_passed_pagination = ''.join(body_passed_pagination_file.readlines())
        responses.add(
            responses.Response(
                method='GET',
                url='https://habr.com/ru/pagination_fail/',
                body=body_passed_pagination,
                status=200,
            )
        )

        self.habr_parser = HabrParser()
        self.URL = url_type('https://habr.com/ru/')
        self.URL_with_passed_pagination = url_type('https://habr.com/ru/pagination_fail/')

    @responses.activate
    def test_connection(self):
        r = requests.get('https://habr.com/ru/')
        self.assertEqual(r.text[:15], '<!DOCTYPE html>')
        self.assertEqual(r.status_code, 200)

    @responses.activate
    def test_method(self):
        data = self.habr_parser.get_data(self.URL)
        pages_count = self.habr_parser.get_pages_count(data)
        self.assertEqual(pages_count, 2)

    @responses.activate
    def test_IndexError_fail(self):
        try:
            self.habr_parser.get_data(self.URL_with_passed_pagination)
        except IndexError:
            raise


class GetArticleContentMethodTestCase(TestCase):
    @pytest.mark.datafiles(FIXTURE_DIR/'html_body/first_article_content_body.html')
    def setUp(self) -> None:
        with open(FIXTURE_DIR/'html_body/first_article_content_body.html') as article_body_file:
            article_html_body = ''.join(article_body_file.readlines())
        responses.add(
            responses.Response(
                method='GET',
                url='https://habr.com/ru/post/1/',
                body=article_html_body,
                status=200,

            )
        )
        self.habr_parser = HabrParser()
        self.URL = url_type('https://habr.com/ru/post/1/')

    @responses.activate
    def test_connection(self):
        r = requests.get('https://habr.com/ru/post/1/')
        self.assertEqual(r.text[:15], '<!DOCTYPE html>')
        self.assertEqual(r.status_code, 200)

    @responses.activate
    def test_method(self):
        content = self.habr_parser.get_article_content(self.URL)
        self.assertEqual(content, 'First article content. It is a p tag. The end.')


class ParseAndCreateArticlesOnSimplePageTestCase(TestCase):
    @pytest.mark.datafiles(
        FIXTURE_DIR/'html_body/article_list_body_page_1.html',
        FIXTURE_DIR/'html_body/first_article_content_body.html',
        FIXTURE_DIR/'html_body/second_article_content_body.html'
    )
    def setUp(self) -> None:
        with open(FIXTURE_DIR/'html_body/article_list_body_page_1.html') as article_body_file:
            article_list_body = ''.join(article_body_file.readlines())
        responses.add(
            responses.Response(
                method='GET',
                url='https://habr.com/ru/',
                body=article_list_body,
                status=200,
                match_querystring=True
            )
        )
        with open(FIXTURE_DIR/'html_body/first_article_content_body.html') as first_article_body_file:
            first_article_body = ''.join(first_article_body_file.readlines())
        responses.add(
            responses.Response(
                method='GET',
                url='https://habr.com/ru/post/1/',
                body=first_article_body,
                status=200,
                match_querystring=True
            )
        )
        with open(FIXTURE_DIR/'html_body/second_article_content_body.html') as second_article_body_file:
            second_article_body = ''.join(second_article_body_file.readlines())
        responses.add(
            responses.Response(
                method='GET',
                url='https://habr.com/ru/post/2/',
                body=second_article_body,
                status=200,
                match_querystring=True
            )
        )
        self.habr_parser = HabrParser()
        self.URL = 'https://habr.com/ru/'

    @responses.activate
    def test_connection(self):
        r = requests.get('https://habr.com/ru/')
        self.assertEqual(r.text[:15], '<!DOCTYPE html>')
        self.assertEqual(r.status_code, 200)

    @responses.activate
    def test_method(self):
        self.habr_parser.parse_and_create_articles_on_simple_page(self.URL)
        article_qs = Article.objects.all()
        self.assertEqual(article_qs.count(), 2)

    @responses.activate
    def test_method_fail(self):
        self.habr_parser.parse_and_create_articles_on_simple_page(self.URL)
        article_qs = Article.objects.all()
        self.assertEqual(article_qs.count(), 2)


class ParseAndCreateArticlesMethodTestCase(TestCase):
    @pytest.mark.datafiles(
        FIXTURE_DIR/'html_body/article_list_body_page_1.html',
        FIXTURE_DIR/'html_body/article_list_body_page_2.html',
        FIXTURE_DIR/'html_body/first_article_content_body.html',
        FIXTURE_DIR/'html_body/second_article_content_body.html',
        FIXTURE_DIR/'html_body/third_article_content_body.html'
    )
    def setUp(self) -> None:
        with open(FIXTURE_DIR/'html_body/article_list_body_page_1.html') as article_body_file:
            article_list_body = ''.join(article_body_file.readlines())
        responses.add(
            responses.Response(
                method='GET',
                url='https://habr.com/ru/',
                body=article_list_body,
                status=200,
                match_querystring=True
            )
        )
        responses.add(
            responses.Response(
                method='GET',
                url='https://habr.com/ru/page1',
                body=article_list_body,
                status=200,
                match_querystring=True
            )
        )
        with open(FIXTURE_DIR/'html_body/article_list_body_page_2.html') as second_page_article_body_file:
            second_article_list_body = ''.join(second_page_article_body_file.readlines())
        responses.add(
            responses.Response(
                method='GET',
                url='https://habr.com/ru/page2',
                body=second_article_list_body,
                status=200,
                match_querystring=True
            )
        )
        with open(FIXTURE_DIR/'html_body/first_article_content_body.html') as first_article_body_file:
            first_article_body = ''.join(first_article_body_file.readlines())
        responses.add(
            responses.Response(
                method='GET',
                url='https://habr.com/ru/post/1/',
                body=first_article_body,
                status=200,
                match_querystring=True
            )
        )
        with open(FIXTURE_DIR/'html_body/second_article_content_body.html') as second_article_body_file:
            second_article_body = ''.join(second_article_body_file.readlines())
        responses.add(
            responses.Response(
                method='GET',
                url='https://habr.com/ru/post/2/',
                body=second_article_body,
                status=200,
                match_querystring=True
            )
        )
        with open(FIXTURE_DIR/'html_body/third_article_content_body.html') as third_article_body_file:
            third_article_body = ''.join(third_article_body_file.readlines())
        responses.add(
            responses.Response(
                method='GET',
                url='https://habr.com/ru/post/3/',
                body=third_article_body,
                status=200,
                match_querystring=True
            )
        )
        self.habr_parser = HabrParser()
        self.URL = 'https://habr.com/ru/'

    @responses.activate
    def test_connection(self):
        r = requests.get(self.URL)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.text[:15], '<!DOCTYPE html>')

    @responses.activate
    def test_method(self):
        self.habr_parser.parse_and_create_articles()
        article_qs = Article.objects.all()
        self.assertEqual(article_qs.count(), 3)

    @responses.activate
    def test_valid_created(self):
        self.habr_parser.parse_and_create_articles()
        endpoint = api_reverse('articles-api:articles')
        response = self.client.get(endpoint, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_response_data = OrderedDict(
            [
                ('count', 3),
                ('next', None),
                ('previous', None),
                ('results', [
                    OrderedDict(
                        [
                            ('title', 'Third article title.'),
                            ('content', 'Some content of third article. And p teg. Complete.')
                        ]
                    ),
                    OrderedDict(
                        [
                            ('title', 'I`m second title!'),
                            ('content', 'Content of second article. It is a p tag. Ended.')
                        ]
                    ),
                    OrderedDict(
                        [
                            ('title', 'First article title.'),
                            ('content', 'First article content. It is a p tag. The end.')
                        ]
                    )
                ]
                 )
            ]
        )
        self.assertEqual(response.data, expected_response_data)

