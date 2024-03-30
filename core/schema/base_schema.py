from datetime import datetime
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field, HttpUrl

# Shared properties


class BaseModel(BaseModel):
    class Config:
        from_attributes: bool = True
        populate_by_name = True

