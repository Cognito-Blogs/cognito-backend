from fastapi import APIRouter, Depends, HTTPException
from database import posts_collection, users_collection
from schemas.post_schema import PostCreate, PostOut
from utils.auth_utils import get_current_user
from bson import ObjectId
from datetime import datetime

router = APIRouter(prefix="/api/posts", tags=["Posts"])

@router.post("/", response_model=PostOut)
def create_post(post: PostCreate, current_user: dict = Depends(get_current_user)):
    post_data = post.dict()
    post_data.update({
        "author_id": str(current_user["_id"]),
        "author_username": current_user["username"],
        "created_at": datetime.utcnow()
    })
    res = posts_collection.insert_one(post_data)
    post_data["id"] = str(res.inserted_id)
    return post_data

@router.get("/", response_model=list[PostOut])
def list_posts(skip: int = 0, limit: int = 10, username: str = None):
    query = {}
    if username:
        user = users_collection.find_one({"username": username})
        if not user:
            return []
        query["author_id"] = str(user["_id"])

    posts = list(posts_collection.find(query).skip(skip).limit(limit).sort("created_at", -1))
    for p in posts:
        p["id"] = str(p["_id"])
    return posts

@router.get("/{id}", response_model=PostOut)
def get_post(id: str):
    post = posts_collection.find_one({"_id": ObjectId(id)})
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post["id"] = str(post["_id"])
    return post
