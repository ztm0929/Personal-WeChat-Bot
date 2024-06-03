import feedparser
from datetime import datetime, timedelta
import os
import logging

RSS_URL = "http://localhost:4000/feeds/all.atom"
LOG_FILE_PATH = os.path.join('logs', 'last_push_time.txt')
TIMEZONE_OFFSET = timedelta(hours=8)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_rss_content(rss_url):
    try:
        return feedparser.parse(rss_url)
    except Exception as e:
        logging.error(f"Failed to fetch RSS content: {e}")
        return None

def filter_new_content(entries, last_push_time):
    new_entries = []
    for entry in entries:
        try:
            published_time = datetime.strptime(entry.updated, "%Y-%m-%dT%H:%M:%S.%fZ") + TIMEZONE_OFFSET
            if published_time > last_push_time:
                new_entries.append(entry)
        except ValueError as e:
            logging.warning(f"Failed to parse date for entry {entry.id}: {e}")
    return new_entries

def get_last_push_time():
    try:
        with open(LOG_FILE_PATH, 'r') as f:
            return datetime.fromisoformat(f.read().strip())
    except FileNotFoundError:
        logging.info("Last push time file not found. Assuming no previous pushes.")
        return datetime.now() - timedelta(days=1)
    except Exception as e:
        logging.error(f"Error reading last push time: {e}")
        return datetime.now() - timedelta(days=1)

def set_last_push_time(push_time):
    os.makedirs('logs', exist_ok=True)
    try:
        with open(LOG_FILE_PATH, 'w') as f:
            f.write(push_time.isoformat())
    except Exception as e:
        logging.error(f"Error writing last push time: {e}")

def generate_message(entries):
    messages = []
    for i, entry in enumerate(entries, start=1):
        published_time = datetime.strptime(entry.updated, "%Y-%m-%dT%H:%M:%S.%fZ") + TIMEZONE_OFFSET
        # message = (
        #     f"# {i}\n"
        #     f"Title: {entry.title}\n"
        #     f"Link: {entry.link}\n"
        #     f"Published: {published_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        #     f"Author: {entry.author}\n"
        #     "------"
        # )
        message = (
            f"{entry.title}\n"
            f"#{entry.author}\n"
            "------"
        )
        messages.append(message)
    return "\n".join(messages)

def push_updates():
    last_push_time = get_last_push_time()
    current_time = datetime.now()
    
    rss_content = fetch_rss_content(RSS_URL)
    if rss_content is None:
        return

    new_entries = filter_new_content(rss_content.entries, last_push_time)
    
    if new_entries:
        logging.info(f"发现 {len(new_entries)} 条新内容，开始推送...")
        message = generate_message(new_entries)
        set_last_push_time(current_time)
        return message
    else:
        logging.info("没有发现新内容，无需推送。")
        return "没有发现新内容，无需推送。"

# Example usage:
if __name__ == "__main__":
    message = push_updates()
    if message:
        print(message)
