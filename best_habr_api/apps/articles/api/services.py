import requests
from bs4 import BeautifulSoup

from articles.models import Article


HEADERS = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
        'accept': '/*/'
    }


def get_data(URL, HEADERS):
    """Return text-data."""
    data = requests.get(URL, headers=HEADERS).text
    return data


def get_pages_count(data):
    """Return pages count."""
    soup = BeautifulSoup(data, 'html.parser')
    pagination = soup.find_all('li', class_='toggle-menu__item_pagination')
    pages_count = len(pagination)
    return pages_count


def get_article_content(url, HEADERS):
    """Return article content."""
    content_data = get_data(URL=url, HEADERS=HEADERS)
    soup = BeautifulSoup(content_data, 'html.parser')
    content_soup = soup.find('div', class_='post__text')
    valid_tags = ('p', 'h2')
    content_list = []
    for tag in content_soup.descendants:
        if tag.name in valid_tags:
            content_list.append(tag.get_text().replace(u'\xa0', ' ').strip('\r \n'))
        if not tag.name:
            content_list.append(tag.replace(u'\xa0', ' ').strip('\r \n'))
    content = ''.join(content_list)
    return content


def create_article(title, url, content):
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


def parse_and_create_article_list(URL, HEADERS):
    """Parse article fields and create objects."""
    data = get_data(URL, HEADERS)
    soup = BeautifulSoup(data, 'html.parser')
    items = soup.find_all('article', class_='post_preview')

    for item in items:
        title = item.find('a', class_='post__title_link').get_text()
        article_url = item.find('a', class_='post__title_link').get('href')
        content = get_article_content(url=article_url, HEADERS=HEADERS)
        create_article(title, article_url, content)


def parse_and_create_articles():
    """Parse and create article."""
    URL = 'https://habr.com/ru'

    data = get_data(URL, HEADERS)
    pages_count = get_pages_count(data)

    for page_number in range(pages_count+1):
        URL = 'https://habr.com/ru/page' + str(page_number)
        parse_and_create_article_list(URL, HEADERS)
