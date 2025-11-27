"""
Content Classification Agent (CCA)

Uses AI (Gemini LLM) to classify content into categories and detect
emotional triggers that may lead to addictive behavior.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base_agent import BaseAgent
from typing import Dict, Any
import json


class ContentClassificationAgent(BaseAgent):
    """
    Content Classification Agent - AI-powered content analysis.
    
    Responsibilities:
    - Classify content into categories (educational, productive, neutral, addictive, harmful)
    - Detect emotional triggers (FOMO, anger, excitement, etc.)
    - Analyze thumbnail sentiment
    - Provide confidence scores
    
    Uses LLM for deep semantic understanding.
    """
    
    def __init__(self, name: str):
        super().__init__(name)
        self.llm_client = None
        self._initialize_llm()
    
    def _initialize_llm(self):
        """Initialize LLM client."""
        try:
            # Import here to avoid circular dependency
            sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'backend', 'services'))
            from llm_client import get_llm_client
            self.llm_client = get_llm_client("gemini")
            self.log("LLM client initialized successfully")
        except Exception as e:
            self.log(f"Failed to initialize LLM client: {e}", "WARNING")
            self.llm_client = None
    
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Classify content using AI.
        
        Args:
            data: Feed item with metadata from FIA
            
        Returns:
            Classification results with category, triggers, confidence
        """
        self.log("Classifying content...")
        
        try:
            # Extract feed item
            feed_item = data.get("feed_item", data.get("raw_feed", data))
            
            if not feed_item:
                return self.handle_error(
                    ValueError("No feed item found in data"),
                    "Content classification"
                )
            
            # Try LLM classification first
            if self.llm_client:
                result = self._classify_with_llm(feed_item)
                if result:
                    self.log(f"LLM classification: {result.get('category')} (confidence: {result.get('confidence')})")
                    return self.create_response("success", result)
            
            # Fallback to heuristic classification
            self.log("Using heuristic classification (LLM unavailable)", "WARNING")
            result = self._classify_heuristic(feed_item)
            
            return self.create_response("success", result)
            
        except Exception as e:
            return self.handle_error(e, "Content classification")
    
    def _classify_with_llm(self, feed_item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Classify using LLM (Gemini).
        
        Args:
            feed_item: Content metadata
            
        Returns:
            Classification dict or None if failed
        """
        try:
            # Import prompts
            sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'backend', 'core'))
            from prompts import CCA_SYSTEM_PROMPT, format_cca_prompt
            
            # Format prompt with feed item data
            user_prompt = format_cca_prompt(feed_item)
            
            # Generate classification
            response = self.llm_client.generate(
                system_prompt=CCA_SYSTEM_PROMPT,
                user_prompt=user_prompt,
                temperature=0.3  # Lower temperature for more consistent classification
            )
            
            if not response:
                return None
            
            # Parse JSON response
            classification = self.llm_client.parse_json_response(response)
            
            if not classification:
                self.log("Failed to parse LLM response", "ERROR")
                return None
            
            # Validate classification
            if not self._validate_classification(classification):
                self.log("Invalid classification structure", "ERROR")
                return None
            
            return classification
            
        except Exception as e:
            self.log(f"LLM classification error: {e}", "ERROR")
            return None
    
    def _classify_heuristic(self, feed_item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fallback heuristic classification (rule-based).
        
        Args:
            feed_item: Content metadata
            
        Returns:
            Classification dict
        """
        title = feed_item.get("title", "").lower()
        duration = feed_item.get("duration_sec", 0)
        context = feed_item.get("context", {})
        title_indicators = context.get("title_indicators", {})
        
        # Determine category
        if title_indicators.get("has_educational_keywords"):
            category = "educational"
            confidence = 0.75
        elif title_indicators.get("has_addictive_keywords"):
            category = "addictive"
            confidence = 0.80
        elif title_indicators.get("has_clickbait_keywords"):
            category = "entertainment"
            confidence = 0.70
        else:
            category = "neutral"
            confidence = 0.60
        
        # Detect triggers
        triggers = []
        if duration < 60:
            triggers.append("short_duration")
        if "compilation" in title or "best of" in title:
            triggers.append("compilation")
        if any(kw in title for kw in ["funny", "meme", "laugh"]):
            triggers.append("humor")
        if any(kw in title for kw in ["shocking", "insane", "crazy"]):
            triggers.append("shock")
        if any(kw in title for kw in ["viral", "trending", "must see"]):
            triggers.append("FOMO")
        if title_indicators.get("has_clickbait_keywords"):
            triggers.append("clickbait")
        
        # Determine thumbnail sentiment
        if title_indicators.get("has_clickbait_keywords"):
            thumbnail_sentiment = "clickbait"
        elif category == "educational":
            thumbnail_sentiment = "positive"
        elif category == "addictive":
            thumbnail_sentiment = "negative"
        else:
            thumbnail_sentiment = "neutral"
        
        # Generate reason
        reason = self._generate_reason(category, triggers, duration)
        
        return {
            "category": category,
            "reason": reason,
            "triggers": triggers,
            "thumbnail_sentiment": thumbnail_sentiment,
            "confidence": confidence
        }
    
    def _validate_classification(self, classification: Dict[str, Any]) -> bool:
        """Validate classification structure."""
        required_fields = ["category", "reason", "triggers", "thumbnail_sentiment", "confidence"]
        
        if not all(field in classification for field in required_fields):
            return False
        
        valid_categories = ["educational", "productive", "neutral", "entertainment", "addictive", "harmful"]
        if classification["category"] not in valid_categories:
            return False
        
        if not isinstance(classification["triggers"], list):
            return False
        
        if not (0 <= classification["confidence"] <= 1):
            return False
        
        return True
    
    def _generate_reason(self, category: str, triggers: list, duration: int) -> str:
        """Generate human-readable reason for classification."""
        if category == "addictive":
            if "short_duration" in triggers and "compilation" in triggers:
                return "Short compilation triggers dopamine loops"
            elif "short_duration" in triggers:
                return "Short-form content encourages binge-watching"
            elif "compilation" in triggers:
                return "Compilation format promotes extended viewing"
            else:
                return "Content patterns suggest addictive potential"
        
        elif category == "educational":
            return "Educational content for skill development"
        
        elif category == "productive":
            return "Productive content aligned with goals"
        
        elif category == "harmful":
            return "Content may have negative impact"
        
        else:
            return "General content without strong indicators"


# Test the agent
if __name__ == "__main__":
    agent = ContentClassificationAgent("CCA_Test")
    
    test_item = {
        "feed_item": {
            "title": "Try Not To Laugh - Funny Memes Compilation 2024",
            "duration_sec": 45,
            "channel": "MemeWorld",
            "platform": "youtube",
            "context": {
                "content_type": "short_form",
                "title_indicators": {
                    "has_addictive_keywords": True,
                    "has_educational_keywords": False,
                    "has_clickbait_keywords": False
                }
            }
        }
    }
    
    result = agent.process(test_item)
    
    print(json.dumps(result, indent=2))
