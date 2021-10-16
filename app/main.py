from pprint import pprint

from app.config.database import MongoDB
from app.crawler.topic import TopicCrawler
from app.crawler.trending import TrendingCrawler 


if __name__ == '__main__':
    db = MongoDB(db_name='github')

    topics_col = db.get_collection('topics')
    topic_crawler = TopicCrawler()
    repos = topic_crawler.crawl()
    # TODO: add index to update duplicated repos
    topics_col.insert_many(repos)

    trending_col = db.get_collection('trending')
    trending_crawler = TrendingCrawler()
    repos = trending_crawler.crawl()
    trending_col.insert_many(repos)

    db.close()
