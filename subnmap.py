# !/usr/bin/env python
#  -*- coding: utf-8 -*-
import sys
from lib.common import initOptions, getIPs, sortNmapXML
from lib.interface import *
from config import ENABLE_WEBSOC


def main():
    if '-h' in sys.argv:
        usage = 'Usage:\n python subnmap.py DOMAIN [auto] [j1] [j2] [j3]\n' \
                'Example:\n python subnmap.py baidu.com' \
                '\n python subnmap.py wooyun.org auto j1' \
                '\n\nArgument:\n DOMAIN\t base domain for scanning.' \
                '\nOptions:\n j1\tjump subdomain gathering (Sublist3r,subDomainsBrute).' \
                '\n j2\tjump port scanning (nmap).' \
                '\n j3\tjump bruteforce (hydra).' \
                '\n auto\trun all steps automaticly with default settings.'
        sys.exit(usage)

    conf.AUTO = True if 'auto' in sys.argv else False

    initOptions()
    # logger.log(CUSTOM_LOGGING.SYSINFO, paths)

    if 'j1' not in sys.argv:
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
