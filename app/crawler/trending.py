from repository import RepoCrawler


class TrendingCrawler(RepoCrawler):
    def __init__(self):
        super().__init__()
        self.base_url = 'https://github.com/trending'
