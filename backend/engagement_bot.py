#!/usr/bin/env python3
"""
Engagement Bot (dry-run by default)

What it does (when DRY_RUN=False):
- Finds the last posted video (reads ~/mysite_dashboard/last_posted_video_id.txt)
- Fetches recent comments
- Randomly likes some comments
- Replies using short friendly templates (never spammy)
- Optionally pins one “great” comment

Safe defaults:
- DRY_RUN=True (prints actions without calling API)
- Rate limits + caps per run
"""

import os
import json
import random
import time
from datetime import datetime, timezone

# ---------- CONFIG ----------
DRY_RUN = True  # <- set to False when you're ready to go live
MAX_REPLIES_PER_RUN = 6
MAX_LIKES_PER_RUN = 10
SLEEP_BETWEEN_ACTIONS_SEC = (4, 9)  # random sleep range
STATE_PATH = os.path.expanduser("~/mysite_dashboard/backend/engagement_state.json")
LAST_VIDEO_ID_PATH = os.path.expanduser("~/mysite_dashboard/last_posted_video_id.txt")

# Optional (if you want to try real API later)
TIKTOK_API_TOKEN = os.environ.get("TIKTOK_API_TOKEN", "")
CREATOR_USER_ID = os.environ.get("TIKTOK_USER_ID", "")  # your account’s numeric ID if needed

# Short, varied replies (randomized so it feels natural)
REPLY_TEMPLATES = [
    "Appreciate you! 🙌",
    "Thanks for the love! 🔥",
    "Great question — new video soon! ✨",
    "You’re awesome — thanks for watching! 🙏",
    "Facts 😎",
    "Much love! 🚀"
]

POSITIVE_KEYWORDS = {"love", "cool", "fire", "🔥", "nice", "great", "wow", "amazing", "helpful"}
QUESTION_MARK_WEIGHT = 0.85  # higher chance to reply if comment has a question


def utc_now_str():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z")


def load_state():
    if os.path.exists(STATE_PATH):
        try:
            with open(STATE_PATH, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {"replied_comment_ids": [], "liked_comment_ids": [], "pinned_comment_ids": []}


def save_state(state):
    tmp = STATE_PATH + ".tmp"
    with open(tmp, "w") as f:
        json.dump(state, f)
    os.replace(tmp, STATE_PATH)


def read_last_video_id():
    if not os.path.exists(LAST_VIDEO_ID_PATH):
        print(f"[ENGAGE] No last_posted_video_id.txt found. Nothing to engage with.")
        return None
    with open(LAST_VIDEO_ID_PATH, "r") as f:
        vid = f.read().strip()
    if not vid:
        print(f"[ENGAGE] last_posted_video_id.txt is empty.")
        return None
    return vid


# ------- TikTok API hooks (safe stubs right now) -------
# If/when you’re ready to go live, replace stubs with real TikTokApi calls.

def fetch_recent_comments_stub(video_id, limit=50):
    """
    Stub: returns mock comments for dry-run demonstration.
    Replace with TikTokApi call when ready (and set DRY_RUN=False).
    """
    # minimal fake comments to show behavior
    sample = [
        {"id": "c1", "user_id": "u7", "text": "Love this 🔥", "ts": "2025-08-31T15:00:00Z"},
        {"id": "c2", "user_id": "u8", "text": "When’s part 2?", "ts": "2025-08-31T15:05:00Z"},
        {"id": "c3", "user_id": "u9", "text": "Nice tips 🙌", "ts": "2025-08-31T15:06:00Z"},
    ]
    return sample[:limit]


def like_comment(video_id, comment_id):
    if DRY_RUN:
        print(f"[DRY-RUN] would LIKE comment {comment_id} on video {video_id}")
        return True
    # TODO: Replace with real API call
    return True


def reply_to_comment(video_id, comment_id, text):
    if DRY_RUN:
        print(f"[DRY-RUN] would REPLY to {comment_id} on video {video_id}: {text}")
        return True
    # TODO: Replace with real API call
    return True


def pin_comment(video_id, comment_id):
    if DRY_RUN:
        print(f"[DRY-RUN] would PIN comment {comment_id} on video {video_id}")
        return True
    # TODO: Replace with real API call
    return True


# ------- Decision logic -------

def should_like(text):
    text_l = text.lower()
    hit = any(k in text_l for k in POSITIVE_KEYWORDS)
    # small random chance to like anyway
    return hit or random.random() < 0.25


def should_reply(text):
    text_l = text.lower()
    has_q = "?" in text_l
    positive = any(k in text_l for k in POSITIVE_KEYWORDS)
    base = 0.2
    p = base + (QUESTION_MARK_WEIGHT if has_q else 0) + (0.2 if positive else 0)
    p = min(p, 0.95)
    return random.random() < p


def choose_reply():
    return random.choice(REPLY_TEMPLATES)


def maybe_sleep():
    time.sleep(random.randint(*SLEEP_BETWEEN_ACTIONS_SEC))


def main():
    print("--------------------------------------------")
    print(f"[ENGAGE] Starting engagement run @ {utc_now_str()}")

    video_id = read_last_video_id()
    if not video_id:
        print(f"[ENGAGE] Done (no target video).")
        return

    # Load state so we never re-like or re-reply to same comment id
    state = load_state()
    replied = set(state.get("replied_comment_ids", []))
    liked = set(state.get("liked_comment_ids", []))
    pinned = set(state.get("pinned_comment_ids", []))

    comments = fetch_recent_comments_stub(video_id, limit=50)

    replies_done = 0
    likes_done = 0
    pinned_done = False

    for c in comments:
        cid = c["id"]
        ctext = c.get("text", "")

        # LIKE
        if cid not in liked and likes_done < MAX_LIKES_PER_RUN and should_like(ctext):
            if like_comment(video_id, cid):
                liked.add(cid)
                likes_done += 1
                maybe_sleep()

        # REPLY
        if cid not in replied and replies_done < MAX_REPLIES_PER_RUN and should_reply(ctext):
            msg = choose_reply()
            if reply_to_comment(video_id, cid, msg):
                replied.add(cid)
                replies_done += 1
                maybe_sleep()

        # PIN one good comment
        if not pinned_done and not pinned and ( "love" in ctext.lower() or "🔥" in ctext ):
            if pin_comment(video_id, cid):
                pinned.add(cid)
                pinned_done = True
                maybe_sleep()

    # Save state
    state["replied_comment_ids"] = list(replied)
    state["liked_comment_ids"] = list(liked)
    state["pinned_comment_ids"] = list(pinned)
    save_state(state)

    print(f"[ENGAGE] Finished engagement run @ {utc_now_str()} | likes={likes_done}, replies={replies_done}, pinned={pinned_done}")


if __name__ == "__main__":
    main()
