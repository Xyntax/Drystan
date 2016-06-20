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
    paths.NMAP_OUTPUT_PATH = os.path.abspath(os.path.join(paths.OUTPUT_PATH, 'nmap.txt'))

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
    c = open(paths.DOMAIN_OUTPUT_PATH, 'r').read()
    f2 = open(paths.IP_PATH, 'w')
    for each in getIP(c):
        f2.write(each + '\n')
    f2.close()


def runNmap(auto=False):
    while True:
        try:
            base_command = 'nmap -iL ' + paths.IP_PATH

            print '\n' + '[e.g.] ' + base_command + ' -p1-65535 -sV --open --script=auth, brute, vuln'
            print '[1] --script=auth,brute'
            print '[2] -p1-65535 -sV --script=auth,default,brute'

            input_command = raw_input(' > ' + base_command) if not auto else 1
            if str(input_command) is '1':
                input_command = '--script=auth,brute'
            elif str(input_command) is '2':
                input_command = '-p1-65535 -sV --script=auth,default,brute'
            else:
                pass
            command = base_command + ' ' + input_command

            logger.log(CUSTOM_LOGGING.SUCCESS, 'Execute Command: ' + command)
            p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            c = p.stdout.read()
            print c
            file = open(paths.NMAP_OUTPUT_PATH, 'w')
            file.write(c)
            file.close()
            # retval = p.wait()

            if auto:
                break
        except KeyboardInterrupt:
            break
            # ip = conf.TARGET_DOMAIN


def runHydra(auto=False):
    '''
    hydra -L userlist.txt -P pws.txt -M targets.txt ssh
    '''
    while True:
        try:
            base_command = 'hydra -M ' + paths.IP_PATH + ' -L ' + paths.USR_LIST + ' -P ' + paths.PWD_LIST

            print '\n' + '[e.g.] ' + base_command + ' ssh'

            input_command = raw_input(' > ' + base_command) if not auto else 'ssh'
            command = base_command + ' ' + input_command

            logger.log(CUSTOM_LOGGING.SUCCESS, 'Execute Command: ' + command)
            p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            c = p.stdout.read()
            print c
            file = open(paths.NMAP_OUTPUT_PATH, 'w')
            file.write(c)
            file.close()
            # retval = p.wait()

            if auto:
                break
        except KeyboardInterrupt:
            break
            # ip = conf.TARGET_DOMAIN


# TODO
def nmapResultHandler():
    c = open(paths.NMAP_OUTPUT_PATH, 'r').read()


if __name__ == '__main__':
    initOptions()
