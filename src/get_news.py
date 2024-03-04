# https://docs.python.org/3/library/json.html
# This library will be used to parse the JSON data returned by the API.
import json
import os
import sys

# https://docs.python.org/3/library/urllib.request.html#module-urllib.request
# This library will be used to fetch the API.
import urllib.request
from datetime import datetime

import requests

from core.db import Session
from core.db.db_utils import *

# Example usage
from core.news_api import TestNews

# requests_cache.install_cache('demo_cache')
# requests.get('https://httpbin.org/delay/1')


# url = f"https://gnews.io/api/v4/top-headlines?category={category}&lang=en&country=us&max=10&apikey={apikey}"


# output = None

#     for i in range(len(articles)):
#         # articles[i].title
#         print(f"Title: {articles[i]['title']}")
#         # articles[i].description
#         print(f"Description: {articles[i]['description']}")
#         # You can replace {property} below with any of the article properties returned by the API.
#         # articles[i].{property}
#         # print(f"{articles[i]['{property}']}")

#         # Delete this line to display all the articles returned by the request. Currently only the first article is displayed.
#         break

apikey = "70aa5daa071d66bf09522bece9ee15a5"
test = TestNews(category="general", n_news=10, lang="en", country="us", apikey=apikey)

news = test.get_news()

for i in range(len(news)):
    print()
    print(f"Title: {news[i].title}")
    print(f"Description: {news[i].description}")
