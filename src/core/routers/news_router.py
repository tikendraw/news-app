from fastapi import APIRouter, Depends
from ..db.db_utils import get_news_from_db, get_db

router = APIRouter(prefix="/news")

@router.get("/")
async def get_news():
    return {"message": "Hello, World!"}