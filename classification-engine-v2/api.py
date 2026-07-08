from fastapi import FastAPI
import joblib

app = FastAPI()

model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

@app.post("/classify")
def classify(ticket: dict):
    text = ticket["text"]
    X = vectorizer.transform([text])
    category = model.predict(X)[0]

    probabilities = model.predict_proba(X)[0]
    confidence = max(probabilities)

    return {
        "category": category,
        "confidence": round(float(confidence), 2)
    }
