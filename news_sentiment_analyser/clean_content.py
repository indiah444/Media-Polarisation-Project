"""Cleaning HTML content"""

import re

from bs4 import BeautifulSoup

STOP_PHRASES = ["fox news", "democracy now", "democracy now!"]


def clean_html_tags(html_text: str) -> str:
    """Returns text with HTML tags removed"""
    soup = BeautifulSoup(html_text, "html.parser")

    for a_tag in soup.find_all('a'):
        strong_tag = a_tag.find('strong')
        if strong_tag:
            a_tag.decompose()

    return soup.get_text()


def clean_multiple_spaces(text: str) -> str:
    """Returns text multiple spaces removed"""
    return re.sub(r'\s+', ' ', text)


def remove_stop_phrases(text: str, phrases: list[str]) -> str:
    """Remove any matched stop phrases from the text, ignoring case"""
    pattern = re.compile('|'.join(re.escape(phrase)
                         for phrase in phrases), re.IGNORECASE)
    return pattern.sub('', text)


def clean_content(content: str):
    """Cleans HTML content including removal of ads and handling the extra
    whitespace."""
    content = clean_multiple_spaces(content)
    return remove_stop_phrases(content, STOP_PHRASES)
