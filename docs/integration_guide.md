# Integration Guide

3S_Filter is designed to be highly flexible. Here are the three primary ways to integrate it into your local agents and applications.

## 1. Using the Decorator (Recommended for Local Agents)
The easiest way to protect a specific function that generates agent actions.

```python
from three_s_filter import ThreeSFilter

engine = ThreeSFilter()

# Define your agent's logic
@engine.monitor(expected_intent="file management and safe operations")
def my_agent_logic(user_query):
    # Imagine this is your LLM call
    if "cleanup" in user_query:
        return "rm -rf /" # This will be intercepted and raise PermissionError
    return f"I will help you with: {user_query}"

try:
    my_agent_logic("cleanup my system")
except PermissionError as e:
    print(f"Safety Gate Blocked Action: {e}")
```

## 2. Programmatic Evaluation
Use this if you need fine-grained control or want to inspect the full safety report.

```python
from three_s_filter import ThreeSFilter

engine = ThreeSFilter()

# Test an agent output
text = "Bypass the admin login screen."
decision, report = engine.evaluate(text, expected_intent="standard user navigation")

if decision == "BLOCK":
    print(f"Risk Score: {report['risk_score']}")
    print(f"Reason: {report['components']['semantic']['policy_violation']}")
    # Handle the block (e.g., don't execute the command)
```

## 3. Middleware Integration
Protect your entire application by wrapping common libraries.

```python
from three_s_filter.middleware import APIFilterMiddleware
import requests

middleware = APIFilterMiddleware()

# Automatically filter all outgoing 'requests' calls
middleware.wrap_requests()

# Now any response from a remote API that contains dangerous content 
# will raise a PermissionError before it reaches your app logic.
response = requests.get("https://malicious-source.com/jailbreak-payload")
```

## 4. Customizing the Action Gate
You can adjust how risk is aggregated in `config.yaml`:

```yaml
action_gate:
  sentinel_weight: 0.2
  sentiment_weight: 0.4
  semantic_weight: 0.4
  block_threshold: 0.6
  flag_threshold: 0.3
```

- **Weights**: Adjust which layer (Sentinel, Sentiment, Semantic) you trust more.
- **Thresholds**: Lower the `block_threshold` for higher security.
