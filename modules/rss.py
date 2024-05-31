import feedparser
from datetime import datetime, timedelta
import time
import schedule
import os

def fetch_rss_content(rss_url):
    return feedparser.parse(rss_url)

def filter_new_content(entries, last_push_time):
    new_entries = []
    for entry in entries:
        published_time = datetime.strptime(entry.updated, "%Y-%m-%dT%H:%M:%S.%fZ") + timedelta(hours=8)
        if published_time > last_push_time:
            new_entries.append(entry)
    return new_entries

def get_last_push_time():
    try:
        with open('logs/last_push_time.txt', 'r') as f:
            last_push_time = datetime.fromisoformat(f.read().strip())
    except FileNotFoundError:
        last_push_time = datetime.now() - timedelta(days=1)
    return last_push_time

def set_last_push_time(push_time):
    os.makedirs('logs', exist_ok=True)
    with open('logs/last_push_time.txt', 'w') as f:
        f.write(push_time.isoformat())

def push_updates():
    rss_url = "http://localhost:4000/feeds/all.atom"
    last_push_time = get_last_push_time()
    current_time = datetime.now()

    rss_content = fetch_rss_content(rss_url)
    new_entries = filter_new_content(rss_content.entries, last_push_time)

    if new_entries:
        messages = []
        print(f"发现 {len(new_entries)} 条新内容，开始推送...")
        for i, entry in enumerate(new_entries, start=1):
            published_time = datetime.strptime(entry.updated, "%Y-%m-%dT%H:%M:%S.%fZ") + timedelta(hours=8)
            message = (
                f"# {i}\n"
                f"Title: {entry.title}\n"
                f"Link: {entry.link}\n"
                f"Published: {published_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"Author: {entry.author}\n"
                "------"
            )
            messages.append(message)
        set_last_push_time(current_time)
        return "\n".join(messages)
    else:
        print("没有发现新内容，无需推送。")