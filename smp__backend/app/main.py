from fastapi import FastAPI
import uvicorn
from app.model import train_model, load_model
import gradio as gr
import re
from app.predict_model import fetch_news, predict_sentiment


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

@app.get("/predict/")
def predict():
    # Ottieni le notizie relative all'azienda
    company = "apple"
    print(company)

    news = fetch_news(company)
    if not news:
        return {"error": "No news found for the company"}
    
    # Predici la direzione delle azioni
    prediction = predict_sentiment(news)
    return {"company": company, "prediction": prediction}

@app.post("/")
def funzione__avvio(modello, azienda):
#if __name__ == "__main__":
    train_model(modello)

    #predict_sentiment(azienda)

    # Gradio UI
    interface = gr.Interface(
        fn=predict_sentiment,
        inputs="text",
        outputs="label",
        title="Political Sentiment Analysis",
        description="Predict if a comment or tweet is written by a Republican or Democrat."
    )

    #interface.launch()

    #uvicorn.run(app, host="0.0.0.0", port=8000)
