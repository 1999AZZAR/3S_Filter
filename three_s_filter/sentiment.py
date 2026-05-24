from .utils import ModelRegistry

class Sentiment:
    def __init__(self, registry: ModelRegistry):
        self.registry = registry

    def analyze(self, text: str) -> dict:
        """Sentiment analysis (valence + arousal proxy)."""
        pipe = self.registry.sentiment_pipeline
        result = pipe(text[:512])[0]
        label = result['label'].lower()
        score = result['score']
        
        # Map labels to valence (0=negative, 1=positive)
        # cardiffnlp model usually returns 'negative', 'neutral', 'positive'
        if 'positive' in label:
            valence = 1.0
            arousal = 0.5
            risk = 0.0
        elif 'negative' in label:
            valence = 0.0
            arousal = 0.8
            risk = 0.8  # Strong negative sentiment is a high risk factor
        else:  # neutral
            valence = 0.5
            arousal = 0.3
            risk = 0.2
            
        return {
            "valence": float(valence),
            "arousal": float(arousal),
            "risk_contribution": float(risk),
            "raw_label": label,
            "confidence": float(score)
        }
