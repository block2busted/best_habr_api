import requests
from bs4 import BeautifulSoup

from articles.models import Article


def get_data(URL, HEADERS):
    """Return text-data"""
    data = requests.get(URL, headers=HEADERS).text
    return data


def get_article_content(url, HEADERS):
    """Return article content."""
    content_data = get_data(URL=url, HEADERS=HEADERS)
    content_soup = BeautifulSoup(content_data, 'html.parser')
    content_items = content_soup.find('div', class_='post__body')
    content = []
    for node in content_items.descendants:
        if not node.name:
            content.append(node.strip('\r'.replace('\n', ' ')))
    content_string = ''.join(content)
    return content_string


def create_article(title, url, content):
    """Create article objects."""
    article = Article.objects.create(
        title=title,
        url=url,
        content=content
    )
    article.save()


def get_article_fields(data):
    """Get article title, url and content."""
    soup = BeautifulSoup(data, 'html.parser')
    items = soup.find_all('article', class_='post_preview')
    for item in items:
        title = item.find('a', class_='post__title_link').get_text()
        article_url = item.find('a', class_='post__title_link').get('href')
        content = get_article_content(url=article_url, HEADERS=HEADERS)
        create_article(title, article_url, content)


def parse_and_create_articles():
    """Parse and create article."""
    URL = 'https://habr.com/ru/'
    HEADERS = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
        'accept': '/*/'
    }

    data = get_data(URL, HEADERS)
    get_article_fields(data)


if __name__ == '__main__':
    parse_and_create_articles()