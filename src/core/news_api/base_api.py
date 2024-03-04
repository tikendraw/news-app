from datetime import datetime
from typing import List, Optional


class NewsAPI:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url
        

    def get_news(self, query: str, page: int = 1) -> Optional[ArticlesResponse]:
        response = requests.get(url)

        return parse_news(response.json()) if response.status_code == 200 else None

    def parse_news(self, news: dict) -> NewsArticle:
        raise NotImplementedError()

