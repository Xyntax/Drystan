# !/usr/bin/env python
#  -*- coding: utf-8 -*-
from lib.common import initOptions, getIPs, sortNmapXML, searchHTTP
from lib.interface import *
import sys
from config import *


def startDomainFlow():
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
        portScan()
        # Hydra()

    searchHTTP()
    if 'jweb' not in sys.argv:
        BBScan()
        if ENABLE_WEBSOC:
            WebSOC()


def startIpFlow():
    BingC()

    Nmap()
    sortNmapXML()
    portScan()

    Hydra()

    searchHTTP()
    BBScan()

    if ENABLE_WEBSOC:
        WebSOC()
    if ENABLE_POCSCAN:
        pocscan()