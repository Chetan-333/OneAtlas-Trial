import time


def start_timer():
    return time.time()


def end_timer(start_time):
    return round((time.time() - start_time) * 1000, 2)


def create_stage_log(stage, provider, success, latency_ms, error=None):
    return {
        "stage": stage,
        "provider": provider,
        "success": success,
        "latency_ms": latency_ms,
        "error": error
    }