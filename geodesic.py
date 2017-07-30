#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: cirq
# Created Time: 2017-07-30 12:05:40

import pickle
import numpy as np
from timer import timer
from template_finder import TemplateFinder

class Geodesic(object):
    def __init__(self, filename):
        try:
            with open(filename.replace('.', '@') + '.pickle', 'r') as r:
                self.__tf = pickle.load(r)
        except IOError:
            print 'No such pickle!'
            __import__('sys').exit(1)
        self.huechannel = self.__tf.read_huechannel('int32')

    @staticmethod
    def __straight_distance(sp, ep, distance, axis):
        """
            Calculate the geodesic distance if two points line on the
            same straight aixs.
        :param axis: either 'x' or 'y', the coordinate axis, followed
                    by the specfic coordinate.
        :type axis: (char, int)
        :return: the geodesic distance measured by distance function
        :rtype: uint32
        """
        it_is_so_many_long = np.uint32(0)
        if axis[0] == 'x':
            if sp < ep:
                for i in range(sp+1, ep+1):
                    it_is_so_many_long += distance((axis[1], i-1), (axis[1], i))
            else:               # it only can be sp > ep
                for i in range(ep, sp)[::-1]:
                    it_is_so_many_long += distance((axis[1], i+1), (axis[1], i))
        if axis[0] == 'y':
            if sp < ep:
                for j in range(sp+1, ep+1):
                    it_is_so_many_long += distance((j-1, axis[1]), (j, axis[1]))
            else:               # it only can be sp > ep
                for j in range(ep, sp)[::-1]:
                    it_is_so_many_long += distance((j+1, axis[1]), (j, axis[1]))
        return it_is_so_many_long

    """
     @staticmethod
    def __get_from_direction(sp, ep):
        ""
            Get the direction analog from l, lt, t directions. Totally 4 
            possibilities since I have convinced that sp and ep will not
            line on the same horizontal or vertical line.
        :return: three function analog the direction (l, lt, t)
        :rtype: function, function, function
        ""
        if sp[0] < ep[0] and sp[1] < ep[1]:
            from_l = lambda x, y: (x, y-1)
            from_lt = lambda x, y: (x-1, y-1)
            from_t = lambda x, y: (x-1, y)
        elif sp[0] < ep[0] and sp[1] > ep[1]:
            from_l = lambda x, y: (x, y+1)
            from_lt = lambda x, y: (x-1, y+1)
            from_t = lambda x, y: (x-1, y)
        elif sp[0] > ep[0] and sp[1] > ep[1]:
            from_l = lambda x, y: (x, y+1)
            from_lt = lambda x, y: (x+1, y+1)
            from_t = lambda x, y: (x+1, y)
        else:
            from_l = lambda x, y: (x, y-1)
            from_lt = lambda x, y: (x+1, y-1)
            from_t = lambda x, y: (x+1, y)
        return from_l, from_lt, from_t

    @staticmethod
    def __get_to_direction(sp, ep):
        ""
            Get the direction analog to r, rb, b directions. Totally 4 
            possibilities since I have convinced that sp and ep will not
            line on the same horizontal or vertical line.
        :return: three function analog the direction (r, rb, b)
        :rtype: function, function, function
        ""
        if sp[0] < ep[0] and sp[1] < ep[1]:
            to_r = lambda x, y: (x, y+1)
            to_rb = lambda x, y: (x+1, y+1)
            to_b = lambda x, y: (x+1, y)
        elif sp[0] < ep[0] and sp[1] > ep[1]:
            to_r = lambda x, y: (x, y-1)
            to_rb = lambda x, y: (x+1, y-1)
            to_b = lambda x, y: (x+1, y)
        elif sp[0] > ep[0] and sp[1] > ep[1]:
            to_r = lambda x, y: (x, y-1)
            to_rb = lambda x, y: (x-1, y-1)
            to_b = lambda x, y: (x-1, y)
        else:
            to_r = lambda x, y: (x, y+1)
            to_rb = lambda x, y: (x-1, y+1)
            to_b = lambda x, y: (x-1, y)
        return to_r, to_rb, to_b
    """

    @staticmethod
    def __get_from_direction(sp, ep):
        """
            Get the direction analog from l, lt, t directions. Totally 4 
            possibilities since I have convinced that sp and ep will not
            line on the same horizontal or vertical line.
        :return: three function analog the direction (l, lt, t)
        :rtype: function, function, function
        """
        if sp[0] < ep[0] and sp[1] < ep[1]:
            from_l = lambda y: y-1
            from_lt = lambda x, y: (x-1, y-1)
            from_t = lambda x: x-1
        elif sp[0] < ep[0] and sp[1] > ep[1]:
            from_l = lambda y: y+1
            from_lt = lambda x, y: (x-1, y+1)
            from_t = lambda x: x-1
        elif sp[0] > ep[0] and sp[1] > ep[1]:
            from_l = lambda y: y+1
            from_lt = lambda x, y: (x+1, y+1)
            from_t = lambda x: x+1
        else:
            from_l = lambda y: y-1
            from_lt = lambda x, y: (x+1, y-1)
            from_t = lambda x: x+1
        return from_l, from_lt, from_t

    @staticmethod
    def __get_to_direction(sp, ep):
        """
            Get the direction analog to r, rb, b directions. Totally 4 
            possibilities since I have convinced that sp and ep will not
            line on the same horizontal or vertical line.
        :return: three function analog the direction (r, rb, b)
        :rtype: function, function, function
        """
        if sp[0] < ep[0] and sp[1] < ep[1]:
            to_r = lambda y: y+1
            to_rb = lambda x, y: (x+1, y+1)
            to_b = lambda x: x+1
        elif sp[0] < ep[0] and sp[1] > ep[1]:
            to_r = lambda y: y-1
            to_rb = lambda x, y: (x+1, y-1)
            to_b = lambda x: x+1
        elif sp[0] > ep[0] and sp[1] > ep[1]:
            to_r = lambda y: y-1
            to_rb = lambda x, y: (x-1, y-1)
            to_b = lambda x: x-1
        else:
            to_r = lambda y: y+1
            to_rb = lambda x, y: (x-1, y+1)
            to_b = lambda x: x-1
        return to_r, to_rb, to_b

    def __geodesic_distance_complicated(self, sp, ep):
        """
            Calculate the distance between two pixels in self's huechannel.
            Applying dynamic programming as searching stretegy.
        :param sp: the starting point.
        :type sp: (x, y)
        :param ep: the ending point.
        :type ep: (x, y)
        :return: the geodesic distance between sp and ep.
        :rtype: uint32
        """
        distance = lambda p, q: np.abs(self.huechannel[p[0]][p[1]] - self.huechannel[q[0]][q[1]])
        if sp == ep:                # The same pixel point.
            return np.uint32(0)
        elif sp[0] == ep[0]:        # At the same row.
            return self.__straight_distance(sp[1], ep[1], distance, axis=('x', sp[0]))
        elif sp[1] == ep[1]:        # At the same column.
            return self.__straight_distance(sp[0], ep[0], distance, axis=('y', ep[1]))
        else:
            routemap = np.zeros(shape=self.__tf.shape, dtype='uint32')
            # l, lt, t stand for left, left top, top, respectively
            from_l, from_lt, from_t = self.__get_from_direction(sp, ep)
            # r, rb, b stand for right, right bottom, bottom, respectively
            to_r, to_rb, to_b = self.__get_to_direction(sp, ep)
            i, j = sp
            while i != ep[0]:
                if i != sp[0]:
                    fi, fj = from_t(i), j
                    routemap[i][j] = routemap[fi][fj] + distance((i, j), (fi, fj))
                while j != ep[1]:
                    if i == sp[0]:
                        fi, fj = i, j
                        j = to_r(j)
                        routemap[i][j] = routemap[fi][fj] + distance((i, j), (fi, fj))
                    else:
                        j = to_r(j)
                        li, lj = i, from_l(j)
                        lti, ltj = from_lt(i, j)
                        ti, tj = from_t(i), j
                        l = routemap[li][lj] + distance((i, j), (li, lj))
                        lt = routemap[lti][ltj] + distance((i, j), (lti, ltj))
                        t = routemap[ti][tj] + distance((i, j), (ti, tj))
                        routemap[i][j] = min([l, lt, t])
                i, j = to_b(i), sp[1]
                if i == ep[0]:
                    fi, fj = from_t(i), j
                    routemap[i][j] = routemap[fi][fj] + distance((i, j), (fi, fj))
                    while j != ep[1]:
                        j = to_r(j)
                        li, lj = i, from_l(j)
                        lti, ltj = from_lt(i, j)
                        ti, tj = from_t(i), j
                        l = routemap[li][lj] + distance((i, j), (li, lj))
                        lt = routemap[lti][ltj] + distance((i, j), (lti, ltj))
                        t = routemap[ti][tj] + distance((i, j), (ti, tj))
                        routemap[i][j] = min([l, lt, t])
            return routemap[ep[0]][ep[1]]

    def __geodesic_distance_simple(self, sp, ep):
        """
            Calculate the distance between two pixels in self's huechannel.
            Using simply geometric relationship on color wheel.
        :param sp: the starting point.
        :type sp: (x, y)
        :param ep: the ending point.
        :type ep: (x, y)
        :return: the geodesic distance between sp and ep.
        :rtype: int64
        """
        angle = self.huechannel[sp[0]][sp[1]] - self.huechannel[ep[0]][ep[1]]
        return min(angle%360, (-angle)%360)

    def test(self):
        p, q = (1, 1), (730, 481)
        print self.__geodesic_distance_complicated(p, q)
        print self.__geodesic_distance_simple(p, q)


if __name__ == '__main__':
    geo = Geodesic('cat.png')
    geo.test()
