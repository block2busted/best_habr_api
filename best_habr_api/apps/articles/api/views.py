from rest_framework import generics

from articles.models import Article
from .serializers import ArticleListSerializer


class ArticleListAPI(generics.ListAPIView):
    """"""
    permission_classes = []
    authentication_classes = []
    queryset = Article.objects.all()
    serializer_class = ArticleListSerializer

