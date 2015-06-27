#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import getopt
import socket
import threading
from Queue import Queue


line = 20
lock = threading.Lock()


def print_help():
    pr("""#-------------------------------------------------#
# -a start_ip : 扫描局域网中所有 IP 对应的 hostname, start_ip 为局域网前三位 IP
# -i IP       : 查找指定 IP 对应的 hostname
# -h hostname : 查找指定 hostname 对应的 IP
# -f filename : 输出文件保存地址
#-------------------------------------------------#
# Usage       : ./NetScan.py -a start_ip
# Example     : ./NetScan.py -a 192.168.0  -f /tmp/netscan.txt""")


class NetScan(threading.Thread):
    ip = None
    aliases = None
    addresses = None

    def __init__(self, queue, result):
        threading.Thread.__init__(self)
        self.queue = queue
        self.result = result

    def run(self):
        while True:
            if self.queue.empty():
                break
            self.scan()

    def scan(self):
        self.ip = self.queue.get()
        try:
            self.name, self.aliases, self.addresses = socket.gethostbyaddr(self.ip)
            pr("%s ===> %s" % (self.ip, self.name))
            self.result[self.ip] = self.name
        except Exception, e:
            pr(self.ip.ljust(15), e)


def pr(*args):
    lock.acquire()
    for i in args:
        print i,
    print
    lock.release()


def ip_range(start_ip):
    return ["%s.%s" % (start_ip, i) for i in range(1, 255)]


def ip2hostname(ip):
    try:
        name, aliases, addresses = socket.gethostbyaddr(ip)
    except Exception as e:
        pr(e)
        return ''
    else:
        return name


def hostname2ip(hostname):
    try:
        target_ip = socket.gethostbyname(hostname)
    except Exception as e:
        pr(e)
        return ''
    else:
        return target_ip


def main():
    if len(sys.argv) < 3:
        print_help()
        sys.exit(1)
    else:
        try:
            opts, args = getopt.getopt(sys.argv[1:], "a:i:h:f:")
        except:
            print_help()
            sys.exit(1)

    start_ip = None
    single_ip = None
    hostname = None
    savefile = None

    for opt, arg in opts:
        if opt == '-a':
            start_ip = arg
        elif opt == '-i':
            single_ip = arg
        elif opt == '-h':
            hostname = arg
        elif opt == '-f':
            savefile = arg
        else:
            pr("参数设置错误！！！")
            print_help()
            sys.exit(1)

    if start_ip:
        ips = ip_range(start_ip)
        queue = Queue()
        for ip in ips:
            queue.put(ip)
        threads = []
        dic = {'abc': 'hw'}
        for p in range(line):
            t = NetScan(queue, dic)
            t.start()
            threads.append(t)
        for t in threads:
            t.join()

        pr("------------------finish------------------")
        if dic and savefile:
            pr("查询出 hostname：%s" % len(dic))
            try:
                f = open(savefile, 'w')
                i = 0
                for key in dic:
                    f.write("%d : %s ===> %s \n" % (i, key, dic[key]))
                    i += 1
                f.close()
            except Exception as e:
                pr(e)
    elif single_ip:
        pr("%s ===> %s" % (single_ip, ip2hostname(single_ip)))
    else:
        pr("%s ===> %s" % (hostname, hostname2ip(hostname)))


if __name__ == '__main__':
    main()
