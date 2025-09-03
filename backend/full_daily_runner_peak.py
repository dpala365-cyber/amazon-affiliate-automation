#!/usr/bin/env python3
import os
import json
import shutil
import logging
from datetime import datetime, timezone, timedelta

# --- Paths ---
BASE = "/home/dav25/mysite_dashboard/backend"
VIDEOS_JSON = os.path.join(BASE, "videos.json")
VIDEOS_FOLDER = os.path.join(BASE, "videos")
POSTED_FOLDER = os.path.join(BASE, "posted")
LOGS_FOLDER = os.path.join(BASE, "logs")
LOG_FILE = os.path.join(LOGS_FOLDER, "post_log.txt")

# --- Logging ---
os.makedirs(LOGS_FOLDER, exist_ok=True)
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# --- USA Eastern Time ---
ET = timezone(timedelta(hours=-5))  # Eastern Standard Time (adjust for DST if needed)
current_hour_et = datetime.now(ET).hour

# --- Peak Hours in ET ---
PEAK_HOURS_ET = [8,9,10,12,13,14,18,19,20]

if current_hour_et not in PEAK_HOURS_ET:
    logging.info(f"⏰ Current ET hour ({current_hour_et}) not in peak hours. Skipping post.")
    exit()

# --- Read videos.json ---
if not os.path.exists(VIDEOS_JSON):
    logging.error("videos.json not found! Automation aborted.")
    exit()

with open(VIDEOS_JSON, "r") as f:
    try:
        videos = json.load(f)
    except json.JSONDecodeError:
        logging.error("videos.json is invalid! Automation aborted.")
        exit()

if not videos:
    logging.warning("No videos listed in videos.json. Skipping.")
    exit()

# --- Post up to 5 videos ---
to_post = videos[:5]

for video in to_post:
    video_path = video.get("video_path")
    caption = video.get("caption", "")
    hashtags = " ".join(video.get("hashtags", []))

    if not os.path.exists(video_path):
        logging.warning(f"Video not found: {video_path}. Skipping.")
        continue

    # --- Simulate posting ---
    logging.info(f"✅ Posted video {video_path} with caption: {caption} {hashtags}")

    # --- Move video to posted folder ---
    shutil.move(video_path, os.path.join(POSTED_FOLDER, os.path.basename(video_path)))
    logging.info(f"📦 Moved {video_path} → {POSTED_FOLDER}")

logging.info("🎯 Peak-hour automation run completed.")
