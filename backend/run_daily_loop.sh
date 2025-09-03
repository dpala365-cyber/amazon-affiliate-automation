#!/bin/bash

# Navigate to project directory
cd ~/mysite_dashboard

# Activate virtual environment
source venv/bin/activate

# Log file
LOGFILE=cleanup.log

# Print start time
echo "--------------------------------------------" >> $LOGFILE
echo "Daily runner started: $(date -u)" >> $LOGFILE

# Run TikTok post scheduler
python3 backend/tiktok_post_scheduler.py >> $LOGFILE 2>&1

# Run weekly analytics update
python3 backend/weekly_analytics_update.py >> $LOGFILE 2>&1

# Print end time
echo "Daily runner finished: $(date -u)" >> $LOGFILE
echo "--------------------------------------------" >> $LOGFILE
