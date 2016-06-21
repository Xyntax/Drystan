# !/usr/bin/env python
#  -*- coding: utf-8 -*-
import re


def getIP(content, remove_duplicate=True, remove_private=False):
    """
    > print getIP('ffeac12.2.2.2asf^&10.10\n.1.1ffa2\n')
    ['12.2.2.2','10.10.1.1']

    """
    content = content.replace('\n', ',')
    p = re.compile(r'(?:(?:2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(?:2[0-4]\d|25[0-5]|[01]?\d\d?)')
    _ = re.findall(p, content)
    ans = list(set(_)) if remove_duplicate else _

    if remove_private:
        for each in ans:
            if _isPrivateIP(each):
                ans.remove(each)

    return ans


def _isPrivateIP(strict_IP):
    p1 = re.compile(r'^10\.|^172\.(?:1[6789]|2\d|31)\.|^192\.168\.|^127\.')
    return True if re.match(p1, strict_IP) else False





if __name__ == '__main__':
    l = [80]
    print xml2port(open('../output/sinosig.com/nmap-tcp.xml').read())
