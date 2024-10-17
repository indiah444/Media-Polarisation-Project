"""Testing streamlit pages."""

import pytest
from streamlit.testing.v1.app_test import AppTest


@pytest.mark.parametrize("file", [
    ("pages/2_About.py"),
    ("pages/3_Sentiment_Over_Time.py"),
    ("pages/4_Topic_Filter.py"),
    ("pages/6_Subscribe.py"),
    ("1_Home.py")

])
def test_page_runs(file):
    """Test that pages run without exception"""
    at = AppTest.from_file(file)
    at.run(timeout=10)
    assert not at.exception


def test_subscribe_elements_submission_page():
    at = AppTest.from_file("pages/6_Subscribe.py")
    at.run()
    assert at.button[0].label == "Submit"


def test_unsubscribe_elements_submission_page():
    at = AppTest.from_file("pages/6_Subscribe.py")
    at.run()
    assert at.button[1].label == "Unsubscribe"
