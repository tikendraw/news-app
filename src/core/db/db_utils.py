from ..news_model import NewsArticle
from . import Session
from .news_table import NewsArticleORM


# Function to parse JSON articles and insert into database if valid
def add_articles_to_db(json_data: dict, session: Session) -> None:
    articles = json_data.get('articles', [])
    for article_data in articles:
        article = NewsArticle(**article_data)
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


# Function to get all articles from database
def get_articles_from_db(session: Session) -> list:
    return session.query(NewsArticleORM).all()

# Get n latest articles from the db
def get_n_latest_articles_from_db(session: Session, n: int) -> list:
    return (
        session.query(NewsArticleORM)
        .order_by(NewsArticleORM.published_at.desc())
        .limit(n)
        .all()
    )
    
# delete article using id
def delete_article_from_db(session: Session, article_id: int) -> None:
    session.query(NewsArticleORM).filter(NewsArticleORM.id == article_id).delete()
    session.commit()

# delete all articles from db
def delete_all_articles_from_db(session: Session) -> None:
    session.query(NewsArticleORM).delete()
    session.commit()