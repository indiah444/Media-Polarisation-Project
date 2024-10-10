"""File to convert all extraction results into pandas dataframe"""

import pandas as pd


def convert_to_dataframe(articles: list[dict]) -> pd.DataFrame:
    """
    Convert the list of articles results into a Pandas DataFrame.
    also adds a new column where all rows are name of news source
    """

    df = pd.DataFrame(articles)
    available_columns = df.columns
    required_columns = ["title", "content", "link", "published"]
    if not all(x in available_columns for x in required_columns):
        return None

    df['source_name'] = 'Democracy Now!'
    print(f"No. rows: {len(df.index)}")
    df.drop_duplicates(subset=["title", "content", "link", "published"],
                       keep='first')
    print(f"No. rows after dropping duplicates: {len(df.index)}")
    return df
