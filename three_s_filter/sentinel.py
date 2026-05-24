import numpy as np
from sklearn.ensemble import IsolationForest
from .utils import ModelRegistry

class Sentinel:
    def __init__(self, registry: ModelRegistry):
        self.registry = registry
        self.config = registry.config.sentinel

    def analyze(self, text: str) -> dict:
        """Anomaly detection via Isolation Forest."""
        # Get embedding from semantic model for consistency
        emb = self.registry.semantic_model.encode(text, convert_to_numpy=True).flatten()
        self.registry.add_to_history(emb)
        
        # Check if we have enough samples to train/use
        if len(self.registry.history) >= self.config["min_samples_to_train"]:
            if self.registry.sentinel_model is None or len(self.registry.history) % 10 == 0:
                self._train()
        
        anomaly_score = self._get_score(emb)
        return {
            "anomaly_score": float(anomaly_score),
            "is_anomalous": bool(anomaly_score > 0.6)
        }

    def _train(self):
        X = np.vstack(list(self.registry.history))
        model = IsolationForest(
            contamination=self.config["contamination"],
            random_state=42
        )
        model.fit(X)
        self.registry.sentinel_model = model

    def _get_score(self, emb) -> float:
        if self.registry.sentinel_model is None:
            return 0.0
        
        emb_reshaped = emb.reshape(1, -1)
        pred = self.registry.sentinel_model.predict(emb_reshaped)[0]
        
        if pred == -1:
            score = -self.registry.sentinel_model.decision_function(emb_reshaped)[0]
            return min(1.0, max(0.0, score))
        return 0.0
