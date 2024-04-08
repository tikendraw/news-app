from datetime import datetime
from typing import List, Optional, Union
import os
import requests
from icecream import ic
from pydantic import BaseModel, Field, HttpUrl

from ..schema import GoogleNewsArticle
from .base_api import NewsAPI

LANGUAGES = ["TR", "EN", "FR", "DE", "IT", "ZH", "ES", "RU", "KO", "PT"]


class GoogleNewsAPI(NewsAPI):
    """
    https://rapidapi.com/ctr-ou-ctr-ou-default/api/google-news-api1

    10 requests/day
    1000 requests per hour

    """

    def __init__(
        self,
        apikey: str,
    ):
        self.host = "google-news-api1.p.rapidapi.com"
        self.base_url = f"https://{self.host}/search"

        if not apikey:
            try:
                apikey = os.environ["X-RapidAPI-Key"]
            except KeyError:
                raise ValueError(
                    "X-RapidAPI-Key is required, get from https://rapidapi.com/ , Set environment variable X-RapidAPI-Key or just pass it."
                )

        self.headers = {
            "X-RapidAPI-Key": apikey,
            "X-RapidAPI-Host": self.host,
        }

    def _make_request(self, q: str = None, language: str = "EN") -> requests.Response:
        if language not in LANGUAGES:
            raise ValueError(f"language must be one of {LANGUAGES}")

        querystring = {
            "language": language,
            "q": q,
        }
        querystring = {i: j for i, j in querystring.items() if j is not None}

        response = requests.get(self.base_url, headers=self.headers, params=querystring)

        return response

    def get_news(self, q: str, language: str = "EN") -> Optional[List[GoogleNewsArticle]]:
        response = self._make_request(q, language)
        if response.status_code != 200:
            print(response.status_code, response.text)
            return None
        return self.parse_news(response.json())

    def parse_news(self, news: dict) -> list[GoogleNewsArticle]:
        news_data = news['news']['news']