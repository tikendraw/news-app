import json
import urllib.parse
import urllib.request
from typing import Optional

from icecream import ic
from pydantic import BaseModel, Field, root_validator, validator

from ..news_model import NewsArticle
from .base_api import NewsAPI

LANGUAGES = [
    "ar",
    "zh",
    "nl",
    "en",
    "fr",
    "de",
    "el",
    "he",
    "hi",
    "it",
    "ja",
    "ml",
    "mr",
    "no",
    "pt",
    "ro",
    "ru",
    "es",
    "sv",
    "ta",
    "te",
    "uk",
]
COUNTRIES = [
    "au",
    "br",
    "ca",
    "cn",
    "eg",
    "fr",
    "de",
    "gr",
    "hk",
    "in",
    "ie",
    "il",
    "it",
    "jp",
    "nl",
    "no",
    "pk",
    "pe",
    "ph",
    "pt",
    "ro",
    "ru",
    "sg",
    "es",
    "se",
    "ch",
    "tw",
    "ua",
    "gb",
    "us",
]
# class TestNews(NewsAPI):


class GNewsAPI(NewsAPI):

    def __init__(
        self,
        apikey: str,
        category: str = "general",
        n_news: int = 10,
        lang: str = "en",
        country: str = "us",
    ):

        self.apikey = apikey
        self.category = category
        self.n_news = n_news
        self.lang = lang
        self.country = country

        if not self.apikey:
            raise ValueError("API key is required")

        if self.lang not in LANGUAGES:
            raise ValueError(f"language must me one of {LANGUAGES}")

        if self.country not in COUNTRIES:
            raise ValueError(f"country must me one of {COUNTRIES}")

        self.base_url = f"https://gnews.io/api/v4/top-headlines?category={self.category}&lang={self.lang}&country={self.country}&max={self.n_news}&apikey={self.apikey}"

    def parse_news(self, data: dict) -> Optional[list[NewsArticle]]:
        if articles := data.get("articles", []):
            return [NewsArticle(**article_data) for article_data in articles]
        else:
            return None

    def get_news(self) -> Optional[list[NewsArticle]]:
        with urllib.request.urlopen(self.base_url) as response:
            data = json.loads(response.read().decode("utf-8"))
            ic(type(data))
            return self.parse_news(data)


# class TestNews(BaseModel):
#     apikey: str
#     category: str = None
#     query: str = None
#     n_news: int = None
#     lang: str = None
#     country: str = None
#     base_url: str = None

#     class Config:
#         allow_mutation_of_frozen_self = True

#     @validator('apikey')
#     def build_url(cls, value):
#         if not value:
#             raise ValueError("API key is required")
#         cls.base_url = cls._build_url(cls)
#         return value

#     def _build_url(self) -> str:
#         base_endpoint = "https://gnews.io/api/v4/"
#         if self.query:
#             # If query is provided, use search endpoint
#             params = {
#                 'q': self.query,
#                 'lang': self.lang,
#                 'country': self.country,
#                 'max': self.n_news,
#                 'apikey': self.apikey
#             }
#             params = {key: value for key, value in params.items() if value is not None}

#             encoded_params = urllib.parse.urlencode(params)
#             return f"{base_endpoint}search?{encoded_params}"
#         else:
#             # Use top-headlines endpoint
#             params = {
#                 'category': self.category,
#                 'lang': self.lang,
#                 'country': self.country,
#                 'max': self.n_news,
#                 'apikey': self.apikey
#             }
#             params = {key: value for key, value in params.items() if value is not None}

#             encoded_params = urllib.parse.urlencode(params)
#             return f"{base_endpoint}top-headlines?{encoded_params}"


#     def parse_news(self, data: dict) -> Optional[list[NewsArticle]]:
#         if articles := data.get('articles', []):
#             return [NewsArticle(**article_data) for article_data in articles]
#         else:
#             return None

#     def get_news(self) -> Optional[list[NewsArticle]]:
#         url = self.base_url
#         ic(url)
#         with urllib.request.urlopen(url) as response:
#             data = json.loads(response.read().decode("utf-8"))
#             return self.parse_news(data)


#     @validator('lang')
#     def validate_lang(cls, value):
#         # Language code validation
#         if value.lower() not in LANGUAGES:
#             raise ValueError(f"Invalid language code: {value}")
#         return value

#     @validator('country')
#     def validate_country(cls, value):
#         # Country code validation
#         if value.lower() not in COUNTRIES:
#             raise ValueError(f"Invalid country code: {value}")
#         return value

#     @validator('query')
#     def validate_query(cls, value):
#         if value and len(value) < 3:
#             raise ValueError("Query must be at least 3 characters long")
#         return value
