from typing import List

from pydantic import BaseModel, Field

class ArticleSummary(BaseModel):
    ai_title: str = Field(description="Catching title for an article")
    summary: str = Field(description="Summary of an article in 100 words only")
    tags: List[str] | None = Field(description="tags related to the article")
    category: list[str] | None = Field(description="Category of an article. should be from Politics, Economics, Business, Technology, Science, Health, Entertainment, Sports, Education, Environment, Lifestyle, Travel")
    locations: list[str] | None = Field(description="Location this article is about")
    
