import logging

import requests
from typic import URL as url_type, NetworkAddressValueError

from articles.models import Article

logger = logging.getLogger(__name__)


def create_article_object(title: str, url: url_type, content: str) -> None:
    """Create Article-object if does not exists in the DataBase.
    """
    article_obj = Article.objects.filter(
        title=title,
        url=url
    )
    if not article_obj.exists():
        try:
            article = Article.objects.create(
                title=title,
                url=url,
                content=content
            )
            article.save()
        except requests.exceptions.InvalidSchema:
            logger.error(NetworkAddressValueError(f"{url!r} is not a valid network address."))
