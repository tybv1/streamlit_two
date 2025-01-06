import streamlit as st
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from newspaper import Article
import nltk

# Download NLTK resources if not already downloaded
nltk.download("punkt")


def fetch_and_display_news(category, num_articles):
    """
    Fetches news articles from Google News based on the selected category
    and number of articles, summarizes them, and displays the summarized
    content on a Streamlit UI.

    Args:
        category (str): The category of news to fetch
                       (e.g., 'WORLD', 'NATION', 'BUSINESS',
                       'TECHNOLOGY', 'ENTERTAINMENT', 'SPORTS',
                       'SCIENCE', 'HEALTH').
        num_articles (int): The maximum number of news articles to fetch.
    """

    if category == "Trending News":
        site = "https://news.google.com/news/rss"
    elif category == "Favourite Topics":
        topic = st.selectbox(
            "Choose your favourite Topic",
            [
                "Choose Topic",
                "WORLD",
                "NATION",
                "BUSINESS",
                "TECHNOLOGY",
                "ENTERTAINMENT",
                "SPORTS",
                "SCIENCE",
                "HEALTH",
            ],
        )
        if topic != "Choose Topic":
            site = (
                f"https://news.google.com/news/rss/headlines/section/TOPIC/{topic}"
            )
        else:
            return
    elif category == "Search Topic":
        query = st.text_input("Enter your Topic")
        if query:
            site = f"https://news.google.com/news/rss/search?q={query}"
        else:
            return
    else:
        return

    try:
        op = urlopen(site)
        rd = op.read()
        op.close()
        sp_page = soup(rd, "xml")
        news_list = sp_page.find_all("item")

        # Display news articles with their summaries and metadata
        for i, news in enumerate(news_list[:num_articles]):
            st.write(f"**Title:** {news.title.text}")
            st.write(f"**Link:** {news.link.text}")
            news_data = Article(news.link.text)
            news_data.download()
            news_data.parse()
            news_data.nlp()
            st.write(f"**Summary:** {news_data.summary}")
            st.write(f"**Image:** {news_data.top_image}")
            st.write(f"**Published Date:** {news.pubDate.text}")
            st.write("---")

    except Exception as e:
        st.error(f"An error occurred: {e}")


def main():
    """
    Main function to create the Streamlit UI and handle user input.
    """

    st.title("Google News Summarizer")

    # UI elements for user input
    category = st.selectbox(
        "Select your Category", ["Trending News", "Favourite Topics", "Search Topic"]
    )
    num_articles = st.slider("Number of News:", 5, 25, 5)

    # Fetch and display news based on user input
    fetch_and_display_news(category, num_articles)


if __name__ == "__main__":
    main()
