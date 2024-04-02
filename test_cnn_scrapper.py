from core.db.db_utils import get_db
from core.db.news_tables import NewsArticleORM
from core.scrapper.cnn_scrapper import CNNScraper
from core.db.crud.news_crud import add_article

cnn_scapper = CNNScraper(enable_cache=True)
articles = cnn_scapper.run(n=10)

def you_summarier_function(content:str) -> str:
    ...
    
for num,article in enumerate(articles):
    article.content_summary = your_summarier_function(article.content)
    add_article(article=article, db=next(get_db()), orm_class=NewsArticleORM )
    
# cnn_scapper.write_db(session=next(get_db()), orm_class=NewsArticleORM)
print("Done!!!")