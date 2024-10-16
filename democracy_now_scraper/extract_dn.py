"""A file to webscrape article information from Democracy Now! A-Z Topics page."""

from datetime import datetime, timedelta

import grequests
from bs4 import BeautifulSoup


def fetch_response_html(response) -> BeautifulSoup:
    """Return html content of response"""

    return BeautifulSoup(response.content, "html.parser")


def chunk_links(links: list[str], chunk_size: int) -> list[list[str]]:
    """Split the list of links into smaller chunks."""

    return [links[i:i + chunk_size] for i in range(0, len(links), chunk_size)]


def fetch_article_responses(links: list[str]) -> list:
    """
    Fetches article responses asynchronously using 
    grequests in increments of 50.
    """

    responses = []
    link_chunks = chunk_links(links, 50)

    for chunk in link_chunks:
        article_requests = (grequests.get(x, timeout=30) for x in chunk)
        responses.extend(grequests.map(article_requests))

    return responses


def get_article_title(soup: BeautifulSoup) -> str:
    """Return title of article given the web body"""

    try:
        article_tag = soup.find(
            "div", class_="container-fluid", id="story_content")
        title_tag = article_tag.find("h1")
        return title_tag.get_text(strip=True)

    except AttributeError:
        return None


def get_headline_title(soup: BeautifulSoup) -> str:
    """Return title of article given the headline body"""

    try:
        article = soup.find("article", class_="headline")
        title_tag = article.find("h1")
        return title_tag.get_text(strip=True)

    except AttributeError:
        return None


def get_article_contents(soup: BeautifulSoup) -> str:
    """Return content of article given the web body"""

    try:
        story_summary = soup.find("div", class_="story_summary")
        paragraphs = story_summary.find_all("p")
        transcript = soup.find(
            "div", class_="mobile_anchor_target", id="transcript")
        paragraphs.extend(transcript.find_all("p"))
        return "\n".join([p.get_text(strip=True) for p in paragraphs])

    except AttributeError:
        return None


def get_headline_contents(soup: BeautifulSoup) -> str:
    """Return content of article given the headline body"""

    try:
        headline_summary = soup.find("div", class_="headline_summary")
        paragraphs = headline_summary.find_all("p")
        return "\n".join([p.get_text(strip=True) for p in paragraphs])

    except AttributeError:
        return None


def reformat_date(date: str) -> str:
    """
    Change from American date to standard YYYY-MM-DD.
    Expecting data in "October 07, 2024" or "Oct 07, 2024".
    """

    try:
        date_obj = datetime.strptime(date, "%B %d, %Y")
    except ValueError:
        try:
            date_obj = datetime.strptime(date, "%b %d, %Y")
        except ValueError:
            return None

    return date_obj.strftime("%Y-%m-%d")


def get_article_date(soup: BeautifulSoup) -> str:
    """Return date of article given the web body"""

    try:
        article_tag = soup.find(
            "div", class_="container-fluid", id="story_content")
        date = article_tag.find("span", class_="date")
        return reformat_date(date.get_text(strip=True))

    except AttributeError:
        return None


def get_headline_date(soup: BeautifulSoup) -> str:
    """Return date of article given the web body"""

    try:
        first_headline = soup.find("article", class_="headline")
        date = first_headline.find("span", class_="date")
        return reformat_date(date.get_text(strip=True))

    except AttributeError:
        return None


def scrape_article(response) -> dict:
    """
    Get the title, content and date of an article
    from Democracy Now article page.
    """

    soup = fetch_response_html(response)
    if '/headlines/' in response.url:
        title = get_headline_title(soup)
        content = get_headline_contents(soup)
        date = get_headline_date(soup)
    else:
        title = get_article_title(soup)
        content = get_article_contents(soup)
        date = get_article_date(soup)

    if any(x is None for x in (title, content, date)):
        return f"Failed to fetch content from {response.url}"

    return {"title": title, "content": content,
            "link": response.url, "published": date}


def get_all_topic_links() -> list[str]:
    """Return links to all topics on the Democracy Now topics A-Z page."""

    try:
        response = fetch_article_responses(
            ["https://www.democracynow.org/topics/browse"])[0]

        if response is None:
            print(
                'Democracy Now url "https://www.democracynow.org/topics/browse" not responding')
            return []

        soup = fetch_response_html(response)
        topic_links = []
        link_container = soup.find_all("div", class_="container-fluid")[4]
        for li in link_container.find_all("li"):
            link = li.find("a")
            href = link.get("href")
            if href:
                topic_links.append(f"https://www.democracynow.org{href}")

        return topic_links

    except Exception as e:  # pylint: disable=W0718
        print(f"Failed to fetch topic links: {e}")
        return []


def get_all_links_from_topic(topic_response) -> list[str]:
    """Return links for a given topic page on Democracy Now."""

    soup = fetch_response_html(topic_response)
    articles = soup.find_all(
        "a", attrs={"data-ga-action": "Topic: Story Headline"})
    article_links = [
        f"https://www.democracynow.org{link.get('href')}" for link in articles if link.get("href")]
    return article_links


def get_all_links_from_all_topics() -> list[str]:
    """Scrape through all news from every DN topic"""

    topic_links = get_all_topic_links()
    print(f"Found {len(topic_links)} topic links")
    if not topic_links:
        return []

    responses = fetch_article_responses(topic_links)
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
            article_info = scrape_article(response)
            if isinstance(article_info, str):
                print(article_info)
            else:
                articles.append(article_info)
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

    except ValueError:
        # very old links do not have date in the url and should be classified as old
        return True

    return True


def scrape_democracy_now(days_old: int) -> list[dict]:
    """Scrape the democracy now pages to obtain all stories"""

    all_links = get_all_links_from_all_topics()
    print(f"Retreived {len(all_links)} article links")
    all_valid_links = [
        x for x in all_links if not link_is_old(x, days_old)]
    print(
        f"{len(all_valid_links)} article links are within {days_old} days old")
    results = parse_all_links(all_valid_links)
    print(f"Extracted title and content from {len(results)} articles")
    return results


if __name__ == "__main__":
    print(scrape_democracy_now(3))
