from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, HttpUrl
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import Mapped, declarative_base, mapped_column


class Source(BaseModel):
    name: str
    url: HttpUrl

class NewsArticle(BaseModel):
    title: str
    description: Optional[str]
    content: Optional[str]
    url: Optional[HttpUrl]
    image: Optional[HttpUrl]
    published_at: Optional[datetime] = Field(alias="publishedAt")
    source: Optional[Source]

class ArticlesResponse(BaseModel):
    totalArticles: int
    articles: List[NewsArticle]


# Define SQLAlchemy ORM model
Base = declarative_base()

class NewsArticleORM(Base):
    __tablename__ = 'news_articles'

    # id = Column(Integer, primary_key=True)
    id: Mapped[int] = mapped_column(primary_key=True)

    title = Column(String)
    description = Column(String)
    content = Column(String)
    url = Column(String)
    image = Column(String)
    published_at = Column(DateTime)
    source_name = Column(String)
    source_url = Column(String)
