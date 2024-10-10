"""Tests for clean_fn.py"""
import pytest
from unittest.mock import patch
from clean_fn import clean_text


def test_clean_text_empty():
    """Checks that clean text works with an empty input"""
    assert clean_text("") == ""


@pytest.mark.parametrize(
    "text, expected", [
        ("http://", ""),
        ("a http://", "a"),
        ("http:// b", "a")
    ]
)
def test_clean_text_http(text, expected):
    """Checks that hyperlink starts are removed"""
    assert clean_text(text) == expected
