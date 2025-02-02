from fastapi import FastAPI
import uvicorn
from app.model import train_model, load_model
import gradio as gr
import re
from app.predict_model import fetch_news, predict_sentiment
import app.config as conf


from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
# Configura CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)

""" # Gradio interface
def predict_sentiment(text):

    text__cleaned = re.sub(r'\s+', ' ', text)  # Rimuove spazi multipli
    text__cleaned = re.sub(r'[^\w\s]', '', text)  # Rimuove simboli

    model = load_model()
    return model.predict([text__cleaned])[0] """


@app.get("/")
def funzione__avvio():
#if __name__ == "__main__":
    azienda = "apple"

    model = open(conf.DATASET_PATH, 'rb')

    if not model:
        train_model("rf")

    news = fetch_news(azienda)
    if not news:
        return {"error": "No news found for the company"}
    
    # Predici la direzione delle azioni
    prediction = predict_sentiment(news)
    with open('/home/octavian/Documenti/UNI/ll_ov__febbraio/smp__backend/data/prova.txt', 'w', encoding='utf-8') as file:
        file.write(news[3])
    return {"company": azienda, "prediction": prediction, "news": news}

    #uvicorn.run(app, host="0.0.0.0", port=8000)
