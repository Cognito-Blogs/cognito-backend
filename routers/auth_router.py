from fastapi import APIRouter, Response, HTTPException, Depends
from database import users_collection
from schemas.user_schema import UserRegister, UserLogin, UserOut
from utils.auth_utils import hash_password, verify_password, get_current_user
from utils.jwt_utils import create_access_token
from bson import ObjectId

router = APIRouter(prefix="/api/auth", tags=["Auth"])

@router.post("/register", response_model=UserOut)
def register_user(user: UserRegister):
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    user.password = hash_password(user.password)
    res = users_collection.insert_one(user.dict())
    return {"id": str(res.inserted_id), "username": user.username, "email": user.email}

@router.post("/login")
def login_user(user: UserLogin, response: Response):
    db_user = users_collection.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(db_user["_id"])})
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,
        samesite="lax"
    )
    return {"message": "Logged in"}

@router.post("/logout")
def logout_user(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logged out"}

@router.get("/me", response_model=UserOut)
def get_me(current_user: dict = Depends(get_current_user)):
    return {
        "id": str(current_user["_id"]),
        "username": current_user["username"],
        "email": current_user["email"]
    }
