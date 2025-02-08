import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
import pickle
import app.config as conf

import re
import nltk
import string
from sklearn.feature_selection import SelectKBest, chi2
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from sklearn.svm import SVC

# Scaricare le risorse necessarie
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

# Funzione di pre-processing
def preprocess_text(text):
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    
    # Rimozione di link, menzioni e numeri
    text = re.sub(r'http\S+|www\S+|@\S+|\d+', '', text)
    
    # Rimozione di punteggiatura e conversione in minuscolo
    text = text.translate(str.maketrans('', '', string.punctuation)).lower()
    
    # Tokenizzazione e lemmatizzazione
    words = text.split()
    words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
    
    return text

def train_model(tipo__modello):
    df = pd.read_csv(conf.DATASET_PATH)

    # Preprocess data90
    df = df.dropna(subset=['Sentiment', 'News'])
    X = df['News']
    y = df['Sentiment']

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create pipeline
    if tipo__modello == "rf":
        pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(min_df=5, preprocessor=preprocess_text, ngram_range=(1,2))),  # Min_df per filtrare parole rare
            ('feature_selection', SelectKBest(chi2, k=500)),  # Selezione delle migliori feature
            ('clf', RandomForestClassifier(n_estimators=100, random_state=42))
        ])
    else:
        pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(min_df=5, preprocessor=preprocess_text, ngram_range=(1,2))),  # Min_df per filtrare parole rare
            ('feature_selection', SelectKBest(chi2, k=500)),  # Selezione delle migliori feature
            ('clf', SVC(kernel='linear', C=1.0, probability=True)) 
        ])

    # Train model
    pipeline.fit(X_train, y_train)

    # Evaluate model
    y_pred = pipeline.predict(X_test)
    print(f"Accuracy: {accuracy_score(y_test, y_pred)}")

    # Save model
    if tipo__modello == "rf":
        with open(conf.MODEL_PATH__rf, 'wb') as f:
            pickle.dump(pipeline, f)
    else:
        with open(conf.MODEL_PATH, 'wb') as f:
            pickle.dump(pipeline, f)

    return accuracy_score(y_test, y_pred)
