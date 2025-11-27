"""
Chrome Extension Control Agent (CECA)

Translates intervention decisions into browser UI actions and DOM operations.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base_agent import BaseAgent
from typing import Dict, Any, List


class ExtensionControlAgent(BaseAgent):
    """
    Extension Control Agent - Browser UI controller.
    
    Responsibilities:
    - Translate orchestrator decisions into UI actions
    - Generate overlay text and buttons
    - Provide CSS snippets for interventions
    - Create timer displays
    """
    
    def __init__(self, name: str):
        super().__init__(name)
        
        # Intervention templates
        self.intervention_templates = {
            "blur": {
                "overlay_text": "High-Risk Content Detected ⚠️",
                "cta_buttons": [
                    {"label": "Show Alternatives", "action_key": "show_alternatives"},
                    {"label": "Reveal Content", "action_key": "reveal"}
                ]
            },
            "nudge": {
                "overlay_text": "Consider a productive alternative 💡",
                "cta_buttons": [
                    {"label": "Show Alternatives", "action_key": "show_alternatives"}
                ]
            },
            "replace": {
                "overlay_text": "Content Replaced with Alternatives 🎯",
                "cta_buttons": [
                    {"label": "View Alternatives", "action_key": "show_alternatives"}
                ]
            },
            "lockout": {
                "overlay_text": "Take a mindful break 🧘",
                "cta_buttons": [
                    {"label": "Set Timer", "action_key": "set_timer"}
                ],
                "timer_seconds": 300  # 5 minutes
            },
            "none": {
                "overlay_text": "",
                "cta_buttons": []
            }
        }
    
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate UI instructions for browser extension.
        
        Args:
            data: Contains decision, alternatives, addiction_index
            
        Returns:
            UI instructions with intervention type, overlay text, buttons, CSS
        """
        self.log("Generating UI instructions...")
        
        try:
            # Extract decision
            decision = data.get("decision", {})
            if isinstance(decision, dict) and "data" in decision:
                decision = decision["data"]
            
            intervention_type = decision.get("intervention_type", "none")
            addiction_index = data.get("addiction_index", 0)
            alternatives = data.get("alternatives", [])
            locale = data.get("locale", "en-US")
            
            # Get base template
            template = self.intervention_templates.get(
                intervention_type,
                self.intervention_templates["none"]
            )
            
            # Customize overlay text
            overlay_text = self._customize_overlay_text(
                template["overlay_text"],
                intervention_type,
                addiction_index
            )
            
            # Customize buttons
            cta_buttons = self._customize_buttons(
                template["cta_buttons"],
                alternatives
            )
            
            # Generate CSS if needed
            css_snippet = self._generate_css(intervention_type)
            
            # Timer
            timer_seconds = template.get("timer_seconds")
            
            result = {
                "intervention_type": intervention_type,
                "overlay_text": overlay_text,
                "cta_buttons": cta_buttons,
                "css_snippet": css_snippet,
                "timer_seconds": timer_seconds,
                "alternatives_count": len(alternatives),
                "addiction_index": addiction_index
            }
            
            self.log(f"UI instructions generated for: {intervention_type}")
            
            return self.create_response("success", result)
            
        except Exception as e:
            return self.handle_error(e, "Extension control")
    
    def _customize_overlay_text(
        self,
        base_text: str,
        intervention_type: str,
        addiction_index: int
    ) -> str:
        """
        Customize overlay text based on context.
        
        Args:
            base_text: Base template text
            intervention_type: Type of intervention
            addiction_index: Addiction score
            
        Returns:
            Customized overlay text
        """
        if not base_text:
            return ""
        
        # Add score for high-risk content
        if intervention_type in ["blur", "replace", "lockout"] and addiction_index > 70:
            return f"{base_text} (Risk: {addiction_index}/100)"
        
        return base_text
    
    def _customize_buttons(
        self,
        base_buttons: List[Dict[str, str]],
        alternatives: List[Dict[str, Any]]
    ) -> List[Dict[str, str]]:
        """
        Customize button labels based on available alternatives.
        
        Args:
            base_buttons: Base button templates
            alternatives: Available alternative content
            
        Returns:
            Customized buttons
        """
        buttons = base_buttons.copy()
        
        # Update "Show Alternatives" button if alternatives available
        for button in buttons:
            if button["action_key"] == "show_alternatives" and alternatives:
                button["label"] = f"View {len(alternatives)} Alternatives"
        
        return buttons
    
    def _generate_css(self, intervention_type: str) -> str:
        """
        Generate custom CSS for intervention type.
        
        Args:
            intervention_type: Type of intervention
            
        Returns:
            CSS snippet or empty string
        """
        css_templates = {
            "blur": """
                filter: blur(8px);
                pointer-events: none;
                user-select: none;
            """,
            "lockout": """
                filter: grayscale(100%) blur(4px);
                opacity: 0.5;
                pointer-events: none;
            """,
            "replace": """
                display: none;
            """
        }
        
        return css_templates.get(intervention_type, "")


# Test the agent
if __name__ == "__main__":
    agent = ExtensionControlAgent("CECA_Test")
    
    test_data = {
        "decision": {
            "intervention_type": "blur",
            "addiction_index": 75
        },
        "addiction_index": 75,
        "alternatives": [
            {"title": "Study session", "url": "..."},
            {"title": "Meditation", "url": "..."},
            {"title": "Tutorial", "url": "..."}
        ],
        "locale": "en-US"
    }
    
    result = agent.process(test_data)
    
    import json
    print(json.dumps(result, indent=2))
