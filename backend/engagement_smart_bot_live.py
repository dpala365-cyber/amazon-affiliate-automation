#!/usr/bin/env python3
import os
import time
from datetime import datetime, timezone
import random
import openai

# -------------------------------
# CONFIGURATION
# -------------------------------
VIDEO_ID_FILE = os.path.expanduser("~/mysite_dashboard/last_posted_video_id.txt")
LOG_FILE = os.path.expanduser("~/mysite_dashboard/cleanup.log")

# OpenAI API key (set as env variable for security)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Maximum number of comments to respond per run
MAX_COMMENTS = 10

# -------------------------------
# HELPER FUNCTIONS
# -------------------------------
def log(msg):
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {msg}\n")
    print(msg)

def fetch_recent_comments(video_id):
    """
    Placeholder function: Replace with actual TikTok API call
    Returns list of dicts: [{'id': 'c1', 'text': 'Great vid!'}, ...]
    """
    return [
        {"id": f"c{i+1}", "text": txt}
        for i, txt in enumerate(["Love it!", "Awesome video!", "Nice work!"])
    ][:MAX_COMMENTS]

def like_comment(comment_id):
    log(f"[LIVE ENGAGE] Liked comment {comment_id}")
    # Add TikTok API call here

def pin_comment(comment_id):
    log(f"[LIVE ENGAGE] Pinned comment {comment_id}")
    # Add TikTok API call here

def reply_comment_gpt(comment_text):
    """
    Generate smart reply using OpenAI GPT API
    """
    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a friendly, short, and engaging social media commenter."},
                {"role": "user", "content": f"Reply to this TikTok comment in a friendly, engaging way: '{comment_text}'"}
            ],
            temperature=0.7,
            max_tokens=60
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        log(f"[ERROR] GPT reply failed: {e}")
        return "Glad you liked it! 😄"

def reply_comment(comment_id, reply_text):
    log(f"[LIVE ENGAGE] Replied to {comment_id}: {reply_text}")
    # Add TikTok API call here

# -------------------------------
# MAIN LIVE ENGAGEMENT LOGIC
# -------------------------------
def main():
    if not os.path.exists(VIDEO_ID_FILE):
        log("[ERROR] No last posted video ID found.")
        return
    with open(VIDEO_ID_FILE, "r") as f:
        video_id = f.read().strip()

    log(f"[ENGAGE] Starting live engagement run for video {video_id} @ {datetime.now(timezone.utc)}")

    comments = fetch_recent_comments(video_id)
    likes = 0
    replies = 0
    pinned = False

    for c in comments:
        comment_id = c["id"]
        comment_text = c["text"]

        # Like comment
        like_comment(comment_id)
        likes += 1

        # GPT-powered reply
        reply_text = reply_comment_gpt(comment_text)
        reply_comment(comment_id, reply_text)
        replies += 1

        # Randomly pin one comment
        if not pinned and random.random() < 0.3:
            pin_comment(comment_id)
            pinned = True

        # Delay between actions
        time.sleep(random.randint(3, 6))

    log(f"[ENGAGE] Finished live engagement run | likes={likes}, replies={replies}, pinned={pinned}")

if __name__ == "__main__":
    main()
