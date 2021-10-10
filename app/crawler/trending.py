from app.crawler.repository import RepoCrawler


class TrendingCrawler(RepoCrawler):
    def __init__(self):
        super().__init__()
        self.base_url = 'https://github.com/trending'

    def _crawl_trending_page(self):
        """Collect all items of trending and repo pages

        Returns:
            components (list):
        """
        # treding page
        soup = self.make_soup(url=self.base_url)
        page_source = soup.prettify()
        components = []
        repo_boxes = self.find_by_xpath(page_source, '//*[@id="js-pjax-container"]/div[3]/div/div[2]/article[@class="Box-row"]')
        for ith, repo in enumerate(repo_boxes):
            repo_name = self.find_one_by_xpath(repo, '//h1/a/@href')
            # fetch star, folks and today_star
            #TODO: fix this
            #today_star = self.find_one_by_xpath(page_source, '//*[@id="js-pjax-container"]/div[3]/div/div[2]/article[2]/div[2]/span[3]/text()')
            today_star = "TODO"
            # wrap up components
            repo_info = {
                'name': repo_name,
                'link': f"https://github.com/{repo_name}",
                'rank': ith,
                'today_star': today_star
            }
            components.append(repo_info)
        #logger.info('Successfully fetch trending page')
        return(components)

    def crawl(self):
        """ Fetch data for database"""
        # get trending page
        repo_pool = self._crawl_trending_page()
        num_repo = len(repo_pool)
        # get each repo page
        for idx, repo in enumerate(repo_pool):
            fetch_tried = 0
            while 1: # try to fetch until get enough information
                try:
                    repo_info = self.parse_repo(repo['link'])
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
        return repo_pool

if __name__=='__main__':
    crawler = TrendingCrawler()
    crawler.collect_treding_page()

