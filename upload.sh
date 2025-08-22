#!/bin/zsh
# Script to run upload_post.py

# Random sleep interval between 0 and 5 hours
SECONDS=0
sleep $(( $RANDOM % 18001 ))

# Create logs directory
mkdir -p logs/upload

# Generate timestamp once
TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)
LOGFILE="logs/upload/${TIMESTAMP}.log"

# Write start time to log
date > "$LOGFILE"

# Convert seconds into H:M:S
HOURS=$(( SECONDS / 3600 ))
MINUTES=$(( (SECONDS % 3600) / 60 ))
SECONDS=$(( SECONDS % 60 ))
printf "Slept for %02dh %02dm %02ds\n" "$HOURS" "$MINUTES" "$SECONDS" >> "$LOGFILE"

# Run upload_post.py and append all output to the same log file
venv/bin/python3 upload_post.py >> "$LOGFILE" 2>&1
