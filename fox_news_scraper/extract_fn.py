"""A file to extract information from various Fox News RSS feeds."""

import feedparser
import grequests
import requests
from bs4 import BeautifulSoup


def fetch_rss_feed(feed_url: str) -> feedparser.FeedParserDict:
    """Fetches and parsers the RSS feed from the provided URL."""

    feed = feedparser.parse(feed_url)
    return feed


def get_article_content(article_url: str) -> str:
    """Scrapes the full content of an article from a given URL."""

    try:
        response = requests.get(article_url, timeout=10)
        if response.status_code != 200:
            return f"Couldn't connect to article, status_code: {response.status_code}"

        soup = BeautifulSoup(response.content, "html.parser")
        article_body = soup.find("div", class_="article-body")

        if article_body:
            return article_body.get_text(separator=" ", strip=True)

        return "Full content not found or unable to parse."

    except Exception as e:
        return f"Failed to fetch full content from {article_url}: {e}"


def parse_feed_entries(feed: feedparser.FeedParserDict) -> list[dict]:
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


def fetch_from_multiple_feeds(feed_urls: list[str]) -> list[dict]:
    """Fetches and parses entries from multiple RSS feeds."""

    async_list = []
    for url in feed_urls:
        action_item = grequests.get(url)
        async_list.append(action_item)

    responses = grequests.map(async_list)

    all_entries = []
    for response in responses:
        if response and response.status_code == 200:
            feed = feedparser.parse(response.content)
            entries = parse_feed_entries(feed)
            all_entries.extend(entries)
        else:
            print(f"Failed to fetch feed from {url}, status_code: {
                  response.status_code if response else "No response"}")

    return all_entries


if __name__ == "__main__":

    test_feed = fetch_rss_feed(
        "https://moxie.foxnews.com/google-publisher/politics.xml")
    test_feed_urls = [
        "https://moxie.foxnews.com/google-publisher/politics.xml",
        "https://moxie.foxnews.com/google-publisher/world.xml",
        "https://moxie.foxnews.com/google-publisher/science.xml"
    ]

    test_extract = parse_feed_entries(test_feed)
    test_extract_multiple_feeds = fetch_from_multiple_feeds(test_feed_urls)

    print(test_extract)
    print(test_extract_multiple_feeds)
