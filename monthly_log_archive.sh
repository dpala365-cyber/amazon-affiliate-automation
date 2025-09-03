#!/bin/bash
ARCHIVE_DIR=~/mysite_dashboard/log_archive
mkdir -p "$ARCHIVE_DIR"
TIMESTAMP=$(date +"%Y-%m-%d")
cp ~/mysite_dashboard/cleanup.log "$ARCHIVE_DIR/cleanup_$TIMESTAMP.log"
> ~/mysite_dashboard/cleanup.log
echo "Archived cleanup.log for $TIMESTAMP"
