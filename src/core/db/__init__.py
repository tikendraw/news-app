import yaml
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .news_tables import Base, NewsArticleORM

# read db config.yaml from current directory
with open("config/db_config.yaml", "r") as f:
    config = yaml.safe_load(f)
    SQLALCHEMY_DATABASE_URL = config["SQLALCHEMY_DATABASE_URL"]


# Create SQLite engine and session

engine = create_engine(SQLALCHEMY_DATABASE_URL,
                       connect_args={"check_same_thread": False} #needed only for SQLite
                       )
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)