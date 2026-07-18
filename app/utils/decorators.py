"""Common decorator functions."""

import functools
import time
from typing import Any, Callable, TypeVar, cast

from app.utils.logger import get_logger

logger = get_logger(__name__)

F = TypeVar("F", bound=Callable[..., Any])


def log_execution(func: F) -> F:
    """Decorator to log function execution."""
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        logger.debug(f"Executing {func.__name__}")
        try:
            result = func(*args, **kwargs)
            logger.debug(f"Completed {func.__name__}")
            return result
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}", exc_info=True)
            raise

    return cast(F, wrapper)


def time_execution(func: F) -> F:
    """Decorator to measure function execution time."""
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start
        logger.debug(f"{func.__name__} took {duration:.3f}s")
        return result

    return cast(F, wrapper)


def retry(max_attempts: int = 3, delay: float = 1.0) -> Callable:
    """Decorator to retry function on failure."""
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    logger.warning(
                        f"Attempt {attempt + 1}/{max_attempts} failed for "
                        f"{func.__name__}: {str(e)}. Retrying..."
                    )
                    time.sleep(delay)

        return cast(F, wrapper)

    return decorator
