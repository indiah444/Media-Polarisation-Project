"""Testing streamlit pages."""
from unittest.mock import patch
import pytest
from streamlit.testing.v1.app_test import AppTest


def test_subscribe_elements_submission_page():
    """Tests the presence of the subscribe button"""
    at = AppTest.from_file("pages/6_Subscribe.py")
    at.run()
    assert at.button[0].label == "Submit"


def test_unsubscribe_elements_submission_page():
    """Tests the presence of the unsubscribe button"""
    at = AppTest.from_file("pages/6_Subscribe.py")
    at.run()
    assert at.button[1].label == "Unsubscribe"


def test_home_page():
    """Tests that the home page runs without exception"""
    at = AppTest.from_file("pages/2_About.py")
    at.run()
    assert at.button[1].label == "Unsubscribe"
