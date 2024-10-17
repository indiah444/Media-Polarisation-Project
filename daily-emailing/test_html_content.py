# pylint: skip-file

from unittest.mock import patch

import pandas as pd

from html_content import pivot_df, add_source_columns, add_topic_rows, generate_html_with_links, generate_html, add_unsubscribe_link, get_url_html


class TestPivot:

    def test_pivot_dataframe(self):
        data = {'topic_name': ['topic1', 'topic1', 'topic2', 'topic2'],
                'source_name': ['source1', 'source2', 'source1', 'source2'],
                'avg_polarity_score': [0.3, -0.2, 0.5, -0.7]}
        df = pd.DataFrame(data)
        result = pivot_df(df)
        expected_data = {'source1': [0.3, 0.5], 'source2': [-0.2, -0.7]}
        expected_df = pd.DataFrame(expected_data, index=['topic1', 'topic2'])
        expected_df.index.name = 'topic_name'
        expected_df.columns.name = 'source_name'
        pd.testing.assert_frame_equal(result, expected_df)

    def test_pivot_df_empty(self):
        df = pd.DataFrame(
            columns=['topic_name', 'source_name', 'avg_polarity_score'])
        result = pivot_df(df)
        expected_df = pd.DataFrame([], columns=[], index=[])
        expected_df.index.name = 'topic_name'
        expected_df.columns.name = 'source_name'
        pd.testing.assert_frame_equal(result, expected_df)

    def test_pivot_df_with_none_values(self):
        data = {'topic_name': ['topic1', 'topic1', 'topic2', 'topic2'],
                'source_name': ['source1', 'source2', 'source1', 'source2'],
                'avg_polarity_score': [0.3, None, 0.5, -0.7]}
        df = pd.DataFrame(data)
        result = pivot_df(df)
        expected_data = {'source1': [0.3, 0.5], 'source2': ['N/A', -0.7]}
        expected_df = pd.DataFrame(expected_data, index=['topic1', 'topic2'])
        expected_df.index.name = 'topic_name'
        expected_df.columns.name = 'source_name'
        pd.testing.assert_frame_equal(result, expected_df)


class TestAddSourceColumns:

    def test_with_valid_df(self):
        expected_data = {'source1': [0.3, 0.5], 'source2': [-0.2, -0.7]}
        df = pd.DataFrame(expected_data, index=['topic1', 'topic2'])
        df.index.name = 'topic_name'
        df.columns.name = 'source_name'
        result = add_source_columns(df)
        expected = "<th style='background-color: white;'>source1</th><th style='background-color: white;'>source2</th>"
        assert result == expected

    def test_empty_df(self):
        df = pd.DataFrame({})
        result = add_source_columns(df)
        expected = ""
        assert result == expected


class TestAddTopicRows:

    def test_add_topic_rows(self):
        data = {'source1': [0.3, 0.6],
                'source2': [-0.2, -0.7]}
        df = pd.DataFrame(data, index=['topic1', 'topic2'])
        result = add_topic_rows(df)
        expected = ("<tr><td style='background-color: white;'>topic1</td>"
                    "<td style='background-color: #fafafa;'>0.30</td>"
                    "<td style='background-color: #fafafa;'>-0.20</td></tr>"
                    "<tr><td style='background-color: white;'>topic2</td>"
                    "<td style='background-color: #b6f7ae;'>0.60</td>"
                    "<td style='background-color: #fabbb7;'>-0.70</td></tr>")
        assert result == expected

    def test_empty_df(self):
        df = pd.DataFrame({})
        result = add_topic_rows(df)
        expected = ""
        assert result == expected


class TestGenerateHtmlWithLinks:

    @patch('html_content.get_url_html')
    @patch('html_content.get_yesterday_links_and_titles')
    def test_with_links(self, mock_get_yesterday_links, mock_get_url_html):
        mock_get_yesterday_links.return_value = [{'title': 'article1', 'link': 'http://example.com/article1', 'topic': 'topic1'},
                                                 {'title': 'article2', 'link': 'http://example.com/article2', 'topic': 'topic2'}]
        mock_get_url_html.side_effect = lambda url: f'<li><a href="{
            url["link"]}">{url["title"]}</a></li>'.strip()
        result = generate_html_with_links()

        expected = ("<h2>Yesterday's articles:</h2>"
                    '<h4>topic1</h4>\n<ul>\n'
                    '<li><a href="http://example.com/article1">article1</a></li>'
                    "</ul>"
                    '<h4>topic2</h4>\n<ul>\n'
                    '<li><a href="http://example.com/article2">article2</a></li>'
                    "</ul>")
        assert result == expected

    @patch('html_content.get_yesterday_links_and_titles')
    def test_with_no_links(self, mock_get_yesterday_links):
        mock_get_yesterday_links.return_value = []
        result = generate_html_with_links()
        expected = ("<h2>Yesterday's articles:</h2>")
        assert result == expected

    def test_get_url_html(self):
        url_details = {'title': 'title', 'link': 'link'}
        res = get_url_html(url_details)
        assert res == '<li><a href="link">title</a></li>'


class TestAddUnsubscribeLink:

    @patch('html_content.ENV', {
        "EC2_HOST": "test_host"
    })
    def test_add_unsubscribe_link(self):
        result = add_unsubscribe_link()
        assert result == '<a href="test_host:8501/Subscribe" target="_blank">Unsubscribe here</a>'


class TestGenerateHtml:

    @patch('html_content.add_unsubscribe_link')
    @patch('html_content.pivot_df')
    @patch('html_content.add_source_columns')
    @patch('html_content.add_topic_rows')
    @patch('html_content.generate_html_with_links')
    def test_generate_html_with_data(self, mock_generate_html_with_links, mock_add_topic_rows, mock_add_source_columns, mock_pivot_df, mock_add_unsubscribe_link):

        mock_pivot_df.return_value = pd.DataFrame({
            'source1': [0.3, 0.5],
            'source2': [-0.2, -0.7]
        }, index=['topic1', 'topic2'])

        mock_add_source_columns.return_value = "<th style='background-color: #fafafa;'>source1</th><th style='background-color: #fabbb7;'>source2</th>"
        mock_add_topic_rows.return_value = (
            "<tr><td style='background-color: white;'>topic1</td>"
            "<td style='background-color: #fafafa;'>0.30</td>"
            "<td style='background-color: #fabbb7;'>-0.20</td></tr>"
            "<tr><td style='background-color: white;'>topic2</td>"
            "<td style='background-color: #fafafa;'>0.50</td>"
            "<td style='background-color: #fabbb7;'>-0.70</td></tr>"
        )
        mock_generate_html_with_links.return_value = "<p>Yesterday's articles:</p><a href='http://example.com/article1'>http://example.com/article1</a>"
        mock_add_unsubscribe_link.return_value = "<a>link<\a>"
        data = {
            'topic_name': ['topic1', 'topic2'],
            'source_name': ['source1', 'source2'],
            'avg_polarity_score': [0.3, -0.2]
        }

        df = pd.DataFrame(data)
        result = generate_html(df)

        assert 'Average Content Polarity Score by Topic and Source (Published Yesterday - ' in result
        assert 'Yesterday\'s articles:' in result
        assert "<a href='http://example.com/article1'>http://example.com/article1</a>" in result
        assert '<th style=\'background-color: #fafafa;\'>source1</th>' in result
        assert '<tr><td style=\'background-color: white;\'>topic1</td>' in result
        assert '<tr><td style=\'background-color: white;\'>topic2</td>' in result

    @patch('html_content.add_unsubscribe_link')
    @patch('html_content.pivot_df')
    @patch('html_content.add_source_columns')
    @patch('html_content.add_topic_rows')
    @patch('html_content.generate_html_with_links')
    def test_generate_html_with_empty_dataframe(self, mock_generate_html_with_links, mock_add_topic_rows, mock_add_source_columns, mock_pivot_df, mock_add_unsubscribe_link):

        mock_pivot_df.return_value = pd.DataFrame(
            columns=['source1', 'source2'])
        mock_add_source_columns.return_value = "<th style='background-color: #fafafa;'>source1</th><th style='background-color: #fabbb7;'>source2</th>"
        mock_add_topic_rows.return_value = ""
        mock_add_unsubscribe_link.return_value = "<a>link<\a>"
        mock_generate_html_with_links.return_value = "<p>Yesterday's articles:</p>"

        df = pd.DataFrame(columns=['topic_name', 'source_name',
                                   'avg_polarity_score'])
        result = generate_html(df)

        assert 'Average Content Polarity Score by Topic and Source' in result
        assert 'Yesterday\'s articles:' in result
        assert "<th style='background-color: #fafafa;'>source1</th>" in result
        assert "<th style='background-color: #fabbb7;'>source2</th>" in result
        assert '<tbody>' in result
        assert '</tbody>' in result
