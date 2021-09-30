import requests
import requests_random_user_agent  # get random user agent
from bs4 import BeautifulSoup
from lxml import html


class BaseCrawler:
    @staticmethod
    def _request(url):
        user_agent = requests.Session().headers['User-Agent']
        headers = {'user-agent': user_agent, 'referer': "https://github.com/"}
        session = requests.session()
        resp = session.get(url, headers=headers)
        return resp

    def make_soup(self, url, parser='lxml') -> BeautifulSoup:
        resp = self._request(url)
        soup = BeautifulSoup(resp.content, parser)
        return soup

    @staticmethod
    def find_by_xpath(html_source, xpath_expression):
        root = html.fromstring(html_source)
        result = root.xpath(xpath_expression)
        try:
            return [html.tostring(e) for e in result]
        except Exception:
            return result

    def find_one_by_xpath(self, html_source, xpath_expression):
        return self.find_by_xpath(html_source, xpath_expression)[0]
