from pydantic import BaseModel
from typing import List
from datetime import datetime

class PostCreate(BaseModel):
    title: str
    content: str
    tags: List[str] = []
    published: bool = True

class PostOut(BaseModel):
    id: str
    title: str
    slug: str
    content: str
    author_username: str
    created_at: datetime
