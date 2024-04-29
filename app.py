from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

app = Flask(__name__)

def scrape_amazon_reviews(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    reviews = []
    review_elements = soup.find_all('div', {'data-hook': 'review'})
    
    for review_element in review_elements:
        review_text_element = review_element.find('span', {'data-hook': 'review-body'})
        if review_text_element:
            reviews.append(review_text_element.get_text(strip=True))
    
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

@app.route('/', methods=['GET', 'POST'])
def index():
    sentiment = None
    if request.method == 'POST':
        url = request.form['url']
        reviews = scrape_amazon_reviews(url)
        if not reviews:
            sentiment = "No reviews found."
        else:
            sentiment = analyze_sentiment(reviews)
    return render_template('ok.html', sentiment=sentiment)

if __name__ == "__main__":
    app.run(debug=True)
