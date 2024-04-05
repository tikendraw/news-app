from core.db.db_utils import get_db
from core.db.news_tables import NewsArticleORM
from core.scrapper.cnn_scrapper import CNNScraper
from core.db.crud.news_crud import add_article
from core.langchain_summarizer.summary_chain import get_summary, ArticleSummary

cnn_scapper = CNNScraper(enable_cache=True)
articles = cnn_scapper.run(n=3)



for num,article in enumerate(articles,1):
    
    
    article_summary = get_summary(article=article.content)
    
    if isinstance(article_summary, ArticleSummary):        
        article.content_summary = article_summary.content_summary
        article.locations = article_summary.locations
        article.keywords = article_summary.tags
        article.category = article_summary.category
        article.meta_data['ai_title'] = article_summary.title
        
    add_article(article=article, db=next(get_db()), orm_class=NewsArticleORM )
    
    print()
    print(f"{num}  :  {article.title}")
    print("ai_title: ", article.meta_data.get("ai_title", None))
    print("content length", len(article.content.split()))
    print("summary length", len(article.content_summary.split()))
    print("Compressed to: ", (len(article.content_summary.split())/len(article.content.split())) * 100 , "%")
    
# cnn_scapper.write_db(session=next(get_db()), orm_class=NewsArticleORM)
print("Done!!!")