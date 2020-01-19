import logging
import os
from logging.handlers import RotatingFileHandler


def _get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[MCZ MUSA %(name)s][%(asctime)s][%(levelname)s] %(message)s')

    file_handler = RotatingFileHandler('mcz_musa.log', maxBytes=5000, backupCount=1)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


def get_logger(name: str) -> logging.Logger:
    log = _get_logger(name)
    return log
