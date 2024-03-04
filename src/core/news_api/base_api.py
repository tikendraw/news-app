from datetime import datetime
from typing import List, Optional

import requests
from pydantic import BaseModel

from ..news_model import NewsArticle


class NewsAPI:

    def __init__(self):
        self.base_url = None

    def get_news(self, *args, **kwargs) -> Optional[NewsArticle]:
        response = requests.get(self.base_url, *args, **kwargs)

        return parse_news(response.json()) if response.status_code == 200 else None

    def parse_news(self, news: dict) -> NewsArticle:
        raise NotImplementedError()
