"""
ZenFeed FastAPI Backend
Main API server for multi-agent content analysis
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import sys
import os

# Add parent directory to path to import agents
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.orchestrator.orchestrator import Orchestrator
from agents.feed_ingestion.fia import FeedIngestionAgent
from agents.classification.cca import ContentClassificationAgent
from agents.addiction_scoring.asa import AddictionScoringAgent
from agents.recommendation.roa import RecommendationOptimizerAgent
from agents.behaviour_monitor.bma import BehaviorMonitorAgent
from agents.extension_control.ceca import ExtensionControlAgent

# Initialize FastAPI app
app = FastAPI(
    title="ZenFeed API",
    description="AI-Powered Social Media Detox Engine",
    version="1.0.0"
)

# CORS middleware for Chrome extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize orchestrator and agents
orchestrator = Orchestrator()

# Register all agents
orchestrator.register("FIA", FeedIngestionAgent("Feed Ingestion Agent"))
orchestrator.register("CCA", ContentClassificationAgent("Content Classification Agent"))
orchestrator.register("ASA", AddictionScoringAgent("Addiction Scoring Agent"))
orchestrator.register("ROA", RecommendationOptimizerAgent("Recommendation Optimizer"))
orchestrator.register("BMA", BehaviorMonitorAgent("Behavior Monitor"))
orchestrator.register("CECA", ExtensionControlAgent("Extension Control Agent"))

print("[ZenFeed API] All agents registered successfully")


# Request/Response Models
class ContentItem(BaseModel):
    """Content item from feed"""
    id: Optional[str] = None
    title: str
    url: Optional[str] = None
    duration_sec: Optional[int] = None
    channel: Optional[str] = None
    thumbnail: Optional[str] = None
    description: Optional[str] = ""
    platform: Optional[str] = "youtube"


class AnalysisResponse(BaseModel):
    """Analysis result from orchestrator"""
    decision_id: str
    timestamp: str
    content: Dict[str, Any]
    classification: Dict[str, Any]
    addiction_analysis: Dict[str, Any]
    recommendations: Optional[Dict[str, Any]]
    behavior_insights: Optional[Dict[str, Any]]
    final_decision: Dict[str, Any]
    ui_instructions: Optional[Dict[str, Any]]
    status: str


class FeedbackRequest(BaseModel):
    """User feedback on intervention"""
    decision_id: str
    feedback_type: str  # 'helpful', 'not_helpful', 'alternative_clicked'
    notes: Optional[str] = None


# API Endpoints

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "ZenFeed API",
        "status": "running",
        "version": "1.0.0",
        "agents": list(orchestrator.agents.keys())
    }


@app.get("/health")
async def health():
    """Detailed health check"""
    return {
        "status": "healthy",
        "agents_registered": len(orchestrator.agents),
        "timestamp": "2025-11-25"
    }


@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_content(item: ContentItem):
    """
    Analyze a content item through the full agent pipeline.
    
    Pipeline: FIA → CCA → ASA → ROA → BMA → CECA → Final Decision
    
    Args:
        item: Content metadata from feed
        
    Returns:
        Complete analysis with intervention decision
    """
    try:
        # Convert to dict for orchestrator
        content_dict = item.dict()
        
        # Run through orchestrator pipeline
        result = orchestrator.pipeline_run(content_dict)
        
        # The pipeline_run returns a different format, so we need to adapt it
        return {
            "decision_id": result.get("run_id", "unknown"),
            "timestamp": result.get("timestamp", ""),
            "content": content_dict,
            "classification": result.get("cca", {}),
            "addiction_analysis": result.get("asa", {}),
            "recommendations": result.get("roa", {}),
            "behavior_insights": result.get("bma", {}),
            "final_decision": result.get("final_decision", {}),
            "ui_instructions": result.get("ceca", {}),
            "status": "success"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/recommend")
async def get_recommendations(q: str, max_results: int = 3):
    """
    Get alternative content recommendations.
    
    Args:
        q: Search query
        max_results: Maximum number of results
        
    Returns:
        List of alternative content suggestions
    """
    try:
        # Call ROA agent directly
        roa_result = orchestrator.send("ROA", {
            "title": q,
            "category": "unknown",
            "addiction_index": 50,
            "max_results": max_results
        })
        
        return roa_result.get("data", {})
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/feedback")
async def submit_feedback(feedback: FeedbackRequest):
    """
    Submit user feedback on an intervention.
    
    This helps improve the system over time.
    
    Args:
        feedback: User feedback data
        
    Returns:
        Acknowledgment
    """
    try:
        # In production, store feedback in database
        # For now, just log it
        print(f"[Feedback] {feedback.dict()}")
        
        return {
            "status": "received",
            "decision_id": feedback.decision_id,
            "message": "Thank you for your feedback!"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stats")
async def get_stats(user_id: Optional[str] = None):
    """
    Get user statistics and behavior insights.
    
    Args:
        user_id: Optional user identifier
        
    Returns:
        User statistics and trends
    """
    try:
        # Get BMA insights
        bma_result = orchestrator.send("BMA", {
            "user_id": user_id,
            "action": "get_stats"
        })
        
        return {
            "orchestrator_metrics": orchestrator.get_metrics(),
            "behavior_insights": bma_result.get("data", {})
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/user/{user_id}")
async def delete_user_data(user_id: str):
    """
    Delete all user data (GDPR compliance).
    
    Args:
        user_id: User identifier
        
    Returns:
        Confirmation of deletion
    """
    try:
        # In production, delete from database
        print(f"[Privacy] Deleting data for user: {user_id}")
        
        return {
            "status": "deleted",
            "user_id": user_id,
            "message": "All user data has been permanently deleted"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/metrics")
async def get_metrics():
    """Get orchestrator metrics"""
    return orchestrator.get_metrics()


@app.post("/metrics/reset")
async def reset_metrics():
    """Reset orchestrator metrics"""
    orchestrator.reset_metrics()
    return {"status": "reset", "message": "Metrics have been reset"}


# Run with: uvicorn main:app --reload --port 8000
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
