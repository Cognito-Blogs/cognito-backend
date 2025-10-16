# routers/comments.py
from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from bson import ObjectId
from main import db
from routers.auth import get_current_user
from datetime import datetime

router = APIRouter()

class CommentIn(BaseModel):
    post_id: str
    content: str
    parent_comment_id: str | None = None

@router.post("/")
def create_comment(payload: CommentIn, request: Request):
    user = get_current_user(request)
    if not user:
        raise HTTPException(401, "Authentication required")
    comment = {
        "post_id": ObjectId(payload.post_id),
        "author_id": user["_id"],
        "content": payload.content,
        "parent_comment_id": ObjectId(payload.parent_comment_id) if payload.parent_comment_id else None,
        "created_at": datetime.utcnow()
    }
    res = db.comments.insert_one(comment)
    # increment count
    db.posts.update_one({"_id": ObjectId(payload.post_id)}, {"$inc": {"comments_count": 1}})
    return {"id": str(res.inserted_id)}

@router.get("/post/{post_id}")
def get_comments(post_id: str):
    cursor = db.comments.find({"post_id": ObjectId(post_id)}).sort("created_at", 1)
    comments = []
    for c in cursor:
        c["id"] = str(c["_id"])
        c["author_id"] = str(c["author_id"])
        if c.get("parent_comment_id"):
            c["parent_comment_id"] = str(c["parent_comment_id"])
        comments.append(c)
    return comments
