# pylint: skip-file
"""Tests the content cleaning methods"""

import pytest
from clean_content import clean_html_tags, clean_multiple_spaces, clean_content


def test_clean_content():
    test_content = """During the 20th century, human life expectancy at birth rose by about 30 years in high-income nations,the study noted, driven by advancements in <a href="https: // www.foxnews.com/health" target="_blank" rel="noopener">public health</a>.</p><p><a href="https: // www.foxnews.com/health/ultra-processed-foods-repercussions-childrens-health-nutritionist-warns" target="_blank" rel="noopener"><strong>ULTRA-PROCESSED FOODS MAKE UP 60% OF AMERICA'S DIET, WHO'S AT BIGGEST RISK</strong></a></p><p>"""
    assert clean_content(
        test_content, True) == "During the 20th century, human life expectancy at birth rose by about 30 years in high-income nations,the study noted, driven by advancements in public health."


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
