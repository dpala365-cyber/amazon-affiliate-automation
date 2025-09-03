#!/bin/bash

echo "===== Morning TikTok Automation Status ====="
echo "Date & Time: $(date -u) UTC"
echo

# Check if videos folder has any files
video_count=$(ls -1 ~/mysite_dashboard/videos/*.mp4 2>/dev/null | wc -l)
echo "Videos ready to post: $video_count"

# Check last post
last_post=$(tail -n 10 ~/mysite_dashboard/cleanup.log | grep "Daily TikTok post executed" | tail -n 1)
if [ -z "$last_post" ]; then
  echo "No TikTok posts have been executed yet."
else
  echo "Last TikTok post: $last_post"
fi

# Check peak hour
peak_hour=$(grep "Updated peak hour" ~/mysite_dashboard/cleanup.log | tail -n 1 | awk '{print $NF}')
echo "Current peak hour: $peak_hour UTC"

# Check if daily runner is running
runner_pid=$(pgrep -f run_daily_loop.sh)
if [ -z "$runner_pid" ]; then
  echo "Daily runner loop: NOT running"
else
  echo "Daily runner loop: RUNNING (PID: $runner_pid)"
fi

echo "==========================================="
