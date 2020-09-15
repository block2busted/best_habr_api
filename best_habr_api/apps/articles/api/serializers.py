from articles.models import Article
from rest_framework import serializers


class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = [
            'title',
            'url',
            'content'
        ]

    def get_content(self, value):
        return value[:700]

