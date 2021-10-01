from config.database import MongoDB
from pprint import pprint

from crawler.topic import TopicCrawler

if __name__ == '__main__':
    db = MongoDB(db_name='github')

    # Crawl github topics
    topics_col = db.get_collection('topics')

    topic_crawler = TopicCrawler()
    repos = topic_crawler.crawl()
    # TODO: add index to update duplicated repos
    topics_col.insert_many(repos)

    for item in topics_col.find():
        pprint(item)

    db.close()
