"""
dashboard/youtube_dashboard.py
- Generates Plotly charts for YouTube trending data in MongoDB.
- Writes interactive HTML files to dashboard_output/ so you can open them in browser.
"""

import os
from pymongo import MongoClient
import pandas as pd
import plotly.express as px
from config import MONGO_URI, MONGO_DB, MONGO_COLLECTION

# Output folder for html charts
OUT_DIR = os.path.join(os.getcwd(), "dashboard_output")
os.makedirs(OUT_DIR, exist_ok=True)

def load_data(limit=None):
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB]
    coll = db[MONGO_COLLECTION]
    cursor = coll.find().limit(limit) if limit else coll.find()
    data = list(cursor)
    if not data:
        raise ValueError("No data found in MongoDB collection. Run the pipeline first.")
    df = pd.DataFrame(data)

    # Ensure required fields exist
    for col in ["viewCount", "likeCount", "commentCount", "title", "channel", "category", "fetchedAt"]:
        if col not in df.columns:
            df[col] = None

    # Convert numeric fields safely
    df["viewCount"] = pd.to_numeric(df["viewCount"], errors="coerce").fillna(0).astype(int)
    df["likeCount"] = pd.to_numeric(df["likeCount"], errors="coerce").fillna(0).astype(int)
    df["commentCount"] = pd.to_numeric(df["commentCount"], errors="coerce").fillna(0).astype(int)

    # Shorten titles for display
    df["short_title"] = df["title"].astype(str).apply(lambda x: x if len(x) <= 60 else x[:57] + "...")

    return df

def top_videos_by_views(df, top_n=10):
    top = df.nlargest(top_n, "viewCount")
    fig = px.bar(top, x="short_title", y="viewCount", title=f"Top {top_n} Trending Videos by Views",
                 labels={"short_title":"Title","viewCount":"Views"})
    out = os.path.join(OUT_DIR, f"top_{top_n}_videos_by_views.html")
    fig.write_html(out)
    print("Saved:", out)
    return fig

def top_channels(df, top_n=10):
    agg = df.groupby("channel", as_index=False)["viewCount"].sum().nlargest(top_n, "viewCount")
    fig = px.bar(agg, x="channel", y="viewCount", title=f"Top {top_n} Channels by Total Views",
                 labels={"channel":"Channel","viewCount":"Total Views"})
    out = os.path.join(OUT_DIR, f"top_{top_n}_channels.html")
    fig.write_html(out)
    print("Saved:", out)
    return fig

def category_distribution(df):
    # treat category as string
    df["category"] = df["category"].astype(str).fillna("unknown")
    fig = px.histogram(df, x="category", title="Category Distribution (counts)")
    out = os.path.join(OUT_DIR, "category_distribution.html")
    fig.write_html(out)
    print("Saved:", out)
    return fig

def main():
    try:
        df = load_data()
    except Exception as e:
        print("Error loading data:", e)
        return

    top_videos_by_views(df)
    top_channels(df)
    category_distribution(df)
    print("All dashboard files saved in:", OUT_DIR)

if __name__ == "__main__":
    main()
