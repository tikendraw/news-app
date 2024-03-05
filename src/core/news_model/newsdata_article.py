from datetime import datetime
from typing import List, Optional, Union

from pydantic import BaseModel, Field, HttpUrl

from .news import NewsArticle


# Shared properties
class NewsDataArticle(NewsArticle):
    article_id: str = Field(alias="article_id")
    url: Union[HttpUrl, str] = Field(alias="link")
    keywords: Union[list[str], None] = Field(alias="keywords", default=None)
    author: Union[list, None] = Field(alias="creator", default=None)
    video_url: Union[HttpUrl, str, None] = Field(alias="video_url", default=None)
    published_at: Optional[datetime] = Field(alias="pubDate", default=None)
    image: Union[HttpUrl, str, None] = Field(alias="image_url", default=None)
    source_id: str = Field(alias="source_id")
    source_url: Union[HttpUrl, str] = Field(alias="source_url")

    country: list = Field(alias="country", default=None)
    category: list = Field(alias="category", default=None)
    language: str = Field(alias="language", default="english")
    ai_tags: Union[list[str], str] = Field(alias="ai_tags", default=None)
    sentiment: str = Field(alias="sentiment", default=None)
    sentiment_stats: Union[dict, str] = Field(alias="sentiment_stats", default=None)
    ai_region: str = Field(alias="ai_region", default=None)
