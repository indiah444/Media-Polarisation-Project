"""A file to extract information from various Fox News RSS feeds."""

import grequests
import feedparser
import requests
from bs4 import BeautifulSoup


def fetch_rss_feed(feed_url: str) -> feedparser.FeedParserDict:
    """Fetches and parsers the RSS feed from the provided URL."""

    feed = feedparser.parse(feed_url)
    return feed


def get_headline_title(div) -> str:
    """Return title of headline given the headline div"""

    title_tag = div.find("h2")
    return title_tag.get_text(strip=True)


def get_headline_contents(div) -> str:
    """Return content of headline given the headline div"""

    content_tags = div.find_all("p")
    return '\n'.join([x.get_text(strip=True) for x in content_tags])


def scrape_headlines(response) -> dict | str:
    """
    Get the titles and content of headlines 
    from the Democracy Now headlines page
    """

    try:
        soup = BeautifulSoup(response.content, "html.parser")
        headline_divs = soup.find_all("div", class_="headline")

        headlines = []
        for div in headline_divs:
            title = get_headline_title(div)
            content = get_headline_contents(div)
            headlines.append({"title": title, "content": content})

        return headlines if headlines else "No headlines found"

    except Exception as e:
        return f"Failed to fetch content from {response.url}: {e}"


def get_article_title(soup) -> str:
    """Return title of headline given the headline div"""

    title_tag = soup.find("h1", class_="article__title")
    return title_tag.get_text(strip=True)


def get_article_contents(soup) -> str:
    """Return content of headline given the headline div"""

    article_body = soup.find("div", class_="article__body")
    if not article_body:
        return "No Content Found"

    paragraphs = article_body.find_all("p")
    return "\n".join([p.get_text(strip=True) for p in paragraphs])


def scrape_article(response: str) -> dict | str:
    """
    Get the title and main content of an article 
    from Democracy Now article page.
    """

    try:
        soup = BeautifulSoup(response.content, "html.parser")
        title = get_article_title(soup)
        content = get_article_contents(soup)

        return {"title": title, "content": content}

    except Exception as e:

        return f"Failed to fetch content from {response.url}: {e}"


def fetch_article_responses(feed_entries: list) -> list:
    """Fetches article responses asynchronously using grequests."""

    article_requests = (grequests.get(entry.link) for entry in feed_entries)
    return grequests.map(article_requests)


def process_headlines_entry(entry, response) -> list[dict] | str:
    """Processes a headline entry and extracts its contents."""

    page_link = entry.link
    scraping_result = scrape_headlines(response)

    if isinstance(scraping_result, list):
        return [{"title": res["title"], "content": res["content"],
                 "link": page_link, "published": entry.published}
                for res in scraping_result]
    else:
        return scraping_result


def process_article_entry(entry, response) -> dict | str:
    """Processes an article entry and extracts its contents."""

    content = scrape_article(response)

    if isinstance(content, dict):
        return {"title": entry.title, "content": content["content"],
                "link": entry.link, "published": entry.published}
    else:
        return content


def handle_response(entry, response) -> list[dict] | None:
    """Handles the response based on its status and content type."""

    if response.status_code != 200:
        print(f"Error code {response.status_code} for {entry.link}")
        return None

    if '/headlines' in entry.link:
        return process_headlines_entry(entry, response)
    else:
        return [process_article_entry(entry, response)]


def parse_feed_entries(feed: feedparser.FeedParserDict) -> list[dict]:
    """Parses the entries of a feed and extracts relevant fields."""

    entries = []
    responses = fetch_article_responses(feed.entries)

    for entry, response in zip(feed.entries, responses):
        processed_entries = handle_response(entry, response)

        if processed_entries is None:
            continue
        elif isinstance(processed_entries, list):
            entries.extend(processed_entries)
        else:
            print(processed_entries)

    return entries


def fetch_from_multiple_feeds(feed_urls: list[str]) -> list[dict]:
    """Fetches and parses entries from multiple RSS feeds."""

    all_entries = []
    for url in feed_urls:
        feed = fetch_rss_feed(url)
        entries = parse_feed_entries(feed)
        all_entries.extend(entries)

    return all_entries


if __name__ == "__main__":

    urls = ["https://www.democracynow.org/democracynow.rss"]
    for res in fetch_from_multiple_feeds(urls):
        print(res)
