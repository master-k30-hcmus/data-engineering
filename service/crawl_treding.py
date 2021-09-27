import os
import requests
from bs4 import BeautifulSoup

class TrendingCrawler:
    def __init__(self):
        self.SITE = 'https://github.com/trending'

    def _request_page(self, link, method="lxml"):
        """Request page
        
        Params:
            link (str): link of page
        Returns:
            soup (bs4.BeautifulSoup):
        """
        page = requests.get(link)
        soup = BeautifulSoup(page.content, method)
        return soup

    def collect_components(self):
        """Collect all items of trending and repo pages"""
        soup = self._request_page(self.SITE)
        # treding page
        boxes = soup.find_all('article', class_="Box-row")
        components = []
        for box in boxes:
            # fetch link
            ref = box.find('h1', class_="h3 lh-condensed").get_text()
            ref = ref.replace('\n', '')
            ref = ref.replace(' ', '')
            ret = 'https://github.com/{}'.format(ref)
            # fetch description
            try:
                info = box.find('p', class_="col-9 color-text-secondary my-1 pr-4").get_text() 
                info = info.replace('\n', '')
            except AttributeError: # There is no description
                info = None
            # fetch star, folks and today_star
            interact_box = box.find('div',  class_="f6 color-text-secondary mt-2")
            interact_box_items = interact_box.find_all('a')
            items = []
            for item in interact_box_items:
                try:
                    res = item.get_text() 
                    res = res.replace('\n', '')
                    res = res.replace(' ', '')
                    res = res.replace(',', '')
                    items.append(int(res))
                except (TypeError, ValueError):
                    pass
            # fetch today stars
            today_star = interact_box.find('span', class_='d-inline-block float-sm-right')
            today_star = today_star.get_text()
            today_star = today_star.replace('\n', '')
            #TODO: try here to get if there is 0 star
            today_star = today_star.replace(' stars today', '')
            today_star = today_star.replace(' ', '')
            today_star = int(today_star)
            # fetch repo page
            repo_items = self._collect_repo_items(ref)
            # wrap up components
            results = {
                'link': ref,
                'info': info,
                'star': items[0],
                'folks': items[1],
                'today_star': today_star
            }.update(repo_items)
            components.append(results)
        return(components)

    def _collect_repo_items(self, repo_link):
        return({}) 

if __name__=='__main__':
    crawler = TrendingCrawler()
    crawler.collect_components()
