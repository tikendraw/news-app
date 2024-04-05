from typing import Any, Dict, List

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass



class NewsArticleSummaryORM(Base):
    __tablename__ = "news_article_summaries"

    id: Mapped[int] = mapped_column(primary_key=True)
    news_article_id: Mapped[int] = mapped_column(ForeignKey("news_articles.id"))
    summary_column: Mapped[str] = Column(String)
    tags: Mapped[List[str]] = mapped_column(JSON, nullable=True)
    locations: Mapped[List[str]] = mapped_column(JSON, nullable=True)
    ai_title: Mapped[str] = Column(String, nullable=True)

    news_article = relationship("NewsArticleORM", back_populates="summary")
    

class NewsArticleORM(Base):
    __tablename__ = "news_articles"

    id: Mapped[int] = mapped_column(primary_key=True)
    published_at = Column(String)
    title = Column(String)
    author = Column(String)
    category: Mapped[List[str]] = mapped_column(JSON, nullable=True)
    description = Column(String)
    content = Column(String)
    content_summary = Column(String)
    url = Column(String)
    images: Mapped[List[str]] = mapped_column(JSON, nullable=True)
    source_name = Column(String)
    meta_data: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=True)
    locations: Mapped[List[str]] = mapped_column(JSON, nullable=True)
    keywords: Mapped[List[str]] = mapped_column(JSON, nullable=True)

    summary = relationship("NewsArticleSummaryORM", back_populates="news_article")
    
