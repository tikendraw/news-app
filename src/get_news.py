import os
from datetime import datetime

from dotenv import load_dotenv
from icecream import ic

from core.db import Session
from core.db.db_utils import *
from core.sources.apis import GNewsAPI, GoogleNewsAPI, NewsDataAPI
from core.utils import rate_limiter

load_dotenv()

# gnews_apikey = os.environ.get("GNEWS_API_KEY")
# gnews = GNewsAPI(category="general", n_news=100, lang="en", country="us", apikey=gnews_apikey)

# news = gnews.get_news()

# # print(news)
# add_articles_to_db(session=Session(), articles=news)

# newsdata_apikey = os.environ.get("NEWSDATA_API_KEY")
# newsdata = NewsDataAPI(apikey=newsdata_apikey)

# response = newsdata.get_news(country="jp")
# print(response)

# response = newsdata.get_news(country='jp')
# print(response)
# response = newsdata._make_request(country='cn')
# response = response['results'][0]
# for i, j in response.items():
#     # print(i,'===', type(j))

# for i in response:
#     print(i['title'])
#     print(i['link'])
#     print()


# Google news test
# google_news_apikey = os.environ.get("X-RapidAPI-Key")
# gnapi = GoogleNewsAPI(apikey=google_news_apikey)

# news = gnapi._make_request()
# ic(type(news))
# ic(news)
# ic(dir(news))


# @rate_limiter_with_wait(requests_per_second=2, requests_per_minute=3, wait=True)
# def req():
#     print(datetime.now(),':: hi')

limits = {1: 2, 60: 3}  # 2 req/sec  # 3 req/min


@rate_limiter_with_wait(requests_per_second=4, requests_per_minute=3, wait=True)
def req():
    print(datetime.now(), ":: hi")


if __name__ == "__main__":
    for i in range(7):
        req()
