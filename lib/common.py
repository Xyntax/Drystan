# !/usr/bin/env python
#  -*- coding: utf-8 -*-
__author__ = 'xy'

import os
import sys
import subprocess
import webbrowser
from lib.data import paths, conf, logger
from lib.log import CUSTOM_LOGGING
from lib.extracts import getIP
from thirdparty.colorama.initialise import init as winowsColorInit
from lib.nmapXMLsort import xml2port
from config import brutePort


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
    paths.OUTPUT_PATH = os.path.join(os.path.join(paths.ROOT_PATH, 'output'), conf.TARGET_DOMAIN)
    if not os.path.exists(paths.OUTPUT_PATH):
        os.mkdir(paths.OUTPUT_PATH)

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


def initOptions():
    if subprocess.mswindows:
        winowsColorInit()
    conf.TARGET_DOMAIN = sys.argv[1]
    setPaths()


def getIPs():
    ans = []

    path1 = os.path.join(paths.OUTPUT_PATH, 'sublist3r.txt')
    path2 = paths.DOMAIN_OUTPUT_PATH
    path3 = os.path.join(paths.OUTPUT_PATH, 'DNS-zoneTransfer.txt')

    if os.path.isfile(path3):
        for each in getIP(open(path3, 'r').read(), True, True):
            ans.append(each)

    if os.path.isfile(path1):
        for each in open(path1).readlines():
            p = subprocess.Popen('nslookup ' + each.strip(), shell=True, stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT)
            c = p.stdout.read()
            for ip in getIP(c, True, True):
                ans.append(ip)

    if os.path.isfile(path2):
        for each in getIP(open(path2, 'r').read(), True, True):
            ans.append(each)

    ans = set(ans)
    f = open(paths.IP_PATH, 'w')
    for each in ans:
        f.write(each + '\n')
    f.close()
    logger.log(CUSTOM_LOGGING.SYSINFO, 'Total: ' + str(len(ans)))


def sortNmapXML():
    if not os.path.isfile(paths.TCP):
        return
    d = xml2port(open(paths.TCP).read())
    for key, value in d.items():
        f = open(os.path.join(paths.OUTPUT_PATH, str(key)), 'w')
        for each in value:
            f.write(each + '\n')
        f.close()


def runSublist3r(auto=False):
    '''
    python sublist3r.py -d domain.com -o output
    '''
    if not auto:
        try:
            raw_input('> Enter to continue,Ctrl-C to jump this step.')
        except KeyboardInterrupt:
            return
    try:
        base_command = 'python ' + os.path.join(paths.ROOT_PATH,
                                                'Sublist3r/sublist3r.py') + ' -d ' + conf.TARGET_DOMAIN + ' -o ' + os.path.join(
            paths.OUTPUT_PATH, 'sublist3r.txt')

        print '\n' + '[RUN] ' + base_command
        input_command = raw_input(' > enable proxychains?[y/N]') if not auto else 'n'
        if input_command in ['Y', 'y']:
            command = 'proxychains ' + base_command
        else:
            command = base_command
        logger.log(CUSTOM_LOGGING.SUCCESS, 'Execute Command: ' + command)
        os.system(command)
    except KeyboardInterrupt:
        return
        # except Exception, e:
        #     print logger.log(CUSTOM_LOGGING.WARNING, 'Connection Error: ' + e)
        #     pass


def runSubDomainBrute(auto=False):
    if not auto:
        try:
            raw_input('> Enter to continue,Ctrl-C to jump this step.')
        except KeyboardInterrupt:
            return
    path = os.path.join(paths.ROOT_PATH, 'subDomainsBrute')
    os.chdir(path)
    command = 'python subDomainsBrute.py -t 50 ' + conf.TARGET_DOMAIN + ' -o ' + os.path.join(
        paths.OUTPUT_PATH, 'subDomain.txt')
    logger.log(CUSTOM_LOGGING.SUCCESS, 'Execute Command: ' + command)
    os.system(command)
    os.chdir(paths.ROOT_PATH)
    print ''  # it's a joke


def runNmap(auto=False):
    if not auto:
        try:
            raw_input('> Enter to continue,Ctrl-C to jump this step.')
        except KeyboardInterrupt:
            return
    command = 'sudo nmap -iL ' + paths.IP_PATH + ' -Pn --open --script=auth,default -oX ' + paths.TCP
    os.system(command)


def _hydraCommand(src, port):
    command = 'hydra -q -f -en -M ' + src + ' -L ' + paths.USR_LIST + ' -P ' + paths.PWD_LIST + ' ' + str(port)
    logger.log(CUSTOM_LOGGING.SYSINFO, 'Execute Command: ' + command)
    try:
        os.system(command)
    except KeyboardInterrupt:
        return


def runHydra(auto=False):
    if not auto:
        try:
            raw_input('> Enter to continue,Ctrl-C to jump this step.')
        except KeyboardInterrupt:
            print ''
            return
    for k, v in brutePort.items():
        fpath = os.path.join(paths.OUTPUT_PATH, k)
        if os.path.isfile(fpath):
            logger.log(CUSTOM_LOGGING.SUCCESS, 'Targets brute on service: ' + v)
            _hydraCommand(fpath, v)
    else:
        logger.log(CUSTOM_LOGGING.SYSINFO, ' (hydra) No available ports for brute')
