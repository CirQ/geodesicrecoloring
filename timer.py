#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: cirq
# Created Time: 2017-07-29 11:50:25

import time

def timer(unit):
    """
        A decorator to estimate the execution time of function.
    :param unit: the unit measurement required. Can only be 'ms' or 's'
    :type unit: char
    """
    def funcwrapper(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            ret = func(*args, **kwargs)
            end = time.time()
            if unit == 'ms':
                duration = (end - start) * 1000
                print '\n\n=> Function %s executes for %.8f millisecond. <=\n\n' % (func.__name__, duration)
            elif unit == 's':
                duration = end - start
                print '\n\n=> Function %s executes for %.8f second. <=\n\n' % (func.__name__, duration)
            else:
                raise ValueError('unit can only be "ms" or "s"')
            return ret
        return wrapper
    return funcwrapper


if __name__ == '__main__':
    @timer(unit='ms')
    def somefunction():
        print "fuck you"

    somefunction()
