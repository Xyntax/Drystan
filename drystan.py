# !/usr/bin/env python
#  -*- coding: utf-8 -*-
import sys
from lib.common import initOptions, getIPs, sortNmapXML
from lib.interface import *
from lib.enums import TARGET_MODE
from config import ENABLE_WEBSOC


def main():
    if '-h' in sys.argv:
        usage = 'Usage:\n python drystan.py DOMAIN [auto] [j1] [j2] [j3]' \
                '\n python drystan.py IP [auto]' \
                'Example:\n python drystan.py baidu.com' \
                '\n python drystan.py wooyun.org auto j1' \
                '\n python drystan.py 132.13.211.2' \
                '\n\nArgument:\n DOMAIN\t base domain for scanning.' \
                '\nOptions:\n j1\tjump subdomain gathering (Sublist3r,subDomainsBrute).' \
                '\n j2\tjump port scanning (nmap).' \
                '\n j3\tjump bruteforce (hydra).' \
                '\n auto\trun all steps automaticly with default settings.'
        sys.exit(usage)

    conf.AUTO = True if 'auto' in sys.argv else False

    initOptions()
    # logger.log(CUSTOM_LOGGING.SYSINFO, paths)
    if conf.MODE is TARGET_MODE.IP:
        sys.argv.append('j1')

    if 'j1' not in sys.argv:
        whois()
        dig()
        theHarvester()
        DNSzoneTransfer()
        Sublist3r()
        SubDomainBrute()
    getIPs()

    if 'j2' not in sys.argv:
        Nmap()
    sortNmapXML()

    if 'j3' not in sys.argv:
        Hydra()

    if 'jweb' not in sys.argv:
        if ENABLE_WEBSOC:
            WebSOC()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.log(CUSTOM_LOGGING.ERROR, 'User quit.')
        sys.exit(0)
