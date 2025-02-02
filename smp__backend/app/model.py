import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
import app.config as conf
import pickle

def train_model(tipo__modello):
    df = pd.read_csv(conf.DATASET_PATH)

    # Preprocess data
    df = df.dropna(subset=['Sentiment', 'News'])
    X = df['News']
    y = df['Sentiment']

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create pipeline
    if tipo__modello == "rf":
        pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(stop_words='english')),
            ('clf', RandomForestClassifier(n_estimators=100, random_state=42))
        ])
    else:
        pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(stop_words='english')),  # Converti testo in vettori TF-IDF
            ('clf', SVC(kernel='linear', C=1.0, probability=True))  # Classificatore SVC con kernel lineare
        ])

    # Train model
    pipeline.fit(X_train, y_train)

    # Evaluate model
    y_pred = pipeline.predict(X_test)
    print(f"Accuracy: {accuracy_score(y_test, y_pred)}")

    # Save model
    with open(conf.MODEL_PATH, 'wb') as f:
        pickle.dump(pipeline, f)

def load_model():
    with open(conf.MODEL_PATH, 'rb') as f:
        return pickle.load(f)
