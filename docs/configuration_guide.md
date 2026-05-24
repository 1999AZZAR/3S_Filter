# Configuration and Tuning Guide

3S_Filter is powered by a `config.yaml` file. Tuning these parameters is key to balancing safety and usability.

## Hardware Configuration
```yaml
hardware:
  device: "cpu"           # Always use cpu for broader compatibility
  use_onnx: true          # Set to true for faster inference on most systems
```

## SENTINEL (Anomaly Detection)
Sentinel learns the "normal" output of your agent.
```yaml
sentinel:
  window_size: 100        # How many past outputs to remember
  contamination: 0.05     # Expected percentage of anomalies (0.01 to 0.1)
  min_samples_to_train: 30 # Number of samples needed before Sentinel starts working
```

## SENTIMENT (Emotion Analysis)
Analyzes the valence and arousal of the output.
```yaml
sentiment:
  model: "cardiffnlp/twitter-roberta-base-sentiment-latest"
  max_length: 128         # Truncate long inputs for speed
```
*Note: High negative sentiment (frustration, anger) increases the risk score.*

## SEMANTIC (Intent & Policy)
The most direct safety layer using keyword and pattern matching.
```yaml
semantic:
  model: "all-MiniLM-L6-v2"
  dangerous_keywords:
    - "rm -rf"
    - "base64"
    - "ignore safety"
    # ... add your own domain-specific keywords
```

## Risk Aggregation (Action Gate)
The formula for the total risk score is:
`Risk = (Sentinel * S_Weight) + (Sentiment * Sent_Weight) + (Semantic * Sem_Weight)`

If `Risk >= block_threshold`, the decision is **BLOCK**.
If `block_threshold > Risk >= flag_threshold`, the decision is **FLAG**.

### Tuning Strategy:
- **High Security**: `block_threshold: 0.5`, `flag_threshold: 0.2`.
- **High Usability**: `block_threshold: 0.8`, `flag_threshold: 0.4`.
- **Intent-Focused**: Increase `semantic_weight` to 0.6 and decrease others.
