# ml_models/embeddings.py
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import os
import joblib

MODEL_NAME = os.getenv("EMBED_MODEL", "all-MiniLM-L6-v2")
EMB_MODEL = SentenceTransformer(MODEL_NAME)

def embed_texts(texts):
    # texts: list[str]
    return EMB_MODEL.encode(texts, show_progress_bar=True, convert_to_numpy=True)

def build_faiss_index(embeddings, ids=None, index_path=None):
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    if index_path:
        faiss.write_index(index, index_path)
        if ids is not None:
            joblib.dump(ids, index_path + ".ids")
    return index

def load_faiss_index(index_path):
    index = faiss.read_index(index_path)
    ids = joblib.load(index_path + ".ids")
    return index, ids

def search_index(index, query_emb, top_k=5):
    D, I = index.search(query_emb.reshape(1, -1), top_k)
    return I[0], D[0]
