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


def clean_content(content: str, is_html: bool):
    if is_html:
        content = clean_html_tags(content)
    return clean_multiple_spaces(content)


if __name__ == "__main__":
    ...
