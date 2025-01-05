from fastapi import FastAPI
from pydantic import BaseModel
from textblob import TextBlob

app = FastAPI()

class TextInput(BaseModel):
    text: str
@app.get("/")
def read_root():
    return {"message": "Welcome to the Sentiment Analysis API!"}

@app.post("/sentiment")
async def analyze_sentiment(input: TextInput):
    analysis = TextBlob(input.text)
    polarity = analysis.sentiment.polarity  # -1 (negative) to 1 (positive)

    if polarity < -0.5:
        recommendation = ["Depression", "Self-Harm"]
    elif polarity < 0:
        recommendation = ["Anxiety"]
    elif polarity >= 0.5:
        recommendation = ["Well-Being", "Happiness"]
    else:
        recommendation = ["Neutral Assessment"]

    return {"polarity": polarity, "recommendation": recommendation}
