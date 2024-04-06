from core.db.db_utils import get_db
from core.db.crud.news_crud import NewsArticleRepository

db = next(get_db())
news_repo = NewsArticleRepository()


articles = news_repo.get_all(db)
for article in articles:
    print("title: ",article.title)
    print("content: ",article.content[:1000] + '...')
    print("published at: ",article.published_at)
    print()