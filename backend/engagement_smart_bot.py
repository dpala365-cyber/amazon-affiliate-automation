#!/usr/bin/env python3
import os
import random
from datetime import datetime, timezone

# --- Load last posted video ID ---
VIDEO_ID_FILE = os.path.expanduser('~/mysite_dashboard/last_posted_video_id.txt')
if os.path.exists(VIDEO_ID_FILE):
    with open(VIDEO_ID_FILE, 'r') as f:
        last_video_id = f.read().strip()
else:
    last_video_id = "TEST_VIDEO_ID_123"

# --- Sample comments on the video (replace with real API fetch later) ---
comments = [
    "Awesome video!",
    "How much is this?",
    "Love it!",
    "When is the next one?",
    "Amazing content!"
]

# --- Reply templates based on keywords ---
reply_templates = {
    "awesome": ["Thanks a lot! 💫", "Glad you liked it! 🙌"],
    "how much": ["Check the link in bio for details! 🔗", "Price info is in the description! 💰"],
    "love": ["Much love! ❤️", "Appreciate you! 🙏"],
    "when": ["Stay tuned! 🚀", "Next video coming soon! ⏳"],
    "amazing": ["You're awesome — thanks for watching! 🙌", "Happy you enjoyed it! 😊"]
}

# --- Engagement percentage (only 10% of comments to start) ---
ENGAGE_PERCENT = 10
daily_likes = 0
daily_replies = 0
pinned_comment_done = False

print(f"[ENGAGE] Starting smart engagement run @ {datetime.now(timezone.utc)} UTC")
for comment in comments:
    if random.randint(1, 100) <= ENGAGE_PERCENT:
        # Like the comment
        daily_likes += 1
        print(f"[SMART ENGAGE] Would LIKE comment '{comment}' on video {last_video_id}")
        
        # Reply to the comment based on keyword match
        for keyword, replies in reply_templates.items():
            if keyword.lower() in comment.lower():
                daily_replies += 1
                reply = random.choice(replies)
                print(f"[SMART ENGAGE] Would REPLY to '{comment}' on video {last_video_id}: {reply}")
                # Pin the first comment we reply to (only once)
                if not pinned_comment_done:
                    pinned_comment_done = True
                    print(f"[SMART ENGAGE] Would PIN comment '{comment}' on video {last_video_id}")
                break

print(f"[ENGAGE] Finished smart engagement run @ {datetime.now(timezone.utc)} UTC | likes={daily_likes}, replies={daily_replies}, pinned={pinned_comment_done}")
