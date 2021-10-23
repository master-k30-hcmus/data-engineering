from app.config.database import MongoDB
from app.crawler.topic import TopicCrawler
from app.crawler.trending import TrendingCrawler 


if __name__ == '__main__':
    db = MongoDB(db_name='github')

    trending_crawler = TrendingCrawler(collection=db.get_collection('trending'))
    trending_crawler.crawl()

    topic_crawler = TopicCrawler(collection=db.get_collection('topics'))
    topic_crawler.crawl()

    db.close()
