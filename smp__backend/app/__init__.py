from fastapi import FastAPI
import uvicorn
from app.model import train_model, load_model
import gradio as gr

app = FastAPI()

# Endpoint to predict sentiment
@app.post("/predict/")
def predict(text: str):
    model = load_model()
    prediction = model.predict([text])[0]
    return {"prediction": prediction}

# Gradio interface
def predict_sentiment(text):
    model = load_model()
    return model.predict([text])[0]

if __name__ == "__main__":
    train_model()

    # Gradio UI
    interface = gr.Interface(
        fn=predict_sentiment,
        inputs="text",
        outputs="label",
        title="Political Sentiment Analysis",
        description="Predict if a comment or tweet is written by a Republican or Democrat."
    )

    uvicorn.run(app, host="127.0.0.1", port=8000) 