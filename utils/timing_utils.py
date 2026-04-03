import time
from functools import wraps

def timer(label: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start
            print(f"[{label}] completed in {elapsed:.4f}s")
            return result
        return wrapper
    return decorator

def time_it(label: str, func, *args, **kwargs):
    start = time.perf_counter()
    result = func(*args, **kwargs)
    elapsed = time.perf_counter() - start
    print(f"[{label}] completed in {elapsed:.4f}s")
    return result, elapsed
