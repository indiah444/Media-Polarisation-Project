"""A file to extract information from various Fox News RSS feeds."""

import feedparser


def fetch_rss_feed(feed_url):
    """Fetches and parsers the RSS feed from the provided URL."""

    feed = feedparser.parse(feed_url)
    return feed


def parse_feed_entries(feed):
    """Parses the entries of a feed and extracts relevant fields."""

    entries = []
    for entry in feed.entries:
        content = entry.get("content:encoded", entry.get(
            "description", "No content available."))
        entries.append({
            "title": entry.title,
            "content": content,
            "link": entry.link,
            "published": entry.published
        })

    return entries


def fetch_from_multiple_feeds(feed_urls):
    """Fetches and parses entries from multiple RSS feeds."""

    all_entries = []
    for url in feed_urls:
        feed = fetch_rss_feed(url)
        entries = parse_feed_entries(feed)
        all_entries.extend(entries)

    return all_entries


if __name__ == "__main__":

    test_fn = fetch_rss_feed(
        "https://moxie.foxnews.com/google-publisher/politics.xml")

    test_extract = parse_feed_entries(test_fn)

    print(test_extract)
