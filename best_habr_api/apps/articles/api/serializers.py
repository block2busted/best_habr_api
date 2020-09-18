from articles.models import Article
from rest_framework import serializers


class ArticleListSerializer(serializers.ModelSerializer):
    """Serializer of Article-object on ListAPIView
    with title and first 700 characters of object content fields.
    """
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
    """Serializer of Article-object on DetailAPIView
    with title, url and content fields.
    """
    class Meta:
        model = Article
        fields = [
            'title',
            'url',
            'content'
        ]