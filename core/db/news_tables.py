from typing import Any, Dict, List
from sqlalchemy.orm import Session

from sqlalchemy import JSON, Boolean, Column, ForeignKey, String
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import event


class Base(DeclarativeBase):
    pass



class NewsArticleSummaryORM(Base):
    __tablename__ = "news_article_summaries"

    id: Mapped[int] = mapped_column(primary_key=True)
    news_article_id: Mapped[int] = mapped_column(ForeignKey("news_articles.id"))
    ai_title: Mapped[str] = Column(String, nullable=True)
    summary: Mapped[str] = Column(String)
    tags: Mapped[List[str]] = mapped_column(JSON, nullable=True)
    locations: Mapped[List[str]] = mapped_column(JSON, nullable=True)
    category: Mapped[List[str]] = mapped_column(JSON, nullable=True)

    news_article = relationship("NewsArticleORM", back_populates="summary")

@event.listens_for(NewsArticleSummaryORM, 'after_insert')
def set_is_summarized(mapper, connection, target):
    with Session(connection) as session:
        article = session.query(NewsArticleORM).get(target.news_article_id)
        article.is_summarized = True
        session.commit()

class NewsArticleORM(Base):
    __tablename__ = "news_articles"

    id: Mapped[int] = mapped_column(primary_key=True)
    published_at = Column(String)
    title = Column(String)
    author = Column(String)
    category: Mapped[List[str]] = mapped_column(JSON, nullable=True)
    description = Column(String)
    content = Column(String)
    url = Column(String)
    images: Mapped[List[str]] = mapped_column(JSON, nullable=True)
    source_name = Column(String)
    meta_data: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=True)
    locations: Mapped[List[str]] = mapped_column(JSON, nullable=True)
    keywords: Mapped[List[str]] = mapped_column(JSON, nullable=True)

    summary = relationship("NewsArticleSummaryORM", back_populates="news_article")
    is_summarized: Mapped[bool] = Column(Boolean, default=False)
        