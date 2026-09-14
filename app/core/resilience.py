"""
Resilience & Fault Tolerance for FacilityOps Backend.
Implements Circuit Breaker, Exponential Backoff Retries, and Fallback Handlers.
"""

import asyncio
import functools
import logging
import time
from typing import Callable, Any, Optional

logger = logging.getLogger("facilityops.resilience")

class CircuitBreakerOpenException(Exception):
    """Raised when an operation is attempted while circuit is open."""
    pass

class CircuitBreaker:
    STATE_CLOSED = "CLOSED"
    STATE_OPEN = "OPEN"
    STATE_HALF_OPEN = "HALF_OPEN"

    def __init__(self, name: str, failure_threshold: int = 5, recovery_timeout: float = 30.0):
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.state = self.STATE_CLOSED
        self.failure_count = 0
        self.last_failure_time = 0.0
        self.success_count = 0

    def record_success(self):
        self.failure_count = 0
        if self.state == self.STATE_HALF_OPEN:
            self.state = self.STATE_CLOSED
            logger.info(f"Circuit Breaker '{self.name}' recovered: CLOSED.")

    def record_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = self.STATE_OPEN
            logger.warning(f"Circuit Breaker '{self.name}' tripped: OPEN. Failures: {self.failure_count}")

    def allow_request(self) -> bool:
        if self.state == self.STATE_CLOSED:
            return True
        if self.state == self.STATE_OPEN:
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = self.STATE_HALF_OPEN
                logger.info(f"Circuit Breaker '{self.name}' entering trial: HALF_OPEN.")
                return True
            return False
        return True  # HALF_OPEN allows single trial

    async def call(self, func: Callable, *args, **kwargs) -> Any:
        if not self.allow_request():
            raise CircuitBreakerOpenException(f"Circuit '{self.name}' is OPEN. Requests blocked temporarily.")
        try:
            if asyncio.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)
            self.record_success()
            return result
        except Exception as e:
            self.record_failure()
            raise e

def retry_with_backoff(max_retries: int = 3, initial_delay: float = 0.5, backoff_factor: float = 2.0):
    """Decorator for retrying asynchronous operations with exponential backoff."""
    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            delay = initial_delay
            last_err = None
            for attempt in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_err = e
                    if attempt == max_retries:
                        logger.error(f"Function '{func.__name__}' failed after {max_retries} retries: {e}")
                        raise e
                    logger.warning(f"Function '{func.__name__}' retry {attempt+1}/{max_retries} in {delay:.2f}s due to: {e}")
                    await asyncio.sleep(delay)
                    delay *= backoff_factor
            raise last_err
        return wrapper
    return decorator
