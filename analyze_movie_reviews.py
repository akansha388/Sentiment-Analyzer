import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Download required NLTK resources (only needed once)
nltk.download('vader_lexicon')

# Initialize the SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()

def analyze_sentiment(review_text):
    scores = sia.polarity_scores(review_text)
    compound = scores['compound']

    if compound > 0.05:
        sentiment = "Positive"
    elif compound < -0.05:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return sentiment, compound

# Sample review 1
review = "The movie was amazing, I loved it!"
sentiment, score = analyze_sentiment(review)
print(f"Sentiment: {sentiment}")
print(f"Compound Score: {score}")

# Sample review 2
review = "The movie was terrible and a waste of time."
sentiment, score = analyze_sentiment(review)
print(f"Sentiment: {sentiment}")
print(f"Compound Score: {score}")

# User input review
custom_review = input("\nEnter your own movie review: ")
custom_sentiment, custom_score = analyze_sentiment(custom_review)
print(f"Sentiment: {custom_sentiment}")
print(f"Compound Score: {custom_score}")
