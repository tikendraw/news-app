from typing import Iterable, List, Type

# Function to parse JSON articles and insert into database if valid
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ...schema.article import Article
from .. import SessionLocal
from ..db_exceptions import (AddArticleError, DatabaseError,
                             DeleteArticleError, UpdateArticleError)
from ..news_tables import Base


# Funtions to do operation with db
def add_article(article: Article, db: Session, orm_class: Type):
    """
    Adds an article to the database. Rolls back the transaction if the article already exists.


    Parameters
    ----------
    article: The article to add.
    db: The database session.
    orm_class: The ORM class to use for the article.


    """
    article_orm = orm_class(
        published_at=article.published_at,
        title=article.title,
        author=article.author,
        category=article.category,
        description=article.description,
        content=article.content,
        url=article.url,
        content_summary=article.content_summary,
        images=article.images,
        source_name=article.source_name,
        locations=article.locations
    )

    db.add(article_orm)

    try:
        db.commit()
    # except IntegrityError:
        # db.rollback()
    except Exception as e:
        # raise AddArticleError(f"Error adding article: {e}")
        raise e

def update_article(article_id:int, article: Article, db: Session, orm_class: Type):
    article_orm = db.query(orm_class).filter_by(id=article_id).first()

    if article_orm is None:
        raise UpdateArticleError(f"Article with URL {article.url} does not exist.")
    else:
        article_orm.published_at = article.published_at
        article_orm.title = article.title
        article_orm.author = article.author
        article_orm.category = article.category
        article_orm.description = article.description
        article_orm.content = article.content
        article_orm.url = article.url
        article_orm.images = article.images
        article_orm.source_name = article.source_name
        article_orm.locations = article.locations
        db.commit()


def get_articles(db: Session, orm_class: Type):
    return db.query(orm_class).all()


def get_n_articles(db: Session, orm_class: Type, n: int):
    
    if n > 0:
        return db.query(orm_class).limit(n).all()
    elif n == -1:
        return db.query(orm_class).all()
    else:
        return None

def delete_article(article_id:int, db: Session, orm_class: Type):
    try: 
        article_orm = db.query(orm_class).filter_by(id=article_id).first()
        db.delete(article_orm)
        db.commit()
    except Exception as e:
        raise DeleteArticleError(f"Error deleting article: {e}")