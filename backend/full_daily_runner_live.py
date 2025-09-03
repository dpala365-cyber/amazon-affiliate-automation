#!/usr/bin/env python3
import json
import logging
from datetime import datetime, timezone
import shutil
import os
import subprocess

# --- Setup paths ---
BASE = os.path.dirname(os.path.abspath(__file__))
VIDEOS_JSON = os.path.join(BASE, "videos.json")
VIDEOS_DIR = os.path.join(BASE, "videos")
POSTED_DIR = os.path.join(BASE, "posted")
LOGS_DIR = os.path.join(BASE, "logs")
LOG_FILE = os.path.join(LOGS_DIR, "post_log.txt")

# --- Setup logging ---
os.makedirs(LOGS_DIR, exist_ok=True)
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# --- Define peak hours (ET for USA audience 45-65y) ---
PEAK_HOURS_ET = [7, 12, 18]  # Example hours, adjust to analytics

# --- Get current hour in ET ---
current_hour = datetime.now(timezone.utc).astimezone().hour

logging.info(f"⏰ Current ET hour ({current_hour}) check")

# --- Check if it's peak hour ---
if current_hour not in PEAK_HOURS_ET:
    logging.info(f"⏰ Not peak hours. Skipping post.")
else:
    # --- Load videos.json ---
    if not os.path.exists(VIDEOS_JSON):
        logging.error(f"❌ {VIDEOS_JSON} not found. No videos to post.")
        exit()

    with open(VIDEOS_JSON, "r") as f:
        try:
            videos = json.load(f)
        except json.JSONDecodeError:
            logging.error("❌ videos.json is invalid JSON")
            exit()

    if not videos:
        logging.info("⚠️ No videos found in videos.json")
        exit()

    # --- Post videos ---
    for video in videos:
        video_path = video.get("video_path")
        caption = video.get("caption", "")
        hashtags = " ".join(video.get("hashtags", []))

        if not os.path.exists(video_path):
            logging.warning(f"⚠️ Video not found: {video_path}. Skipping.")
            continue

        # Simulate posting (replace this with TikTok API call)
        logging.info(f"✅ Posted video {video_path} with caption: {caption} {hashtags}")

        # Move video to posted folder
        os.makedirs(POSTED_DIR, exist_ok=True)
        shutil.move(video_path, os.path.join(POSTED_DIR, os.path.basename(video_path)))
        logging.info(f"📦 Moved {video_path} → {POSTED_DIR}")

logging.info("🎯 Daily automation run completed")

# --- Run TikTok engagement bot after posting videos ---
try:
    subprocess.run([
        "python3",
        "/home/dav25/mysite_dashboard/backend/tiktok_engagement_bot.py"
    ], check=True)
    print("🎯 Engagement bot completed successfully.")
except subprocess.CalledProcessError as e:
    print(f"⚠️ Engagement bot failed: {e}")
