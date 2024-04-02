from core.db.db_utils import get_db
from core.db.news_tables import NewsArticleORM
from core.scrapper.cnn_scrapper import CNNScraper

cnn_scapper = CNNScraper(enable_cache=True)
articles = cnn_scapper.run()

for num,article in enumerate(articles):
    print(num, ' : ', article.title)
    print("author:  ", article.author)
    print("pub   : ", article.published_at)
    print("url   : ", article.url)
    print("\n")

cnn_scapper.write_db(session=next(get_db()), orm_class=NewsArticleORM)
print("Done!!!")