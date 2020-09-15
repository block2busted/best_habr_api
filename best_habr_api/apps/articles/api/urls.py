from django.urls import path
from .views import ArticleListAPI


urlpatterns = [
    path('', ArticleListAPI.as_view(), name='articles'),
]