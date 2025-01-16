import streamlit as st
from utils.sentiment_analyzer import analyze_news_sentiment
from utils.chatbot import get_chatbot_response
from utils.data_visualization import plot_covid_data, load_covid_data
# from utils.api_utils import get_news_articles # If you need to fetch news
import pandas as pd
from newspaper import Article
import nltk
from textblob import TextBlob
from newsapi import NewsApiClient

NEWS_API_KEY = "344f818938c84d2daa61d8063de09ff7"

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

    newsapi = NewsApiClient(api_key=NEWS_API_KEY)

    # all_articles = newsapi.get_top_headlines(q=topic, page_size=10)
    all_articles = newsapi.get_everything(q=topic, page_size=10)

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


def main():
    st.title("Multipurpose Streamlit Application")

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose a page", ["NewsAPI Summariser", "Chatbot", "COVID-19 Dashboard"])
    
    if page == "NewsAPI Summariser":
        st.header("News summariser and sentiment analysis")

        # Dropdown for topic selection
        topics = ["Technology", "Business", "Sports", "Entertainment", "Health", "Science"]
        selected_topic = st.selectbox("Select a topic:", topics)

        # Text input for a new topic
        new_topic = st.text_input("Or type a new topic:")

        # Determine the final topic to use
        final_topic = new_topic if new_topic else selected_topic

        # Fetch and display news for the final topic
        fetch_and_display_news(final_topic)

    elif page == "Chatbot":
        st.header("Chatbot")
        user_input = st.text_input("You:", key="user_input")  # Use key to manage input state
        if st.session_state.user_input:
            response = get_chatbot_response(st.session_state.user_input)
            st.text_area("Chatbot:", value=response, height=200, key="chatbot_response")

    elif page == "COVID-19 Dashboard":
        st.header("COVID-19 Data Dashboard")
        try:
            covid_data = load_covid_data("data/covid_data.csv")
            plot_covid_data(covid_data)
        except FileNotFoundError:
            st.error("COVID-19 data file not found. Please check the data directory.")  


if __name__ == "__main__":
    main()
