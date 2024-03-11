from sqlalchemy import Column, DateTime, Integer, String
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
    category = Column(String)
    description = Column(String)
    content = Column(String)
    url = Column(String)
    image = Column(String)
    source_name = Column(String)
    source_url = Column(String)


class ScienceArticleORM(Base):
    __tablename__ = "science_articles"

    id: Mapped[int] = mapped_column(primary_key=True)
    published_at = Column(DateTime)
    title = Column(String)
    author = Column(String)
    category = Column(String)
    description = Column(String)
    content = Column(String)
    url = Column(String)
    image = Column(String)
    source_name = Column(String)
    source_url = Column(String)


class SportsArticleORM(Base):
    __tablename__ = "sports_articles"

    id: Mapped[int] = mapped_column(primary_key=True)
    published_at = Column(DateTime)
    title = Column(String)
    author = Column(String)
    category = Column(String)
    description = Column(String)
    content = Column(String)
    url = Column(String)
    image = Column(String)
    source_name = Column(String)
    source_url = Column(String)
