import json
import urllib.parse
import urllib.request
from typing import Optional

from icecream import ic
from pydantic import BaseModel, Field, root_validator, validator

from ..news_model import GNewsArticle
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


class GNewsAPIError(Exception):
    pass


class GNewsAPI(NewsAPI):
    ERROR_MESSAGES = {
        400: "Bad Request -- Your request is invalid.",
        401: "Unauthorized -- Your API key is wrong.",
        403: "Forbidden -- You have reached your daily quota, the next reset is at 00:00 UTC.",
        429: "Too Many Requests -- You have made more requests per second than you are allowed.",
        500: "Internal Server Error -- We had a problem with our server. Try again later.",
        503: "Service Unavailable -- We're temporarily offline for maintenance. Please try again later.",
    }

    def __init__(
        self,
        apikey: str,
        category: str = "general",
        n_news: int = 100,
        lang: str = "en",
        country: str = "us",
    ):
        self.apikey = apikey
        self.category = category
        self.n_news = n_news
        self.lang = lang
        self.country = country

        if not self.apikey:
            try:
                apikey = os.environ.get("GNEWS_API_KEY")
            except KeyError as e:
                raise ValueError(
                    "API key is required. Get if from https://gnews.io/ . pass as argument or set GNEWS_API_KEY environment variable"
                ) from e

        if self.lang not in LANGUAGES:
            raise ValueError(f"language must me one of {LANGUAGES}")

        if self.country not in COUNTRIES:
            raise ValueError(f"country must me one of {COUNTRIES}")

        self.base_url = f"https://gnews.io/api/v4/top-headlines?category={self.category}&lang={self.lang}&country={self.country}&max={self.n_news}&apikey={self.apikey}"

    def parse_news(self, data: dict) -> Optional[list[GNewsArticle]]:
        articles = data.get("articles", [])
        if len(articles) > 0:
            return [GNewsArticle(**article_data) for article_data in articles]
        else:
            return None

    def get_news(self) -> Optional[list[GNewsArticle]]:
        try:
            with urllib.request.urlopen(self.base_url) as response:
                if response.status in self.ERROR_MESSAGES:
                    raise GNewsAPIError(self.ERROR_MESSAGES[response.status])
                data = json.loads(response.read().decode("utf-8"))
                return self.parse_news(data)
        except urllib.error.URLError as e:
            raise GNewsAPIError(f"Failed to connect to the server: {e.reason}") from e
        except json.JSONDecodeError as e:
            raise GNewsAPIError(
                "Failed to parse response data. JSON decoding error."
            ) from e


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


#     def parse_news(self, data: dict) -> Optional[list[GNewsArticle]]:
#         if articles := data.get('articles', []):
#             return [GNewsArticle(**article_data) for article_data in articles]
#         else:
#             return None

#     def get_news(self) -> Optional[list[GNewsArticle]]:
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
