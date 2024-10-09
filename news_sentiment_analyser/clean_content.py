'''Cleaning HTML content'''
from bs4 import BeautifulSoup
import re


def clean_html_tags(html_text: str) -> str:
    '''Returns text with HTML tags removed'''
    soup = BeautifulSoup(html_text, "html.parser")

    for a_tag in soup.find_all('a'):
        strong_tag = a_tag.find('strong')
        if strong_tag:
            a_tag.decompose()

    return soup.get_text()


def clean_multiple_spaces(text: str) -> str:
    '''Returns text multiple spaces removed'''
    return re.sub(r'\s+', ' ', text)


def clean_ads(article_content: str) -> str:
    '''Returns article content with HTML Hyperlink text removed.'''


if __name__ == "__main__":
    ...
