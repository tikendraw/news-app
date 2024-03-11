from icecream import ic

from core.db import Session
from core.db.news_tables import NewsArticleORM, ScienceArticleORM
from core.news_schema import NewsArticle

news = NewsArticle(
    title="science",
    content="test science",
)

from core.db.db_utils import *

db = next(get_db())

# a = add_article_to_db(news, db, ScienceArticleORM)
# print(a)

a = delete_article_from_db(news, db, ScienceArticleORM)
