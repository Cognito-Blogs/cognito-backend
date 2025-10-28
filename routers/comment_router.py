from fastapi import APIRouter, Depends, HTTPException
from database import comments_collection, posts_collection
from schemas.comment_schema import CommentCreate, CommentOut
from utils.auth_utils import get_current_user
from datetime import datetime
from bson import ObjectId

router = APIRouter(prefix="/api/comments", tags=["Comments"])

@router.post("/", response_model=CommentOut)
def create_comment(comment: CommentCreate, current_user: dict = Depends(get_current_user)):
    post = posts_collection.find_one({"_id": ObjectId(comment.post_id)})
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    data = {
        "post_id": comment.post_id,
        "author_id": str(current_user["_id"]),
        "author_username": current_user["username"],
        "content": comment.content,
        "created_at": datetime.utcnow(),
    }
    res = comments_collection.insert_one(data)
    data["id"] = str(res.inserted_id)
    return data

@router.get("/post/{post_id}", response_model=list[CommentOut])
def list_comments(post_id: str):
    comments = list(comments_collection.find({"post_id": post_id}).sort("created_at", -1))
    for c in comments:
        c["id"] = str(c["_id"])
    return comments
