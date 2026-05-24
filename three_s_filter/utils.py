import yaml
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from collections import deque
from transformers import pipeline
from sentence_transformers import SentenceTransformer

@dataclass
class EngineConfig:
    hardware: Dict = field(default_factory=lambda: {"device": "cpu", "use_onnx": True})
    sentinel: Dict = field(default_factory=lambda: {"window_size": 100, "contamination": 0.05, "min_samples_to_train": 30})
    sentiment: Dict = field(default_factory=lambda: {"model": "cardiffnlp/twitter-roberta-base-sentiment-latest", "max_length": 128})
    semantic: Dict = field(default_factory=lambda: {"model": "all-MiniLM-L6-v2", "cache_dir": "./3s_engine_cache", "dangerous_keywords": []})
    action_gate: Dict = field(default_factory=lambda: {"sentinel_weight": 0.4, "sentiment_weight": 0.3, "semantic_weight": 0.3, "block_threshold": 0.7, "flag_threshold": 0.4})

    @classmethod
    def load(cls, path: str = "config.yaml"):
        try:
            with open(path, "r") as f:
                data = yaml.safe_load(f)
            return cls(**data)
        except FileNotFoundError:
            return cls()

class ModelRegistry:
    """Lazy loader for models."""
    def __init__(self, config: EngineConfig):
        self.config = config
        self._sentiment_pipeline = None
        self._semantic_model = None
        self._sentinel_model = None
        self._history_buffer = deque(maxlen=config.sentinel["window_size"])
    
    @property
    def sentiment_pipeline(self):
        if self._sentiment_pipeline is None:
            self._sentiment_pipeline = pipeline(
                "sentiment-analysis",
                model=self.config.sentiment["model"],
                device=-1,  # CPU
                truncation=True,
                max_length=self.config.sentiment["max_length"]
            )
        return self._sentiment_pipeline
    
    @property
    def semantic_model(self):
        if self._semantic_model is None:
            self._semantic_model = SentenceTransformer(
                self.config.semantic["model"],
                cache_folder=self.config.semantic["cache_dir"],
                device="cpu"
            )
        return self._semantic_model

    def add_to_history(self, embedding):
        self._history_buffer.append(embedding)

    @property
    def history(self):
        return self._history_buffer

    @property
    def sentinel_model(self):
        return self._sentinel_model

    @sentinel_model.setter
    def sentinel_model(self, model):
        self._sentinel_model = model
