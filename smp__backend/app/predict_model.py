import pickle
import nltk
from nltk.corpus import stopwords, wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import contractions
import re
import requests
from bs4 import BeautifulSoup
import app.config as conf

# Scaricare risorse necessarie per NLTK
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

# Inizializza il lemmatizzatore
lemmatizer = WordNetLemmatizer()

def fetch_news(company):
    """
    Recupera le notizie finanziarie di una società e pulisce i testi.
    """
    url = f"https://newsdata.io/api/1/news?apikey=pub_68025b675d00f75bb196fb60da1220893be9b&q={company}&language=en&category=business"
    response = requests.get(url)
    
    if response.status_code == 200:
        response.encoding = 'utf-8-sig'
        news_list = []

        # Estrarre e pulire le notizie
        for article in response.json().get("results", []):
            text = article.get("description", "")
            if text:
                cleaned_text = preprocess_text(text)
                news_list.append(cleaned_text)
        
        print(news_list)
        return news_list
    else:
        raise Exception(f"Errore nel recupero dati. Status: {response.status_code}")

def preprocess_text(text):
    """
    Pulisce e normalizza il testo delle notizie.
    """
    # Espansione delle contrazioni (es. "don't" -> "do not")
    text = contractions.fix(text)

    # Rimozione HTML
    text = BeautifulSoup(text, "html.parser").get_text()

    # Rimozione caratteri speciali e numeri
    text = re.sub(r'\W+', ' ', text)

    # Tokenizzazione
    tokens = word_tokenize(text)

    # Rimozione stopwords e lemmatizzazione
    stop_words = set(stopwords.words('english'))
    tokens = [lemmatizer.lemmatize(word.lower()) for word in tokens if word.isalpha() and word.lower() not in stop_words]

    return " ".join(tokens)

def predict_sentiment(news_list):
    """
    Predice il sentiment delle notizie usando un modello pre-addestrato.
    """
    processed_news = []
    new_sentiments = []

    # Carica il modello
    with open(conf.MODEL_PATH, 'rb') as f:
        model = pickle.load(f)

    # Prepara il testo per la previsione
    for news in news_list:
        processed_news.append(news)

    # Predizione del sentiment
    predictions = model.predict(processed_news)

    # Creazione dell'output strutturato
    for i, news in enumerate(news_list):
        new_sentiments.append({
            "news": news,
            "sentiment": predictions.tolist()[i]
        })

    return new_sentiments
