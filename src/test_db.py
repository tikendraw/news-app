from core.db.db_utils import *

db = next(get_db())

from fastapi import FastAPI

from core.routers import news_router

app = FastAPI()

app.include_router(news_router.article_router)
