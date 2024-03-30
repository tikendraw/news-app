from datetime import datetime
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field, HttpUrl

from ...schema.article import NewsArticle


# Shared properties
class NewsDataArticle(NewsArticle):
    article_id: str = Field(alias="article_id")
    title: str = Field(alias="title")
    url: Union[HttpUrl, str] = Field(alias="link")
    keywords: Union[list[str], None] = Field(alias="keywords", default=None)
    author: Union[list, None] = Field(alias="creator", default=None)
    video_url: Union[HttpUrl, str, None] = Field(alias="video_url", default=None)
    description: Union[str, None] = Field(alias="description", default=None)
    content: Union[str, None] = Field(alias="content", default=None)
    published_at: Optional[datetime] = Field(alias="pubDate", default=None)
    image: Union[HttpUrl, str, None] = Field(alias="image_url", default=None)
    source_name: str = Field(alias="source_id")
    source_url: Union[HttpUrl, str] = Field(alias="source_url")
    source_icon: Union[HttpUrl, str, None] = Field(alias="source_icon", default=None)

    country: list = Field(alias="country", default=None)
    category: list = Field(alias="category", default=None)
    language: str = Field(alias="language", default="english")
    ai_tag: Union[list[str], str] = Field(alias="ai_tag", default=None)
    sentiment: str = Field(alias="sentiment", default=None)
    sentiment_stats: Union[dict, str] = Field(alias="sentiment_stats", default=None)
    ai_region: str = Field(alias="ai_region", default=None)
    meta_data: Optional[Dict[str, Union[str, List[str]]]] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.meta_data = {
            "article_id": kwargs.get("article_id"),
            "keywords": kwargs.get("keywords"),
            "video_url": kwargs.get("video_url"),
            "source_icon": kwargs.get("source_icon"),
            "source_priority": kwargs.get("source_priority"),
            "ai_tag": kwargs.get("ai_tag"),
            "sentiment": kwargs.get("sentiment"),
            "sentiment_stats": kwargs.get("sentiment_stats"),
            "ai_region": kwargs.get("ai_region"),
            
        }