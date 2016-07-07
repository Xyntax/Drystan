# !/usr/bin/env python
#  -*- coding: utf-8 -*-
__author__ = 'xy'

import os
from requests import exceptions, get
from lib.data import logger
from lib.enums import CUSTOM_LOGGING


def checkHTTP(url, port=0):
    if '://' not in url:
        url = 'http://' + url
    if port:
        port = str(port)
        l = url.split(':')
        if len(l) is 2:
            url = url + ':' + port
        if len(l) is 3:
            l[-1] = port
            url = ':'.join(l)

    try:
        get(url, timeout=5,
            headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:46.0) Gecko/20100101 Firefox/46.0'})
    except exceptions.ConnectionError:
        return False
    logger.log(CUSTOM_LOGGING.SYSINFO, 'HTTP protocol found: ' + url)
    return url


def checkFileHTTP(path, port):
    port = str(port)
    logger.log(CUSTOM_LOGGING.SUCCESS, 'Checking port: ' + port)
    ans = []
    for each in open(path):
        url = checkHTTP(each.strip(), port)
        if url:
            if url.endswith(':80'):
                url = url.replace(':80', '')
            ans.append(url)
    return ans


def checkFolderHTTP(path):
    logger.log(CUSTOM_LOGGING.SUCCESS, 'Entry folder: ' + path)
    ans = []
    for each in os.listdir(path):
        if each.startswith('.') or each.startswith('~'):
            continue
        file = os.path.join(path, each)
        if os.path.isfile(file):
            ans.extend(checkFileHTTP(file, each))
    return ans
