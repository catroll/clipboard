#!/bin/env python
# -*- coding: utf-8 -*-

"""
使用 libvirt 抓取 KVM 虚拟机的缩略图（待验证）
from http://www.oschina.net/code/snippet_1988449_49174
"""

import libvirt
import os
import uuid
try:
    from PIL import Image
    print("PIL")
except ImportError:
    import Image
def handler(stream, buf, opaque):
    fd = opaque
    os.write(fd, buf)
THUMBNAIL_SIZE =(256, 256)
thumbnail = '/home/hcc/test/screenshot/test-' + str(uuid.uuid4())
command = "touch " + thumbnail
print(command)
os.system(command)
fd = os.open(thumbnail, os.O_WRONLY | os.O_TRUNC | os.O_CREAT, 0644)
try:
    conn = libvirt.open('qemu:///system')
    d1 = conn.lookupByName('test')
    print(d1.info())
    print(d1.name())
    stream = conn.newStream(0)
    d1.screenshot(stream, 0, 0)
    stream.recvAll(handler, fd)
    if os.path.getsize(thumbnail) == 0:
        image = Image.new("RGB", THUMBNAIL_SIZE, 'black')
        image.save(thumbnail)
    else:
        print("else")
        im = Image.open(thumbnail)
        im.thumbnail(THUMBNAIL_SIZE)
        im.save(thumbnail,'PNG')
except libvirt.libvirtError:
    try:
        stream.abor()
    except:
        pass
else:
    stream.finish()
finally:
    os.close(fd)

