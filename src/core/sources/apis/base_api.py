from datetime import datetime
from typing import List, Optional, Union

import requests
from pydantic import BaseModel, HttpUrl

from ...schema.article import NewsArticle


class NewsAPI:
    def __init__(self, api_key: Union[str, None] = None):
        self.apikey = api_key

    def parse_news(self, news: dict):
        raise NotImplementedError()

    def _make_request(self, **kwargs) -> requests.Response:
        raise NotImplementedError()
        
    def get_news(self, *args, **kwargs):
        response = self._make_request(**kwargs)            
        return self.parse_news(response.json() if response.status_code == 200 else {})
