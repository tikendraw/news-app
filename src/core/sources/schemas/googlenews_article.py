from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, Field, HttpUrl

from .news import NewsArticle


class GoogleNewsArticle(NewsArticle):
    article_id: str = Field(alias="title")
    url: Union[HttpUrl, str] = Field(alias="link")
    keywords: Union[list[str], None] = None
    author: Union[list, None] = None
    video_url: Union[HttpUrl, str, None] = None
    published_at: Optional[datetime] = Field(alias="date", default=None)
    image: Union[HttpUrl, str, None] = Field(alias="source", default=None)
    source_id: str = Field(alias="source", default=None)
    source_url: Union[HttpUrl, str] = None

    country: list = None
    category: list = None
    language: str = Field(alias="language", default="english")
    ai_tags: Union[list[str], str] = None
    sentiment: str = None
    sentiment_stats: Union[dict, str] = None
    ai_region: str = None
