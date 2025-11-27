"""
Addiction Scoring Agent (ASA)

Calculates addiction risk index (0-100) based on content classification
and behavioral signals.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base_agent import BaseAgent
from typing import Dict, Any
from datetime import datetime


class AddictionScoringAgent(BaseAgent):
    """
    Addiction Scoring Agent - Computes addiction risk metrics.
    
    Responsibilities:
    - Calculate Addiction Index (0-100)
    - Determine risk level (low/moderate/high/critical)
    - Recommend intervention type
    - Identify major contributing factors
    """
    
    def __init__(self, name: str):
        super().__init__(name)
        
        # Category base scores
        self.category_scores = {
            "harmful": 90,
            "addictive": 70,
            "entertainment": 40,
            "neutral": 20,
            "productive": 10,
            "educational": 5
        }
        
        # Trigger weights
        self.trigger_weights = {
            "short_duration": 10,
            "compilation": 10,
            "humor": 5,
            "shock": 8,
            "FOMO": 12,
            "clickbait": 7,
            "repetition": 15
        }
    
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate addiction score.
        
        Args:
            data: Contains classification results and behavioral context
            
        Returns:
            Addiction analysis with index, risk level, and recommended action
        """
        self.log("Calculating addiction score...")
        
        try:
            # Extract classification
            classification = data.get("classification", {})
            if isinstance(classification, dict) and "data" in classification:
                classification = classification["data"]
            
            # Extract behavioral context
            context = data.get("context", {})
            
            # Calculate base score from category
            category = classification.get("category", "neutral")
            base_score = self.category_scores.get(category, 20)
            
            # Add trigger contributions
            triggers = classification.get("triggers", [])
            trigger_score = sum(self.trigger_weights.get(t, 5) for t in triggers)
            
            # Add behavioral factors
            behavioral_score = self._calculate_behavioral_score(context)
            
            # Calculate final index (capped at 100)
            addiction_index = min(100, base_score + trigger_score + behavioral_score)
            
            # Determine risk level
            risk_level = self._determine_risk_level(addiction_index)
            
            # Recommend action
            recommended_action = self._recommend_action(addiction_index, risk_level)
            
            # Identify major factors
            major_factors = self._identify_major_factors(
                category, triggers, context, behavioral_score
            )
            
            result = {
                "addiction_index": addiction_index,
                "risk_level": risk_level,
                "recommended_action": recommended_action,
                "major_factors": major_factors,
                "breakdown": {
                    "base_score": base_score,
                    "trigger_score": trigger_score,
                    "behavioral_score": behavioral_score
                }
            }
            
            self.log(f"Addiction Index: {addiction_index}/100 ({risk_level} risk)")
            
            return self.create_response("success", result)
            
        except Exception as e:
            return self.handle_error(e, "Addiction scoring")
    
    def _calculate_behavioral_score(self, context: Dict[str, Any]) -> int:
        """
        Calculate score contribution from behavioral signals.
        
        Args:
            context: Behavioral context (session time, repeat count, etc.)
            
        Returns:
            Behavioral score contribution
        """
        score = 0
        
        # Session duration (minutes in last hour)
        session_minutes = context.get("session_minutes", 0)
        if session_minutes > 60:
            score += 20
        elif session_minutes > 30:
            score += 15
        elif session_minutes > 15:
            score += 10
        elif session_minutes > 5:
            score += 5
        
        # Repeat viewing pattern
        repeat_count = context.get("repeat_count", 0)
        if repeat_count > 5:
            score += 20
        elif repeat_count > 2:
            score += 15
        elif repeat_count > 0:
            score += 10
        
        # Time of day (late night = higher risk)
        time_of_day = context.get("time_of_day", "")
        if time_of_day:
            try:
                hour = int(time_of_day.split(":")[0])
                if 23 <= hour or hour < 6:  # Late night / early morning
                    score += 10
            except:
                pass
        
        # User explicitly searched (lower risk)
        if context.get("user_searched", False):
            score -= 5
        
        return max(0, score)
    
    def _determine_risk_level(self, addiction_index: int) -> str:
        """Determine risk level from addiction index."""
        if addiction_index >= 81:
            return "critical"
        elif addiction_index >= 61:
            return "high"
        elif addiction_index >= 31:
            return "moderate"
        else:
            return "low"
    
    def _recommend_action(self, addiction_index: int, risk_level: str) -> str:
        """
        Recommend intervention action.
        
        Args:
            addiction_index: Addiction score
            risk_level: Risk level
            
        Returns:
            Recommended action type
        """
        if addiction_index >= 91:
            return "lockout"
        elif addiction_index >= 81:
            return "replace"
        elif addiction_index >= 61:
            return "blur"
        elif addiction_index >= 30:
            return "nudge"
        else:
            return "none"
    
    def _identify_major_factors(
        self,
        category: str,
        triggers: list,
        context: Dict[str, Any],
        behavioral_score: int
    ) -> list:
        """
        Identify major contributing factors to addiction score.
        
        Returns:
            List of factor descriptions
        """
        factors = []
        
        # Category factor
        if category in ["addictive", "harmful"]:
            factors.append(f"Content category: {category}")
        
        # Trigger factors
        high_weight_triggers = [t for t in triggers if self.trigger_weights.get(t, 0) >= 10]
        if high_weight_triggers:
            factors.append(f"High-risk triggers: {', '.join(high_weight_triggers)}")
        
        # Behavioral factors
        if behavioral_score >= 15:
            if context.get("session_minutes", 0) > 30:
                factors.append("Extended session duration")
            if context.get("repeat_count", 0) > 2:
                factors.append("Repeated viewing pattern")
            
            time_of_day = context.get("time_of_day", "")
            if time_of_day:
                try:
                    hour = int(time_of_day.split(":")[0])
                    if 23 <= hour or hour < 6:
                        factors.append("Late-night usage")
                except:
                    pass
        
        return factors if factors else ["Low-risk content"]


# Test the agent
if __name__ == "__main__":
    agent = AddictionScoringAgent("ASA_Test")
    
    test_data = {
        "classification": {
            "category": "addictive",
            "triggers": ["short_duration", "compilation", "humor"],
            "confidence": 0.89
        },
        "context": {
            "session_minutes": 35,
            "repeat_count": 3,
            "time_of_day": "23:45",
            "user_searched": False
        }
    }
    
    result = agent.process(test_data)
    
    import json
    print(json.dumps(result, indent=2))
