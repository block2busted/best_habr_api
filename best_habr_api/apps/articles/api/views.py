from rest_framework import generics

from articles.models import Article
from .serializers import ArticleListSerializer, ArticleDetailSerializer
from .paginations import ArticlePagination


class ArticleListAPIView(generics.ListAPIView):
    """Endpoint returning all Article-objects.
    """
    permission_classes = []
    authentication_classes = []
    queryset = Article.objects.all()
    serializer_class = ArticleListSerializer
    pagination_class = ArticlePagination


class ArticleDetailAPIView(generics.RetrieveAPIView):
    """Endpoint returning Article-object details by PK.
    """
    permission_classes = []
    authentication_classes = []
    queryset = Article.objects.all()
    serializer_class = ArticleDetailSerializer
