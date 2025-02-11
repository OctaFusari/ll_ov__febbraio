from fastapi import FastAPI
from app.model import train_model
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

class dataFE_model(BaseModel):
    name: str
    model:str

@app.post("/")
def funzione__avvio(dataFE: dataFE_model):
    if(dataFE.model == "rf" and os.path.exists(conf.MODEL_PATH__rf__try) and os.path.getsize(conf.MODEL_PATH__rf__try) == 0):
        train_model("rf")
    elif(dataFE.model == "svc" and os.path.exists(conf.MODEL_PATH__try) and os.path.getsize(conf.MODEL_PATH__try) == 0):
        train_model("svc")
        
    news = fetch_news(dataFE.name)
    if not news:
        return {"error": "No news found for the company"}
    
    # Predici la direzione delle azioni
    prediction = predict_sentiment(news, dataFE.model)
    return prediction


""" 

la domanda è che le informazioni detenute in questi articoli sono realmente rilevanti per l'andamento del mercato?
collezionare per giorno e per settimana le informazioni stampate dai quotidiani e poi andare a raccolgile le informazioni di andamento di borsa
poi vedere se le news realmente hanno potere predittivo sull'abbassamento e la crescita del mercato

ogni giorno raccogli 1oo news e bisogna capire se parla di quella azienda e poi capire se questo testo influenza il mercato
 """