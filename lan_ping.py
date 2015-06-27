#!/usr/bin/env python
# -*- coding:utf8 -*-

import Queue
import threading
import subprocess
import re
import sys

lock = threading.Lock()
DEFAULT_THREAD_NUM = 100


def get_ips(ip):
    a = re.match(r'(.*\d+)\.(\d+)-(\d+)', ip)
    if not a:
        raise Exception('IP range error')
    start = int(a.group(2))
    end = int(a.group(3)) + 1
    ips = []
    for i in range(start, end):
        ips.append(a.group(1) + "." + str(i))
    return ips


def ping(queue):
    while True:
        if queue.empty():
            sys.exit()
        ip = queue.get()
        ret = subprocess.call("ping -c 1 %s" % ip, shell=True,
                              stdout=open('/dev/null', 'w'),
                              stderr=subprocess.STDOUT)
        lock.acquire()
        if ret == 0:
            print ip
        lock.release()
        queue.task_done()


def main():
    args, arg_num = sys.argv, len(sys.argv)
    if arg_num < 2 or arg_num > 3:
        print "Usage: %s IP段(如:192.168.1.1-254) 线程数(默认:100)" % args[0]
        exit()
    ip_range = get_ips(args[1])
    thread_num = int(args[2]) if arg_num == 3 and args[2].isdigit() else DEFAULT_THREAD_NUM
    queue = Queue.Queue()
    for i in ip_range:
        queue.put(i)
    for q in range(thread_num):
        worker = threading.Thread(target=ping, args=(queue,))
        worker.setDaemon(True)
        worker.start()
    queue.join()


if __name__ == "__main__":
    main()
