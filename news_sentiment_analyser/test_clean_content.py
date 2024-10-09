"""Tests the content cleaning methods"""
import pytest
from clean_content import clean_ads, clean_html_tags, clean_multiple_spaces


@pytest.mark.parametrize("html, expected", [
    ("""We’ve seen over the past century that, in general, <a href="https: // www.vox.com/23150467/natural-disaster-climate-change-early-warning-hurricane-wildfire">natural disasters are killing fewer people</a>.""",
     """We’ve seen over the past century that, in general, natural disasters are killing fewer people."""),
    ("", ""),
    (" ", " ")
])
def test_clean_html_tags(html, expected):
    '''Tests that html tags are cleaned as expected'''
    assert clean_html_tags(html) == expected


def test_clean_multiple_spaces():
    '''Tests that multiple spaces are replaced by a single space'''

    assert True
