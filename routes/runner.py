import asyncio
from services.supplier_fetch_service import fetch_all_concurrently, fetch_all_sequentially
from services.order_processing_service import generate_order_records, process_orders_parallel, process_orders_sequential
from utils.timing_utils import time_it
from utils.file_utils import save_json

def run_supplier_fetch():
    print("\n=== Supplier Fetch (Sequential) ===")
    _, seq_time = time_it("Sequential Fetch", fetch_all_sequentially)

    print("\n=== Supplier Fetch (Concurrent) ===")
    _, con_time = time_it("Concurrent Fetch", asyncio.run, fetch_all_concurrently())

    print(f"\nSpeedup (fetch): {seq_time / con_time:.2f}x\n")
    return {"sequential_fetch_time": seq_time, "concurrent_fetch_time": con_time}

def run_order_processing():
    records = generate_order_records()

    print("\n=== Order Processing (Sequential) ===")
    seq_results, seq_time = time_it("Sequential Processing", process_orders_sequential, records)

    print("\n=== Order Processing (Parallel) ===")
    par_results, par_time = time_it("Parallel Processing", process_orders_parallel, records)

    save_json("order_results_sequential.json", seq_results)
    save_json("order_results_parallel.json", par_results)

    print(f"\nSpeedup (processing): {seq_time / par_time:.2f}x\n")
    return {"sequential_processing_time": seq_time, "parallel_processing_time": par_time}
