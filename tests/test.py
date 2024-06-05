import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import re
import time
import feedparser
import logging
from datetime import timedelta
from wcferry import Wcf

# Load environment variables from .env file
load_dotenv()

# Initialize Wcf instance
wcf = Wcf()

# Constants
RSS_URL = "http://localhost:4000/feeds/all.atom"
LOG_FILE_PATH = os.path.join('logs', 'last_push_time.txt')
TIMEZONE_OFFSET = timedelta(hours=8)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_data_from_script(scripts):
    match_cdn, match_username, match_msg_desc = None, None, None
    for script in scripts:
        if 'var cdn_url_1_1' in script.text:
            match_cdn = re.search(r'var cdn_url_1_1 = "(.*)";', script.text)
        if 'var user_name' in script.text:
            match_username = re.search(r'var user_name = "(.*)";', script.text)
        if 'var msg_desc = htmlDecode' in script.text:
            match_msg_desc = re.search(r'var msg_desc = htmlDecode\("(.*)"\);', script.text)
        if match_cdn and match_username and match_msg_desc:
            break
    return match_cdn, match_username, match_msg_desc

def send_rich_text(entry):
    url = entry['link']
    max_retries = 3
    match_cdn, match_username, match_msg_desc = None, None, None

    for _ in range(max_retries):
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            scripts = soup.find_all('script')
            match_cdn, match_username, match_msg_desc = extract_data_from_script(scripts)
            if match_cdn and match_username and match_msg_desc:
                break
        except requests.exceptions.RequestException as e:
            logging.error(f"Error occurred when requesting URL: {e}")
            time.sleep(1)

    if match_cdn and match_username and match_msg_desc:
        cdn_url_1_1 = match_cdn.group(1)
        username = match_username.group(1)
        msg_desc = match_msg_desc.group(1)
        logging.info(f"CDN URL: {cdn_url_1_1}, Username: {username}, Message Description: {msg_desc}")
        try:
            wcf.send_rich_text(
                name=entry['author'],
                account=username,
                title=entry['title'],
                digest=msg_desc,
                url=url,
                thumburl=cdn_url_1_1,
                receiver=os.getenv("测试专用")
            )
        except Exception as e:
            logging.error(f"Error occurred when sending rich text: {e}")
    else:
        logging.error("Failed to extract necessary data from the script")

def send_text(entries):
    messages = []
    for entry in entries:
        messages.append(f"{entry['title']}\n#{entry['author']}\n------")
    message = "\n".join(messages)
    try:
        wcf.send_text(message, os.getenv("测试专用"), "")
    except Exception as e:
        logging.error(f"Error occurred when sending text: {e}")

def main():
    feed_entries = feedparser.parse(RSS_URL).entries
    entries = [{'title': entry.title, 'link': entry.link, 'author': entry.author} for entry in feed_entries]

    for entry in entries:
        logging.info(f"Processing entry: {entry['title']} - {entry['link']}")
        send_rich_text(entry)

    time.sleep(3)
    send_text(entries)

if __name__ == "__main__":
    main()
