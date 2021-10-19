import logging

from .const import LOGGER_NAME

DISABLE_LOGGER = False

_LOGGER = logging.getLogger(LOGGER_NAME)
_LOGGER.addFilter(lambda record: not DISABLE_LOGGER)
