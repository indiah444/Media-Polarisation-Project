"""A file to extract information from various Fox News RSS feeds."""

import feedparser
import grequests
from bs4 import BeautifulSoup


def fetch_rss_feed(feed_url: str) -> feedparser.FeedParserDict:
    """Fetches and parsers the RSS feed from the provided URL."""

    feed = feedparser.parse(feed_url)
    return feed


def parse_article_content(response) -> str:
    """Parses the article content from the HTML response."""

    soup = BeautifulSoup(response.content, "html.parser")
    article_body = soup.find("div", class_="article-body")

    if article_body:
        content = article_body.get_text(separator=" ", strip=True)
        return content

    return "Full content not found or unable to parse."


def get_article_content(article_url: str) -> str:
    """Scrapes the full content of an article from a given URL."""

    try:
        response = grequests.get(article_url)
        if response.status_code != 200:
            return f"Couldn't connect to article, status_code: {response.status_code}"

        content = parse_article_content(response)
        return content

    except Exception as e:
        return f"Failed to fetch full content from {article_url}: {e}"


def parse_feed_entries(feed: feedparser.FeedParserDict) -> list[dict]:
    """Parses the entries of a feed and extracts relevant fields."""

    entries = []
    article_requests = (grequests.get(entry.link) for entry in feed.entries)

    responses = grequests.map(article_requests)

    for entry, response in zip(feed.entries, responses):
        if response and response.status_code == 200:
            content = parse_article_content(response)
        else:
            content = f"Couldn't connect to article, status_code: {
                response.status_code if response else "No response."}"

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
            print(f"Failed to fetch feed from {response.url if response else "No URL"}, status_code: {
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
