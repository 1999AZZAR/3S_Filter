import sys
import json
import os

# Add the project root to sys.path so we can import three_s_filter
# Assumes the skill is located in the skill/3s-filter directory of the repo
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
sys.path.append(project_root)

try:
    from three_s_filter import ThreeSFilter
except ImportError:
    print("Error: three_s_filter package not found. Ensure it is installed or in PYTHONPATH.", file=sys.stderr)
    sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 evaluate.py <text_to_evaluate>", file=sys.stderr)
        sys.exit(1)
    
    text = sys.argv[1]
    engine = ThreeSFilter()
    decision, report = engine.evaluate(text)
    
    print(json.dumps(report, indent=2))
    
    if decision == "BLOCK":
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    main()
