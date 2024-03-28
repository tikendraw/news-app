from datetime import datetime
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field, HttpUrl

from ...schema.article import NewsArticle


class GNewsArticle(NewsArticle):
    title: str = Field(alias="title")
    url: Union[str, None] = Field(alias="url", default=None)
    description: Union[str, None] = Field(alias="description", default=None)
    content: Union[str, None] = Field(alias="content", default=None)
    published_at: Optional[datetime] = Field(alias="publishedAt", default=None)
    image: Union[str, None] = Field(alias="image", default=None)    
    source: Optional[Dict] = Field(default={},alias = "source",)

    source_name: Optional[str] = Field(default=None)
    source_url: Optional[Union[HttpUrl, str]] = Field(default=None)


    country: Union[list, None] = Field(alias="country", default=None)
    category: Union[list, None] = Field(alias="category", default=None)
    language: Union[str,None] = Field(alias="language", default=None)
    author: Union[list, None] = Field(alias="creator", default=None)
    meta_data: Optional[Dict[str, Union[str, List[str]]]] = Field(
        alias="metadata", default={}
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source_name = self.source.get('name', None)
        self.source_url = self.source.get('url', None)
        del self.source
        