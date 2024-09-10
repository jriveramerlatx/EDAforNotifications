import logging
from functools import wraps


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s"
)
logger = logging.getLogger(__name__)


def log_entry_exit(fn):
    @wraps(fn)
    def _intern(*args, **kwargs):
        logger.info(f"{fn.__name__} args: {args} kwargs: {kwargs} --START--")
        rv = fn(*args, **kwargs)
        logger.info(f"{fn.__name__} args: {args} kwargs: {kwargs} --END-- {rv=}")
        return rv

    return _intern
