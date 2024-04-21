from icecream import ic

from core.db.crud.news_crud import NewsArticleRepository, NewsArticleSummaryRepository
from core.db.db_utils import get_db
from core.db.news_tables import NewsArticleSummaryORM
from core.langchain_summarizer.summary_chain import get_summary
from core.scrapper.cnn_scrapper import CNNScraper
from core.schema.article import Article
from core.schema.article_summary import ArticleSummary
from sqlalchemy.orm import Session


def add_article_and_summary_to_db(article:Article, article_summary:ArticleSummary, session:Session):
    news_repo = NewsArticleRepository()
    summary_repo = NewsArticleSummaryRepository()
    
    # add article to database and get the id
    article_orm = news_repo.add(article, session)
    # create summary orm instance 
    summary_orm = NewsArticleSummaryORM(
        news_article_id=article_orm.id,
        summary=article_summary.summary,
        tags=article_summary.tags,
        category=article_summary.category,
        locations=article_summary.locations,
        ai_title=article_summary.ai_title
    )
    # add summary instance to database
    summary_orm = summary_repo.add(summary_orm, session)
    
    return article_orm, summary_orm

    
    
def main():
    with next(get_db()) as session:

        for num, article in enumerate(articles, 1):
            article_summary = get_summary(article=article.content)  # Get the ArticleSummary object
            
            try:
                # add article to database and get the id
                article_orm, summary_orm = add_article_and_summary_to_db(article=article, article_summary=article_summary, session=session)

                ic(article.title)
                ic(article_orm.id)
                print("--"*20)
                print()

            except AttributeError as e:
                print("Attribute error:",e)
            except Exception as e:
                ic(e)
            
    

if __name__=='__main__':

    cnn_scrapper = CNNScraper(enable_cache=True)
    articles = cnn_scrapper.run(category='base',n=10, cache=True)

    main()
    
    