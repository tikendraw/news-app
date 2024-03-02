import os
import sys
from datetime import datetime

print(sys.path)
from icecream import ic
from pydantic import BaseModel, Field, HttpUrl
from sqlalchemy import Column, DateTime, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker

from ..core.news_model.news import Base, NewsArticle, NewsArticleORM

ic.enable() 

ic(os.getcwd())

# Create SQLite engine and session
engine = create_engine('sqlite:///database/articles.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Function to parse JSON articles and insert into database if valid
def process_articles(json_data):
    articles = json_data.get('articles', [])
    for article_data in articles:
        # ic(article_data)
        # ic(type(article_data))
        article = NewsArticle(**article_data)
        ic(article)
        try:
            article_orm = NewsArticleORM(
                title=article.title,
                description=article.description,
                content=article.content,
                url=str(article.url),
                image=str(article.image),
                published_at=article.published_at,
                source_name=article.source.name,
                source_url=str(article.source.url)
            )
            session.add(article_orm)
            session.commit()
            print(f"Article '{article.title}' added to database.")
        except Exception as e:
            print(f"Failed to add article '{article.title}' to database:", e)
            print(e)
            session.rollback()


# test to check adding instance to db
# Example usage
json_data = {
    "total Articles": 54904,
    "articles": [
        {
            "title": "Pixel 8 and 7 Pro’s design gets revealed even more with fresh crisp renders",
            "description": "Now we have a complete image of what the next Google flagship phones will look like. All that's left now is to welcome them during their October announcement!",
            "content": "Google’s highly anticipated upcoming Pixel 7 series is just around the corner, scheduled to be announced on October 6, 2022, at 10 am EDT during the Made by Google event. Well, not that there is any lack of images showing the two new Google phones, b... [1419 chars]",
            "url": "https://www.phonearena.com/news/google-pixel-7-and-pro-design-revealed-even-more-fresh-renders_id142800",
            "image": "https://m-cdn.phonearena.com/images/article/142800-wide-two_1200/Googles-Pixel-7-and-7-Pros-design-gets-revealed-even-more-with-fresh-crisp-renders.jpg",
            "publishedAt": "2022-09-28T08:14:24Z",
            "source": {
                "name": "PhoneArena",
                "url": "https://www.phonearena.com"
            }
        }
    ]
}

process_articles(json_data)
