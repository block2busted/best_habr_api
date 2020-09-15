from rest_framework import generics

from articles.models import Article

from .serializers import ArticleListSerializer, ArticleDetailSerializer


class ArticleListAPIView(generics.ListAPIView):
    """"""
    permission_classes = []
    authentication_classes = []
    queryset = Article.objects.all()
    serializer_class = ArticleListSerializer


class ArticleDetailAPIView(generics.RetrieveAPIView):
    """"""
    permission_classes = []
    authentication_classes = []
    queryset = Article.objects.all()
    serializer_class = ArticleDetailSerializer