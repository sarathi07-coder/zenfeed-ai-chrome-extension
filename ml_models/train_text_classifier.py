# ml_models/train_text_classifier.py
import os
import joblib
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

DATA_PATH = os.getenv("TEXT_DATA_PATH", "data/processed/sample_dataset.csv")
MODEL_OUT = os.getenv("TEXT_MODEL_OUT", "ml_models/text_classifier.pkl")

def load_data(path=DATA_PATH):
    return pd.read_csv(path)

def train():
    df = load_data()
    X = (df["title"].fillna("") + " " + df["description"].fillna("")).values
    y = df["label"].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1,2), max_features=10000)),
        ("clf", LogisticRegression(max_iter=200))
    ])
    pipeline.fit(X_train, y_train)
    preds = pipeline.predict(X_test)
    print(classification_report(y_test, preds))
    os.makedirs(os.path.dirname(MODEL_OUT), exist_ok=True)
    joblib.dump(pipeline, MODEL_OUT)
    print(f"Saved text classifier to {MODEL_OUT}")
    return pipeline

if __name__ == "__main__":
    train()
