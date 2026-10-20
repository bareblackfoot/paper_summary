#!/bin/bash

# Set working directory to script location
cd "$(dirname "$0")"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Set log file path
LOG_FILE="paper_collector.log"

# Run the paper collector and log output
echo "=== Paper Collection Started at $(date) ===" >> "$LOG_FILE"
python paper_collector.py >> "$LOG_FILE" 2>&1
echo "=== Paper Collection Finished at $(date) ===" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# Deactivate virtual environment if it was activated
if [ -n "$VIRTUAL_ENV" ]; then
    deactivate
fi 