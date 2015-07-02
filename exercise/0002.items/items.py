# -*- coding: utf-8 -*-

import re

items_pattern = re.compile('[^\s]+')


def line_items(items_str):
    return items_pattern.findall(items_str)


def lines_items(items_str):
    return [line_items(line) for line in items_str.split('\n')]


def vertical_items(items_str):
    def trim(lists):
        while [] in lists:
            lines.remove([])

    lines = lines_items(items_str)
    trim(lines)
    items = []
    while lines:
        for line in lines:
            items.append(line.pop(0))
        trim(lines)
    return items


def horizontal_items(items_str):
    lines = lines_items(items_str)
    items = []
    for line in lines:
        items.extend(line)
    return items


if __name__ == '__main__':
    print vertical_items("""
    lxc-attach           lxc-destroy          lxc-start          
    lxc-autostart        lxc-device           lxc-start-ephemeral
    lxc-cgroup           lxc-dnsmasq          lxc-stop           
    lxc-checkconfig      lxc-execute          lxc-top            
    lxc-checkpoint       lxc-freeze           lxc-unfreeze       
    lxc-clone            lxc-info             lxc-unshare        
    lxc-config           lxc-ls               lxc-usernsexec     
    lxc-console          lxc-monitor          lxc-wait           
    lxc-create           lxc-snapshot 
    """)
    print horizontal_items("""
    a b c d e f g
    h i j k l m n
    """)

