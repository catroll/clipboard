# Python 练习题

## 0001 工资条

```
$ python 0001.income_tax/income.py -h
usage: income.py [-h] [--work work_days] [--leave leave_days] wage

按照工资计算公式计算最终能领到的工资。

positional arguments:
  wage                基本工资，默认 6000

optional arguments:
  -h, --help          show this help message and exit
  --work work_days    工作天数，默认 23
  --leave leave_days  请假天数，默认 0（暂不支持）
```

## 0002 条目解析

实在也不知道叫什么名字好。

``` python
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
# ['lxc-attach', 'lxc-autostart', 'lxc-cgroup', 'lxc-checkconfig', 'lxc-checkpoint', 'lxc-clone', 'lxc-config', 'lxc-console', 'lxc-create', 'lxc-destroy', 'lxc-device', 'lxc-dnsmasq', 'lxc-execute', 'lxc-freeze', 'lxc-info', 'lxc-ls', 'lxc-monitor', 'lxc-snapshot', 'lxc-start', 'lxc-start-ephemeral', 'lxc-stop', 'lxc-top', 'lxc-unfreeze', 'lxc-unshare', 'lxc-usernsexec', 'lxc-wait']
print horizontal_items("""
a b c d e f g
h i j k l m n
""")
# ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n']
```

