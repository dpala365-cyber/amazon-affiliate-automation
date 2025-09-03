#!/bin/bash
# daily_runner.sh
# Run multiple TikTok posts in one day from a single scheduled job

echo "=== TikTok Daily Runner Started ==="

# Run immediately at 23:00 UTC (≈ 7pm US Eastern, 4pm US Pacific)
python3 /home/dav25/mysite_dashboard/post_video.py --time "23:00"

# Sleep 4 hours → run at 03:00 UTC (≈ 11pm US Eastern, 8pm US Pacific)
sleep 14400
python3 /home/dav25/mysite_dashboard/post_video.py --time "03:00"

# Sleep 5 hours → run at 08:00 UTC (≈ 4am US Eastern, 1am US Pacific)
sleep 18000
python3 /home/dav25/mysite_dashboard/post_video.py --time "08:00"

# Sleep 6 hours → run at 14:00 UTC (≈ 10am US Eastern, 7am US Pacific)
sleep 21600
python3 /home/dav25/mysite_dashboard/post_video.py --time "14:00"

# Sleep 6 hours → run at 20:00 UTC (≈ 4pm US Eastern, 1pm US Pacific)
sleep 21600
python3 /home/dav25/mysite_dashboard/post_video.py --time "20:00"

echo "=== TikTok Daily Runner Finished ==="
