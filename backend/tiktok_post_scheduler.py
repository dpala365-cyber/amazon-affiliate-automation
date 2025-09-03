#!/usr/bin/env python3
import time
from datetime import datetime, timedelta, timezone
import subprocess
import os

# -------------------------------
# CONFIGURATION
# -------------------------------
DAILY_RUNNER_PATH = os.path.expanduser("~/mysite_dashboard/daily_runner.sh")
LOG_FILE = os.path.expanduser("~/mysite_dashboard/cleanup.log")
PEAK_HOUR_FILE = os.path.expanduser("~/mysite_dashboard/current_peak_hour.txt")

ENGAGEMENT_DELAY_MINUTES = 15
WEEKLY_ANALYTICS_DAY = 6  # Sunday

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
    try:
        subprocess.run(cmd, shell=True, check=True)
        log(f"[DONE] {description}")
    except subprocess.CalledProcessError as e:
        log(f"[ERROR] {description}: {e}")

def get_peak_hour():
    try:
        with open(PEAK_HOUR_FILE, "r") as f:
            return int(f.read().strip())
    except:
        return 14  # fallback default

def get_next_peak_time():
    peak_hour_utc = get_peak_hour()
    now = datetime.now(timezone.utc)
    next_run = now.replace(hour=peak_hour_utc, minute=0, second=0, microsecond=0)
    if now >= next_run:
        next_run += timedelta(days=1)
    return next_run

# -------------------------------
# DAILY SCHEDULER LOOP
# -------------------------------
log("[SCHEDULER] Starting daily scheduler...")

while True:
    now = datetime.now(timezone.utc)
    next_run = get_next_peak_time()
    wait_seconds = (next_run - now).total_seconds()

    log(f"[SCHEDULER] Current UTC time: {now}")
    log(f"[SCHEDULER] Next daily runner scheduled at: {next_run}")
    log(f"[SCHEDULER] Waiting {int(wait_seconds)} seconds until next run...")

    time.sleep(wait_seconds)

    # Run daily runner
    run_command(DAILY_RUNNER_PATH, description="Daily runner (TikTok post + basic tasks)")

    # Wait and run smart engagement bot
    log(f"[SCHEDULER] Waiting {ENGAGEMENT_DELAY_MINUTES} minutes before engagement bot...")
    time.sleep(ENGAGEMENT_DELAY_MINUTES * 60)
    if os.path.exists(os.path.expanduser("~/mysite_dashboard/backend/engagement_smart_bot.py")):
        run_command("python3 ~/mysite_dashboard/backend/engagement_smart_bot.py", description="Smart engagement bot")
    else:
        log("[WARN] Smart engagement bot not found. Skipping...")

    # Weekly analytics (only on specified day)
    if datetime.now(timezone.utc).weekday() == WEEKLY_ANALYTICS_DAY:
        if os.path.exists(os.path.expanduser("~/mysite_dashboard/backend/weekly_analytics_update.py")):
            run_command("python3 ~/mysite_dashboard/backend/weekly_analytics_update.py", description="Weekly analytics update")
        else:
            log("[WARN] Weekly analytics script not found. Skipping...")

    log("[SCHEDULER] Daily run completed. Waiting for next scheduled time...\n")
