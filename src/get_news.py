import json
import os
from datetime import datetime

from dotenv import load_dotenv
from icecream import ic

from core.db import SessionLocal
from core.db.crud.news_crud import add_article
from core.db.db_utils import get_db
from core.db.news_tables import NewsArticleORM
from core.sources.apis import GNewsAPI, GoogleNewsAPI, NewsDataAPI
from core.utils import rate_limiter

load_dotenv()

gnews_apikey = os.environ.get("GNEWS_API_KEY")
gnews = GNewsAPI(apikey=gnews_apikey)

news = gnews._make_request(
    # q = "sunny leone",
    category="general", 
    max=10, 
    lang="en", 
    country="in"
)
# ic("dict",news)

news = gnews.parse_news(news)
ic(news[0])
db = next(get_db())

for article in news:
    # ic(article.model_dump_json())
    # break
    add_article(article, db, NewsArticleORM)
    print("Added article title: ",article.title)
    # break
# print(news)
# ic(type(news))
# ic(news)

# # dump gnews json data in do json file
# with open("gnews.json", "w") as f:
#     json.dump(news, f)


# newsdata api test
# rate limit 100/day
# newsdata_apikey = os.environ.get("NEWSDATA_API_KEY")
# newsdata = NewsDataAPI(apikey=newsdata_apikey)
# response = newsdata.get_news(country='ru')
# ic(response)


# Google news test
# rate limit 10/month
# google_news_apikey = os.environ.get("X-RapidAPI-Key")
# gnapi = GoogleNewsAPI(apikey=google_news_apikey)

# news = gnapi._make_request()
# ic(type(news))
# # ic(news.status_code)
# ic(news)
# # ic(dir(news))

# # dump the news json
# with open("google_news.json", "w") as f:
#     json.dump(news, f)


# @rate_limiter_with_wait(requests_per_second=2, requests_per_minute=3, wait=True)
# def req():
#     print(datetime.now(),':: hi')

# limits = {1: 2, 60: 3}  # 2 req/sec  # 3 req/min


# @rate_limiter_with_wait(requests_per_second=4, requests_per_minute=3, wait=True)
# def req():
#     print(datetime.now(), ":: hi")


# if __name__ == "__main__":
#     for i in range(7):
#         req()
