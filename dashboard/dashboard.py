import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime, timedelta
from db_functions import create_connection, get_topic_names, get_topic_dict


def get_bubble_data(topic_id):

    three_days_ago = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')

    query = f"""
        SELECT 
            s.source_name,
            AVG(a.content_polarity_score) AS avg_polarity_score,
            COUNT(a.article_id) AS article_count
        FROM article_topic_assignment ata
        JOIN article a ON ata.article_id = a.article_id
        JOIN source s ON a.source_id = s.source_id
        WHERE ata.topic_id = %s AND a.date_published >= %s
        GROUP BY s.source_name
    """

    with create_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (topic_id, three_days_ago))
            data = cur.fetchall()

    return pd.DataFrame(data)


def get_scatter_data(topic_id):
    query = f"""
        SELECT 
            a.article_title,
            a.title_polarity_score,
            a.content_polarity_score,
            s.source_name
        FROM article_topic_assignment ata
        JOIN article a ON ata.article_id = a.article_id
        JOIN source s ON a.source_id = s.source_id
        WHERE ata.topic_id = %s
    """

    with create_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (topic_id,))
            data = cur.fetchall()

    return pd.DataFrame(data)


def main():
    st.title("Topic-Based Polarity Analysis with Altair")

    st.sidebar.header("Select Topic")
    topic_names = get_topic_names()
    topic_dict = get_topic_dict()
    selected_topic = st.sidebar.selectbox("Choose a topic:", topic_names)

    st.subheader(
        f"Bubble Chart: Average Polarity by Source (Topic: {selected_topic})")

    if selected_topic:
        topic_id = topic_dict[selected_topic]
        bubble_data = get_bubble_data(topic_id)

        if not bubble_data.empty:

            bubble_chart = alt.Chart(bubble_data).mark_circle().encode(
                x=alt.X('source_name:N', title='Source'),
                y=alt.Y('avg_polarity_score:Q',
                        title='Average Polarity Score'),
                size=alt.Size('article_count:Q', title='Number of Articles'),
                color=alt.Color('source_name:N', title='Source'),
                tooltip=['source_name', 'avg_polarity_score', 'article_count']
            ).properties(
                width=800,
                height=400
            )

            st.altair_chart(bubble_chart, use_container_width=True)
        else:
            st.write("No data available for the selected topic in the last 3 days.")

    st.subheader(
        f"Scatter Plot: Title vs Content Polarity (Topic: {selected_topic})")

    if selected_topic:
        scatter_data = get_scatter_data(topic_id)

        if not scatter_data.empty:

            scatter_chart = alt.Chart(scatter_data).mark_point(filled=True).encode(
                x=alt.X('title_polarity_score:Q',
                        scale=alt.Scale(domain=[-1, 1]),
                        axis=alt.Axis(title='Title Polarity Score', grid=True)),
                y=alt.Y('content_polarity_score:Q',
                        scale=alt.Scale(domain=[-1, 1]),
                        axis=alt.Axis(title='Content Polarity Score', grid=True)),
                color=alt.Color('source_name:N', title='Source'),
                tooltip=['article_title', 'title_polarity_score',
                         'content_polarity_score', 'source_name']
            ).properties(
                width=800,
                height=400
            ).interactive()

            zero_line = alt.Chart(pd.DataFrame({'x': [0], 'y': [0]})).mark_rule(color='black').encode(
                x='x:Q'
            ) + alt.Chart(pd.DataFrame({'x': [0], 'y': [0]})).mark_rule(color='black').encode(
                y='y:Q'
            )

            final_chart = scatter_chart + zero_line

            final_chart = final_chart.configure_axis(
                grid=True
            ).configure_view(
                stroke=None
            )

            st.altair_chart(final_chart, use_container_width=True)
        else:
            st.write("No articles found for the selected topic.")


if __name__ == "__main__":
    main()
