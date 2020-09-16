from django.urls import path
from .views import ArticleListAPIView, ArticleDetailAPIView


urlpatterns = [
    path('', ArticleListAPIView.as_view(), name='articles'),
    path('<int:pk>/', ArticleDetailAPIView.as_view(), name='article-detail')
]