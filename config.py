# !/usr/bin/env python
#  -*- coding: utf-8 -*-
__author__ = 'xy'

# hydra will brute all open ports below
brutePort = {
    '110': 'pop3',
    '995': 'pop3s',
    '22': 'ssh',
    '21': 'ftp',
    '990': 'ftps',
    '143': 'imap',
    '194': 'irc',
    '161': 'snmp',
    '992': 'telnets',
    '23': 'telnet',
    '3306': 'mysql',
    '1433': 'mssql',
    '1521': 'oracle',
    '6379': 'redis',
}

# define ports for WEB-application scan(http/https,spider,scripts)
webPort = [80, 443]

ENABLE_WEBSOC = True
