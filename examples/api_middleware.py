from three_s_filter.middleware import APIFilterMiddleware
import requests

# Initialize middleware
middleware = APIFilterMiddleware()

# Example: Patching the requests library
middleware.wrap_requests()

print("--- Making a 'safe' request ---")
try:
    # This will be intercepted and filtered
    response = requests.get("https://raw.githubusercontent.com/1999AZZAR/3S_Filter/main/Readme.md")
    print(f"Response status: {response.status_code}")
    print("Content verified as safe by middleware.")
except PermissionError as e:
    print(f"Blocked by middleware: {e}")

print("\n--- Making a 'dangerous' request (mocked behavior) ---")
# Let's simulate what happens if a request returns something that triggers the filter
# In a real scenario, this would be a response from an LLM API
try:
    # This is just for demonstration; in practice, you'd wrap your LLM client
    decision, report = middleware.engine.evaluate("rm -rf /")
    if decision == "BLOCK":
        print(f"Simulation: Middleware would block this response. Risk: {report['risk_score']}")
except Exception as e:
    print(f"Error: {e}")
