"""
LLM Client Service

Handles communication with LLM APIs (Gemini, OpenAI, etc.)
Provides unified interface for all agents.
"""

import os
import json
import logging
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger("ZenFeed.LLMClient")


class LLMClient:
    """
    Unified LLM client supporting multiple providers.
    
    Supports:
    - Google Gemini
    - OpenAI GPT
    - Anthropic Claude (fallback)
    """
    
    def __init__(self, provider: str = "gemini"):
        """
        Initialize LLM client.
        
        Args:
            provider: LLM provider ("gemini", "openai", "anthropic")
        """
        self.provider = provider.lower()
        self.api_key = self._get_api_key()
        self.client = self._initialize_client()
        
        logger.info(f"LLM Client initialized with provider: {self.provider}")
    
    def _get_api_key(self) -> str:
        """Get API key from environment."""
        if self.provider == "gemini":
            key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        elif self.provider == "openai":
            key = os.getenv("OPENAI_API_KEY")
        elif self.provider == "anthropic":
            key = os.getenv("ANTHROPIC_API_KEY")
        else:
            raise ValueError(f"Unknown provider: {self.provider}")
        
        if not key:
            logger.warning(f"No API key found for {self.provider}, using mock mode")
            return "mock_key"
        
        return key
    
    def _initialize_client(self):
        """Initialize provider-specific client."""
        if self.api_key == "mock_key":
            return None  # Mock mode
        
        try:
            if self.provider == "gemini":
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                return genai.GenerativeModel('gemini-2.0-flash')
            
            elif self.provider == "openai":
                from openai import OpenAI
                return OpenAI(api_key=self.api_key)
            
            elif self.provider == "anthropic":
                from anthropic import Anthropic
                return Anthropic(api_key=self.api_key)
            
        except ImportError as e:
            logger.error(f"Failed to import {self.provider} library: {e}")
            return None
        except Exception as e:
            logger.error(f"Failed to initialize {self.provider} client: {e}")
            return None
    
    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 500
    ) -> Optional[str]:
        """
        Generate completion from LLM.
        
        Args:
            system_prompt: System instruction
            user_prompt: User message
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text or None if failed
        """
        if not self.client:
            logger.warning("No LLM client available, using mock response")
            return self._mock_response(user_prompt)
        
        try:
            if self.provider == "gemini":
                return self._generate_gemini(system_prompt, user_prompt, temperature)
            
            elif self.provider == "openai":
                return self._generate_openai(system_prompt, user_prompt, temperature, max_tokens)
            
            elif self.provider == "anthropic":
                return self._generate_anthropic(system_prompt, user_prompt, temperature, max_tokens)
            
        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            return self._mock_response(user_prompt)
    
    def _generate_gemini(self, system_prompt: str, user_prompt: str, temperature: float) -> str:
        """Generate using Gemini."""
        # Gemini combines system and user prompts
        full_prompt = f"{system_prompt}\n\n{user_prompt}"
        
        response = self.client.generate_content(
            full_prompt,
            generation_config={
                "temperature": temperature,
                "max_output_tokens": 500
            }
        )
        
        return response.text
    
    def _generate_openai(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float,
        max_tokens: int
    ) -> str:
        """Generate using OpenAI."""
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        return response.choices[0].message.content
    
    def _generate_anthropic(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float,
        max_tokens: int
    ) -> str:
        """Generate using Anthropic Claude."""
        response = self.client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_prompt}
            ]
        )
        
        return response.content[0].text
    
    def _mock_response(self, user_prompt: str) -> str:
        """
        Generate mock response for testing without API key.
        
        Returns realistic JSON responses based on prompt content.
        """
        prompt_lower = user_prompt.lower()
        
        # Mock CCA response
        if "classify this content" in prompt_lower or "classification" in prompt_lower:
            if "meme" in prompt_lower or "funny" in prompt_lower or "compilation" in prompt_lower:
                return json.dumps({
                    "category": "addictive",
                    "reason": "Short-form compilation triggers dopamine loops",
                    "triggers": ["short_duration", "compilation", "humor"],
                    "thumbnail_sentiment": "clickbait",
                    "confidence": 0.89
                })
            elif "tutorial" in prompt_lower or "learn" in prompt_lower:
                return json.dumps({
                    "category": "educational",
                    "reason": "Tutorial content for skill development",
                    "triggers": [],
                    "thumbnail_sentiment": "positive",
                    "confidence": 0.92
                })
            else:
                return json.dumps({
                    "category": "neutral",
                    "reason": "General content without strong indicators",
                    "triggers": [],
                    "thumbnail_sentiment": "neutral",
                    "confidence": 0.65
                })
        
        # Mock ASA response
        elif "addiction score" in prompt_lower or "compute addiction" in prompt_lower:
            return json.dumps({
                "addiction_index": 72,
                "major_factors": ["short_duration", "compilation", "repeat_viewing"],
                "risk_level": "high",
                "recommended_action": "blur"
            })
        
        # Mock ROA response
        elif "alternatives" in prompt_lower or "suggest" in prompt_lower:
            return json.dumps({
                "alternatives": [
                    {
                        "title": "Study With Me - 30 min Pomodoro Focus Session",
                        "reason": "Productive alternative with structured time",
                        "search_query": "study with me pomodoro 30 minutes",
                        "type": "video",
                        "estimated_duration": 1800
                    },
                    {
                        "title": "5-Minute Meditation Break for Focus",
                        "reason": "Quick mental reset to improve concentration",
                        "search_query": "5 minute meditation focus",
                        "type": "guided_exercise",
                        "estimated_duration": 300
                    },
                    {
                        "title": "Python Basics - 10 Minute Tutorial",
                        "reason": "Learn a valuable skill in short time",
                        "search_query": "python tutorial 10 minutes beginner",
                        "type": "video",
                        "estimated_duration": 600
                    }
                ]
            })
        
        # Mock BMA response
        elif "behavior" in prompt_lower or "analyze" in prompt_lower:
            return json.dumps({
                "user_summary": {
                    "avg_daily_addictive_minutes": 45,
                    "streak_days": 3,
                    "trend": "increasing"
                },
                "early_warning": True,
                "suggested_intervention_schedule": "Increase nudges during evening hours (6-10 PM)",
                "insights": [
                    "Late-night usage pattern detected",
                    "Increased short-form content consumption",
                    "Declining engagement with educational content"
                ]
            })
        
        # Mock CECA response
        elif "ui instructions" in prompt_lower or "generate ui" in prompt_lower:
            return json.dumps({
                "intervention_type": "blur",
                "overlay_text": "Take a mindful break 🧘",
                "cta_buttons": [
                    {"label": "Show Alternatives", "action_key": "show_alternatives"},
                    {"label": "Reveal Content", "action_key": "reveal"}
                ],
                "css_snippet": "",
                "timer_seconds": None
            })
        
        # Default mock response
        return json.dumps({
            "status": "mock",
            "message": "Mock LLM response (no API key configured)"
        })
    
    def parse_json_response(self, response: str) -> Optional[Dict[str, Any]]:
        """
        Parse JSON from LLM response.
        
        Handles cases where LLM includes extra text around JSON.
        
        Args:
            response: Raw LLM response
            
        Returns:
            Parsed JSON dict or None if parsing failed
        """
        if not response:
            return None
        
        try:
            # Try direct parse first
            return json.loads(response)
        except json.JSONDecodeError:
            # Try to extract JSON from markdown code blocks
            if "```json" in response:
                start = response.find("```json") + 7
                end = response.find("```", start)
                json_str = response[start:end].strip()
                return json.loads(json_str)
            
            # Try to find JSON object in text
            start = response.find("{")
            end = response.rfind("}") + 1
            if start >= 0 and end > start:
                json_str = response[start:end]
                return json.loads(json_str)
            
            logger.error(f"Failed to parse JSON from response: {response[:100]}...")
            return None


# Global LLM client instance
_llm_client = None

def get_llm_client(provider: str = "gemini") -> LLMClient:
    """Get or create global LLM client instance."""
    global _llm_client
    if _llm_client is None:
        _llm_client = LLMClient(provider)
    return _llm_client


# Test the client
if __name__ == "__main__":
    client = LLMClient("gemini")
    
    test_prompt = """Classify this content:
    
    Title: "Try Not To Laugh - Funny Memes Compilation"
    Duration: 45 seconds
    
    Provide classification as JSON."""
    
    response = client.generate(
        system_prompt="You are a content classifier. Return JSON only.",
        user_prompt=test_prompt
    )
    
    print("Response:", response)
    
    parsed = client.parse_json_response(response)
    print("\nParsed JSON:", json.dumps(parsed, indent=2))
