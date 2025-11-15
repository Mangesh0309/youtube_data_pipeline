# config.py — safe version that reads from environment
import os

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB = os.getenv("MONGO_DB", "youtube_db")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "trending_videos")
