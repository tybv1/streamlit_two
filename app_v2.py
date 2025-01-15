import streamlit as st
from newspaper import Article
import nltk
from textblob import TextBlob

# Import the News API client library
from newsapi import NewsApiClient

# Replace with your actual News API key
NEWS_API_KEY = "344f818938c84d2daa61d8063de09ff7"

# Download NLTK resources if not already downloaded
nltk.download('punkt')


def analyze_sentiment(article_text):
    """
    Performs sentiment analysis on the given article text.

    Args:
        article_text (str): The text content of the article.

    Returns:
        tuple: The sentiment label (e.g., "Positive", "Negative", "Neutral")
               and the sentiment score as a float.
    """
    analysis = TextBlob(article_text)
    if analysis.sentiment.polarity > 0:
        return "Positive", analysis.sentiment.polarity
    elif analysis.sentiment.polarity < 0:
        return "Negative", analysis.sentiment.polarity
    else:
        return "Neutral", analysis.sentiment.polarity


def fetch_and_display_news(topic):
    """
    Fetches 5 news articles from NewsAPI.org based on the topic,
    summarizes them, performs sentiment analysis, and displays the
    results in Streamlit.

    Args:
        topic (str): The topic for news articles.
    """

    newsapi = NewsApiClient(api_key=NEWS_API_KEY)

    all_articles = newsapi.get_top_headlines(q=topic, page_size=5)

    if all_articles['status'] == 'ok':
        articles = all_articles['articles']

        for article in articles:
            st.write(f"**Title:** {article['title']}")
            st.write(f"**Link:** {article['url']}")

            try:
                news_data = Article(article['url'])
                news_data.download()
                news_data.parse()
                news_data.nlp()

                if news_data.summary:
                    sentiment, score = analyze_sentiment(news_data.summary)
                    st.write(f"**Summary:** {news_data.summary}")
                    st.write(f"**Sentiment:** {sentiment} ({score:.2f})")
                else:
                    st.write("**Summary:** Unable to generate summary for this article.")

                st.write(f"**Published Date:** {article['publishedAt']}")
                st.write("---")

            except Exception as e:
                st.error(f"An error occurred processing the article: {e}")
    else:
        st.error(f"Failed to fetch news: {all_articles['message']}")


if __name__ == "__main__":
    st.title("NewsAPI Summarizer")

    # Dropdown for topic selection
    topics = ["Technology", "Business", "Sports", "Entertainment", "Health", "Science"]
    selected_topic = st.selectbox("Select a topic:", topics)

    # Fetch and display news for the selected topic
    fetch_and_display_news(selected_topic)
