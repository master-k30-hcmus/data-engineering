from tqdm import tqdm
from re import findall
from pymongo.collection import Collection

from app.config.logger import Logger
from app.crawler.repository import RepoCrawler


class TrendingCrawler(RepoCrawler):
    def __init__(self, collection: Collection):
        super().__init__()
        self.logger = Logger(name=type(self).__name__)
        self.collection = collection
        self.base_url = 'https://github.com/trending'

    def _crawl_trending_page(self):
        """Collect all items of trending and repo pages

        Returns:
            components (list):
        """
        soup = self.make_soup(url=self.base_url)
        page_source = soup.prettify()

        components = []
        repo_boxes = self.find_by_xpath(page_source, '//*[@id="js-pjax-container"]/div[3]/div/div[2]/article[@class="Box-row"]')
        for ith, repo in enumerate(repo_boxes):
            repo_name = self.find_one_by_xpath(repo, '//h1/a/@href')

            # fetch star, folks and today_star
            today_star = self.find_by_xpath(repo, '//div[2]/span[@class="d-inline-block float-sm-right"]/text()')[1]
            today_star = today_star.strip()
            today_star = findall(r'\d+', today_star)[0]

            # wrap up components
            repo_info = {
                'name': repo_name,
                'link': f"https://github.com{repo_name}",
                'rank': ith,
                'today_star': int(today_star)
            }
            components.append(repo_info)

        self.logger.info('Successfully fetch trending page')
        return components

    def crawl(self):
        """ Fetch data for database"""
        self.logger.info(f'Start crawl trending page')

        # get trending page
        repo_pool = self._crawl_trending_page()
        num_repo = len(repo_pool)
        self.logger.info(f'Fetch {num_repo} repositories')

        # get each repo page
        for idx, repo in enumerate(tqdm(repo_pool)):
            repo_info = self.parse_repo(repo['link'])
            repo_pool[idx].update(repo_info)

        self.upsert_many(repo_pool)
        self.logger.info(f"Upserted {num_repo} trending repos.")

        return repo_pool

    def upsert_many(self, repos):
        for repo in repos:
            self.collection.update_one(filter={"name": repo.get("name")}, update={"$set": repo}, upsert=True)
