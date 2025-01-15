from transformers import pipeline

def analyze_news_sentiment(text):
    """
    Analyzes the sentiment of a news article using a pre-trained model.

    Args:
        text: The text of the news article.

    Returns:
        A dictionary containing the sentiment label (e.g., 'POSITIVE', 'NEGATIVE') and the score.
    """
    sentiment_pipeline = pipeline("sentiment-analysis")  # Or specify a model: "distilbert-base-uncased-finetuned-sst-2-english"
    result = sentiment_pipeline(text)[0]  # Get the first result
    return result