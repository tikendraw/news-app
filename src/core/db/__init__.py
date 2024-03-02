import os
import sys
from datetime import datetime
from pathlib import Path

# sys.path.append(str(Path(__file__).parent.parent.parent.absolute()))
print(sys.path)
from icecream import ic
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker

from core.news_model.news import Base, NewsArticle, NewsArticleORM

ic.enable() 

ic(os.getcwd())

# Create SQLite engine and session
engine = create_engine('sqlite:///database/articles.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
