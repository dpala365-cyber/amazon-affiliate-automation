#!/bin/bash
# Activate virtual environment
source ~/mysite_dashboard/venv/bin/activate

# Run the daily live posting script
python3 ~/mysite_dashboard/backend/full_daily_runner_live.py

# Run the engagement bot immediately after posting
python3 ~/mysite_dashboard/backend/tiktok_engagement_bot.py
