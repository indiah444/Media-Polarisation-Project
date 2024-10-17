"""Testing streamlit pages."""
from unittest.mock import patch
import pytest
from streamlit.testing.v1.app_test import AppTest


def test_subscribe_elements_submission_page():
    at = AppTest.from_file("pages/6_Subscribe.py")
    at.run()
    assert at.button[0].label == "Submit"


def test_unsubscribe_elements_submission_page():
    at = AppTest.from_file("pages/6_Subscribe.py")
    at.run()
    assert at.button[1].label == "Unsubscribe"
