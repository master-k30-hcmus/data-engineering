from tqdm import tqdm
from re import findall
from pymongo.collection import Collection

from app.config.logger import Logger
from app.crawler.repository import RepoCrawler


class TopicCrawler(RepoCrawler):
    def __init__(self, collection: Collection):
        super().__init__()
        self.logger = Logger(name=type(self).__name__)
        self.collection = collection
        self.base_url = 'https://github.com/topics'
        self.query_params = 'o=desc&s=updated'  # sort by recently updated

    def crawl(self):
        self.logger.info(f'Start crawl topic page')

        soup = self.make_soup(url=self.base_url)
        page_source = soup.prettify()

        # fetch popular topics
        topics = self.find_by_xpath(page_source, '//*[@id="js-pjax-container"]/div[4]/div[2]//ul/li/a/@title')
        topics = [t.replace("Topic: ", "") for t in topics]
        for topic in topics:
            repos = self._parse_topic_page(topic)
            self.upsert_many(repos)
            self.logger.info(f"Upserted topic={topic}")

    def upsert_many(self, repos):
        for repo in repos:
            self.collection.update_one(filter={"name": repo.get("name")}, update={"$set": repo}, upsert=True)

    def _parse_topic_page(self, topic: str):
        topic_url = f'{self.base_url}/{topic}?{self.query_params}'
        self.browser.get(topic_url)

        # TODO: uncomment later when app's stable
        # while True:
        #     try:
        #         WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="js-pjax-container"]/div[2]/div[2]/div/div[1]/form/button'))).click()
        #         time.sleep(3)
        #     except TimeoutException:
        #         print("No more LOAD MORE RESULTS button to be clicked")
        #         break

        page_source = self.browser.page_source

        topic_info = self.find_one_by_xpath(page_source, '//h2[@class="h3 color-text-secondary"]/text()')
        topic_info = topic_info.replace(",", "")
        num_repo = findall(r'\d+', topic_info)
        self.logger.info(f"Total {num_repo[0]} repositories in topic={topic}")

        hrefs = self.find_by_xpath(page_source, '//div[@class="col-md-8 col-lg-9"]/article/div[1]/div/div[1]/h3/a[2]/@href')
        self.logger.info(f"Fetch {len(hrefs)} repositories")

        repos = []
        for _, href in enumerate(tqdm(hrefs)):
            url = 'https://github.com' + href
            repo = self.parse_repo(url)
            if repo:
                repo.update({"topic": topic})
                repos.append(repo)
        return repos
