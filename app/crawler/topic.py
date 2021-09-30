from .repository import RepoCrawler


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
            repos = self._parse_topic_page(topic)
            all_repos.extend(repos)
        return all_repos

    def _parse_topic_page(self, topic: str):
        topic_url = f'{self.base_url}/{topic}?{self.query_params}'
        soup = self.make_soup(url=topic_url)
        page_source = soup.prettify()

        # TODO: crawl repos in topic, also update repo with extra info
        repos = []
        repo = self.parse_repo(url='https://github.com/nestjs/serve-static')
        if repo:
            repo.update({"topic": topic})
            repos.append(repo)
        return repos
