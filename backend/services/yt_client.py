# backend/services/yt_client.py
import os
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
import logging
logger = logging.getLogger("yt_client")

YT_API_KEY = os.getenv("YT_API_KEY", "YOUR_YT_API_KEY")

def build_youtube_client():
    return build("youtube", "v3", developerKey=YT_API_KEY)

def fetch_video_metadata(video_id):
    youtube = build_youtube_client()
    res = youtube.videos().list(part="snippet,contentDetails,statistics", id=video_id).execute()
    items = res.get("items", [])
    if not items:
        return None
    item = items[0]
    snippet = item["snippet"]
    content = item.get("contentDetails", {})
    stats = item.get("statistics", {})
    meta = {
        "id": video_id,
        "title": snippet.get("title",""),
        "description": snippet.get("description",""),
        "channel": snippet.get("channelTitle",""),
        "publishedAt": snippet.get("publishedAt",""),
        "duration": content.get("duration",""),
        "viewCount": int(stats.get("viewCount", 0)),
        "likeCount": int(stats.get("likeCount", 0)) if stats.get("likeCount") else None
    }
    return meta

def fetch_video_transcript(video_id):
    try:
        text_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        return " ".join([p["text"] for p in text_list])
    except (TranscriptsDisabled, NoTranscriptFound) as e:
        logger.debug(f"No transcript: {video_id} -> {e}")
        return ""
