#!/bin/bash

# Directories
BASE_DIR="$HOME/mysite_dashboard"
BACKEND_DIR="$BASE_DIR/backend"
LOG_FILE="$BASE_DIR/cleanup.log"

# Function to log messages with timestamp
log() {
    echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') - $1" >> "$LOG_FILE"
}

# Infinite loop for continuous daily automation
while true; do
    log "--------------------------------------------"
    log "Starting daily TikTok automation and analytics check..."

    # Run weekly analytics (runs every Sunday)
    DAY_OF_WEEK=$(date -u '+%u')  # 1=Mon ... 7=Sun
    if [ "$DAY_OF_WEEK" -eq 7 ]; then
        log "Running weekly analytics update..."
        python3 "$BACKEND_DIR/weekly_analytics_update.py"
        log "Weekly analytics update finished"
    fi

    # Run TikTok post scheduler
    log "Running TikTok post scheduler..."
    python3 "$BACKEND_DIR/tiktok_post_scheduler.py"

    # Cleanup log files (optional: archive or rotate)
    log "Cleanup check finished"

    # Sleep for 1 hour before next check
    log "Next check in 1 hour..."
    sleep 3600
done
