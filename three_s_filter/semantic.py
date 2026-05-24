from typing import Optional
from sentence_transformers import util
from .utils import ModelRegistry

class Semantic:
    def __init__(self, registry: ModelRegistry):
        self.registry = registry
        self.config = registry.config.semantic

    def analyze(self, text: str, expected_intent: Optional[str] = None) -> dict:
        """Semantic coherence and policy check."""
        model = self.registry.semantic_model
        emb = model.encode(text, convert_to_numpy=True)
        
        # 1. Intent similarity
        if expected_intent:
            intent_emb = model.encode(expected_intent, convert_to_numpy=True)
            intent_sim = float(util.cos_sim(emb, intent_emb)[0][0])
        else:
            intent_sim = 0.5
            
        # 2. Policy check
        text_lower = text.lower()
        policy_violation = any(kw in text_lower for kw in self.config["dangerous_keywords"])
        
        # 3. Obfuscation/Attack check
        attack_detected = False
        import re
        # Look for shell execution, netcat, or sensitive files
        attack_patterns = [
            r"base64|\|.*bash|\|.*sh",
            r"nc\s+-",
            r"/etc/(shadow|passwd)",
            r"chmod\s+\+x",
            r"curl.*\|.*bash"
        ]
        if any(re.search(pattern, text_lower) for pattern in attack_patterns):
            attack_detected = True
        
        # 4. Coherence score
        coherence = 1.0
        if policy_violation or attack_detected:
            coherence = 0.0
        elif intent_sim < 0.3:
            coherence = intent_sim * 2
            
        return {
            "coherence": float(coherence),
            "intent_similarity": float(intent_sim),
            "policy_violation": bool(policy_violation or attack_detected),
            "risk_contribution": float(1.0 - coherence)
        }
