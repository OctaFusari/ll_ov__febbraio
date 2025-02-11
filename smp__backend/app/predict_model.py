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

        art__conv = []

        # Estrarre e pulire le notizie
        for article in response.json().get("results", []):
            text = article.get("description", "")
            content = article.get("content", "")
            link = article.get("link", "")
            if text:
                unione = " ".join(filter(None, [article.get("title", ""), text]))
                if content:
                    unione = " ".join(filter(None, [article.get("title", ""), text,content]))
                art__conv.append({"title":article.get("title", ""), "text__pulito":preprocess_text(unione), "testo__grezzo":text, "sentiment":"", "link":link})

        return art__conv
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

    # Conversione in minuscolo
    text = text.lower()

    # Rimozione della punteggiatura
    text = re.sub(r'[^\w\s]', '', text)

    # Rimozione di link, menzioni e numeri
    text = re.sub(r'http\S+|www\S+|@\S+|\d+', '', text)

    # Tokenizzazione
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    tokens = [lemmatizer.lemmatize(word.lower()) for word in tokens if word.isalpha() and word.lower() not in stop_words]

    return ' '.join(tokens)

def predict_sentiment(news_list, tipo_mod):
    """
    Predice il sentiment delle notizie usando un modello pre-addestrato.
    """
    processed_news = []

    if(tipo_mod == "rf"):
        print(tipo_mod)
        # Carica il modello
        with open(conf.MODEL_PATH__rf__try, 'rb') as f:
            model = pickle.load(f)
    elif(tipo_mod == "svc"):
        # Carica il modello
        with open(conf.MODEL_PATH__try, 'rb') as f:
            model = pickle.load(f)

    # Prepara il testo per la previsione
    for news in news_list:
        processed_news.append(news["testo__grezzo"])

    # Predizione del sentiment
    predictions = model.predict(processed_news)

    # Creazione dell'output strutturato
    for i, news in enumerate(news_list):
        news["sentiment"] = predictions.tolist()[i]

    return news_list
