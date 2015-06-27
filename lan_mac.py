#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
通过 scapy 获取局域网中所有主机 mac 地址
from: http://www.oschina.net/code/snippet_1024339_35430

提示：运行时加上 sudo！

结果如下：

94:de:80:47:06:1b - 10.1.33.39
74:d4:35:be:cd:27 - 10.1.33.51
...

from scapy.all import ls, lsc, TCP
print ' Packages '.center(70, '*')
print ls()  # ls(TCP)
print ' Functions '.center(70, '*')
print lsc()

srp:  Send and receive packets at layer 2
"""

from scapy.all import srp
# WARNING: No route found for IPv6 destination :: (no default route?)
from scapy.all import Ether, ARP

network = '10.1.33.91/21'

try:
    ans, unans = srp(Ether(dst="FF:FF:FF:FF:FF:FF") / ARP(pdst=network), timeout=2, verbose=False)
except Exception, e:
    print 'Exception:', str(e)
    exit()
else:
    for snd, rcv in ans:
        addresses = rcv.sprintf("%Ether.src% - %ARP.psrc%")
        print addresses
