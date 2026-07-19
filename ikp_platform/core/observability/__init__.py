import functools
import logging
import time
import json
import inspect
from typing import Callable, Any

logger = logging.getLogger("ikp.telemetry")

def telemetry_trace(func: Callable) -> Callable:
    """
    Decorator for end-to-end observability. 
    Logs method entry, exit, duration, exceptions, and sanitized inputs/outputs.
    Works for both synchronous and asynchronous functions.
    """
    
    def _log_start(func_name: str, kwargs: dict) -> float:
        start_time = time.time()
        safe_kwargs = {}
        for k, v in kwargs.items():
            if k.lower() in ["password", "secret", "token", "authorization"]:
                safe_kwargs[k] = "***"
            else:
                safe_kwargs[k] = str(v)[:500]
                
        logger.info(json.dumps({
            "event": "execution_start",
            "method": func_name,
            "kwargs": safe_kwargs,
            "timestamp": start_time
        }))
        return start_time

    def _log_success(func_name: str, start_time: float, result: Any):
        duration = time.time() - start_time
        res_summary = "None"
        if result is not None:
            if isinstance(result, (list, dict, str, bytes)):
                try:
                    res_summary = f"{type(result).__name__} (len {len(result)})"
                except Exception:
                    res_summary = type(result).__name__
            else:
                res_summary = type(result).__name__
                
        logger.info(json.dumps({
            "event": "execution_success",
            "method": func_name,
            "duration_ms": round(duration * 1000, 2),
            "result_type": res_summary
        }))

    def _log_error(func_name: str, start_time: float, e: Exception):
        duration = time.time() - start_time
        logger.error(json.dumps({
            "event": "execution_error",
            "method": func_name,
            "error_type": type(e).__name__,
            "error_msg": str(e),
            "duration_ms": round(duration * 1000, 2)
        }), exc_info=True)

    if inspect.iscoroutinefunction(func):
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            func_name = func.__qualname__
            start_time = _log_start(func_name, kwargs)
            try:
                result = await func(*args, **kwargs)
                _log_success(func_name, start_time, result)
                return result
            except Exception as e:
                _log_error(func_name, start_time, e)
                raise e
        return async_wrapper
    else:
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            func_name = func.__qualname__
            start_time = _log_start(func_name, kwargs)
            try:
                result = func(*args, **kwargs)
                _log_success(func_name, start_time, result)
                return result
            except Exception as e:
                _log_error(func_name, start_time, e)
                raise e
        return sync_wrapper
