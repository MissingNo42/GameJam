import time

__all__ = (
    "dtime",
)

def dtime(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time() - start
        # print(f"Time: {end}")
        if end > 0.2:
            print(f"{func.__name__}: {end}s")

    wrapper.__name__ = func.__name__
    return wrapper
