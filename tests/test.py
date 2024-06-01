import feedparser

rss_url = 'http://localhost:4000/feeds/all.atom'

rss_content = feedparser.parse(rss_url)

for i, entry in enumerate(rss_content.entries):
    print(f"{i + 1}、{entry.title}")