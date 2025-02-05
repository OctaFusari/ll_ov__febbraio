from fastapi import FastAPI
import uvicorn
from app.model import train_model, load_model
import gradio as gr
import re
from app.predict_model import fetch_news, predict_sentiment
import app.config as conf
import os
from pydantic import BaseModel


from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
# Configura CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
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

class dataFE_model(BaseModel):
    name: str
    model:str

@app.post("/")
def funzione__avvio(dataFE: dataFE_model):
#if __name__ == "__main__":

    model = open(conf.MODEL_PATH, 'rb')

    if os.path.exists(conf.MODEL_PATH) and os.path.getsize(conf.MODEL_PATH) == 0:
        if(dataFE.model == "rf"):
            train_model("rf")
        else:
            train_model("svm")
    else:
        print(model)
        news = fetch_news(dataFE.name)
        if not news:
            return {"error": "No news found for the company"}
        
        # Predici la direzione delle azioni
        prediction = predict_sentiment(news)
        """ with open('/home/octavian/Documenti/UNI/ll_ov__febbraio/smp__backend/data/prova.txt', 'w', encoding='utf-8') as file:
            file.write(news[3]) """
        return {"company": dataFE.name, "prediction": prediction, "news": news}

    #uvicorn.run(app, host="0.0.0.0", port=8000)
