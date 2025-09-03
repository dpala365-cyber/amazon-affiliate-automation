#!/usr/bin/env python3
import json
import random
import time
import os
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))

VIDEOS_JSON = os.path.join(BASE, "videos.json")
LOG_FILE = os.path.join(BASE, "logs/engagement_log.txt")

# AI-generated niche comments for your target audience
AI_COMMENTS = [
    "Wow! Just what I needed for brain fog! 🧠",
    "This supplement looks amazing! #NeuroActive6",
    "My energy levels need this! 💪",
    "Perfect for boosting focus and memory! 🧠✨",
    "Love how this supports healthy aging! 🌿",
    "Finally something for brain health that works! 🧠",
]

def log_action(action):
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now()} - {action}\n")
    print(action)

def simulate_engagement(video_path):
    # Simulate multiple likes
    for i in range(3):
        log_action(f"✅ Liked video {os.path.basename(video_path)}")
        time.sleep(random.uniform(0.5, 1.5))

    # Simulate commenting
    comment = random.choice(AI_COMMENTS)
    log_action(f"💬 Commented on {os.path.basename(video_path)}: {comment}")
    time.sleep(random.uniform(0.5, 1.5))

    # Simulate sharing
    log_action(f"🔄 Shared video {os.path.basename(video_path)}")
    time.sleep(random.uniform(0.5, 1.5))

def main():
    if not os.path.exists(VIDEOS_JSON):
        log_action("⚠️ videos.json not found. Exiting engagement bot.")
        return

    with open(VIDEOS_JSON, "r") as f:
        videos = json.load(f)

    for video in videos:
        video_path = video["video_path"]
        if not os.path.exists(video_path):
            log_action(f"⚠️ Video not found: {video_path}. Skipping.")
            continue
        simulate_engagement(video_path)

    log_action("🎯 TikTok engagement bot run completed.")

if __name__ == "__main__":
    main()
