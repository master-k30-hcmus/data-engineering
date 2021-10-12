from pprint import pprint

from app.config.database import MongoDB
from app.crawler.topic import TopicCrawler
from app.crawler.trending import TrendingCrawler 


if __name__ == '__main__':
    db = MongoDB(db_name='github')

    ## Crawl github topics
    topics_col = db.get_collection('topics')
    trending_col = db.get_collection('trending')

    topic_crawler = TopicCrawler()
    repos = topic_crawler.crawl()
    # TODO: add index to update duplicated repos
    print(f"Insert {len(repos)} repos")
    topics_col.insert_many(repos)

    trending_crawler = TrendingCrawler()
    repos = trending_crawler.crawl()
    trending_col.insert_many(repos)

    for item in topics_col.find():
        pprint(item)
    db.close()
