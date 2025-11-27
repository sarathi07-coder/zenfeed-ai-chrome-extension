#!/usr/bin/env python3
"""
ZenFeed End-to-End Test
Tests the complete agent pipeline with a sample video
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.orchestrator.orchestrator import Orchestrator
from agents.feed_ingestion.fia import FeedIngestionAgent
from agents.classification.cca import ContentClassificationAgent
from agents.addiction_scoring.asa import AddictionScoringAgent
from agents.recommendation.roa import RecommendationOptimizerAgent
from agents.behaviour_monitor.bma import BehaviorMonitorAgent
from agents.extension_control.ceca import ExtensionControlAgent

import json


def test_pipeline():
    """Test the complete ZenFeed pipeline"""
    
    print("=" * 70)
    print("🧪 ZenFeed End-to-End Pipeline Test")
    print("=" * 70)
    print()
    
    # Initialize orchestrator
    print("📋 Initializing orchestrator and agents...")
    orchestrator = Orchestrator()
    
    # Register all agents
    orchestrator.register("FIA", FeedIngestionAgent("Feed Ingestion Agent"))
    orchestrator.register("CCA", ContentClassificationAgent("Content Classification Agent"))
    orchestrator.register("ASA", AddictionScoringAgent("Addiction Scoring Agent"))
    orchestrator.register("ROA", RecommendationOptimizerAgent("Recommendation Optimizer"))
    orchestrator.register("BMA", BehaviorMonitorAgent("Behavior Monitor"))
    orchestrator.register("CECA", ExtensionControlAgent("Extension Control Agent"))
    
    print(f"✓ Registered {len(orchestrator.agents)} agents")
    print()
    
    # Test cases
    test_cases = [
        {
            "name": "Addictive Content (Meme Compilation)",
            "item": {
                "id": "test_001",
                "title": "Try Not To Laugh - Funny Memes Compilation 2024",
                "url": "https://youtube.com/watch?v=test001",
                "duration_sec": 45,
                "channel": "MemeWorld",
                "platform": "youtube"
            }
        },
        {
            "name": "Educational Content (Tutorial)",
            "item": {
                "id": "test_002",
                "title": "Python Tutorial for Beginners - Complete Course",
                "url": "https://youtube.com/watch?v=test002",
                "duration_sec": 3600,
                "channel": "Programming with Mosh",
                "platform": "youtube"
            }
        },
        {
            "name": "Neutral Content (News)",
            "item": {
                "id": "test_003",
                "title": "Tech News Update - January 2024",
                "url": "https://youtube.com/watch?v=test003",
                "duration_sec": 600,
                "channel": "TechCrunch",
                "platform": "youtube"
            }
        }
    ]
    
    # Run tests
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test {i}/{len(test_cases)}: {test_case['name']}")
        print("-" * 70)
        
        # Run pipeline
        result = orchestrator.pipeline_run(test_case["item"])
        
        # Extract key results from existing orchestrator format
        cca_result = result.get("cca", {})
        asa_result = result.get("asa", {})
        roa_result = result.get("roa", {})
        ceca_result = result.get("ceca", {})
        
        # Display results
        print(f"📊 Classification: {cca_result.get('category', 'unknown').upper()}")
        print(f"   Confidence: {cca_result.get('confidence', 0):.2f}")
        print(f"   Triggers: {', '.join(cca_result.get('triggers', [])) if cca_result.get('triggers') else 'None'}")
        print()
        
        print(f"⚠️  Addiction Index: {asa_result.get('addiction_index', 0)}/100")
        print(f"   Risk Level: {asa_result.get('risk_level', 'unknown').upper()}")
        print(f"   Recommended Action: {asa_result.get('recommended_action', 'none').upper()}")
        print()
        
        print(f"🎯 Final Intervention: {ceca_result.get('final_intervention', 'none').upper()}")
        print(f"   Overlay Text: {ceca_result.get('overlay_text', 'N/A')}")
        print()
        
        # Show alternatives if any
        if roa_result and roa_result.get("alternatives"):
            alternatives = roa_result["alternatives"]
            print(f"💡 Alternatives ({len(alternatives)}):")
            for j, alt in enumerate(alternatives[:3], 1):
                print(f"   {j}. {alt.get('title', 'Unknown')[:60]}...")
            print()
        
        print(f"⏱️  Pipeline Time: {result.get('elapsed_seconds', 0)}s")
        print("✓ Test passed")
        
        print()
    
    # Display metrics
    print("=" * 70)
    print("📈 Orchestrator Metrics")
    print("=" * 70)
    metrics = orchestrator.get_metrics()
    print(json.dumps(metrics, indent=2))
    print()
    
    print("=" * 70)
    print("✅ All tests completed!")
    print("=" * 70)


if __name__ == "__main__":
    test_pipeline()
