#!/usr/bin/env python3
import os
import json
from datetime import datetime
import random

# Base directory
BASE = os.path.expanduser("~/mysite_dashboard/backend")

# Videos folder and JSON
VIDEOS_FOLDER = os.path.join(BASE, "videos")
JSON_FILE = os.path.join(BASE, "videos.json")

# Ensure videos folder exists
os.makedirs(VIDEOS_FOLDER, exist_ok=True)

# Keywords & captions (Health & Wellness, low competition)
KEYWORDS = [
    "Brain Fog Fix", "Memory Boost", "Neuro Active 6", 
    "Focus & Clarity", "Fibermaxing", "Healthy Aging"
]

CAPTIONS = [
    "Don’t scroll without watching! 🚀",
    "Boost your brain today! 🧠",
    "Feel the clarity! 😎",
    "Fibermaxing for your health! 🌱",
    "Neuro Active 6 is your daily brain boost!"
]

HASHTAGS = ["#fyp","#viral","#trending","#health","#wellness","#neuroactive6"]

# Number of videos to generate per day
NUM_VIDEOS = 3

videos_list = []

for i in range(1, NUM_VIDEOS + 1):
    filename = f"video_auto_{datetime.now().strftime('%Y%m%d')}_{i}.mp4"
    filepath = os.path.join(VIDEOS_FOLDER, filename)

    # Create empty dummy video file (replace later with real generation)
    with open(filepath, "wb") as f:
        f.write(b"")  # placeholder for actual video content

    # Random caption
    caption = random.choice(CAPTIONS)
    videos_list.append({
        "video_path": filepath,
        "caption": caption,
        "hashtags": HASHTAGS
    })

# Write videos.json
with open(JSON_FILE, "w") as f:
    json.dump(videos_list, f, indent=2)

print(f"✅ Generated {NUM_VIDEOS} videos and updated videos.json")
