#!/usr/bin/env python3
import os
from datetime import datetime, timezone

# Set video directory
video_dir = os.path.expanduser("~/mysite_dashboard/videos")
posted_dir = os.path.expanduser("~/mysite_dashboard/videos_posted")

# Ensure directories exist
os.makedirs(video_dir, exist_ok=True)
os.makedirs(posted_dir, exist_ok=True)

# Peak hour (will be updated by weekly analytics)
peak_hour = 14  # UTC

# Get current hour in UTC
current_hour = datetime.now(timezone.utc).hour

# Fetch video files
videos = [f for f in os.listdir(video_dir) if f.endswith(".mp4")]

if not videos:
    print(f"No videos found to post. Skipping TikTok post.: {datetime.now(timezone.utc)} UTC")
else:
    if current_hour == peak_hour:
        for video in videos:
            video_path = os.path.join(video_dir, video)
            # Add your TikTok post logic here (API call)
            print(f"Posted video: {video} at {datetime.now(timezone.utc)} UTC")
            # Move posted video to posted_dir
            os.rename(video_path, os.path.join(posted_dir, video))
    else:
        print(f"Current hour {current_hour} UTC is not peak hour ({peak_hour} UTC). Skipping TikTok post.")
