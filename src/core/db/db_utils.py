from typing import Iterable, List, Type

# Function to parse JSON articles and insert into database if valid
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..news_schema import NewsArticle
from . import Session
from .news_tables import Base, NewsArticleORM, ScienceArticleORM, SportsArticleORM


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


# Function to add articles to database


class AddArticleError(Exception):
    """Raised when adding an article to the database fails."""

    pass


class UpdateArticleError(Exception):
    """Raised when updating an article in the database fails."""

    pass


class DatabaseError(Exception):
    """Raised for database-related errors."""

    pass


def add_article_to_db(article: NewsArticle, session: Session, orm_class: Type):
    """
    Adds an article to the database. Rolls back the transaction if the article already exists.


    Parameters
    ----------
    article: The article to add.
    session: The database session.
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
        image=article.image,
        source_name=article.source_name,
        source_url=article.source_url,
    )

    session.add(article_orm)

    try:
        session.commit()
    except IntegrityError:
        session.rollback()


def update_article_in_db(article: NewsArticle, session: Session, orm_class: Type):
    """
    Updates an article in the database. Rolls back the transaction if the article does not exist.


    Parameters
    ----------
    article: The article to update.
    session: The database session.
    orm_class: The ORM class to use for the article.


    """
    article_orm = session.query(orm_class).filter_by(url=article.url).first()

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
        article_orm.image = article.image
        article_orm.source_name = article.source_name
        article_orm.source_url = article.source_url

        session.commit()


def get_articles_from_db(session: Session, orm_class: Type):
    """
    Gives all articles from database.

    Parameters:
    ------------
    session: The database session.
    orm_class: The ORM class to use for the article.

    Returns:
    ------------
    articles: A list of all articles in the database.

    """
    return session.query(orm_class).all()


def get_n_articles_from_db(session: Session, orm_class: Type, n: int):
    """
    Get n articles from database.

    Parameters:
    -----------
    session: The database session.
    orm_class: The ORM class to use for the article.
    n: The number of articles to get.

    Returns:
    -----------
    articles: A list of n articles from the database.

    """
    return session.query(orm_class).limit(n).all()


def delete_article_from_db(article: NewsArticle, session: Session, orm_class: Type):
    """
    Deletes article from database.

    Parameters:
    ----------
    article: The article to delete.
    session: The database session.
    orm_class: The ORM class to use for the article.

    """

    article_orm = session.query(orm_class).filter_by(url=article.url).first()

    if article_orm is None:
        raise DatabaseError(f"Article with URL {article.url} does not exist.")

    session.delete(article_orm)
    session.commit()
