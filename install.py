# !/usr/bin/env python
#  -*- coding: utf-8 -*-
__author__ = 'xy'

import os
from logger import logger


def checkCommand(name):
    logger.info('checking requirement: %s' % name)
    if name in os.popen('which ' + name.strip()).read():
        logger.info('success!')
    else:
        logger.error('failed! please install with "apt-get/yum" manually: %s ' % name)


def checkGithubDownload(url):
    dirname = url.split('/')[-1].replace('.git', '')
    logger.info('checking requirement: %s' % dirname)
    if os.path.isdir(os.path.join(os.path.abspath(os.path.dirname('__file__')), dirname)):
        logger.info('success!')
    else:
        logger.info('downloading %s from github...' % dirname)
        os.system('git clone %s' % url)


githubDownloads = [
    "https://github.com/lijiejie/subDomainsBrute.git",
    "https://github.com/aboul3la/Sublist3r.git",
    "https://github.com/Xyntax/websoc-cli"
]

Commands = [
    'nmap',
    'hydra',
    'nslookup',
    'dig'
]

if __name__ == '__main__':
    for each in Commands:
        checkCommand(each)
    for each in githubDownloads:
        checkGithubDownload(each)
