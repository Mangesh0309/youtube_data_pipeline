"""
scheduler.py
- Keeps the script running and executes youtube_pipeline.py on a schedule.
- Edit the schedule below (every().day.at("09:00") or every().hour).
"""

import os
import time
import logging
import subprocess
import sys
from datetime import datetime
import schedule

# --- ensure logs folder exists ---
os.makedirs("logs", exist_ok=True)

# --- logging config ---
logging.basicConfig(
    filename="logs/scheduler.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# --- path to the pipeline script ---
PIPELINE_SCRIPT = os.path.join(os.getcwd(), "youtube_pipeline.py")

# --- determine python executable (use current interpreter) ---
PYTHON_EXE = sys.executable  # uses the same Python that's running this script

def run_pipeline():
    logging.info("Scheduler triggered pipeline run.")
    try:
        # call pipeline with same python executable; capture return code
        result = subprocess.run([PYTHON_EXE, PIPELINE_SCRIPT], capture_output=True, text=True)
        if result.returncode == 0:
            logging.info("Pipeline finished successfully.")
        else:
            logging.error("Pipeline exited with code %s. stdout: %s stderr: %s",
                          result.returncode, result.stdout, result.stderr)
    except Exception as e:
        logging.exception("Exception while running pipeline: %s", e)

# --- SCHEDULE: choose one approach (uncomment desired schedule) ---

# Run every day at 09:00
schedule.every().day.at("09:00").do(run_pipeline)

# Or run every hour:
# schedule.every().hour.do(run_pipeline)

# Or run every 15 minutes:
# schedule.every(15).minutes.do(run_pipeline)

# Optional: run once immediately on start
run_pipeline()

logging.info("Scheduler started. Awaiting scheduled runs...")
print("Scheduler running. Check logs/scheduler.log for details.")

# main loop
try:
    while True:
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
    logging.info("Scheduler stopped by user at %s", datetime.now())
    print("Scheduler stopped.")
