#!/bin/bash
set -e

# Get today's date in UTC
export TODAY=$(date -u "+%Y-%m-%d")

# Set default environment variables if not already set
export LANGUAGE=${LANGUAGE:-"English"}
export CATEGORIES=${CATEGORIES:-"cs.CV,cs.CL"}
export MODEL_NAME=${MODEL_NAME:-"deepseek-chat"}

# Ensure required environment variables are set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "Error: OPENAI_API_KEY is not set"
    exit 1
fi

if [ -z "$OPENAI_BASE_URL" ]; then
    echo "Error: OPENAI_BASE_URL is not set"
    exit 1
fi

# Create data directory if it doesn't exist
mkdir -p ../data

# Run the spider
cd daily_arxiv
scrapy crawl arxiv

# Run the AI enhancement
cd ../ai
python enhance.py --data ../data/${TODAY}.jsonl

# Convert to markdown
cd ../to_md
python convert.py --data ../data/${TODAY}_AI_enhanced_${LANGUAGE}.jsonl

# Update the README
cd ..
python update_readme.py
