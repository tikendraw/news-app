from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, HttpUrl


class Source(BaseModel):
    name: str = None
    url: HttpUrl = None

class NewsArticle(BaseModel):
    title: str
    description: Optional[str] = None
    content: Optional[str]= None
    url: Optional[HttpUrl]= None
    image: Optional[HttpUrl]= None
    published_at: Optional[datetime] = Field(alias="publishedAt", default=None)
    source: Optional[Source]

class ArticlesResponse(BaseModel):
    totalArticles: int
    articles: List[NewsArticle]

