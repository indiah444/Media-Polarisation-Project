# pylint: skip-file

"""Tests the content cleaning methods"""

import pytest
from clean_content import clean_html_tags, clean_multiple_spaces, clean_content, remove_stop_phrases


def test_clean_content():
    test_content = """During the 20th century, human life expectancy at birth rose by about 30 years in high-income nations,the study noted, driven by advancements in public health"""
    assert clean_content(
        test_content) == "During the 20th century, human life expectancy at birth rose by about 30 years in high-income nations,the study noted, driven by advancements in public health"


@pytest.mark.parametrize("html, expected", [
    ("""We’ve seen over the past century that, in general,<a href="https: // www.vox.com/23150467/natural-disaster-climate-change-early-warning-hurricane-wildfire"> natural disasters are killing fewer people</a>.""",
     """We’ve seen over the past century that, in general, natural disasters are killing fewer people."""),
    ("", ""),
    (" ", " "),
])
def test_clean_html_tags(html, expected):
    '''Tests that html tags are cleaned as expected'''
    assert clean_html_tags(html) == expected


@pytest.mark.parametrize("html, expected", [
    ("""We’ve seen over the  past century that, in      general, natural disasters are killing fewer      people.""",
     """We’ve seen over the past century that, in general, natural disasters are killing fewer people."""),
    ("   ", " "),
    (" ", " ")
])
def test_clean_multiple_spaces(html, expected):
    '''Tests that html tags are cleaned as expected'''
    assert clean_multiple_spaces(html) == expected


@pytest.mark.parametrize("text, phrases, expected", [
    ("FOX News is covering the event.", [
     "fox news"], " is covering the event."),
    ("Democracy Now! is airing today.", [
     "democracy now!"], " is airing today."),
    ("Independent media.", [
     "fox news", "democracy now"], "Independent media."),
    ("Democracy Now! and Fox News are reporting.", [
     "fox news", "democracy now!"], " and  are reporting."),
    ("", ["fox news"], ""),
    ("a", [], "a")
])
def test_case_insensitivity(text, phrases, expected):
    assert remove_stop_phrases(text, phrases) == expected
