import logging
import os
from logging.handlers import SysLogHandler


def _get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "[MCZ MUSA %(name)s][%(asctime)s][%(levelname)s] %(message)s"
    )

    syslog_handler = logging.handlers.SysLogHandler()
    syslog_handler.setLevel(logging.DEBUG)
    syslog_handler.setFormatter(formatter)
    logger.addHandler(syslog_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


def get_logger(name: str) -> logging.Logger:
    log = _get_logger(name)
    return log
