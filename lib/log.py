#!/usr/bin/env python
__author__ = 'xy'

import logging
import sys


class CUSTOM_LOGGING:
    SYSINFO = 9
    SUCCESS = 8
    ERROR = 7
    WARNING = 6


logging.addLevelName(CUSTOM_LOGGING.SYSINFO, "*")
logging.addLevelName(CUSTOM_LOGGING.SUCCESS, "+")
logging.addLevelName(CUSTOM_LOGGING.ERROR, "-")
logging.addLevelName(CUSTOM_LOGGING.WARNING, "!")

LOGGER = logging.getLogger("pocketLog")

LOGGER_HANDLER = None
try:
    from thirdparty.ansistrm.ansistrm import ColorizingStreamHandler

    LOGGER_HANDLER = ColorizingStreamHandler(sys.stdout)
    LOGGER_HANDLER.level_map[logging.getLevelName("*")] = (None, "cyan", False)
    LOGGER_HANDLER.level_map[logging.getLevelName("+")] = (None, "green", False)
    LOGGER_HANDLER.level_map[logging.getLevelName("-")] = (None, "red", False)
    LOGGER_HANDLER.level_map[logging.getLevelName("!")] = (None, "yellow", False)
except ImportError:
    LOGGER_HANDLER = logging.StreamHandler(sys.stdout)

FORMATTER = logging.Formatter("\r[%(levelname)s] %(message)s", "%H:%M:%S")

LOGGER_HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(LOGGER_HANDLER)
LOGGER.setLevel(CUSTOM_LOGGING.WARNING)
