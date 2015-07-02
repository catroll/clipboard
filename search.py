#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
采用二分法，从一个有序列表中查找指定项
量大的话，效果还是比较显著的：

Level#3 [100 - 1000) 373
    0.001343966
    0.002675056
Level#3 [100 - 1000) 319
    0.001302004
    0.002288103
Level#3 [100 - 1000) 928
    0.001221895
    0.006178856
Level#4 [1000 - 10000) 3661
    0.010846853
    0.026495934
Level#4 [1000 - 10000) 7166
    0.011400938
    0.047900915
Level#4 [1000 - 10000) 6165
    0.006521940
    0.026926994
Level#5 [10000 - 100000) 69506
    0.122932911
    0.376063108
Level#5 [10000 - 100000) 93052
    0.090744019
    0.409357071
Level#5 [10000 - 100000) 53121
    0.088862896
    0.255589008
"""


def search(target, lst):
    if not lst[0] <= target <= lst[-1]:
        return -1

    start = -1
    height = len(lst)

    while start + 1 != height:
        if lst[start + 1] == target:
            return start + 1
        if lst[height - 1] == target:
            return height - 1
        middle = int((start + height) / 2)
        if lst[middle] == target:
            return middle
        if lst[middle] < target:
            start = middle
        else:
            height = middle
    return -1


def comparison(target, lst):
    for index, value in enumerate(lst):
        if value == target:
            return index
    return -1


def test():
    def _test(num):
        l = range(1, 11)
        rst = search(num, l)
        if rst == -1:
            print(u"元素不存在")
        else:
            print(u"元素位置在第 %d 位" % rst)

    cases = (-1, 0, 1, 3, 4, 5, 6, 6.1, 10, 11)
    for i in cases:
        _test(i)


def time_test(level):
    import timeit
    import random

    start, end = 10 ** (level - 1), 10 ** level
    target = random.randint(start, end)
    param_string = '%s, range(%s, %s)' % (target, start, end)
    setup = 'from __main__ import search, comparison'
    number = 100

    def _test(function):
        cost = timeit.timeit('%s(%s)' % (function, param_string), setup, number=number)
        print '%15.9f' % cost

    print 'Level#%s [%s - %s) %s' % (level, start, end, target)
    _test('search')
    _test('comparison')


if __name__ == '__main__':
    # test()
    for i in range(3, 6):
        for j in range(3):
            time_test(i)
