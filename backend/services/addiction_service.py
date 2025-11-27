# backend/services/addiction_service.py
import os, joblib, numpy as np
from typing import Dict

ADD_MODEL_PATH = os.getenv("ADDICTION_MODEL_OUT", "ml_models/addiction_model.pkl")
_add_model = None

def load_add_model():
    global _add_model
    if _add_model is None:
        _add_model = joblib.load(ADD_MODEL_PATH)
    return _add_model

def compute_addiction_score(item: Dict, user_context: Dict=None) -> Dict:
    """
    item: { duration_sec, title, description, transcript }
    user_context: { repeat_watch, recent_session_minutes }
    returns: { addiction_index: int, risk_level: str }
    """
    model = load_add_model()
    # simple engineered features
    duration = int(item.get("duration_sec", 0))
    title = item.get("title","").lower()
    is_compilation = int(any(k in title for k in ["compilation","meme","best of","compil"]))
    view_count = int(item.get("viewCount", 0) or 0)
    repeat_watch = int(user_context.get("repeat_watch", 0) if user_context else 0)

    X = [[duration, is_compilation, view_count, repeat_watch]]
    pred = model.predict(X)[0]
    idx = int(max(0, min(100, round(pred))))
    if idx >= 80:
        level = "critical"
    elif idx >= 60:
        level = "high"
    elif idx >= 30:
        level = "moderate"
    else:
        level = "low"
    return {"addiction_index": idx, "risk_level": level}
