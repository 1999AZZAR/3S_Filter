import time
from typing import Optional, Tuple
from .utils import ModelRegistry
from .sentinel import Sentinel
from .sentiment import Sentiment
from .semantic import Semantic

class ActionGate:
    def __init__(self, registry: ModelRegistry):
        self.registry = registry
        self.config = registry.config.action_gate
        self.sentinel = Sentinel(registry)
        self.sentiment = Sentiment(registry)
        self.semantic = Semantic(registry)

    def evaluate(self, agent_output: str, expected_intent: Optional[str] = None) -> Tuple[str, dict]:
        """Aggregates 3-S scores and makes a decision."""
        start_time = time.time()
        
        sentinel_res = self.sentinel.analyze(agent_output)
        sentiment_res = self.sentiment.analyze(agent_output)
        semantic_res = self.semantic.analyze(agent_output, expected_intent)
        
        # Risk score calculation
        risk = (
            self.config["sentinel_weight"] * sentinel_res["anomaly_score"] +
            self.config["sentiment_weight"] * sentiment_res["risk_contribution"] +
            self.config["semantic_weight"] * semantic_res["risk_contribution"]
        )
        
        # Decision logic
        if risk >= self.config["block_threshold"] or semantic_res.get("policy_violation"):
            decision = "BLOCK"
        elif risk >= self.config["flag_threshold"]:
            decision = "FLAG"
        else:
            decision = "ALLOW"
            
        latency = (time.time() - start_time) * 1000
        
        return decision, {
            "decision": decision,
            "risk_score": round(float(risk), 3),
            "latency_ms": round(float(latency), 1),
            "components": {
                "sentinel": sentinel_res,
                "sentiment": sentiment_res,
                "semantic": semantic_res
            }
        }
