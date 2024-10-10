import time

from core.loggers import configure_logging


logger = configure_logging(__name__)


def time_it(func):
    def wrapper(*args, **kwargs):
        start_time = time.time_ns()
        result = func(*args, **kwargs)
        logger.debug(
            f"Function '{func.__name__}' took "
            f"{(time.time_ns() - start_time) / 10**6:.02f}ms to execute.",
        )
        return result
    return wrapper
