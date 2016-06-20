# !/usr/bin/env python
#  -*- coding: utf-8 -*-
from lib.data import paths, conf, logger
from lib.log import CUSTOM_LOGGING
from lib.common import initOptions, runNmap, getIPs
from subDomainsBrute.subDomainsBrute import bruteInterface

initOptions()
# logger.log(CUSTOM_LOGGING.SYSINFO, paths)
logger.log(CUSTOM_LOGGING.SUCCESS, 'Start subDomainsBrute => ' + conf.TARGET_DOMAIN)
bruteInterface()

logger.log(CUSTOM_LOGGING.SUCCESS, 'Extracting IPs from subDomains...')
getIPs()

logger.log(CUSTOM_LOGGING.SUCCESS, 'Staring Nmap... [ctrl-C] to next step.')
runNmap()

