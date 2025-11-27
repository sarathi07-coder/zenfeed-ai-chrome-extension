"""
Feed Ingestion Agent (FIA)

Collects and normalizes feed data from YouTube/Instagram.
Validates and structures content items for downstream agents.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base_agent import BaseAgent
from typing import Dict, Any


class FeedIngestionAgent(BaseAgent):
    """
    Feed Ingestion Agent - First agent in the pipeline.
    
    Responsibilities:
    - Validate incoming content metadata
    - Normalize data structure
    - Extract platform-specific features
    - Add context information
    """
    
    def __init__(self, name: str):
        super().__init__(name)
        self.required_fields = ["title"]
        self.supported_platforms = ["youtube", "instagram"]
    
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process and normalize feed item data.
        
        Args:
            data: Raw content item from extension
            
        Returns:
            Normalized content item with metadata
        """
        self.log("Processing feed item...")
        
        try:
            # Validate required fields
            if not self.validate_input(data, self.required_fields):
                return self.handle_error(
                    ValueError("Missing required fields"),
                    "Input validation"
                )
            
            # Normalize platform
            platform = data.get("platform", "youtube").lower()
            if platform not in self.supported_platforms:
                self.log(f"Unsupported platform: {platform}, defaulting to youtube", "WARNING")
                platform = "youtube"
            
            # Extract and normalize fields
            normalized = {
                "id": data.get("id", self._generate_id(data)),
                "title": data.get("title", "").strip(),
                "url": data.get("url", ""),
                "duration_sec": data.get("duration_sec", 0),
                "channel": data.get("channel", "Unknown"),
                "thumbnail": data.get("thumbnail", ""),
                "description": data.get("description", ""),
                "platform": platform,
                "metadata": {
                    "has_duration": data.get("duration_sec") is not None,
                    "has_thumbnail": bool(data.get("thumbnail")),
                    "title_length": len(data.get("title", "")),
                    "has_description": bool(data.get("description"))
                }
            }
            
            # Add context
            context = self._extract_context(normalized)
            
            self.log(f"Successfully processed: {normalized['title'][:50]}...")
            
            return self.create_response(
                status="success",
                data={
                    "raw_feed": normalized,
                    "context": context,
                    "user_history": data.get("user_history", [])
                }
            )
            
        except Exception as e:
            return self.handle_error(e, "Feed ingestion")
    
    def _generate_id(self, data: Dict[str, Any]) -> str:
        """Generate unique ID for content item if not provided."""
        import hashlib
        content = f"{data.get('title', '')}{data.get('url', '')}"
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    def _extract_context(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract contextual features from the item.
        
        Args:
            item: Normalized content item
            
        Returns:
            Context dictionary with extracted features
        """
        context = {
            "platform": item["platform"],
            "content_type": self._infer_content_type(item),
            "duration_category": self._categorize_duration(item["duration_sec"]),
            "title_indicators": self._extract_title_indicators(item["title"])
        }
        
        return context
    
    def _infer_content_type(self, item: Dict[str, Any]) -> str:
        """Infer content type from metadata."""
        duration = item.get("duration_sec", 0)
        
        if duration < 60:
            return "short_form"  # Shorts, Reels
        elif duration < 600:
            return "medium_form"  # Regular videos
        else:
            return "long_form"  # Long videos, streams
    
    def _categorize_duration(self, duration_sec: int) -> str:
        """Categorize video duration."""
        if duration_sec < 60:
            return "under_1min"
        elif duration_sec < 300:
            return "1_to_5min"
        elif duration_sec < 900:
            return "5_to_15min"
        elif duration_sec < 3600:
            return "15min_to_1hr"
        else:
            return "over_1hr"
    
    def _extract_title_indicators(self, title: str) -> Dict[str, bool]:
        """
        Extract boolean indicators from title.
        
        These help downstream agents make quick decisions.
        """
        title_lower = title.lower()
        
        # Addictive indicators
        addictive_keywords = [
            "try not to laugh", "compilation", "meme", "funny",
            "best of", "fails", "reaction", "tiktok", "viral"
        ]
        
        # Educational indicators
        educational_keywords = [
            "tutorial", "learn", "study", "lecture", "course",
            "guide", "how to", "explained", "documentary"
        ]
        
        # Clickbait indicators
        clickbait_keywords = [
            "you won't believe", "shocking", "must see", "gone wrong",
            "insane", "crazy", "unbelievable"
        ]
        
        return {
            "has_addictive_keywords": any(kw in title_lower for kw in addictive_keywords),
            "has_educational_keywords": any(kw in title_lower for kw in educational_keywords),
            "has_clickbait_keywords": any(kw in title_lower for kw in clickbait_keywords),
            "has_numbers": any(char.isdigit() for char in title),
            "has_caps": any(word.isupper() and len(word) > 2 for word in title.split()),
            "has_emoji": any(ord(char) > 127 for char in title)
        }


# Test the agent
if __name__ == "__main__":
    agent = FeedIngestionAgent("FIA_Test")
    
    test_item = {
        "title": "Try Not To Laugh - Funny Memes Compilation 2024",
        "url": "https://youtube.com/watch?v=test123",
        "duration_sec": 45,
        "channel": "MemeWorld",
        "platform": "youtube"
    }
    
    result = agent.process(test_item)
    
    import json
    print(json.dumps(result, indent=2))
