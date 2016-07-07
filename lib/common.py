# !/usr/bin/env python
#  -*- coding: utf-8 -*-
__author__ = 'xy'

import os
import sys
import subprocess
import webbrowser
from lib.data import paths, conf, logger
from lib.enums import CUSTOM_LOGGING, TARGET_MODE
from lib.extracts import getIP
from lib.nmapXMLsort import xml2port
from config import brutePort, webPort
from thirdparty.IPy import IPy
from lib.util.checkhttp import checkFolderHTTP


def checkRoot():
    if os.geteuid():
        sys.exit('Please run as root')


def openBrowser():
    path = paths.OUTPUT_FILE_PATH
    try:
        webbrowser.open_new_tab(path)
    except Exception, e:
        errMsg = '\n[ERROR] Fail to open file with web browser: %s' % path
        raise Exception(errMsg)


def setPaths():
    # root & output
    paths.ROOT_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

    paths.OUTPUT_BASE = os.path.join(paths.ROOT_PATH, 'output')
    if not os.path.exists(paths.OUTPUT_BASE):
        os.mkdir(paths.OUTPUT_BASE)

    paths.OUTPUT_PATH = os.path.join(paths.OUTPUT_BASE, conf.TARGET)
    if not os.path.exists(paths.OUTPUT_PATH):
        os.mkdir(paths.OUTPUT_PATH)

    paths.PORT_PATH = os.path.join(paths.OUTPUT_PATH, 'port')
    if not os.path.exists(paths.PORT_PATH):
        os.mkdir(paths.PORT_PATH)

    paths.HTTP = os.path.abspath(os.path.join(paths.OUTPUT_PATH, 'http.txt'))
    # Nmap output
    paths.TCP = os.path.abspath(os.path.join(paths.OUTPUT_PATH, 'nmap-tcp.xml'))
    # paths.UDP = os.path.abspath(os.path.join(paths.OUTPUT_PATH, 'nmap-tcp.txt'))
    # Hydra output
    paths.HYDRA_OUTPUT_PATH = os.path.abspath(os.path.join(paths.OUTPUT_PATH, 'hydra.txt'))

    # subDomains output
    paths.DOMAIN_DICT = os.path.join(paths.ROOT_PATH, 'subDomainsBrute/dict')
    paths.DOMAIN_OUTPUT_PATH = os.path.abspath(os.path.join(paths.OUTPUT_PATH, 'subDomain.txt'))
    paths.IP_PATH = os.path.abspath(os.path.join(paths.OUTPUT_PATH, 'ips.txt'))

    # dicts
    paths.DICT_PATH = os.path.abspath(os.path.join(paths.ROOT_PATH, 'dics'))
    paths.USR_LIST = os.path.abspath(os.path.join(paths.DICT_PATH, 'usr10.txt'))
    paths.PWD_LIST = os.path.abspath(os.path.join(paths.DICT_PATH, 'pwd40.txt'))

    paths.THEHARVESTER = os.path.abspath(os.path.join(paths.OUTPUT_PATH, 'theHarvester.html'))


def initOptions():
    checkRoot()
    conf.AUTO = False
    if 'auto' in sys.argv:
        conf.AUTO = True
        logger.log(CUSTOM_LOGGING.SYSINFO, 'Start auto mode~')
    setTarget()
    setPaths()


def getIPs():
    def extract(name):
        _ans = set()
        path = os.path.join(paths.OUTPUT_PATH, name)
        if os.path.isfile(path):
            logger.log(CUSTOM_LOGGING.SYSINFO, 'Extracting IPs from ' + name)
            for each in getIP(open(path, 'r').read(), True, True):
                _ans.add(each)
            logger.log(CUSTOM_LOGGING.SYSINFO, 'Total: ' + str(len(_ans)))
        return _ans

    logger.log(CUSTOM_LOGGING.SUCCESS, '===== extract IP from subDomains =====')
    ans = set()
    ans |= extract('subDomain.txt')
    ans |= extract('DNS-zoneTransfer.txt')
    ans |= extract('theHarvester.html')

    # TODO  oh, fuck this func!
    path1 = os.path.join(paths.OUTPUT_PATH, 'sublist3r.txt')
    if os.path.isfile(path1):
        __ans = set()
        logger.log(CUSTOM_LOGGING.SYSINFO, 'Extracting IPs from sublist3r.txt')
        for each in open(path1).readlines():
            p = subprocess.Popen('nslookup ' + each.strip(), shell=True, stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT)
            c = p.stdout.read()
            for ip in getIP(c, True, True):
                __ans.add(ip)
        logger.log(CUSTOM_LOGGING.SYSINFO, 'Total: ' + str(len(__ans)))
        ans |= __ans

    f = open(paths.IP_PATH, 'w')
    for each in ans:
        f.write(each + '\n')
    f.close()
    logger.log(CUSTOM_LOGGING.SYSINFO, 'Unique IP found: ' + str(len(ans)))


def sortNmapXML():
    logger.log(CUSTOM_LOGGING.SUCCESS, '===== sort nmap results =====')

    def _getWebPorts(port_list=webPort):
        l = []
        for each in port_list:
            if os.path.isfile(os.path.join(paths.PORT_PATH, str(each))):
                l.append(str(each))
        return l

    if not os.path.isfile(paths.TCP):
        logger.log(CUSTOM_LOGGING.WARNING, 'nmap result not found, skip.')
        return
    d = xml2port(open(paths.TCP).read())
    for key, value in d.items():
        f = open(os.path.join(paths.PORT_PATH, str(key)), 'w')
        for each in value:
            f.write(each + '\n')
        f.close()
    conf.EXIST_WEB_PORTS = _getWebPorts()
    logger.log(CUSTOM_LOGGING.SYSINFO, 'Different port found: %d' % len(d))


def auto(func):
    '''''
    A decorate function to track all function invoke information with DEBUG level
    Usage:
    @trace_func
    def any_function(any parametet)
    '''

    def tmp(*args, **kargs):
        logger.log(CUSTOM_LOGGING.SUCCESS, '===== Start %s =====' % func.__name__)
        try:
            if not conf.AUTO:
                raw_input(' >>> Press [Enter] to Continue, or [Ctrl-C] to skip current func.')
            return func(*args, **kargs)
        except KeyboardInterrupt:
            print ''  # it's a trick :)
            return

    return tmp


def port(func):
    '''''
    A decorate function to track all function invoke information with DEBUG level
    Usage:
    @trace_func
    def any_function(any parametet)
    '''

    def tmp(*args, **kargs):
        logger.log(CUSTOM_LOGGING.SUCCESS, '===== Exploiting: %s =====' % func.__name__)
        try:
            if not conf.AUTO:
                raw_input(' >>> Press [Enter] to Continue, or [Ctrl-C] to skip current func.')
            ans = func(*args, **kargs)
            # f = open(os.path.join(paths.OUTPUT_PATH, 'portScan_res.txt'), 'w')
            # f.write(ans)
            # f.close()
            return ans
        except KeyboardInterrupt:
            print ''  # it's a trick :)
            return

    return tmp


def setTarget():
    ori_str = conf.TARGET = sys.argv[1]
    for each in ori_str:
        if each.isalpha():
            conf.MODE = TARGET_MODE.DOMAIN
            break
    else:
        conf.MODE = TARGET_MODE.IP
        try:
            _list = IPy.IP(ori_str)
        except Exception, e:
            sys.exit(logger.error('Invalid IP, %s' % e))


def searchHTTP():
    logger.log(CUSTOM_LOGGING.SUCCESS, '===== Searching IP and ports on HTTP protocol =====')
    f = open(paths.HTTP, 'w')
    ans = checkFolderHTTP(paths.PORT_PATH)
    for each in ans:
        f.write(each + '\n')
    f.close()
    logger.log(CUSTOM_LOGGING.SYSINFO, 'Total: ' + str(len(ans)))


if __name__ == '__main__':
    print getIP(open('../output/cnnc.com.cn/subDomain.txt', 'r').read(), True, True)
