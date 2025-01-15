import requests
from bs4 import BeautifulSoup

def get_news_article(url):
    """
    Fetches the text content of a news article from a URL.
    (This is a basic example and might need adjustments for different websites.)

    Args:
        url: The URL of the news article.

    Returns:
        The text content of the article (or None if an error occurs).
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes

        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract text from paragraph tags (this is a very basic example)
        paragraphs = soup.find_all('p')
        article_text = ' '.join([p.get_text() for p in paragraphs])

        return article_text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching article: {e}")
        return None
    except Exception as e:
        print(f"Error parsing article: {e}")
        return None