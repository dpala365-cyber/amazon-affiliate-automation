#!/bin/bash
LOGFILE=~/cleanup.log

{
echo "============================================"
echo "Starting AGGRESSIVE monthly cleanup: $(date)"

# Delete Python cache files
find ~ -name "*.pyc" -type f -delete

# Clear pip cache
rm -rf ~/.cache/pip
rm -rf ~/.cache/*

# Remove old backups safely
if [ -d ~/old_backup ]; then
    tar -czf ~/old_backup_backup_$(date +%F).tar.gz ~/old_backup
    find ~/old_backup -name ".nfs*" -type f -exec rm -f {} \; 2>/dev/null
    rm -rf ~/old_backup/*
fi

# Remove large log files (>1MB)
find ~ -name "*.log" -type f -size +1M -delete

# Remove __pycache__ directories
find ~ -type d -name "__pycache__" -exec rm -rf {} +

# Remove IPython history and checkpoints
rm -rf ~/.ipython/profile_default/history.sqlite
find ~/.ipython/ -type d -name ".ipynb_checkpoints" -exec rm -rf {} +

# Compress small text files
find ~ -maxdepth 1 -type f -name "*.txt" -exec gzip {} \;

echo "Disk usage after aggressive cleanup:"
du -h --max-depth=1 ~ | sort -hr

echo "Aggressive monthly cleanup done: $(date)"
echo "============================================"
} >> $LOGFILE 2>&1
