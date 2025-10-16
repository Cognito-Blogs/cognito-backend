# routers/auth.py
from fastapi import APIRouter, HTTPException, Depends, Response, Cookie
from pydantic import BaseModel, EmailStr
from main import db
from utils.auth_utils import hash_password, verify_password, create_access_token, decode_token
from datetime import timedelta
from bson import ObjectId

router = APIRouter()

class RegisterIn(BaseModel):
    username: str
    email: EmailStr
    password: str

class LoginIn(BaseModel):
    email: EmailStr
    password: str

@router.post("/register")
def register(payload: RegisterIn):
    users = db.users
    if users.find_one({"email": payload.email}):
        raise HTTPException(400, "Email already in use")
    pwd_hash = hash_password(payload.password)
    user_doc = {
        "username": payload.username,
        "email": payload.email,
        "password_hash": pwd_hash,
        "created_at": datetime.utcnow(),
        "role": "user"
    }
    res = users.insert_one(user_doc)
    return {"id": str(res.inserted_id)}

@router.post("/login")
def login(payload: LoginIn, response: Response):
    users = db.users
    user = users.find_one({"email": payload.email})
    if not user or not verify_password(payload.password, user["password_hash"]):
        raise HTTPException(401, "Invalid credentials")
    token = create_access_token({"user_id": str(user["_id"])})
    # set cookie (httpOnly)
    response.set_cookie(key="access_token", value=token, httponly=True, secure=False, samesite="lax", max_age=60*60*24*7)
    return {"message":"ok", "user": {"id": str(user["_id"]), "username": user["username"]}}

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message":"logged out"}

# helper to get current user (used by other routers)
from fastapi import Request
def get_current_user(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        return None
    payload = decode_token(token)
    if not payload: return None
    uid = payload.get("user_id")
    return db.users.find_one({"_id": ObjectId(uid)})
