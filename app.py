import streamlit as st
from utils.sentiment_analyzer import analyze_news_sentiment
from utils.chatbot import get_chatbot_response
from utils.data_visualization import plot_covid_data, load_covid_data
# from utils.api_utils import get_news_articles # If you need to fetch news
import pandas as pd

def main():
    st.title("Multipurpose Streamlit")

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose a page", ["Sentiment Analysis", "Chatbot", "COVID-19 Dashboard"])

    if page == "Sentiment Analysis":
        st.header("News Sentiment Analysis")
        # Option 1: User enters a URL
        # url = st.text_input("Enter news article URL:")
        # if url:
        #     article_text = get_news_article(url) # You'd implement this in api_utils.py
        #     sentiment = analyze_news_sentiment(article_text)
        #     st.write("Sentiment:", sentiment)

        # Option 2: User enters text directly
        article_text = st.text_area("Enter news article text:")
        if article_text:
            sentiment = analyze_news_sentiment(article_text)
            st.write("Sentiment:", sentiment)

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