from pydantic import BaseModel
from datetime import datetime

class CommentCreate(BaseModel):
    post_id: str
    content: str

class CommentOut(BaseModel):
    id: str
    post_id: str
    author_username: str
    content: str
    created_at: datetime
