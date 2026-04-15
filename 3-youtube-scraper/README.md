# YouTube Channel Scraper

A Python script that scrapes video data from a YouTube channel using Selenium and BeautifulSoup.

## Output Example
```
Channel: Abdul waheed - YouTube
Total Videos: 6

Video #1: Intro to Python | L-1
    URL   : https://www.youtube.com/watch?v=AE6s_VLOUVs
    Views : 116 views
    Age   : 1 month ago
    Date  : Feb 20, 2026
    Likes : 14
```

## Requirements
```
selenium
beautifulsoup4
```
Install with:
```bash
pip install selenium beautifulsoup4
```

You also need **ChromeDriver** matching your Chrome version:
- Download from: https://chromedriver.chromium.org/downloads

## Usage
1. Set your channel URL in `CHANNEL_URL` at the top of `cleaner.py`
2. Run:
```bash
python cleaner.py
```

## How It Works
- Opens the YouTube channel videos page using Selenium
- Scrolls down to load all videos
- Loops through each video and collects:
  - Title
  - URL
  - Views
  - Relative age (e.g. "1 month ago")
  - Exact upload date (by clicking the description to trigger YouTube to render it)
  - Likes
