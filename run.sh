#!/bin/bash
set -e

# Get today's date in UTC
export TODAY=$(date -u "+%Y-%m-%d")

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
