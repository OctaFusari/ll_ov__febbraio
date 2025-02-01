import pickle
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string

nltk.download('stopwords')
nltk.download('punkt')

MODEL_PATH = "/home/octavian/Documenti/mcz_uni_project-main/smp__backend/models/sentiment_model.pkl"

import requests

API_KEY = "d01247718bac41389c538614c1f0e9b4"

def fetch_news(company):
    url = f"https://newsapi.org/v2/everything?q={company}&apiKey={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        articles = response.json().get("articles", [])
        return [article["content"] for article in articles]

    return []

def predict_sentiment(news_list):
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    processed_news = [preprocess_text(news) for news in news_list]
    predictions = model.predict(processed_news)
    positive_indices = [i for i, x in enumerate(predictions) if x == "positive" or x == "negative"]
    print(positive_indices)
    return predictions.tolist()

def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(text)
    tokens = [word.lower() for word in tokens if word.isalpha() and word not in stop_words]
    return " ".join(tokens)