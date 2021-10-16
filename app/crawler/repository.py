import json
from app.config import config
from app.config.github_api import GithubAPI
from app.crawler.base import BaseCrawler


class RepoCrawler(BaseCrawler):
    """
    Crawl a repository's information
    """

    def __init__(self):
        super().__init__()
        self.api = GithubAPI()

    def parse_repo(self, url) -> dict:
        repo_name = url.split('/')[-2:]
        repo_name = repo_name[0] + '/' + repo_name[1]
        repo = {}
        info = self.api.get_info(repo_name)
        repo.update({'repo_info': info})
        # TODO: update more features
        feats = ['languages', 'contributors', 'tags', 'teams', 'topics', 'events']
        for feat in feats:
            repo.update({feat: self.api.get_repo_feature(repo_name, feat)})
        return repo
