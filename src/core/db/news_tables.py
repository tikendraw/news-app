from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# Define SQLAlchemy ORM model
class Base(DeclarativeBase):
    pass


class NewsArticleORM(Base):
    __tablename__ = "news_articles"
    id: Mapped[int] = mapped_column(primary_key=True)
    published_at = Column(DateTime)
    title = Column(String)
    author = Column(String)
    category: Mapped[List[str]] = mapped_column(JSON, nullable=True)
    description = Column(String)
    content = Column(String)
    url = Column(String)
    image = Column(String)
    source_name = Column(String)
    source_url = Column(String)
    meta_data = Column(String)
    country: Mapped[List[str]] = mapped_column(JSON, nullable=True)
    keywords: Mapped[List[str]] = mapped_column(JSON, nullable=True)  # Store keywords as JSON

