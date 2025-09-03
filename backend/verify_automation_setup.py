#!/usr/bin/env python3
import os

# --- Paths ---
backend_folder = "/home/dav25/mysite_dashboard/backend"
required_scripts = [
    "run_daily_loop.sh",
    "tiktok_post_scheduler.py",
    "morning_status.sh",
    "monthly_log_archive.sh",
    "monthly_aggressive_cleanup.sh",
    "auto_cleanup.sh"
]
videos_folder = os.path.join(backend_folder, "videos")
videos_json = os.path.join(backend_folder, "videos.json")
posted_folder = os.path.join(backend_folder, "posted")
logs_folder = os.path.join(backend_folder, "logs")

# --- Verify scripts ---
print("🔹 Checking automation scripts...")
for script in required_scripts:
    path = os.path.join(backend_folder, script)
    if os.path.exists(path):
        print(f"✅ {script} exists")
    else:
        print(f"❌ {script} MISSING")

# --- Verify videos.json ---
print("\n🔹 Checking videos.json...")
if os.path.exists(videos_json):
    print(f"✅ videos.json exists")
else:
    print(f"❌ videos.json MISSING")

# --- Verify videos folder ---
print("\n🔹 Checking videos folder...")
if os.path.exists(videos_folder):
    files = [f for f in os.listdir(videos_folder) if f.endswith(('.mp4', '.mov', '.avi'))]
    if files:
        print(f"✅ {len(files)} video(s) found: {files}")
    else:
        print("❌ No videos found in videos folder")
else:
    print("❌ Videos folder missing")

# --- Verify posted folder ---
print("\n🔹 Checking posted folder...")
if os.path.exists(posted_folder):
    print(f"✅ Posted folder exists")
else:
    print("❌ Posted folder missing")

# --- Verify logs folder ---
print("\n🔹 Checking logs folder...")
if os.path.exists(logs_folder):
    print(f"✅ Logs folder exists")
else:
    print("❌ Logs folder missing")
