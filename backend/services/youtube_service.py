"""
YouTube Data API Service

Handles YouTube API interactions for searching alternative content.
"""

import os
import logging
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("ZenFeed.YouTubeService")


class YouTubeService:
    """
    YouTube Data API wrapper.
    
    Provides:
    - Video search
    - Metadata fetching
    - Quota management
    - Result caching
    """
    
    def __init__(self):
        """Initialize YouTube service."""
        self.api_key = os.getenv("YOUTUBE_API_KEY") or os.getenv("YT_API_KEY")
        self.youtube = None
        self.cache = {}
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize YouTube API client."""
        if not self.api_key or self.api_key == "mock_key":
            logger.warning("No YouTube API key found, using mock mode")
            return
        
        try:
            from googleapiclient.discovery import build
            self.youtube = build('youtube', 'v3', developerKey=self.api_key)
            logger.info("YouTube API client initialized")
        except ImportError:
            logger.error("google-api-python-client not installed")
        except Exception as e:
            logger.error(f"Failed to initialize YouTube client: {e}")
    
    def search(
        self,
        query: str,
        max_results: int = 3,
        order: str = "relevance"
    ) -> List[Dict[str, Any]]:
        """
        Search for videos.
        
        Args:
            query: Search query
            max_results: Maximum number of results
            order: Sort order (relevance, viewCount, date, rating)
            
        Returns:
            List of video results
        """
        # Check cache first
        cache_key = f"{query}_{max_results}_{order}"
        if cache_key in self.cache:
            logger.info(f"Using cached results for: {query}")
            return self.cache[cache_key]
        
        if not self.youtube:
            logger.warning("YouTube client not available, using mock results")
            return self._mock_search(query, max_results)
        
        try:
            # Call YouTube API
            request = self.youtube.search().list(
                part="snippet",
                q=query,
                type="video",
                maxResults=max_results,
                order=order,
                relevanceLanguage="en",
                safeSearch="moderate"
            )
            
            response = request.execute()
            
            # Parse results
            results = []
            for item in response.get("items", []):
                video_id = item["id"]["videoId"]
                snippet = item["snippet"]
                
                results.append({
                    "video_id": video_id,
                    "title": snippet["title"],
                    "description": snippet["description"],
                    "channel": snippet["channelTitle"],
                    "thumbnail": snippet["thumbnails"]["default"]["url"],
                    "url": f"https://www.youtube.com/watch?v={video_id}",
                    "published_at": snippet["publishedAt"]
                })
            
            # Cache results
            self.cache[cache_key] = results
            
            logger.info(f"Found {len(results)} results for: {query}")
            return results
            
        except Exception as e:
            logger.error(f"YouTube search failed: {e}")
            return self._mock_search(query, max_results)
    
    def _mock_search(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Generate mock search results."""
        mock_results = []
        
        query_lower = query.lower()
        
        # Generate contextual mock results
        if "study" in query_lower or "pomodoro" in query_lower:
            mock_results.append({
                "video_id": "mock_study_001",
                "title": "Study With Me - 30 min Pomodoro Focus Session",
                "description": "Productive study session with timer and focus music",
                "channel": "Study Vibes",
                "thumbnail": "https://via.placeholder.com/120x90?text=Study",
                "url": "https://youtube.com/watch?v=mock_study_001",
                "published_at": "2024-01-01T00:00:00Z",
                "duration": 1800
            })
        
        if "meditation" in query_lower or "mindful" in query_lower:
            mock_results.append({
                "video_id": "mock_meditation_001",
                "title": "5-Minute Guided Meditation for Focus",
                "description": "Quick meditation to reset your mind",
                "channel": "Mindful Moments",
                "thumbnail": "https://via.placeholder.com/120x90?text=Meditation",
                "url": "https://youtube.com/watch?v=mock_meditation_001",
                "published_at": "2024-01-01T00:00:00Z",
                "duration": 300
            })
        
        if "tutorial" in query_lower or "learn" in query_lower:
            mock_results.append({
                "video_id": "mock_tutorial_001",
                "title": "Python Tutorial for Beginners - 10 Minutes",
                "description": "Quick introduction to Python programming",
                "channel": "Code Academy",
                "thumbnail": "https://via.placeholder.com/120x90?text=Tutorial",
                "url": "https://youtube.com/watch?v=mock_tutorial_001",
                "published_at": "2024-01-01T00:00:00Z",
                "duration": 600
            })
        
        if "exercise" in query_lower or "workout" in query_lower:
            mock_results.append({
                "video_id": "mock_exercise_001",
                "title": "Quick Desk Exercises - 5 Minutes",
                "description": "Simple exercises you can do at your desk",
                "channel": "Fitness Quick",
                "thumbnail": "https://via.placeholder.com/120x90?text=Exercise",
                "url": "https://youtube.com/watch?v=mock_exercise_001",
                "published_at": "2024-01-01T00:00:00Z",
                "duration": 300
            })
        
        # Fill remaining slots with generic productive content
        while len(mock_results) < max_results:
            idx = len(mock_results) + 1
            mock_results.append({
                "video_id": f"mock_productive_{idx:03d}",
                "title": f"Productive Content {idx}: {query.title()}",
                "description": f"Educational content related to: {query}",
                "channel": "Productive Channel",
                "thumbnail": f"https://via.placeholder.com/120x90?text=Video{idx}",
                "url": f"https://youtube.com/watch?v=mock_productive_{idx:03d}",
                "published_at": "2024-01-01T00:00:00Z",
                "duration": 600
            })
        
        return mock_results[:max_results]
    
    def get_video_details(self, video_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a video.
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            Video details or None
        """
        if not self.youtube:
            return None
        
        try:
            request = self.youtube.videos().list(
                part="snippet,contentDetails,statistics",
                id=video_id
            )
            
            response = request.execute()
            
            if not response.get("items"):
                return None
            
            item = response["items"][0]
            snippet = item["snippet"]
            details = item["contentDetails"]
            stats = item["statistics"]
            
            return {
                "video_id": video_id,
                "title": snippet["title"],
                "description": snippet["description"],
                "channel": snippet["channelTitle"],
                "duration": details["duration"],
                "view_count": int(stats.get("viewCount", 0)),
                "like_count": int(stats.get("likeCount", 0)),
                "comment_count": int(stats.get("commentCount", 0))
            }
            
        except Exception as e:
            logger.error(f"Failed to get video details: {e}")
            return None


# Test the service
if __name__ == "__main__":
    service = YouTubeService()
    
    results = service.search("study with me pomodoro", max_results=3)
    
    import json
    print(json.dumps(results, indent=2))
