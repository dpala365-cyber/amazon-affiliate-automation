#!/usr/bin/env python3
import time
from datetime import datetime, timedelta, timezone
import subprocess
import os

# -------------------------------
# CONFIGURATION
# -------------------------------
VIDEOS_DIR = os.path.expanduser("~/mysite_dashboard/videos")
POSTED_TRACK_FILE = os.path.expanduser("~/mysite_dashboard/posted_videos.txt")
DAILY_RUNNER_PATH = os.path.expanduser("~/mysite_dashboard/daily_runner.sh")
LOG_FILE = os.path.expanduser("~/mysite_dashboard/cleanup.log")
ANALYTICS_FILE = os.path.expanduser("~/mysite_dashboard/backend/weekly_peak_hour.txt")  # stores last computed peak hour

ENGAGEMENT_DELAY_MINUTES = 15
WEEKLY_ANALYTICS_DAY = 6

# -------------------------------
# HELPER FUNCTIONS
# -------------------------------
def log(msg):
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {msg}\n")
    print(msg)

def run_command(cmd, description=""):
    log(f"[RUN] {description}")
    subprocess.run(cmd, shell=True)
    log(f"[DONE] {description}")

def get_unposted_videos():
    if not os.path.exists(POSTED_TRACK_FILE):
        open(POSTED_TRACK_FILE, "a").close()
    with open(POSTED_TRACK_FILE, "r") as f:
        posted = set(line.strip() for line in f.readlines())
    all_videos = sorted(f for f in os.listdir(VIDEOS_DIR) if f.lower().endswith(('.mp4','.mov','.avi')))
    return [v for v in all_videos if v not in posted]

def mark_as_posted(video_file):
    with open(POSTED_TRACK_FILE, "a") as f:
        f.write(video_file + "\n")

def get_last_peak_hour(default=14):
    if os.path.exists(ANALYTICS_FILE):
        with open(ANALYTICS_FILE, "r") as f:
            try:
                return int(f.read().strip())
            except:
                return default
    return default

def get_peak_window(peak_hour):
    now = datetime.now(timezone.utc)
    start_peak = now.replace(hour=peak_hour-1, minute=0, second=0, microsecond=0)
    end_peak = now.replace(hour=peak_hour+1, minute=0, second=0, microsecond=0)
    return start_peak, end_peak

def schedule_times(num_videos, start, end):
    delta = (end - start) / max(num_videos, 1)
    return [start + i * delta for i in range(num_videos)]

# -------------------------------
# DAILY SCHEDULER LOOP
# -------------------------------
log("[SCHEDULER] Starting adaptive daily scheduler...")

while True:
    now = datetime.now(timezone.utc)
    log(f"[SCHEDULER] Current UTC time: {now}")

    unposted_videos = get_unposted_videos()
    if not unposted_videos:
        log("[POST] No new videos to post today. Checking again in 1 hour...")
        time.sleep(3600)
        continue

    peak_hour = get_last_peak_hour()
    start_peak, end_peak = get_peak_window(peak_hour)
    scheduled_times = schedule_times(len(unposted_videos), start_peak, end_peak)

    for video, post_time in zip(unposted_videos, scheduled_times):
        now = datetime.now(timezone.utc)
        wait_seconds = (post_time - now).total_seconds()
        if wait_seconds > 0:
            log(f"[SCHEDULER] Waiting {int(wait_seconds)} seconds until posting video {video}...")
            time.sleep(wait_seconds)

        video_path = os.path.join(VIDEOS_DIR, video)
        log(f"[POST] Posting video: {video}")
        run_command(f"{DAILY_RUNNER_PATH} {video_path}", description=f"Post video {video}")
        mark_as_posted(video)

        log(f"[SCHEDULER] Waiting {ENGAGEMENT_DELAY_MINUTES} minutes before live engagement bot for {video}...")
        time.sleep(ENGAGEMENT_DELAY_MINUTES * 60)
        run_command("python3 ~/mysite_dashboard/backend/engagement_smart_bot_live.py", description=f"Live engagement bot for {video}")

    if datetime.now(timezone.utc).weekday() == WEEKLY_ANALYTICS_DAY:
        run_command("python3 ~/mysite_dashboard/backend/weekly_analytics_update.py", description="Weekly analytics update")

    log("[SCHEDULER] All scheduled videos for today posted. Sleeping until next day...")
    next_day = datetime.now(timezone.utc).replace(hour=0, minute=5, second=0, microsecond=0) + timedelta(days=1)
    time.sleep((next_day - datetime.now(timezone.utc)).total_seconds())
