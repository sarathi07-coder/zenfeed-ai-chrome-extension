"""
Recommendation Optimizer Agent (ROA)

Searches for and ranks productive alternative content to replace
addictive items.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base_agent import BaseAgent
from typing import Dict, Any, List


class RecommendationOptimizerAgent(BaseAgent):
    """
    Recommendation Optimizer Agent - Finds healthy alternatives.
    
    Responsibilities:
    - Search for productive alternatives using YouTube Data API
    - Rank suggestions by relevance + educational value
    - Provide 3 alternatives per addictive item
    - Cache results to minimize API quota usage
    """
    
    def __init__(self, name: str):
        super().__init__(name)
        self.youtube_service = None
        self.llm_client = None
        self.cache = {}
        self._initialize_services()
    
    def _initialize_services(self):
        """Initialize external services (YouTube API, LLM)."""
        # Initialize YouTube Service
        try:
            sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'backend', 'services'))
            from youtube_service import YouTubeService
            self.youtube_service = YouTubeService()
            self.log("YouTube service initialized")
        except Exception as e:
            self.log(f"Failed to initialize YouTube service: {e}", "WARNING")
            self.youtube_service = None

        # Initialize LLM Client
        try:
            from llm_client import get_llm_client
            self.llm_client = get_llm_client("gemini")
            self.log("LLM client initialized")
        except Exception as e:
            self.log(f"Failed to initialize LLM client: {e}", "WARNING")
            self.llm_client = None

    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate alternative recommendations.
        
        Args:
            data: Contains title, category, addiction_index
            
        Returns:
            List of alternative content suggestions
        """
        self.log("Generating recommendations...")
        
        try:
            title = data.get("title", "")
            category = data.get("category", "unknown")
            addiction_index = data.get("addiction_index", 0)
            max_results = data.get("max_results", 3)
            
            # Check cache first
            cache_key = f"{title}_{category}"
            if cache_key in self.cache:
                self.log("Using cached recommendations")
                return self.create_response("success", self.cache[cache_key])
            
            # Generate search queries based on category
            search_queries = self._generate_search_queries(title, category)
            
            # Search for alternatives
            alternatives = []
            for query in search_queries[:max_results]:
                if self.youtube_service:
                    # Use YouTube API
                    results = self.youtube_service.search(query, max_results=1)
                    if results:
                        alternatives.append(self._format_youtube_result(results[0], query))
                else:
                    # Use mock alternatives
                    alternatives.append(self._generate_mock_alternative(query))
            
            # Ensure we have at least 3 alternatives
            while len(alternatives) < 3:
                alternatives.append(self._generate_mock_alternative(
                    f"productive content {len(alternatives) + 1}"
                ))
            
            result = {"alternatives": alternatives[:max_results]}
            
            # Cache the result
            self.cache[cache_key] = result
            
            self.log(f"Generated {len(alternatives)} alternatives")
            
            return self.create_response("success", result)
            
        except Exception as e:
            return self.handle_error(e, "Recommendation generation")

    def _generate_search_queries(self, title: str, category: str) -> List[str]:
        """
        Generate search queries for productive alternatives using Gemini.
        
        Args:
            title: Original content title
            category: Content category
            
        Returns:
            List of search queries
        """
        # Default fallback queries
        default_queries = [
            "python programming tutorial for beginners",
            "productivity tips for students",
            "5 minute meditation for focus"
        ]

        if not self.llm_client:
            self.log("LLM client not available, using default queries", "WARNING")
            return default_queries

        try:
            # Import prompts
            sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'backend', 'core'))
            from prompts import ROA_SYSTEM_PROMPT, format_roa_prompt
            
            # User preferences (could be fetched from a profile service in the future)
            user_prefs = {
                "interests": ["coding", "productivity", "meditation", "science"],
                "preferred_languages": ["python", "java", "javascript", "english", "tamil"],
                "goals": ["learn programming", "improve focus", "reduce screen time"]
            }

            # Format prompt
            user_prompt = format_roa_prompt(
                content={"title": title, "category": category},
                addiction_index=75, # Default high index to trigger good suggestions
                user_prefs=user_prefs
            )

            # Generate with LLM
            response = self.llm_client.generate(
                system_prompt=ROA_SYSTEM_PROMPT,
                user_prompt=user_prompt,
                temperature=0.7
            )

            if not response:
                return default_queries

            # Parse JSON response
            data = self.llm_client.parse_json_response(response)
            
            if not data or "alternatives" not in data:
                return default_queries

            # Extract search queries from the alternatives
            queries = [alt.get("search_query") for alt in data["alternatives"] if alt.get("search_query")]
            
            if not queries:
                return default_queries
                
            self.log(f"Generated dynamic queries: {queries}")
            return queries

        except Exception as e:
            self.log(f"Error generating queries with LLM: {e}", "ERROR")
            return default_queries
    
    def _format_youtube_result(self, result: Dict[str, Any], query: str) -> Dict[str, Any]:
        """Format YouTube API result as alternative."""
        return {
            "title": result.get("title", ""),
            "url": result.get("url", ""),
            "reason": f"Productive alternative matching: {query}",
            "search_query": query,
            "type": "video",
            "estimated_duration": result.get("duration", 600)
        }
    
    def _generate_mock_alternative(self, query: str) -> Dict[str, Any]:
        """Generate mock alternative for testing."""
        mock_alternatives = {
            "study with me": {
                "title": "Study With Me - 30 min Pomodoro Focus Session",
                "url": "https://youtube.com/watch?v=demo_study",
                "reason": "Structured study time with proven productivity technique",
                "type": "video",
                "estimated_duration": 1800
            },
            "meditation": {
                "title": "5-Minute Meditation Break for Focus",
                "url": "https://youtube.com/watch?v=demo_meditation",
                "reason": "Quick mental reset to improve concentration",
                "type": "guided_exercise",
                "estimated_duration": 300
            },
            "tutorial": {
                "title": "Python Basics - 10 Minute Tutorial",
                "url": "https://youtube.com/watch?v=demo_python",
                "reason": "Learn a valuable skill in short time",
                "type": "video",
                "estimated_duration": 600
            },
            "exercise": {
                "title": "Quick Desk Exercises - 5 Minutes",
                "url": "https://youtube.com/watch?v=demo_exercise",
                "reason": "Physical activity to boost energy and focus",
                "type": "guided_exercise",
                "estimated_duration": 300
            },
            "productivity": {
                "title": "3 Productivity Hacks That Actually Work",
                "url": "https://youtube.com/watch?v=demo_productivity",
                "reason": "Practical tips to improve daily efficiency",
                "type": "video",
                "estimated_duration": 480
            }
        }
        
        # Find matching mock alternative
        query_lower = query.lower()
        for key, alt in mock_alternatives.items():
            if key in query_lower:
                return {**alt, "search_query": query}
        
        # Default mock alternative
        return {
            "title": f"Productive Content: {query.title()}",
            "url": f"https://youtube.com/search?q={query.replace(' ', '+')}",
            "reason": "Healthy alternative to addictive content",
            "search_query": query,
            "type": "video",
            "estimated_duration": 600
        }


# Test the agent
if __name__ == "__main__":
    agent = RecommendationOptimizerAgent("ROA_Test")
    
    test_data = {
        "title": "Funny Memes Compilation",
        "category": "addictive",
        "addiction_index": 75,
        "max_results": 3
    }
    
    result = agent.process(test_data)
    
    import json
    print(json.dumps(result, indent=2))
