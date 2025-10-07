import logging
import sys

from mouse_velocity_tracker import conf


def getLogger(name: str) -> logging.Logger:
    configuration = conf.read_config()
    log_level = getattr(logging, configuration["log_level"].upper())

    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    handler = logging.StreamHandler(stream=sys.stderr)
    handler.formatter

    log_format = "%(levelname)s:     [%(asctime)s] %(message)s"
    formatter = logging.Formatter(log_format, datefmt="%Y-%m-%d %H:%M:%S")

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
