from .base import BaseCrawler
from time import sleep
from config import config


class RepoCrawler(BaseCrawler):
    """
    Crawl a repository's information
    """

    def parse_repo(self, url) -> dict:
        retry = 0
        while retry < config['MAX_FETCH_RETRY']:
            try:
                self.browser.get(url)
                page_source = self.browser.page_source

                # fetch number of issues
                num_issues = self.find_one_by_xpath(page_source, '//*[@id="issues-tab"]/span[@class="Counter"]/@title')

                # fetch last commit time
                repo_source = self.find_one_by_xpath(page_source, '//*[@id="repo-content-pjax-container"]')
                last_commit_time = self.find_one_by_xpath(page_source, '//div[contains(@class, "Box-header")]//relative-time/@datetime')

                # fetch tags
                tags = self.find_by_xpath(repo_source, '//a[@class="topic-tag topic-tag-link"]/@data-octo-dimensions')
                tags = [tag.replace("topic:", "") for tag in tags]

                # fetch languages
                languages = []
                lang_elements = self.find_by_xpath(repo_source, '//div[@class="BorderGrid-cell"]/ul[@class="list-style-none"]/li/a')
                for le in lang_elements:
                    pair = self.find_by_xpath(le, '//span/text()')
                    pair = [p.strip() for p in pair]
                    languages.append({"language": pair[0], "value": pair[1]})

                repo = {
                    'url': url,
                    'num_issues': num_issues,
                    'last_commit_time': last_commit_time,
                    'tags': tags,
                    'languages': languages
                }
                return repo
            except Exception:
                self.browser.refresh()
                retry += 1
                sleep(3)

        print(f"Max fetch retry. Skipped repo {url}")
        return dict()
