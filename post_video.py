#!/usr/bin/env python3
import sys
import datetime
import logging
import random
import os
import shutil

# --- Setup logging ---
log_file = "/home/dav25/mysite_dashboard/logs/post_log.txt"
logging.basicConfig(filename=log_file, level=logging.INFO)

# Paths
VIDEO_DIR = "/home/dav25/mysite_dashboard/videos"
POSTED_DIR = "/home/dav25/mysite_dashboard/posted"

# Make sure folders exist
os.makedirs(VIDEO_DIR, exist_ok=True)
os.makedirs(POSTED_DIR, exist_ok=True)

# Hashtags pool
HASHTAGS = [
    "#fyp", "#viral", "#trending", "#explore", "#mustwatch", "#funny",
    "#motivation", "#healthtips", "#lifehack", "#inspiration", "#education",
    "#tiktokviral", "#wow", "#foryou", "#global"
]

# Caption templates
CAPTIONS = [
    "This will blow your mind 😱 {hashtag}",
    "Don’t scroll without watching! 🚀 {hashtag}",
    "This is what you’ve been waiting for 🎯 {hashtag}",
    "Little change = big results 🔥 {hashtag}",
    "Secrets they don’t want you to know 👀 {hashtag}",
    "Proof that consistency wins 🏆 {hashtag}",
    "Game changer alert ⚡ {hashtag}",
    "Simple, but powerful 💡 {hashtag}",
]

def generate_caption():
    """Pick a random caption and attach 3-5 trending hashtags."""
    caption_template = random.choice(CAPTIONS)
    selected_hashtags = random.sample(HASHTAGS, k=random.randint(3, 5))
    hashtag_block = " ".join(selected_hashtags)
    return caption_template.format(hashtag=hashtag_block)

def get_next_video():
    """Pick first available video, recycle if empty."""
    videos = [f for f in os.listdir(VIDEO_DIR) if f.lower().endswith((".mp4", ".mov", ".avi"))]
    videos.sort()

    # If empty, recycle from posted
    if not videos:
        posted = [f for f in os.listdir(POSTED_DIR) if f.lower().endswith((".mp4", ".mov", ".avi"))]
        posted.sort()
        if posted:
            for f in posted:
                shutil.move(os.path.join(POSTED_DIR, f), os.path.join(VIDEO_DIR, f))
            logging.info("♻️ Recycled posted videos back into /videos/")
            videos = [f for f in os.listdir(VIDEO_DIR) if f.lower().endswith((".mp4", ".mov", ".avi"))]
            videos.sort()

    if not videos:
        return None

    return os.path.join(VIDEO_DIR, videos[0])

def move_to_posted(video_path):
    """Move video to /posted after posting."""
    try:
        filename = os.path.basename(video_path)
        dest_path = os.path.join(POSTED_DIR, filename)
        shutil.move(video_path, dest_path)
        logging.info(f"📦 Moved {video_path} → {dest_path}")
    except Exception as e:
        logging.error(f"❌ Could not move video {video_path}: {str(e)}")

def main():
    # Get the time flag (passed from daily_runner.sh)
    run_time = None
    if "--time" in sys.argv:
        idx = sys.argv.index("--time") + 1
        if idx < len(sys.argv):
            run_time = sys.argv[idx]

    now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    logging.info(f"[{now}] Running TikTok post script (target time: {run_time})")

    # Pick next video
    video_path = get_next_video()
    if not video_path:
        logging.info("⚠️ No videos found even after recycle. Skipping post.")
        return

    # Generate caption
    caption = generate_caption()
    logging.info(f"Generated caption: {caption}")

    try:
        # Example TikTok upload call (replace with actual TikTok API logic)
        # api = TikTokAPI("your_token_here")
        # api.upload_video(video_path, caption=caption)
        logging.info(f"✅ Posted video {video_path} with caption: {caption}")

        # Move video after posting
        move_to_posted(video_path)

    except Exception as e:
        logging.error(f"❌ Error posting video: {str(e)}")

if __name__ == "__main__":
    main()
