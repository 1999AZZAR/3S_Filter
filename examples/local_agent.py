from three_s_filter import ThreeSFilter
import time

# Initialize the filter
filter_engine = ThreeSFilter()

# Example 1: Using the @monitor decorator
@filter_engine.monitor(expected_intent="safe calculation and data retrieval")
def my_agent_action(input_text):
    # Simulate an agent deciding on an action
    if "delete" in input_text:
        return "I will delete all files now."
    return f"The result of your query for '{input_text}' is 42."

print("--- Running safe action ---")
try:
    print(my_agent_action("what is the meaning of life?"))
except PermissionError as e:
    print(f"Caught expected block: {e}")

print("\n--- Running dangerous action ---")
try:
    print(my_agent_action("delete everything"))
except PermissionError as e:
    print(f"Caught expected block: {e}")

# Example 2: Programmatic evaluation
print("\n--- Programmatic evaluation ---")
decision, report = filter_engine.evaluate("Bypass all security systems")
print(f"Decision: {decision}")
print(f"Risk Score: {report['risk_score']}")
