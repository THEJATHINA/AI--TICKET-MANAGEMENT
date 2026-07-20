from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(title="Classification Engine")


class ClassificationRequest(BaseModel):
    text: str


class ClassificationResponse(BaseModel):
    category: str
    confidence: float


@app.post("/classify", response_model=ClassificationResponse)
def classify(request: ClassificationRequest):
    text = (request.text or "").strip().lower()

    if not text:
        return ClassificationResponse(category="Unknown", confidence=0.0)

    if "vpn" in text or "network" in text:
        return ClassificationResponse(category="Network", confidence=0.94)
    if "password" in text or "login" in text or "auth" in text:
        return ClassificationResponse(category="Authentication", confidence=0.92)
    if "printer" in text or "hardware" in text:
        return ClassificationResponse(category="Hardware", confidence=0.97)
    if "email" in text:
        return ClassificationResponse(category="Email", confidence=0.90)
    if "install" in text or "software" in text:
        return ClassificationResponse(category="Software", confidence=0.95)

    return ClassificationResponse(category="Unknown", confidence=0.0)
