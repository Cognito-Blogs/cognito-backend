from pymongo import MongoClient
import os

from dotenv import load_dotenv
load_dotenv()

# Mongo client
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
client = MongoClient(MONGO_URL)
db = client["main"]

users_collection = db["users"]
posts_collection = db["posts"]
comments_collection = db["comments"]