# Script to run upload_post.py

# Create logs directory
mkdir -p logs/upload

# Generate timestamp once
TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)
LOGFILE="logs/upload/${TIMESTAMP}.log"

# Write start time to log
date > "$LOGFILE"

# Run upload_post.py and append all output to the same log file
venv/bin/python3 upload_post.py >> "$LOGFILE" 2>&1
