import re
from app.crawler.repository import RepoCrawler


class TopicCrawler(RepoCrawler):
    def __init__(self):
        super().__init__()
        self.base_url = 'https://github.com/topics'
        self.query_params = 'o=desc&s=updated'  # sort by recently updated

    def crawl(self):
        soup = self.make_soup(url=self.base_url)
        page_source = soup.prettify()

        # fetch popular topics
        topics = self.find_by_xpath(page_source, '//*[@id="js-pjax-container"]/div[4]/div[2]//ul/li/a/@title')
        topics = [t.replace("Topic: ", "") for t in topics]
        all_repos = []
        for topic in topics:
            print(f"Crawl topic [{topic}]")
            repos = self._parse_topic_page(topic)
            all_repos.extend(repos)
        return all_repos

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
        num_repo = re.findall(r'\d+', topic_info)
        print(f"Total {num_repo[0]} repos")

        hrefs = self.find_by_xpath(page_source, '//div[@class="col-md-8 col-lg-9"]/article/div[1]/div/div[1]/h3/a[2]/@href')
        print(f"Found {len(hrefs)} hrefs")

        repos = []
        for href in hrefs:
            url = 'https://github.com' + href
            print(f"Parsing repo {url}")
            repo = self.parse_repo(url)
            if repo:
                repo.update({"topic": topic})
                repos.append(repo)
        return repos
