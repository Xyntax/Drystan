# !/usr/bin/env python
#  -*- coding: utf-8 -*-
__author__ = 'xy'

import os
import sys
from logger import logger


def checkCommand():
    for name in Commands:
        logger.info('checking requirement: %s' % name)
        if name in os.popen('which ' + name.strip()).read():
            logger.info('success!')
        else:
            logger.error('failed! please install with "apt-get/yum" manually: %s ' % name)


# TODO
def updateCommand():
    pass


def checkGithubDownload():
    for url in githubDownloads:
        dirname = url.split('/')[-1].replace('.git', '')
        logger.info('checking requirement: %s' % dirname)
        if os.path.isdir(os.path.join(os.path.abspath(os.path.dirname('__file__')), dirname)):
            logger.info('success!')
        else:
            logger.info('downloading %s from github...' % dirname)
            os.system('git clone %s' % url)


def GithubUpdate():
    for each in githubDownloads:
        dirname = each.split('/')[-1].replace('.git', '')
        logger.info('updating: %s' % dirname)
        os.system('cd %s && git pull' % dirname)


githubDownloads = [
    "https://github.com/lijiejie/subDomainsBrute.git",
    "https://github.com/lijiejie/BBScan.git",
    "https://github.com/aboul3la/Sublist3r.git",
    "https://github.com/Xyntax/websoc-cli.git",
    "https://github.com/Xyntax/BingC.git",
    "https://github.com/laramies/theHarvester.git"
]

Commands = [
    'nmap',
    'hydra',
    'nslookup',
    'dig',
    'whois',
    'msfconsole',
    'git'
]

if __name__ == '__main__':

    checkCommand()
    checkGithubDownload()
    if 'update' in sys.argv:
        updateCommand()
        GithubUpdate()
