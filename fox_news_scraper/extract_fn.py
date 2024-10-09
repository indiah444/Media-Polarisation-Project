"""A file to extract information from various Fox News RSS feeds."""

import feedparser
import requests
from bs4 import BeautifulSoup


def fetch_rss_feed(feed_url):
    """Fetches and parsers the RSS feed from the provided URL."""

    feed = feedparser.parse(feed_url)
    return feed


def get_article_content(article_url):
    """Scrapes the full content of an article from a given URL."""

    try:
        response = requests.get(article_url, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")

        article_body = soup.find("div", class_="article-body")
        if article_body:
            return article_body.get_text(separator=" ", strip=True)
        else:
            return "Full content not found or unable to parse."

    except Exception as e:
        return f"Failed to fetch full content from {article_url}: {e}"


def parse_feed_entries(feed):
    """Parses the entries of a feed and extracts relevant fields."""

    entries = []
    for entry in feed.entries:
        content = get_article_content(entry.link)

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
