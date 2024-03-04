from datetime import datetime
from typing import List, Optional

import requests

from ..news_model import ArticlesResponse, NewsArticle


class NewsAPI:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url
        

    def get_news(self, query: str, page: int = 1, *args, **kwargs) -> Optional[ArticlesResponse]:
        response = requests.get(url, *args, **kwargs)

        return parse_news(response.json()) if response.status_code == 200 else None

    def parse_news(self, news: dict) -> NewsArticle:
        raise NotImplementedError()

