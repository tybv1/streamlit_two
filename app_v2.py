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
        str: The sentiment label (e.g., "Positive", "Negative", "Neutral").
    """
    analysis = TextBlob(article_text)
    if analysis.sentiment.polarity > 0:
        return "Positive"
    elif analysis.sentiment.polarity < 0:
        return "Negative"
    else:
        return "Neutral"


def fetch_and_display_news(query):
    """
    Fetches news articles from NewsAPI.org based on the query,
    summarizes them, performs sentiment analysis, and displays the
    results in Streamlit.

    Args:
        query (str): The search query for news articles.
    """

    # Init the News API client
    newsapi = NewsApiClient(api_key=NEWS_API_KEY)

    # Fetch top headlines for the query
    all_articles = newsapi.get_top_headlines(q=query, page_size=5)

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
                    sentiment = analyze_sentiment(news_data.summary)
                    st.write(f"**Summary:** {news_data.summary}")
                    st.write(f"**Sentiment:** {sentiment}")
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
    query = st.text_input("Enter your search query:")
    if query:
        fetch_and_display_news(query)
