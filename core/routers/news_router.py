from typing import Dict, List, Optional, Union

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..schema.article import NewsArticle, ShowArticle 
from ..db.news_tables import NewsArticleORM

from ..db.crud.news_crud import (add_article, delete_article, get_articles,
                                 get_n_articles, update_article)
from ..db.db_exceptions import (AddArticleError, DatabaseError,
                                DeleteArticleError, UpdateArticleError)
from ..db.db_utils import \
    get_db  # Assuming get_db function provides a database session
from ..schema.article import ShowArticle

article_router = APIRouter(
    prefix="/news",
    tags=["news"],
)

@article_router.get("/test")
async def testt():
    return {"message": "Hello, World!"}


@article_router.get("/", response_model=List[ShowArticle], description="Get all news articles", status_code=status.HTTP_200_OK)
async def get_all_articles(db: Session = Depends(get_db)):
    
    
    articles = get_articles(db, NewsArticleORM)  # Use your ORM class here
    if articles:
        return articles
    else :
        raise HTTPException(status_code=404, detail="No articles found")
    

@article_router.post("/", description="Add a new news article", status_code=status.HTTP_201_CREATED)
async def add_article_to_db(article: NewsArticle, db: Session = Depends(get_db)):
    try:
        add_article(article, db, NewsArticleORM)  # Use your ORM class here
    except AddArticleError as e:
        raise HTTPException(status_code=400, detail=f"Error adding article: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding article: {e}")
    

@article_router.delete("/{article_id}")
async def delete_article_from_db(article_id : int, db: Session = Depends(get_db)):
    try:
        delete_article(article_id, db, NewsArticleORM)  # Use your ORM class here
        return {"message": "Article deleted successfully"}
    except DeleteArticleError as e:
        raise HTTPException(status_code=500, detail=f"Error deleting article: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting article: {e}")
    

@article_router.put("/{article_id}", description="Update an existing news article", status_code=status.HTTP_200_OK)
async def update_article_in_db(article_id: int, article: NewsArticle, db: Session = Depends(get_db)):
    try:
        update_article(article_id, article, db, NewsArticleORM)  # Use your ORM class here
        return {"message": "Article updated successfully"}
    except UpdateArticleError as e:
        raise HTTPException(
            status_code=500, detail=f"Error updating article: {e}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error updating article: {e}"
        )