# pylint: skip-file
"""Tests for clean_fn.py"""
import pytest
from unittest.mock import patch
from clean_fn import clean_text, clean_multiple_spaces, remove_stopwords, remove_urls


def test_clean_text_empty():
    """Checks that clean text works with an empty input."""

    assert clean_text("") == ""


@pytest.mark.parametrize(
    "text, expected", [
        ("http://", ""),
        ("link http://", "link"),
        ("http:// link", "link"),
        ("Here is a URL: https://example.com", "Here is a URL:"),
        ("No URL here", "No URL here")
    ]
)
def test_remove_urls(text, expected):
    """Checks that URLs are removed."""

    assert remove_urls(text).strip() == expected


@pytest.mark.parametrize(
    "text, expected", [
        ("hello world", "hello world"),
        ("hello world, and", "hello world,"),
        ("abcdef is a set of letters", "abcdef set letters"),
        ("This is a test sentence with stopwords", "test sentence stopwords")
    ]
)
def test_remove_stopwords(text, expected):
    """Checks that stopwords are removed."""

    assert remove_stopwords(text) == expected


@pytest.mark.parametrize("text, expected", [
    ("""We’ve seen over the  past century that, in      general, natural disasters are killing fewer      people.""",
     """We’ve seen over the past century that, in general, natural disasters are killing fewer people."""),
])
def test_clean_multiple_spaces(text, expected):
    """Tests that multiple spaces are cleaned as expected."""

    assert clean_multiple_spaces(text) == expected


@pytest.mark.parametrize(
    "text, expected", [
        ("Arizona began early voting https://link.com", "arizona began early voting"),
        ("This sentence has stopwords and https://example.com", "sentence stopwords"),
        ("Multiple   spaces    here  and    https://test.com", "multiple spaces"),
    ]
)
def test_clean_text(text, expected):
    """Tests that clean_text applies all the cleaning steps."""

    assert clean_text(text) == expected
