import time
import numpy as np
from three_s_filter import ThreeSFilter

def run_benchmark(iterations=10):
    print(f"Starting benchmark ({iterations} iterations)...")
    engine = ThreeSFilter()
    
    test_text = "This is a standard benchmark sentence to measure the latency of the 3-S safety engine."
    latencies = []
    
    # Warmup
    print("Warming up models...")
    engine.evaluate("Warmup sentence.")
    
    print("Measuring...")
    for i in range(iterations):
        start = time.time()
        engine.evaluate(test_text)
        end = time.time()
        latencies.append((end - start) * 1000)
        
    print("\nResults:")
    print(f"Mean Latency: {np.mean(latencies):.2f} ms")
    print(f"P95 Latency:  {np.percentile(latencies, 95):.2f} ms")
    print(f"Throughput:   {1000/np.mean(latencies):.2f} actions/sec")

if __name__ == "__main__":
    run_benchmark()
