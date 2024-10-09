"""A file to extract information from various Fox News RSS feeds."""

from datetime import datetime, timedelta

import grequests
from bs4 import BeautifulSoup


def fetch_article_responses(links: list[str]) -> list:
    """Fetches article responses asynchronously using grequests."""

    article_requests = (grequests.get(x, timeout=30) for x in links)
    return grequests.map(article_requests)


def get_article_title(soup) -> str:
    """Return title of article given the web body"""

    title_tag = soup.find("h1", class_="article__title")
    if not title_tag:
        return None

    return title_tag.get_text(strip=True)


def get_article_contents(soup) -> str:
    """Return content of article given the web body"""

    article_body = soup.find("div", class_="article__body")
    if not article_body:
        return None

    paragraphs = article_body.find_all("p")
    if not paragraphs:
        return None

    return "\n".join([p.get_text(strip=True) for p in paragraphs])


def reformat_date(date: str):
    """change from american date to standard YYYY-MM-DD"""

    date_obj = datetime.strptime(date, "%B %d, %Y")

    return date_obj.strftime("%Y-%m-%d")


def get_article_date(soup) -> str:
    """Return date of article given the web body"""

    date = soup.find("span", class_="date")
    if not date:
        return None
    try:
        return reformat_date(date.get_text(strip=True))
    except ValueError:
        return None


def scrape_article(response: str) -> dict:
    """
    Get the title and main content of an article
    from Democracy Now article page.
    """

    try:
        soup = BeautifulSoup(response.content, "html.parser")
        title = get_article_title(soup)
        content = get_article_contents(soup)
        date = get_article_date(soup)

        return {"title": title, "content": content,
                "link:": response.url, "published": date}

    except Exception as e:

        return f"Failed to fetch content from {response.url}: {e}"


def get_all_topic_links() -> list[str]:
    """Return links to all topics on the Democracy Now topics A-Z page."""

    try:
        request = grequests.get("https://www.democracynow.org/topics/browse",
                                timeout=30)
        response = grequests.map([request])[0]
        if response is None:
            raise TypeError("Democracy now website not responding")

        soup = BeautifulSoup(response.content, "html.parser")
        topic_links = []
        link_container = soup.find_all("div", class_="container-fluid")[4]
        for li in link_container.find_all("li"):
            link = li.find("a")
            href = link.get("href")
            if href:
                topic_links.append(f"https://www.democracynow.org{href}")

        return topic_links

    except Exception as e:
        return f"Failed to fetch topic links: {e}"


def get_all_links_from_topic(topic_response: str) -> list[str]:
    """Return links for a given topic page on Democracy Now."""

    soup = BeautifulSoup(topic_response.content, "html.parser")
    articles = soup.find_all(
        "a", attrs={"data-ga-action": "Topic: Story Headline"})
    article_links = [
        f"https://www.democracynow.org{link.get('href')}" for link in articles if link.get("href")]
    return article_links


def get_all_links_from_all_topics() -> list[dict]:
    """Scrape through all news from every DN topic"""

    topic_links = get_all_topic_links()
    print(f"Found {len(topic_links)} topic links")
    if isinstance(topic_links, str):
        return []
    responses = [x for x in fetch_article_responses(topic_links)
                 if x is not None]
    all_article_links = []
    for i, response in enumerate(responses):
        if response is None:
            print(f"Could not connect to link: {topic_links[i]}")
        else:
            all_article_links.extend(get_all_links_from_topic(response))

    return all_article_links


def parse_all_links(all_links: list[str]) -> list[dict]:
    """Parses the contents of links listed."""

    articles = []
    responses = fetch_article_responses(all_links)

    for i, response in enumerate(responses):
        if response is None:
            print(f"Could not connect to url: {all_links[i]}")
        else:
            articles.append(scrape_article(response))
    return articles


def link_is_old(link: str, time_diff: int) -> bool:
    """
    Filter out link that are more than 1 week old.
    Expects links in the format 'https://www.democracynow.org/YYYY/M/D/...'.
    """

    one_week_ago = datetime.now() - timedelta(days=time_diff)

    try:
        date_str = '/'.join(link.split('/')[3:6])
        link_date = datetime.strptime(date_str, "%Y/%m/%d")

        if link_date >= one_week_ago:
            return False

    except ValueError as e:
        # print(f"Skipping invalid link: {link}, error: {e}")
        return True

    return True


def scrape_democracy_now():
    """Scrape the democracy now pages to obtain all stories"""

    all_links = get_all_links_from_all_topics()
    all_valid_links = [x for x in all_links if not link_is_old(x, 7)]
    print(f"Retreived {len(all_valid_links)} valid article links")
    results = parse_all_links(all_valid_links)
    print(f"Extracted title and content from {len(all_valid_links)} articles")
    return results


if __name__ == "__main__":

    print(scrape_democracy_now())
