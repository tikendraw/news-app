from core.db.db_utils import get_db
from core.db.news_tables import NewsArticleORM
from core.scrapper.cnn_scrapper import CNNScraper

cnn_scapper = CNNScraper()
articles = cnn_scapper.run()

for num,article in enumerate(articles):
    print(num, ': ', article.title)
    
cnn_scapper.write_db(session=next(get_db()), orm_class=NewsArticleORM)
print("Done!!!")