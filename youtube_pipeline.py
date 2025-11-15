import requests
import pandas as pd
from pymongo import MongoClient
from datetime import datetime
import logging
from config import YOUTUBE_API_KEY, MONGO_URI, MONGO_DB, MONGO_COLLECTION

# Configure Logging
logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

API_URL = "https://www.googleapis.com/youtube/v3/videos"

def fetch_trending_videos():
    """Fetch trending YouTube videos using YouTube Data API."""
    params = {
        "part": "snippet,statistics",
        "chart": "mostPopular",
        "regionCode": "IN",
        "maxResults": 20,
        "key": YOUTUBE_API_KEY
    }

    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        data = response.json()

        videos = []
        for item in data.get("items", []):
            video = {
                "video_id": item["id"],
                "title": item["snippet"]["title"],
                "channel": item["snippet"]["channelTitle"],
                "category": item["snippet"]["categoryId"],
                "publishedAt": item["snippet"]["publishedAt"],
                "viewCount": int(item["statistics"].get("viewCount", 0)),
                "likeCount": int(item["statistics"].get("likeCount", 0)),
                "commentCount": int(item["statistics"].get("commentCount", 0)),
                "fetchedAt": datetime.now()
            }
            videos.append(video)

        logging.info(f"Fetched {len(videos)} trending videos.")
        return videos

    except Exception as e:
        logging.error(f"Error fetching trending videos: {e}")
        return []


def load_to_mongodb(records):
    """Insert/Update YouTube data in MongoDB."""
    try:
        client = MongoClient(MONGO_URI)
        db = client[MONGO_DB]
        collection = db[MONGO_COLLECTION]

        for record in records:
            # upsert prevents duplicates
            collection.update_one(
                {"video_id": record["video_id"]},
                {"$set": record},
                upsert=True
            )

        logging.info(f"Upserted {len(records)} records into MongoDB.")

    except Exception as e:
        logging.error(f"Error loading data to MongoDB: {e}")


def run_pipeline():
    logging.info("=== YouTube Pipeline Started ===")

    records = fetch_trending_videos()

    if records:
        load_to_mongodb(records)
        logging.info("=== Pipeline Completed Successfully ===")
    else:
        logging.warning("Pipeline completed with 0 records fetched.")


if __name__ == "__main__":
    run_pipeline()
