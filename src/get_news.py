import os

from dotenv import load_dotenv

from core.db import Session
from core.db.db_utils import *
from core.news_api import GNewsAPI

load_dotenv()

apikey = os.environ.get("GNEWS_API_KEY")
test = GNewsAPI(category="general", n_news=100, lang="en", country="us", apikey=apikey)

news = test.get_news()

print(news)
add_articles_to_db(session=Session(), articles=news)
