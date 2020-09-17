from typic import URL as url_type

from articles.models import Article


def create_article_object(title: str, url: url_type, content: str):
    """Create article object if it not already in the database."""
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
