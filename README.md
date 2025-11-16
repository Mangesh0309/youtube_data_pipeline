YouTube Trending Data Engineering Pipeline (API → Python → MongoDB)

A complete Data Engineering ETL pipeline that extracts trending video metadata from the YouTube Data API, performs data cleaning & transformation using Python, and loads structured documents into MongoDB.
The project also includes automated scheduling, logging, and interactive dashboards for analytics.

Features

-Extract trending YouTube videos via YouTube Data API
-Transform raw JSON into clean, structured, analytics-ready data
-Store data in MongoDB using upsert logic (avoids duplicates)
-Automated scheduling (daily/hourly) using Python schedule
-Logging system for monitoring pipeline execution
-Interactive Plotly dashboard for insights
-Secure configuration using environment variables
-Modular, production-like project structure

youtube_data_pipeline/
│
├── youtube_pipeline.py         # Main ETL pipeline (extract, transform, load)
├── scheduler.py                # Automated daily/hourly pipeline runs
├── config.py                   # Loads API keys & DB config from environment
│
├── dashboard/
│   └── youtube_dashboard.py    # Interactive analytics dashboard
│
├── sample_output/
│   └── sample_document.json    # Example MongoDB document
│
├── logs/
│   ├── pipeline.log            # Pipeline execution logs
│   └── scheduler.log           # Scheduler logs
│
├── requirements.txt            # Project dependencies
└── README.md                   # Documentation

Setup Instructions
1. Clone the repository
   
   git clone https://github.com/Mangesh0309/youtube_data_pipeline.git
   cd youtube_data_pipeline
2. Create virtual environment
   
   python -m venv venv
   .\venv\Scripts\activate
3. Install dependencies
 
   pip install -r requirements.txt
7. Configure environment variables
   
   Create a .env file in project root:
   
   YOUTUBE_API_KEY=YOUR_API_KEY
   MONGO_URI=mongodb://localhost:27017/
   MONGO_DB=youtube_db
   MONGO_COLLECTION=trending_videos

   config is loaded automatically through config.py.
9. Run the ETL Pipeline
    
   python youtube_pipeline.py
11. Run the Dashboard
    
   python dashboard/youtube_dashboard.py

Generated files appear in dashboard_output/:
- top_10_videos_by_views.html
- top_10_channels.html
- category_distribution.html
 
Open them in your browser to view the insights.


Automated Scheduling (Daily / Hourly)
- Run the Python scheduler:
  python scheduler.py
- You can modify the schedule inside scheduler.py:
  schedule.every().day.at("09:00").do(run_pipeline)
- Or run every hour:
  schedule.every().hour.do(run_pipeline)

Sample MongoDB Document

Located in sample_output/sample_document.json:

{
  "video_id": "Xyz123",
  "title": "Top Trending Songs 2025",
  "channel": "T-Series",
  "category": "10",
  "publishedAt": "2025-01-10T12:34:00Z",
  "viewCount": 9834500,
  "likeCount": 234000,
  "commentCount": 12900,
  "fetchedAt": "2025-11-15T20:21:09"
}


📝 License

MIT License
