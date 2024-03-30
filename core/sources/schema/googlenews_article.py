from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, Field, HttpUrl

from ...schema.article import Article


class GoogleNewsArticle(Article):
    title: str
    url:            str = Field(alias="link", default=None)
    description:    Optional[str] = Field(None, alias="description")
    content:        Optional[str] = Field(None, alias="body")
    published_at:   datetime = Field(alias="date")
    category:       Optional[str] = None
    image:          Optional[str] = None
    source_name:    str = Field(alias="source", default=None)
    source_url:     Optional[str] = Field(None, alias="link")
    meta_data:      Optional[dict] = Field(None, alias="props")
    language:       Optional[str] = Field(None, alias='language')

        
    def __init__(self, **data):
        super().__init__(**data)
        # Populate attributes from props if present
        if self.meta_data:
            self.image = self.meta_data.get('image')
    