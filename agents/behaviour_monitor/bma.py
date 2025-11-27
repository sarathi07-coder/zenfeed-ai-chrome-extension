"""
Behavior Monitor Agent (BMA)

Tracks long-term user behavior patterns and provides early warnings
for addiction escalation.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base_agent import BaseAgent
from typing import Dict, Any, List
from datetime import datetime, timedelta


class BehaviorMonitorAgent(BaseAgent):
    """
    Behavior Monitor Agent - Long-term pattern analysis.
    
    Responsibilities:
    - Track daily/weekly usage patterns
    - Detect doom-scrolling and binge behaviors
    - Identify late-night addiction patterns
    - Provide early warnings
    - Suggest intervention schedules
    """
    
    def __init__(self, name: str):
        super().__init__(name)
        # In-memory storage for demo (use database in production)
        self.user_data = {}
    
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze behavior patterns.
        
        Args:
            data: Contains content_item, addiction_index, category, or action request
            
        Returns:
            Behavior insights and warnings
        """
        self.log("Analyzing behavior patterns...")
        
        try:
            # Check if this is a stats request
            action = data.get("action")
            if action == "get_stats":
                user_id = data.get("user_id", "default")
                return self._get_user_stats(user_id)
            
            # Otherwise, update behavior tracking
            content_item = data.get("content_item", {})
            addiction_index = data.get("addiction_index", 0)
            category = data.get("category", "unknown")
            user_id = data.get("user_id", "default")
            
            # Update user behavior data
            self._update_user_behavior(user_id, content_item, addiction_index, category)
            
            # Analyze patterns
            insights = self._analyze_patterns(user_id)
            
            self.log(f"Behavior analysis complete. Early warning: {insights.get('early_warning', False)}")
            
            return self.create_response("success", insights)
            
        except Exception as e:
            return self.handle_error(e, "Behavior monitoring")
    
    def _update_user_behavior(
        self,
        user_id: str,
        content_item: Dict[str, Any],
        addiction_index: int,
        category: str
    ):
        """Update user behavior tracking."""
        if user_id not in self.user_data:
            self.user_data[user_id] = {
                "daily_minutes": [],
                "category_counts": {},
                "addiction_scores": [],
                "timestamps": [],
                "late_night_count": 0,
                "binge_sessions": 0
            }
        
        user = self.user_data[user_id]
        now = datetime.now()
        
        # Track timestamp
        user["timestamps"].append(now.isoformat())
        
        # Track addiction score
        user["addiction_scores"].append(addiction_index)
        
        # Track category
        if category not in user["category_counts"]:
            user["category_counts"][category] = 0
        user["category_counts"][category] += 1
        
        # Check for late-night usage
        if now.hour >= 23 or now.hour < 6:
            user["late_night_count"] += 1
        
        # Estimate minutes (rough approximation)
        duration = content_item.get("duration_sec", 0) / 60
        if user["daily_minutes"]:
            user["daily_minutes"][-1] += duration
        else:
            user["daily_minutes"].append(duration)
    
    def _analyze_patterns(self, user_id: str) -> Dict[str, Any]:
        """
        Analyze user behavior patterns.
        
        Args:
            user_id: User identifier
            
        Returns:
            Behavior insights and warnings
        """
        if user_id not in self.user_data:
            return {
                "user_summary": {
                    "avg_daily_addictive_minutes": 0,
                    "streak_days": 0,
                    "trend": "stable"
                },
                "early_warning": False,
                "suggested_intervention_schedule": "No intervention needed",
                "insights": []
            }
        
        user = self.user_data[user_id]
        
        # Calculate averages
        avg_addiction_score = (
            sum(user["addiction_scores"]) / len(user["addiction_scores"])
            if user["addiction_scores"] else 0
        )
        
        avg_daily_minutes = (
            sum(user["daily_minutes"]) / len(user["daily_minutes"])
            if user["daily_minutes"] else 0
        )
        
        # Detect trend
        trend = self._detect_trend(user["addiction_scores"])
        
        # Early warning conditions
        early_warning = (
            avg_addiction_score > 60 or
            avg_daily_minutes > 60 or
            user["late_night_count"] > 3 or
            trend == "increasing"
        )
        
        # Generate insights
        insights = self._generate_insights(user, avg_addiction_score, avg_daily_minutes)
        
        # Suggest intervention schedule
        intervention_schedule = self._suggest_intervention_schedule(
            user, early_warning, avg_addiction_score
        )
        
        return {
            "user_summary": {
                "avg_daily_addictive_minutes": round(avg_daily_minutes, 1),
                "avg_addiction_score": round(avg_addiction_score, 1),
                "streak_days": len(user["daily_minutes"]),
                "trend": trend,
                "total_items_viewed": len(user["addiction_scores"])
            },
            "early_warning": early_warning,
            "suggested_intervention_schedule": intervention_schedule,
            "insights": insights
        }
    
    def _detect_trend(self, scores: List[int]) -> str:
        """Detect trend in addiction scores."""
        if len(scores) < 3:
            return "stable"
        
        # Compare recent vs older scores
        recent = scores[-5:] if len(scores) >= 5 else scores[-3:]
        older = scores[:-5] if len(scores) >= 5 else scores[:-3]
        
        if not older:
            return "stable"
        
        recent_avg = sum(recent) / len(recent)
        older_avg = sum(older) / len(older)
        
        if recent_avg > older_avg * 1.25:
            return "increasing"
        elif recent_avg < older_avg * 0.75:
            return "decreasing"
        else:
            return "stable"
    
    def _generate_insights(
        self,
        user: Dict[str, Any],
        avg_score: float,
        avg_minutes: float
    ) -> List[str]:
        """Generate behavioral insights."""
        insights = []
        
        # Late-night usage
        if user["late_night_count"] > 3:
            insights.append("Late-night usage pattern detected (>3 sessions after 11 PM)")
        
        # High addiction score
        if avg_score > 70:
            insights.append(f"Average addiction score is high ({avg_score:.1f}/100)")
        
        # Excessive time
        if avg_minutes > 60:
            insights.append(f"Daily addictive content time exceeds 1 hour ({avg_minutes:.1f} min)")
        
        # Category distribution
        categories = user["category_counts"]
        if "addictive" in categories and categories["addictive"] > 5:
            insights.append(f"High consumption of addictive content ({categories['addictive']} items)")
        
        if "educational" in categories and categories["educational"] < 2:
            insights.append("Low engagement with educational content")
        
        # Positive insights
        if avg_score < 40:
            insights.append("Maintaining healthy content consumption patterns")
        
        return insights if insights else ["No concerning patterns detected"]
    
    def _suggest_intervention_schedule(
        self,
        user: Dict[str, Any],
        early_warning: bool,
        avg_score: float
    ) -> str:
        """Suggest intervention schedule based on patterns."""
        if not early_warning:
            return "Continue current monitoring. No additional interventions needed."
        
        suggestions = []
        
        # Late-night interventions
        if user["late_night_count"] > 3:
            suggestions.append("Increase intervention strength during evening hours (9 PM - 12 AM)")
        
        # High addiction score
        if avg_score > 70:
            suggestions.append("Apply blur interventions more aggressively")
        
        # Category-based
        if user["category_counts"].get("addictive", 0) > 5:
            suggestions.append("Proactively suggest alternatives for short-form content")
        
        return "; ".join(suggestions) if suggestions else "Monitor closely and adjust interventions as needed"
    
    def _get_user_stats(self, user_id: str) -> Dict[str, Any]:
        """Get user statistics."""
        if user_id not in self.user_data:
            return self.create_response("success", {
                "user_id": user_id,
                "message": "No data available for this user"
            })
        
        insights = self._analyze_patterns(user_id)
        return self.create_response("success", insights)


# Test the agent
if __name__ == "__main__":
    agent = BehaviorMonitorAgent("BMA_Test")
    
    # Simulate multiple content views
    for i in range(10):
        test_data = {
            "content_item": {
                "title": f"Video {i}",
                "duration_sec": 45 if i % 2 == 0 else 600
            },
            "addiction_index": 70 if i % 2 == 0 else 30,
            "category": "addictive" if i % 2 == 0 else "educational",
            "user_id": "test_user"
        }
        agent.process(test_data)
    
    # Get stats
    stats = agent.process({"action": "get_stats", "user_id": "test_user"})
    
    import json
    print(json.dumps(stats, indent=2))
