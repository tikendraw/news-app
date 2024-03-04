import os
import sys
from datetime import datetime
from pathlib import Path

from icecream import ic
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker

from .news_table import Base, NewsArticleORM

# Create SQLite engine and session
engine = create_engine("sqlite:///database/articles.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
