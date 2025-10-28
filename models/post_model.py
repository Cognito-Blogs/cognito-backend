from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class Post(BaseModel):
    id: Optional[str]
    title: str
    content: str
    author_id: str
    author_username: str
    tags: List[str] = []
    created_at: datetime = datetime.utcnow()
    published: bool = True
