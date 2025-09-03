#!/bin/bash
LOGFILE=~/cleanup.log

{
echo "--------------------------------------------"
echo "Starting LIGHTWEIGHT daily cleanup: $(date)"

# Delete Python cache files
find ~ -name "*.pyc" -type f -delete

# Remove __pycache__ directories
find ~ -type d -name "__pycache__" -exec rm -rf {} +

# Clear pip cache
rm -rf ~/.cache/pip
rm -rf ~/.cache/*

# Remove large log files (>5MB only)
find ~ -name "*.log" -type f -size +5M -delete

# Remove IPython history
rm -rf ~/.ipython/profile_default/history.sqlite

echo "Disk usage after lightweight cleanup:"
du -h --max-depth=1 ~ | sort -hr

echo "Lightweight daily cleanup done: $(date)"
echo "--------------------------------------------"
} >> $LOGFILE 2>&1
