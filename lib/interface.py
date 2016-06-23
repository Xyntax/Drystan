# !/usr/bin/env python
#  -*- coding: utf-8 -*-
__author__ = 'xy'

import os
from lib.data import paths, conf, logger
from lib.enums import CUSTOM_LOGGING, TARGET_MODE
from lib.common import auto
from config import brutePort
from poc.zonetransfer import poc as zonetransfer_poc


@auto
def DNSzoneTransfer():
    path = os.path.join(paths.OUTPUT_PATH, 'DNS-zoneTransfer.txt')
    logger.info('Target domain: ' + conf.TARGET)
    if zonetransfer_poc(conf.TARGET, path):
        logger.warning('Vulnerable!')
        logger.info('Save results to %s' % path)
    else:
        logger.info('Not vulnerable.')


@auto
def Sublist3r():
    base_command = 'python ' + os.path.join(paths.ROOT_PATH,
                                            'Sublist3r/sublist3r.py') + ' -d ' + conf.TARGET + ' -o ' + os.path.join(
        paths.OUTPUT_PATH, 'sublist3r.txt')

    input_command = raw_input(' > enable proxychains?[y/N]') if not conf.AUTO else 'n'
    if input_command in ['Y', 'y']:
        command = 'proxychains ' + base_command
    else:
        command = base_command
    logger.log(CUSTOM_LOGGING.SUCCESS, 'Execute Command: ' + command)
    os.system(command)


@auto
def SubDomainBrute():
    path = os.path.join(paths.ROOT_PATH, 'subDomainsBrute')
    os.chdir(path)
    command = 'python subDomainsBrute.py -t 50 ' + conf.TARGET + ' -o ' + os.path.join(
        paths.OUTPUT_PATH, 'subDomain.txt')
    logger.log(CUSTOM_LOGGING.SUCCESS, 'Execute Command: ' + command)
    os.system(command)
    os.chdir(paths.ROOT_PATH)
    print ''  # it's a joke


@auto
def Nmap():
    if conf.MODE is TARGET_MODE.DOMAIN:
        command = 'sudo nmap -iL ' + paths.IP_PATH + ' -Pn --open --script=auth,default -oX ' + paths.TCP
    elif conf.MODE is TARGET_MODE.IP:
        c = '.'.join(conf.TARGET.split('.')[0:3]) + '.0/24'
        command = 'sudo nmap %s -Pn --open --script=auth,default -oX %s' % (c, paths.TCP)
    else:
        raise Exception('conf.Mode incorrect in func [@auto Nmap()]')
    os.system(command)


@auto
def Hydra():
    flag = False  # fuck the for-else

    def _hydraCommand(src, port):
        command = 'hydra -q -f -en -M ' + src + ' -L ' + paths.USR_LIST + ' -P ' + paths.PWD_LIST + ' ' + str(port)
        logger.log(CUSTOM_LOGGING.SYSINFO, 'Execute Command: ' + command)
        try:
            os.system(command)
        except KeyboardInterrupt:
            return

    for k, v in brutePort.items():
        fpath = os.path.join(paths.OUTPUT_PATH, k)
        if os.path.isfile(fpath):
            flag = True
            logger.log(CUSTOM_LOGGING.SUCCESS, 'Targets brute on service: ' + v)
            _hydraCommand(fpath, v)
    if not flag:
        logger.log(CUSTOM_LOGGING.SYSINFO, ' (hydra) No available ports for brute, skip.')


@auto
def WebSOC():
    if conf.has_key('EXIST_WEB_PORTS'):
        os.chdir(os.path.join(paths.ROOT_PATH, 'websoc-cli'))
        for each in conf.EXIST_WEB_PORTS:
            os.system('python websoc-cli.py %s %s' % (conf.TARGET, os.path.join(paths.OUTPUT_PATH, str(each))))
    else:
        logger.log(CUSTOM_LOGGING.SYSINFO, ' (websoc) No web application found, skip.')
    os.chdir(paths.ROOT_PATH)


@auto
def theHarvester():
    os.chdir(os.path.join(paths.ROOT_PATH, 'theHarvester'))

    command = "theharvester -d %s -l 100 -b all -f %s" % (conf.TARGET, paths.THEHARVESTER)

    input_command = raw_input(' > enable proxychains?[y/N]') if not conf.AUTO else 'n'
    if input_command in ['Y', 'y']:
        command = 'proxychains ' + command

    os.system(command)
    os.chdir(paths.ROOT_PATH)


@auto
def whois():
    command = "whois %s" % conf.TARGET
    c = os.popen(command).read()
    print c
    open(os.path.join(paths.OUTPUT_PATH, 'whois.txt'), 'w').write(c)


@auto
def dig():
    command = "dig -x %s" % conf.TARGET
    c = os.popen(command).read()
    print c
    open(os.path.join(paths.OUTPUT_PATH, 'dig.txt'), 'w').write(c)


@auto
def BingC():
    os.chdir(os.path.join(paths.ROOT_PATH, 'BingC'))
    path = os.path.join(paths.OUTPUT_PATH, 'bingc.txt')
    command = "python bingC.py %s %s" % ('.'.join(conf.TARGET.split('.')[0:3]) + '.0/24', path)
    os.system(command)
    os.chdir(paths.ROOT_PATH)
