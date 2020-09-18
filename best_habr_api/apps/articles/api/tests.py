import pytest

from articles.models import Article
from rest_framework import serializers

@pytest.fixture
def create_article():
    article_obj = Article.objects.create(
        title='Article title.',
        url='https://www.django-rest-framework.org',
        content='Some short content.'
    )

    article_serializer = serializers.ModelSerializer(model=Article, fields=['title', 'url', 'content'])

    jsonify_article = article_obj(article_serializer)

    valid_response = {
        "title": "Article title.",
        "url": "https://www.django-rest-framework.org",
        "content": "Some short content"
    }
    assert jsonify_article == valid_response
