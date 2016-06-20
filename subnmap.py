# !/usr/bin/env python
#  -*- coding: utf-8 -*-
import sys
from lib.data import paths, conf, logger
from lib.log import CUSTOM_LOGGING
from lib.common import initOptions, runNmap, getIPs, runHydra
from subDomainsBrute.subDomainsBrute import bruteInterface

if '-h' in sys.argv:
    print 'Usage:\n python subnmap.py DOMAIN [auto] [j1] [j2] [j3]\n' \
          'Example:\n python subnmap.py baidu.com' \
          '\n python subnmap.py wooyun.org auto j1' \
          '\n\nArgument:\n DOMAIN\t base domain for scanning.' \
          '\nOptions:\n j1\tjump subDomainsBrute step.' \
          '\n j2\tjump Nmap step.' \
          '\n j3\tjump Hydra step.' \
          '\n auto\trun all steps automaticly with default settings.'
    sys.exit(0)

auto = True if 'auto' in sys.argv else False

initOptions()
# logger.log(CUSTOM_LOGGING.SYSINFO, paths)
logger.log(CUSTOM_LOGGING.SUCCESS, 'Start subDomainsBrute => ' + conf.TARGET_DOMAIN)
if 'j1' not in sys.argv: bruteInterface()

logger.log(CUSTOM_LOGGING.SUCCESS, 'Extracting IPs from subDomains...')
getIPs()

logger.log(CUSTOM_LOGGING.SUCCESS, 'Staring Nmap... [ctrl-C] to next step.')
if 'j2' not in sys.argv: runNmap(auto)

if 'j3' not in sys.argv: runHydra(auto)
