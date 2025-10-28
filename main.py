# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from routers import auth_router, post_router, comment_router

load_dotenv()

app = FastAPI(title="FastBlog API")

origins = [os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(post_router.router)
app.include_router(comment_router.router)
