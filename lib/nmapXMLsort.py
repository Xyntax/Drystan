# !/usr/bin/env python
#  -*- coding: utf-8 -*-
__author__ = 'xy'

import re


def xml2port(content):
    """
    sort nmap-result-xml(-oX) by port

    function return like:
    {'443': ['114.251.14.66', '106.37.199.246', '120.55.235.38', '121.43.73.233'],
     '7001': ['219.143.230.134', '114.251.229.250'],
     '80': ['114.251.229.196', '114.251.14.66', '219.143.230.173', '106.37.199.246', '120.55.235.38', '219.143.230.133', '121.43.73.233', '111.203.203.5']
     }
    """
    port_list = list(set(re.findall(r'portid="(.*?)">', content)))
    # print 'All ports: '
    # print port_list
    ans = dict()
    for port in port_list:
        ans[port] = []

    l = content.split('<address addr="')[1:]
    for each in l:
        for port in port_list:
            if 'portid="%s"' % str(port) in each:
                ans[port].append(each.split('"')[0])

    return ans
