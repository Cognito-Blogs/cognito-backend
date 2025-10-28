from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Comment(BaseModel):
    id: Optional[str]
    post_id: str
    author_id: str
    author_username: str
    content: str
    created_at: datetime = datetime.utcnow()
