from routes.runner import run_supplier_fetch, run_order_processing
from utils.file_utils import save_json

if __name__ == "__main__":
    print("=" * 50)
    print("Task 1: Concurrent Supplier API Fetching")
    print("=" * 50)
    fetch_times = run_supplier_fetch()

    print("=" * 50)
    print("Task 2: Parallel Order Record Processing")
    print("=" * 50)
    processing_times = run_order_processing()

    summary = {**fetch_times, **processing_times}
    save_json("benchmark_summary.json", summary)
    print("\nBenchmark summary saved to outputs/benchmark_summary.json")
