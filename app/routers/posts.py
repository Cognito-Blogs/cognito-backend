# routers/posts.py
from fastapi import APIRouter, HTTPException, Request, Depends
from pydantic import BaseModel
from bson import ObjectId
from datetime import datetime
from main import db
from routers.auth import get_current_user

router = APIRouter()

class PostIn(BaseModel):
    title: str
    content: str
    tags: list[str] = []
    published: bool = True

@router.post("/")
def create_post(payload: PostIn, request: Request):
    user = get_current_user(request)
    if not user:
        raise HTTPException(401, "Authentication required")
    post = {
        "author_id": user["_id"],
        "title": payload.title,
        "content": payload.content,
        "summary": payload.content[:200],
        "tags": payload.tags,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "comments_count": 0,
        "published": payload.published
    }
    res = db.posts.insert_one(post)
    return {"id": str(res.inserted_id), "slug": slug}

@router.get("/")
def list_posts(skip: int = 0, limit: int = 10):
    cursor = db.posts.find({"published": True}).sort("created_at", -1).skip(skip).limit(limit)
    posts = []
    for p in cursor:
        p["id"] = str(p["_id"])
        p["author_id"] = str(p["author_id"])
        posts.append(p)
    return posts


