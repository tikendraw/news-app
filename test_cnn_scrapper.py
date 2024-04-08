from icecream import ic

from core.db.crud.news_crud import (NewsArticleRepository,
                                    NewsArticleSummaryRepository)
from core.db.db_utils import get_db
from core.db.news_tables import NewsArticleSummaryORM
from core.langchain_summarizer.summary_chain import get_summary
from core.scrapper.cnn_scrapper import CNNScraper

url = "https://edition.cnn.com/2024/03/19/media/elon-musk-don-lemon-interview-analysis-hnk-intl/index.html?iid=cnn_buildContentRecirc_end_recirc"
cnn_scrapper = CNNScraper(enable_cache=True)
articles = cnn_scrapper.run(category='base',n=10)
# articles = cnn_scrapper.scrape_urls(urls=[url])

news_repo = NewsArticleRepository()
summary_repo = NewsArticleSummaryRepository()


for num, article in enumerate(articles, 1):
    article_summary = get_summary(article=article.content)  # Get the ArticleSummary object
    try:
        with next(get_db()) as session:
            article_orm = news_repo.add(article, session)
            summary_orm = NewsArticleSummaryORM(
                news_article_id=article_orm.id,
                summary=article_summary.summary,
                tags=article_summary.tags,
                category=article_summary.category,
                locations=article_summary.locations,
                ai_title=article_summary.ai_title
            )
            summary_repo.add(summary_orm, session)
            summary_column = session.query(NewsArticleSummaryORM).filter_by(news_article_id=article_orm.id).first().summary

            ic(article.title)
            ic(article_orm.id)
        # ic(summary_column)
        ic(article_summary)
        ic("--"*22)
        
        print()
    except AttributeError as e:
        print("Attribute error:",e)
    except Exception as e:
        ic(e)
        
print("Done!!!")