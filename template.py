#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: cirq
# Created Time: 2017-07-28 15:35:59

import json
from timer import timer

class Template(object):
    """
        To initiate 7 harmonic models in Itten's theory.
    """
    with open('models.json', 'r') as reader:
        __dic = json.load(reader)

    def __init__(self, ttype):
        if ttype not in Template.__dic:
            raise ValueError('Template type not defined: %s.' % ttype)
        model = Template.__dic[ttype]
        self.__type = str(model['type'])
        self.__snumber = model['snumber']
        self.__start = model['start']
        self.__end = model['end']
        del model
        self.__theta = 0

    def __str__(self):
        string = '\n'\
            '###############################################\n' +\
            '#        Harmonic Template Information        #\n' +\
            '#              Template Type: %1s               #\n' +\
            '#            Number of Sectors: %1d             #\n' +\
            '%s\n' +\
            '#            Rotated by %3d degree            #\n' +\
            '###############################################\n' +\
            '\n'
        if self.__snumber == 1:
            interval = \
            '#             Sector 1: [%3d,%3d]             #' % ((self.__start[0]+self.__theta)%360, (self.__end[0]+self.__theta)%360)
        elif self.__snumber == 2:
            interval = \
            '#             Sector 1: [%3d,%3d]             #\n' % ((self.__start[0]+self.__theta)%360, (self.__end[0]+self.__theta)%360) +\
            '#             Sector 2: [%3d,%3d]             #' % ((self.__start[1]+self.__theta)%360, (self.__end[1]+self.__theta)%360)
        else:
            raise AttributeError('But this error never occurs!')
        return string % (self.__type, self.__snumber, interval, self.__theta)

    @property
    def type(self):
        return self.__type
    @property
    def snumber(self):
        return self.__snumber
    @property
    def start(self):
        return self.__start
    @property
    def end(self):
        return self.__end
    @property
    def theta(self):
        """
            Theta is the angle for which the template rotates
            (in clockwise direction).
        """
        return self.__theta
    @theta.setter
    def theta(self, value):
        if isinstance(value, int):
            if 0 <= value <= 359:
                self.__theta = value
            else:
                raise ValueError('Rotate angle should in [0, 359]')
        else:
            raise TypeError('Expect an int value for rotate angle theta.')

    def covers_hue(self, hue, sector=2):
        """
            Paper Eq.(2), to check whether a hue value belongs to 
            this harmonic template.
        :param hue: a hue value between 0 and 359.
        :type hue: int
        :param sector: in {0, 1, 2}, indicates which sector belongs
        :type sector: int
        :return: whether the sector covers this hue.
        :rtype: bool
        """
        if isinstance(hue, int):
            rback_hue = (hue - self.__theta) % 360
            if self.__snumber == 1:
                return self.__start[0] <= rback_hue <= self.__end[0]
            elif self.__snumber == 2:
                if sector == 0:
                    return self.__start[0] <= rback_hue <= self.__end[0]
                elif sector == 1:
                    return self.__start[1] <= rback_hue <= self.__end[1]
                elif sector == 2:
                    return (self.__start[0] <= rback_hue <= self.__end[0]) or \
                           (self.__start[1] <= rback_hue <= self.__end[1])
                else:
                    raise ValueError('Parameter sector should be 0, 1 or 2.')
            else:
                raise AttributeError('But this error never occurs!')
        else:
            raise TypeError('Expect an int value for hue.')


if __name__ == '__main__':
    t = Template('Y')
    t.theta = 232
    print t
