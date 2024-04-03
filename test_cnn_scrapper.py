from core.db.db_utils import get_db
from core.db.news_tables import NewsArticleORM
from core.scrapper.cnn_scrapper import CNNScraper
from core.db.crud.news_crud import add_article
from core.langchain_summariezer import summary_chain

cnn_scapper = CNNScraper(enable_cache=True)
articles = cnn_scapper.run(n=3)


    
for num,article in enumerate(articles):
    article_summary = summary_chain(article.content)
    article.content_summary = article_summary.content_summary
    article.locations = article_summary.locations
    article.keywords = article_summary.tags
    article.category = article_summary.category
    
    
    add_article(article=article, db=next(get_db()), orm_class=NewsArticleORM )
    
    print(f"{num}:  {article.title}")
    print("ai_tittle: ", article_summary.title)
    print()
    
# cnn_scapper.write_db(session=next(get_db()), orm_class=NewsArticleORM)
print("Done!!!")