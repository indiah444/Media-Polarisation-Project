# pylint: skip-file

"""Tests for transform_articles.py file."""

import unittest
from unittest.mock import patch, MagicMock

import pandas as pd

from transform_articles import (
    transform,
    change_source_name_to_id,
    drop_duplicate_titles,
    drop_already_present_articles,
    get_polarity_scores
)


class TestTransformFunction(unittest.TestCase):
    """Tests for the transform function."""

    @patch('transform_articles.get_source_dict')
    @patch('transform_articles.get_article_titles')
    @patch('transform_articles.add_topics_to_dataframe')
    @patch('transform_articles.get_sentiments')
    def test_transform(self, fake_get_sentiments, fake_add_topics, fake_get_article_titles, fake_get_source_dict):
        """Test the main transform function with valid input."""
        fake_get_source_dict.return_value = {'Source A': 1, 'Source B': 2}
        fake_get_article_titles.return_value = ['Article 1']

        def fake_get_sentiments_func(sia, df, *args):
            return df.assign(compound=0.5, pos=0.1, neg=0.2, neut=0.7)
        fake_get_sentiments.side_effect = fake_get_sentiments_func

        def fake_add_topics_func(df):
            return df
        fake_add_topics.side_effect = fake_add_topics_func
        articles = pd.DataFrame({
            'title': ['Article 1', 'Article 2', 'Article 3'],
            'content': ['Content 1', 'Content 2', 'Content 3'],
            'source_name': ['Source A', 'Source B', 'Source A'],
            'date_published': [pd.Timestamp('2023-01-01'), pd.Timestamp('2023-01-02'), pd.Timestamp('2023-01-03')]
        })
        transformed_articles = transform(articles)
        expected_df = pd.DataFrame({
            'title': ['Article 2', 'Article 3'],
            'content': ['Content 2', 'Content 3'],
            'date_published': [pd.Timestamp('2023-01-02'), pd.Timestamp('2023-01-03')],
            'source_id': [2, 1],
            'title_polarity_score': [0.5, 0.5],
            'content_polarity_score': [0.5, 0.5]
        })
        transformed_articles.reset_index(drop=True, inplace=True)
        expected_df.reset_index(drop=True, inplace=True)

        pd.testing.assert_frame_equal(transformed_articles, expected_df)
        fake_get_source_dict.assert_called_once()
        fake_get_article_titles.assert_called_once()
        fake_add_topics.assert_called_once()


class TestDropDuplicateTitles(unittest.TestCase):
    """Tests for the drop_duplicate_titles function."""

    def test_drop_duplicate_titles(self):
        """Test that duplicate titles are dropped."""
        articles = pd.DataFrame({
            'title': ['Article 1', 'Article 2', 'Article 1'],
            'content': ['Content 1', 'Content 2', 'Content 1']
        })
        result = drop_duplicate_titles(articles)

        expected_df = pd.DataFrame({
            'title': ['Article 1', 'Article 2'],
            'content': ['Content 1', 'Content 2']
        })
        pd.testing.assert_frame_equal(result, expected_df)

    def test_no_duplicates(self):
        """Test that no rows are dropped if there are no duplicates."""
        articles = pd.DataFrame({
            'title': ['Article 1', 'Article 2'],
            'content': ['Content 1', 'Content 2']
        })
        result = drop_duplicate_titles(articles)

        pd.testing.assert_frame_equal(result, articles)


class TestDropAlreadyPresentArticles(unittest.TestCase):
    """Tests for the drop_already_present_articles function."""

    @patch('transform_articles.get_article_titles')
    def test_drop_already_present_articles(self, fake_get_article_titles):
        """Test dropping articles that are already present in the database."""
        fake_get_article_titles.return_value = ['Article 1']
        articles = pd.DataFrame({
            'title': ['Article 1', 'Article 2', 'Article 3'],
            'content': ['Content 1', 'Content 2', 'Content 3']
        })
        result = drop_already_present_articles(articles)

        expected_df = pd.DataFrame({
            'title': ['Article 2', 'Article 3'],
            'content': ['Content 2', 'Content 3']
        })
        result.reset_index(drop=True, inplace=True)
        expected_df.reset_index(drop=True, inplace=True)
        pd.testing.assert_frame_equal(result, expected_df)

    @patch('transform_articles.get_article_titles')
    def test_no_articles_to_drop(self, fake_get_article_titles):
        """Test that no articles are dropped if none are already present."""
        fake_get_article_titles.return_value = []
        articles = pd.DataFrame({
            'title': ['Article 1', 'Article 2'],
            'content': ['Content 1', 'Content 2']
        })
        result = drop_already_present_articles(articles)

        pd.testing.assert_frame_equal(result, articles)


class TestChangeSourceNameToID(unittest.TestCase):
    """Tests for the change_source_name_to_id function."""

    @patch('transform_articles.get_source_dict')
    def test_change_source_name_to_id(self, fake_get_source_dict):
        """Test changing source names to source_ids."""
        fake_get_source_dict.return_value = {'Source A': 1, 'Source B': 2}
        articles = pd.DataFrame({
            'title': ['Article 1', 'Article 2'],
            'source_name': ['Source A', 'Source B']
        })
        result = change_source_name_to_id(articles)

        expected_df = pd.DataFrame({
            'title': ['Article 1', 'Article 2'],
            'source_id': [1, 2]
        })
        pd.testing.assert_frame_equal(result, expected_df)


class TestGetPolarityScores(unittest.TestCase):
    """Tests for the get_polarity_scores function."""

    @patch('transform_articles.get_sentiments')
    @patch('transform_articles.SentimentIntensityAnalyzer')
    def test_get_polarity_scores(self, fake_sia, fake_get_sentiments):
        """Test adding polarity scores for title and content."""
        fake_sia.return_value = MagicMock()
        fake_get_sentiments.side_effect = lambda sia, df, * \
            args: df.assign(compound=0.5, pos=0.1, neg=0.2, neut=0.7)
        articles = pd.DataFrame({
            'title': ['Article 1', 'Article 2'],
            'content': ['Content 1', 'Content 2']
        })
        result = get_polarity_scores(articles)

        expected_df = pd.DataFrame({
            'title': ['Article 1', 'Article 2'],
            'content': ['Content 1', 'Content 2'],
            'title_polarity_score': [0.5, 0.5],
            'content_polarity_score': [0.5, 0.5]
        })
        pd.testing.assert_frame_equal(result, expected_df)
