from articles.models import Article
from rest_framework import serializers


class ArticleListSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Article
        fields = [
            'title',
            'content'
        ]

    def get_content(self, object):
        content = object.content[:700]
        return content


class ArticleDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = [
            'title',
            'url',
            'content'
        ]