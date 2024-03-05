from datetime import datetime
from typing import List, Optional, Union

from pydantic import BaseModel, Field, HttpUrl


class NewsArticle(BaseModel):
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    author: Optional[str] = None
    content: Optional[str] = None
    country: Optional[list[str]] = None
    language: Optional[list[str]] = None
    url: Optional[HttpUrl] = None
    image: Optional[HttpUrl] = None
    published_at: Optional[datetime] = Field(alias="publishedAt", default=None)
    source_name: Optional[str] = None
    source_url: Optional[Union[HttpUrl, str]] = None


class ArticlesResponse(BaseModel):
    totalArticles: int
    articles: List[NewsArticle]
