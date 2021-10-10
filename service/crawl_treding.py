import os
import time
import requests
import progressbar
import logging
from tqdm import tqdm
from bs4 import BeautifulSoup

import utils


#Set up logger
#TODO: need to seperate with this file
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('log_data.log')
formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


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

    def collect_treding_page(self):
        """Collect all items of trending and repo pages

        Returns:
            components (list):
        """
        soup = self._request_page(self.SITE)
        # treding page
        boxes = soup.find_all('article', class_="Box-row")
        components = []
        for box in boxes:
            # fetch link
            ref = box.find('h1', class_="h3 lh-condensed").get_text()
            ref = utils.preprocess_get_text(ref)
            ref = 'https://github.com/{}'.format(ref)
            # fetch description
            try:
                info = box.find('p', class_="col-9 color-text-secondary my-1 pr-4").get_text() 
                info = info.replace('\n', '')
            except AttributeError: 
                logger.debug(f'There is no description in {ref}')
                info = None
            # fetch star, folks and today_star
            interact_box = box.find('div',  class_="f6 color-text-secondary mt-2")
            interact_box_items = interact_box.find_all('a')
            items = []
            for item in interact_box_items:
                try:
                    res = item.get_text() 
                    res = utils.preprocess_get_text(res)
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
            # wrap up components
            results = {
                'link': ref,
                'info': info,
                'star': items[0],
                'folks': items[1],
                'today_star': today_star
            }
            components.append(results)
        logger.info('Successfully fetch trending page')
        return(components)

    def collect_repo_items(self, repo_link='https://github.com/qier222/YesPlayMusic'):
        """Get information from a repo
        
        Params:
            repo_link (str): link to repository
        Returns:
            repo_info (dict):
        """
        main_page = self._request_page(repo_link)
        # fetch issue
        issues_box = main_page.find('a', {'id': 'issues-tab'})
        num_issues = int(issues_box.find('span', class_='Counter').get_text())
        # fetch last commit time
        last_commit_time = main_page.find('a', class_='Link--secondary ml-2')
        last_commit_time = last_commit_time.find('relative-time', class_='no-wrap')
        last_commit_time = last_commit_time.attrs.get('datetime')
        # fetch tags
        #TODO: exception without tags
        tag_pool = main_page.find_all('a', {'data-ga-click': 'Topic, repository page'})
        tag_pool = [utils.preprocess_get_text(tag_pool[idx].get_text()) for idx in range(len(tag_pool))]
        # fetch languages
        try:
            list_lang = main_page.find_all('div', class_='BorderGrid-cell')
            list_lang = [item.find_all('li', class_='d-inline') for item in list_lang]
            list_lang = [item for item in list_lang if len(item) > 0][0]
            list_lang = [lang_box.find_all('span') for lang_box in list_lang]
            ## unpack languages 
            NORMAL_LENGTH_OF_LANGUAGE = 2
            languages = []
            for lang_data in list_lang:
                if len(lang_data) == NORMAL_LENGTH_OF_LANGUAGE:
                    lang = lang_data[0]
                    process = lang_data[1]
                    languages.append((lang.get_text(), process.get_text()))
                else: # Other language
                    lang = lang_data[1]
                    process = lang_data[2]
                    languages.append((lang.get_text(), process.get_text()))
        except IndexError: # there is no languages
            logger.debug(f'There is no language in {repo_link}')
            languages = []
        repo_info = {
            'num_issues': num_issues,
            'last_commit_time': last_commit_time,
            'tags': tag_pool,
            'languages': languages 
        }
        return(repo_info)

    def get_trend_for_db(self):
        """ Fetch data for database"""
        # get trending page
        print('Get trending page')
        repo_pool = self.collect_treding_page()
        num_repo = len(repo_pool)
        # get each repo page
        print('Get each repo page')
        process_bar = progressbar.ProgressBar(maxval=100)
        process_bar.start()
        for idx, repo in enumerate(repo_pool):
            fetch_tried = 0
            while 1: # try to fetch until get enough information
                try:
                    repo_info = crawler.collect_repo_items(repo['link'])
                    repo_pool[idx].update(repo_info)
                    if fetch_tried > 0:
                        logger.warning(f"Sucessfull got information from {repo['link']} after {fetch_tried} times")
                    break
                except AttributeError:
                    fetch_tried+=1
                    MAX_FETCH_TRIED = 10 
                    if fetch_tried > MAX_FETCH_TRIED:
                        logger.warning(f"Cannot get enough information from {repo['link']}")
                        break
                    # pause 2s before fetch again
                    time.sleep(2)
            process_bar.update(int(idx*100/num_repo))
        return repo_pool

if __name__=='__main__':
    crawler = TrendingCrawler()
    crawler.get_trend_for_db()
