# backend/services/ingestion_service.py
import re
from urllib.parse import parse_qs, urlparse

from .yt_client import fetch_video_metadata, fetch_video_transcript

def extract_video_id_from_url(url: str):
    # supports youtube watch urls and youtu.be
    if "youtu.be/" in url:
        return url.split("youtu.be/")[-1].split("?")[0]
    qs = parse_qs(urlparse(url).query)
    return qs.get("v", [None])[0]

def ingest_from_url(url: str):
    vid = extract_video_id_from_url(url)
    if not vid:
        return {"error": "invalid_url", "url": url}
    meta = fetch_video_metadata(vid)
    transcript = fetch_video_transcript(vid)
    meta["transcript"] = transcript
    return meta
