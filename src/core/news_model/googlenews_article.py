from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, Field, HttpUrl
from .news import NewsArticle


class GoogleNewsArticle(NewsArticle):
    article_id: str = Field(alias="title")
    url: Union[HttpUrl, str] = Field(alias="link")
    keywords: Union[list[str], None] = None  # Not provided in the schema
    author: Union[list, None] = None  # Not provided in the schema
    video_url: Union[HttpUrl, str, None] = None  # Not provided in the schema
    published_at: Optional[datetime] = Field(alias="date", default=None)
    image: Union[HttpUrl, str, None] = Field(alias="source", default=None)
    source_id: str = Field(alias="source", default=None)
    source_url: Union[HttpUrl, str] = None  # Not provided in the schema

    country: list = None  # Not provided in the schema
    category: list = None  # Not provided in the schema
    language: str = Field(alias="language", default="english")
    ai_tags: Union[list[str], str] = None  # Not provided in the schema
    sentiment: str = None  # Not provided in the schema
    sentiment_stats: Union[dict, str] = None  # Not provided in the schema
    ai_region: str = None  # Not provided in the schema
