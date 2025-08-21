# Script to run main pipeline(download and create posts)

# Create logs directory
mkdir -p logs/main

# Generate timestamp once
TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)
LOGFILE="logs/main/${TIMESTAMP}.log"

# Write start time to log
date > "$LOGFILE"

# Run main.py and append all output to the same log file
venv/bin/python3 main.py >> "$LOGFILE" 2>&1
