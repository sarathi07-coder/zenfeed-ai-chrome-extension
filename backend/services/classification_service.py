# backend/services/classification_service.py
import os, joblib
from typing import Dict

TEXT_MODEL_PATH = os.getenv("TEXT_MODEL_OUT", "ml_models/text_classifier.pkl")
_text_model = None

def load_text_model():
    global _text_model
    if _text_model is None:
        _text_model = joblib.load(TEXT_MODEL_PATH)
    return _text_model

def classify_content(item: Dict) -> Dict:
    """
    item: { title, description, transcript (optional) }
    returns: {category, probs, confidence}
    """
    model = load_text_model()
    text = (item.get("title","") + " " + item.get("description","") + " " + item.get("transcript",""))
    pred = model.predict([text])[0]
    probs = None
    try:
        probs = model.predict_proba([text])[0].tolist()
    except Exception:
        probs = None
    return {"category": pred, "confidence": None if probs is None else max(probs)}
