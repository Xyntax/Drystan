# !/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
Usage:
  python drystan.py DOMAIN [auto] [j1] [j2] [j3]
  python drystan.py IP [auto]

Example:
  python drystan.py baidu.com
  python drystan.py wooyun.org auto j1
  python drystan.py 132.13.211.2

Argument:
  DOMAIN      base target(domain) for scanning.
  IP          base target(ip) for scanning.

Options:
  j1          jump subdomain gathering (Sublist3r,subDomainsBrute).
  j2          jump port scanning (nmap).
  j3          jump bruteforce (hydra).
  auto        run all steps automaticly with default settings.
"""

import sys
from lib.common import initOptions
from lib.interface import *
from lib.enums import TARGET_MODE
from lib.flow import startDomainFlow, startIpFlow


def main():
    if '-h' in sys.argv:
        sys.exit(__doc__)

    conf.AUTO = True if 'auto' in sys.argv else False

    initOptions()
    # logger.log(CUSTOM_LOGGING.SYSINFO, paths)
    if conf.MODE is TARGET_MODE.IP:
        startIpFlow()
    else:
        startDomainFlow()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.log(CUSTOM_LOGGING.ERROR, 'User quit.')
        sys.exit(0)
