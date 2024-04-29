import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import nltk

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def scrape_amazon_reviews(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    review_elements = soup.find_all('span', {'data-hook': 'review-body'})

    reviews = [review_element.get_text(strip=True) for review_element in review_elements]
    return reviews


def analyze_sentiment(reviews):
    positive_count = 0
    negative_count = 0

    for review in reviews:
        blob = TextBlob(review)
        polarity = blob.sentiment.polarity
        if polarity > 0:
            positive_count += 1
        elif polarity < 0:
            negative_count += 1

    if positive_count > negative_count:
        return "Positive: You can consider buying this product."
    elif positive_count < negative_count:
        return "Negative: Consider before buying this product."
    else:
        return "Neutral: Mixed sentiments. Further analysis may be needed."


def main():
    url = input("Enter the Amazon product URL: ")
    reviews = scrape_amazon_reviews(url)
    if not reviews:
        print("No reviews found.")
    else:
        print("Reviews scraped successfully.")
        print("Analyzing sentiment...")
        sentiment = analyze_sentiment(reviews)
        print(sentiment)

if __name__ == "main":
    main()