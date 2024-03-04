from typing import Iterable, List

# Function to parse JSON articles and insert into database if valid
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..news_model import NewsArticle
from . import Session
from .news_table import NewsArticleORM


class AddArticleError(Exception):
    """Raised when adding an article to the database fails."""

    pass


class UpdateArticleError(Exception):
    """Raised when updating an article in the database fails."""

    pass


class DatabaseError(Exception):
    """Raised for database-related errors."""

    pass


def add_article_to_db(article: NewsArticle, session: Session) -> None:
    """
    Add a single article to the database if it doesn't exist.
    """
    try:
        article_orm = NewsArticleORM(
            title=article.title,
            description=article.description,
            content=article.content,
            url=str(article.url),
            image=str(article.image),
            published_at=article.published_at,
            source_name=article.source.name,
            source_url=str(article.source.url),
        )
        session.add(article_orm)
        session.commit()
    except Exception as e:
        session.rollback()
        raise AddArticleError(
            f"Failed to add article '{article.title}' to database: {str(e)}"
        )


def update_article_in_db(article: NewsArticle, session: Session) -> None:
    """
    Update an existing article in the database.
    """
    try:
        article_orm = (
            session.query(NewsArticleORM).filter_by(url=str(article.url)).first()
        )
        if article_orm:
            article_orm.title = article.title
            article_orm.description = article.description
            article_orm.content = article.content
            article_orm.image = str(article.image)
            article_orm.published_at = article.published_at
            article_orm.source_name = article.source.name
            article_orm.source_url = str(article.source.url)
            session.commit()
        else:
            raise UpdateArticleError(
                f"Article with URL '{article.url}' not found in database. Skipping update."
            )
    except Exception as e:
        session.rollback()
        raise UpdateArticleError(
            f"Failed to update article with URL '{article.url}' in database: {str(e)}"
        )


def add_articles_to_db(articles: Iterable[NewsArticle], session: Session) -> None:
    """
    Add a list of articles to the database.
    """
    add_count = 0
    update_count = 0
    for article in articles:
        if not isinstance(article, NewsArticle):
            raise TypeError("Articles must be a list of NewsArticle objects.")
        try:
            if (
                not session.query(NewsArticleORM)
                .filter_by(url=str(article.url))
                .first()
            ):
                add_article_to_db(article, session)
                add_count += 1
            else:
                update_article_in_db(article, session)
                update_count += 1
        except (AddArticleError, UpdateArticleError) as e:
            print(f"Error occurred while processing article: {str(e)}")

    if add_count:
        print(f"Added {add_count} articles to database.")
    if update_count:
        print(f"Updated {update_count} articles in database.")


# Function to retrieve articles from database
def get_articles_from_db(session: Session) -> List[NewsArticleORM]:
    """Retrieve all articles from the database."""
    try:
        return session.query(NewsArticleORM).all()
    except Exception as e:
        raise DatabaseError(f"Failed to retrieve articles from database: {str(e)}")


def get_n_latest_articles_from_db(session: Session, n: int) -> List[NewsArticleORM]:
    """Retrieve the latest n articles from the database."""
    try:
        return (
            session.query(NewsArticleORM)
            .order_by(NewsArticleORM.published_at.desc())
            .limit(n)
            .all()
        )
    except Exception as e:
        raise DatabaseError(
            f"Failed to retrieve latest articles from database: {str(e)}"
        )


def delete_article_from_db(session: Session, article_id: int) -> None:
    """Delete an article from the database by its ID."""
    try:
        session.query(NewsArticleORM).filter(NewsArticleORM.id == article_id).delete()
        session.commit()
    except Exception as e:
        raise DatabaseError(f"Failed to delete article from database: {str(e)}")


def delete_all_articles_from_db(session: Session) -> None:
    """Delete all articles from the database."""
    try:
        session.query(NewsArticleORM).delete()
        session.commit()
    except Exception as e:
        raise DatabaseError(f"Failed to delete all articles from database: {str(e)}")
