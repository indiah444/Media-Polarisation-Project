'''Cleaning HTML content'''
from bs4 import BeautifulSoup
import re


def clean_html_tags(html_text: str) -> str:
    '''Returns text with HTML tags removed'''
    return BeautifulSoup(html_text, "html.parser").get_text()


def clean_multiple_spaces(text: str) -> str:
    '''Returns text multiple spaces removed'''
    return re.sub(r'\s+', ' ', text)


def clean_ads(article_content: str) -> str:
    '''Returns article content with HTML Hyperlink text removed.'''


if __name__ == "__main__":
    ...
