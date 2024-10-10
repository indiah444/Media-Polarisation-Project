# pylint: skip-file

from transform_dn import convert_to_dataframe


def test_convert_to_dataframe_with_articles():

    articles = [{"title": "Article 1",
                 "content": "Content of article 1.",
                 "link": "https://example.com/article1",
                 "published": "2024-10-01"},
                {"title": "Article 2",
                 "content": "Content of article 2.",
                 "link": "https://example.com/article2",
                 "published": "2024-10-02"}]

    df = convert_to_dataframe(articles)
    assert df.shape[0] == 2
    assert set(df.columns) == {"title", "content",
                               "link", "published", "source_name"}
    assert all(df['source_name'] == 'Democracy Now!')


def test_convert_to_dataframe_empty():
    articles = []

    df = convert_to_dataframe(articles)

    assert df is None


def test_convert_to_dataframe_invalid_data():
    articles = [{"title": "Invalid Article",
                 "content": "No link or published date."}]

    df = convert_to_dataframe(articles)

    assert df is None
