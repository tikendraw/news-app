from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import Mapped, declarative_base, mapped_column

# Define SQLAlchemy ORM model
Base = declarative_base()


class NewsArticleORM(Base):
    __tablename__ = "news_articles"

    # id = Column(Integer, primary_key=True)
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
