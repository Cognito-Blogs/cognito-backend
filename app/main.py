# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from pymongo import MongoClient
from routers import auth, posts, comments

app = FastAPI()

# CORS - trust your frontend origin
origins = [os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,     # needed for cookies
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mongo client
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
client = MongoClient(MONGO_URL)
db = client["blogdb"]

# include routers (defined below or in routers/*.py)
app.include_router(auth.router, prefix="/api/auth")
app.include_router(posts.router, prefix="/api/posts")
app.include_router(comments.router, prefix="/api/comments")
