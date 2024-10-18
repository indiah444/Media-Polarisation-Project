"""Testing streamlit pages."""
from unittest.mock import patch, MagicMock
import pytest
from streamlit.testing.v1.app_test import AppTest
from streamlit_components import select_topic, select_granularity, construct_sidebar, construct_linegraphs_container


@pytest.fixture
def mock_select_topic():
    return lambda x: select_topic(['a', 'b'])


@patch("streamlit.container")
def test_construct_linegraphs_container(mock_container):

    mock_line_graphs = MagicMock()
    mock_container.return_value = mock_line_graphs
    mock_avg_by_title = MagicMock()
    mock_count_by_title = MagicMock()
    mock_avg_by_content = MagicMock()
    mock_count_by_content = MagicMock()

    mock_line_graphs.columns.side_effect = [[mock_avg_by_title, mock_count_by_title],
                                            [mock_avg_by_content, mock_count_by_content]]

    result = construct_linegraphs_container()

    mock_line_graphs.header.assert_any_call("Polarity by Article Titles")
    mock_line_graphs.header.assert_any_call("Polarity by Article Content")
    assert result == [[mock_avg_by_title, mock_count_by_title], [
        mock_avg_by_content, mock_count_by_content]]


@patch("streamlit.sidebar")
@patch("streamlit_components.select_granularity")
@patch("streamlit_components.select_topic")
def test_construct_sidebar(mock_select_topic, mock_select_granularity, mock_sidebar):
    GRANULARITY_TO_HOURS = {"1 hour": "1h",
                            "1 day": "24h", "1 week": str(24*7)+'h'}
    topics_list = ["Topic 1", "Topic 2"]
    mock_select_topic.return_value = "Topic 1"
    mock_select_granularity.return_value = "Hourly"

    result = construct_sidebar(topics_list)

    mock_sidebar.header.assert_called_once_with("Settings")
    mock_select_topic.assert_called_once_with(topics_list)
    mock_select_granularity.assert_called_once_with(GRANULARITY_TO_HOURS)

    assert result == ("Topic 1", "Hourly")


def test_topic_selection_doesnt_raise_error(mock_select_topic):
    """Tests the sidebar topic selection"""
    at = AppTest.from_function(mock_select_topic)
    at.run()
    assert not at.exception


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
    assert not at.exception
