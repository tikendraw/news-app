from icecream import ic

from core.db.crud.news_crud import NewsArticleRepository, NewsArticleSummaryRepository
from core.db.db_utils import get_db
from core.db.news_tables import NewsArticleORM, NewsArticleSummaryORM
from core.langchain_summarizer.summary_chain import ArticleSummary, get_summary
from core.scrapper.cnn_scrapper import CNNScraper

cnn_scapper = CNNScraper(enable_cache=True)
articles = cnn_scapper.run(category='americas',n=5)

news_repo = NewsArticleRepository()
summary_repo = NewsArticleSummaryRepository()


for num, article in enumerate(articles, 1):
    article_summary = get_summary(article=article.content)  # Get the ArticleSummary object
    try:
        with next(get_db()) as session:
            article_orm = news_repo.add(article, session)
            summary_orm = NewsArticleSummaryORM(
                news_article_id=article_orm.id,
                summary_column=article_summary.content_summary,
                tags=article_summary.tags,
                locations=article_summary.locations,
                ai_title=article_summary.ai_title
            )
            summary_repo.add(summary_orm, session)
            summary_column = session.query(NewsArticleSummaryORM).filter_by(news_article_id=article_orm.id).first().summary_column

            ic(article.title)
            ic(article_orm.id)
        ic(summary_column)
        ic("--"*22)
    except AttributeError as e:
        pass
    except Exception as e:
        ic(e)
        
print("Done!!!")