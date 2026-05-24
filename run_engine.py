import sys
import json
import argparse
import time
from three_s_filter import ThreeSFilter

def run_pipe(engine):
    print("3-S Engine [PIPE MODE]: Waiting for input...", file=sys.stderr)
    for line in sys.stdin:
        text = line.strip()
        if not text:
            continue
        decision, report = engine.evaluate(text)
        print(json.dumps(report))

def run_http(engine, port):
    from flask import Flask, request, jsonify
    app = Flask(__name__)

    @app.route('/evaluate', methods=['POST'])
    def evaluate():
        data = request.json
        text = data.get('text', '')
        expected_intent = data.get('expected_intent')
        decision, report = engine.evaluate(text, expected_intent)
        return jsonify(report)

    print(f"3-S Engine [HTTP MODE]: Running on port {port}", file=sys.stderr)
    app.run(host='0.0.0.0', port=port)

def main():
    parser = argparse.ArgumentParser(description="3-S Filter Engine CLI")
    parser.add_argument("--mode", choices=["pipe", "http"], default="pipe", help="Execution mode")
    parser.add_argument("--port", type=int, default=8080, help="HTTP port")
    parser.add_argument("--config", default="config.yaml", help="Path to config file")
    
    args = parser.parse_args()
    
    print("Loading engine...", file=sys.stderr)
    engine = ThreeSFilter(args.config)
    
    if args.mode == "pipe":
        run_pipe(engine)
    elif args.mode == "http":
        run_http(engine, args.port)

if __name__ == "__main__":
    main()
