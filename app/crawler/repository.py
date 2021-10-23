from time import time

from app.config.logger import Logger
from app.api.github import GithubAPI
from app.crawler.base import BaseCrawler


class RepoCrawler(BaseCrawler):
    """
    Crawl a repository's information
    """

    def __init__(self):
        super().__init__()
        self.logger = Logger(name=type(self).__name__)
        self.api = GithubAPI()

    def parse_repo(self, url) -> dict:
        repo_name = url.split('/')[-2:]
        repo_name = repo_name[0] + '/' + repo_name[1]
        repo = {"crawled_at": time()}
        info = self.api.get_info(repo_name)
        repo.update({'repo_info': info})
        # TODO: update more features
        feats = ['languages', 'contributors', 'tags', 'teams', 'topics', 'events']
        for feat in feats:
            repo.update({feat: self.api.get_repo_feature(repo_name, feat)})
        return repo
