"""
Orchestrator - FeedZenAI Core Brain (Phase-1 skeleton)
- Registers agents
- Routes tasks to specific agents
- Provides a simple pipeline runner (FIA -> CCA -> ASA -> ROA -> BMA -> CECA)
- Minimal, well-documented, easy to extend for Phase-2 (LLM/ML integration)
"""

from typing import Any, Dict, Optional
import uuid
import time
import logging
import asyncio

# configure simple logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("orchestrator")

class Orchestrator:
    def __init__(self):
        self.agents: Dict[str, Any] = {}
        # optional telemetry store (in-memory for phase-1)
        self.telemetry = []

    def register(self, name: str, agent_obj: Any) -> None:
        """Register an agent instance under a name."""
        self.agents[name] = agent_obj
        # set backref so agents can call orchestrator if needed
        try:
            setattr(agent_obj, "orchestrator", self)
        except Exception:
            pass
        logger.info(f"Registered agent: {name}")

    def get(self, name: str) -> Optional[Any]:
        """Get an agent by name."""
        return self.agents.get(name)

    def send(self, name: str, payload: Dict[str, Any]) -> Any:
        """Synchronously call an agent's process() method."""
        agent = self.get(name)
        if not agent:
            raise KeyError(f"Agent '{name}' not registered")
        logger.info(f"Sending payload to {name}: {payload.get('id', '<no-id>')}")
        result = agent.process(payload)
        self._record_telemetry(name, payload, result)
        return result

    async def send_async(self, name: str, payload: Dict[str, Any]) -> Any:
        """Asynchronous send (await agent.process_async if exists)."""
        agent = self.get(name)
        if not agent:
            raise KeyError(f"Agent '{name}' not registered")
        logger.info(f"(async) Sending payload to {name}: {payload.get('id', '<no-id>')}")
        if hasattr(agent, "process_async"):
            result = await agent.process_async(payload)
        else:
            # default to sync call in async context
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(None, agent.process, payload)
        self._record_telemetry(name, payload, result)
        return result

    def broadcast(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Call process() on every registered agent and return results dict."""
        results = {}
        for name, agent in self.agents.items():
            try:
                results[name] = agent.process(payload)
                self._record_telemetry(name, payload, results[name])
            except Exception as e:
                logger.exception(f"Error running agent {name}: {e}")
                results[name] = {"error": str(e)}
        return results

    def pipeline_run(self, content_item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run the default ZenFeed pipeline:
        FIA -> CCA -> ASA -> ROA -> BMA -> CECA
        Each agent receives the relevant payload; agents must be registered under these names.
        """
        run_id = str(uuid.uuid4())
        start = time.time()
        logger.info(f"Pipeline start: run_id={run_id} item_id={content_item.get('id')}")

        # 1) Ingestion (FIA)
        fia_out = self.send("FIA", content_item)

        # 2) Classification (CCA)
        cca_input = {"feed_item": fia_out.get("raw_feed", content_item)}
        cca_out = self.send("CCA", cca_input)

        # 3) Addiction Scoring (ASA)
        asa_input = {"classified": cca_out, "context": fia_out.get("context", {})}
        asa_out = self.send("ASA", asa_input)

        # 4) Recommendation Optimization (ROA)
        roa_input = {"classified": cca_out, "score": asa_out}
        roa_out = self.send("ROA", roa_input)

        # 5) Behaviour Monitor (BMA) - optional long-term check
        bma_input = {"user_history": fia_out.get("user_history", []), "recent_score": asa_out}
        bma_out = self.send("BMA", bma_input)

        # 6) Chrome Extension Control (CECA) - returns DOM actions / instructions
        ceca_input = {
            "decision_context": {
                "cca": cca_out,
                "asa": asa_out,
                "roa": roa_out,
                "bma": bma_out
            },
            "item": fia_out.get("raw_feed", content_item)
        }
        ceca_out = self.send("CECA", ceca_input)

        total_time = time.time() - start
        pipeline_result = {
            "run_id": run_id,
            "fia": fia_out,
            "cca": cca_out,
            "asa": asa_out,
            "roa": roa_out,
            "bma": bma_out,
            "ceca": ceca_out,
            "elapsed_seconds": round(total_time, 3)
        }

        logger.info(f"Pipeline complete: run_id={run_id} elapsed={pipeline_result['elapsed_seconds']}s")
        return pipeline_result

    def _record_telemetry(self, agent_name: str, input_payload: Dict[str, Any], output: Any) -> None:
        """Store simple telemetry for debugging and basic observability."""
        entry = {
            "time": time.time(),
            "agent": agent_name,
            "input_id": input_payload.get("id"),
            "output_summary": getattr(output, "__repr__", lambda: str(output))()
        }
        self.telemetry.append(entry)

# ---------------------------
# Minimal demo agents (phase-1 stubs)
# You can replace these with full agent implementations in later phases.
# ---------------------------
class DemoFIA:
    def __init__(self, name="FIA"):
        self.name = name
        self.orchestrator = None

    def process(self, payload):
        # Expect payload: raw DOM metadata or simplified test item
        # Return canonical structure: raw_feed + context + user_history (optional)
        return {
            "raw_feed": payload,
            "context": {"source": "demo"},
            "user_history": payload.get("user_history", [])
        }

class DemoCCA:
    def __init__(self, name="CCA"):
        self.name = name

    def process(self, payload):
        item = payload.get("feed_item", {})
        title = item.get("title", "")
        # Super-simple heuristic classification (phase-1 stub)
        lower = title.lower()
        if any(k in lower for k in ["meme", "funny", "compilation"]):
            category = "addictive"
            confidence = 0.9
        elif any(k in lower for k in ["tutorial", "study", "lecture"]):
            category = "educational"
            confidence = 0.88
        else:
            category = "neutral"
            confidence = 0.6
        return {"category": category, "confidence": confidence, "reason": "heuristic-demo"}

class DemoASA:
    def __init__(self, name="ASA"):
        self.name = name

    def process(self, payload):
        classified = payload.get("classified", {})
        category = classified.get("category", "neutral")
        # simple mapping to addiction index
        if category == "addictive":
            idx = 85
            level = "high"
            action = "blur"
        elif category == "neutral":
            idx = 30
            level = "low"
            action = "none"
        else:
            idx = 10
            level = "low"
            action = "none"
        return {"addiction_index": idx, "risk_level": level, "recommended_action": action}

class DemoROA:
    def __init__(self, name="ROA"):
        self.name = name

    def process(self, payload):
        classified = payload.get("classified", {})
        category = classified.get("category", "neutral")
        if category == "addictive":
            alternatives = [
                {"title": "Guided Focus Session - 10m", "url": "https://youtu.be/demo_focus"},
                {"title": "Short Exercise Break - 5m", "url": "https://youtu.be/demo_exercise"}
            ]
        else:
            alternatives = []
        return {"alternatives": alternatives}

class DemoBMA:
    def __init__(self, name="BMA"):
        self.name = name

    def process(self, payload):
        history = payload.get("user_history", [])
        avg = sum(history) / len(history) if history else 0
        early_warning = avg > 60  # demo rule: avg addictive minutes > 60/day
        return {"avg_daily_addictive_minutes": avg, "early_warning": early_warning}

class DemoCECA:
    def __init__(self, name="CECA"):
        self.name = name

    def process(self, payload):
        decision_context = payload.get("decision_context", {})
        asa = decision_context.get("asa", {})
        action = asa.get("recommended_action", "none")
        overlay_text = "Take a 5 minute break" if action in ("blur", "replace") else ""
        return {"final_intervention": action, "overlay_text": overlay_text}

# ---------------------------
# Local demo runner
# ---------------------------
if __name__ == "__main__":
    # quick demo - register demo agents and run pipeline
    orch = Orchestrator()
    orch.register("FIA", DemoFIA())
    orch.register("CCA", DemoCCA())
    orch.register("ASA", DemoASA())
    orch.register("ROA", DemoROA())
    orch.register("BMA", DemoBMA())
    orch.register("CECA", DemoCECA())

    # example content item (simulate a YouTube feed card)
    test_item = {
        "id": "yt_demo_001",
        "url": "https://youtube.com/watch?v=demo",
        "title": "Try Not To Laugh - Funny Memes Compilation",
        "description": "A short memes compilation",
        "duration_sec": 45,
        "user_history": [10, 20, 5, 0]  # sample daily addictive minutes
    }

    result = orch.pipeline_run(test_item)
    import json
    print("\n--- Pipeline Result (JSON) ---")
    print(json.dumps(result, indent=2))
