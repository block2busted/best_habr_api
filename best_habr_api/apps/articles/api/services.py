from typic import URL as url_type

from articles.models import Article


def create_article_object(title: str, url: url_type, content: str) -> None:
    """Create Article-object if does not exists in the DataBase.
    """
    article_obj = Article.objects.filter(
        title=title,
        url=url
    )
    if not article_obj.exists():
        article = Article.objects.create(
            title=title,
            url=url,
            content=content
        )
        article.save()
