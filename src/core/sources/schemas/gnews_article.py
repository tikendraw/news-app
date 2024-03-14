from datetime import datetime
from typing import List, Optional, Union

from pydantic import BaseModel, Field, HttpUrl

from .news import NewsArticle


class Props(BaseModel):
    site_name: Optional[str] = None
    url: Optional[HttpUrl] = None
    title: Optional[str] = None
    description: Optional[str] = None
    image: Optional[HttpUrl] = None
    types: Optional[str] = Field(alias="type", default=None)
    locale: Optional[str] = None

    class Config:
        populate_by_name = True


class GNewsArticle(NewsArticle):
    title: str
    url: Optional[HttpUrl] = Field(alias="link", default=None)
    description: Optional[str] = None
    source_name: Optional[str] = Field(alias="source", default=None)
    published_at: Optional[datetime] = Field(alias="created_at", default=None)
    props: Props = Field(alias="props", default=None)
    language: Optional[list[str]] = None

    category: Optional[str] = None
    author: Optional[str] = None
    content: Optional[str] = None
    country: Optional[list[str]] = None
    image: Optional[HttpUrl] = None
    source_url: Optional[Union[HttpUrl, str]] = None
