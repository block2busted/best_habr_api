import requests
from bs4 import BeautifulSoup
from typic import URL as url_type, NetworkAddressValueError
import logging

from articles.api.services import create_article_object

logger = logging.getLogger(__name__)


class HabrParser:
    """Parser for best articles from habr."""
    URL = url_type('https://habr.com/ru/')
    HEADERS = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
        'accept': '/*/'
    }

    def get_data(self, URL: url_type) -> requests.models.Response:
        """Return data."""
        try:
            data = requests.get(URL, headers=self.HEADERS)
            return data
        except requests.exceptions.InvalidSchema:
            logger.error(NetworkAddressValueError(f"{URL!r} is not a valid network address."))
        except (requests.ConnectionError, requests.exceptions.TooManyRedirects, requests.exceptions.RequestException) as e:
            logger.error(e)

    def get_pages_count(self, data: requests.models.Response) -> str:
        """Return pages count."""
        soup = BeautifulSoup(data.text, 'html.parser')
        pages_count = soup.find_all('a', class_='toggle-menu__item-link_pagination')[-1].get_text()
        return pages_count

    def get_article_content(self, URL: url_type) -> str:
        """Return article content."""
        content_data = self.get_data(URL)
        soup = BeautifulSoup(content_data.text, 'html.parser')
        article_content = soup.find('div', class_='post__text')
        valid_tags = ('p', 'h2')
        content_list = []
        for tag in article_content.descendants:
            if tag.name in valid_tags:
                content_list.append(tag.get_text().replace(u'\xa0', ' ').strip('\r \n'))
            if not tag.name:
                content_list.append(tag.replace(u'\xa0', ' ').strip('\r \n'))
        content = ''.join(content_list)
        return content

    def parse_and_create_article_list(self, URL: url_type):
        """Parse article fields and create objects."""
        data = self.get_data(URL)
        soup = BeautifulSoup(data.text, 'html.parser')
        article_list_from_one_page = soup.find_all('article', class_='post_preview')

        for article in article_list_from_one_page:
            title = article.find('a', class_='post__title_link').get_text()
            article_url = article.find('a', class_='post__title_link').get('href')
            content = self.get_article_content(article_url)
            create_article_object(title, article_url, content)

    def parse_and_create_articles(self):
        """Parse and create article."""
        data = self.get_data(self.URL)
        pages_count = int(self.get_pages_count(data))
        for page_number in range(1, pages_count + 1):
            self.parse_and_create_article_list(url_type(f'{self.URL}page{page_number}'))
        logger.info('Parsing completed successfully.')
