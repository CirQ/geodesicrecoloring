#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: cirq
# Created Time: 2017-07-30 12:05:40

import cv2
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
        self.filename = filename
        self.huechannel = self.__tf.read_huechannel('uint16')
        self.shape = self.__tf.shape
        # self.dic0, self.dic1 = None, None

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
        :type sp: (x, y) or int
        :param ep: the ending point.
        :type ep: (x, y) or int
        :return: the geodesic distance between sp and ep.
        :rtype: int64
        """
        angle = None
        if isinstance(sp, tuple) and isinstance(ep, tuple):
            angle = self.huechannel[sp[0]][sp[1]] - self.huechannel[ep[0]][ep[1]]
        elif isinstance(sp, int) and isinstance(ep, int):
            angle = sp - ep
        return min(angle%360, (-angle)%360)

    def __belonging_dictionary(self, template):
        """
            Calculate \Omega_{N1} and \Omega_{N2}
        :param template: A template
        :type template: Template
        :return: three dictionaries represent \Omega_{N1} and \Omega_{N2} and \Omega_N
                 if there are two sectors, otherwise return \Omega_N only.
        :rtype: 3 lists of (x, y) / list of (x, y)
        """
        belonging_dic = []
        if template.snumber == 1:
            for i in range(self.shape[0]):
                for j in range(self.shape[1]):
                    if template.covers_hue(int(self.huechannel[i][j]), sector=0):
                        belonging_dic.append((i, j))
            return belonging_dic
        belonging_dic0 = []
        belonging_dic1 = []
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                if template.covers_hue(self.huechannel[i][j], sector=0):
                    belonging_dic0.append((i, j))
                    belonging_dic.append((i, j))
                elif template.covers_hue(self.huechannel[i][j], sector=1):
                    belonging_dic1.append((i, j))
                    belonging_dic.append((i, j))
        return belonging_dic0, belonging_dic1, belonging_dic

    def __find_most_suitable_sector(self, s_pixel, dic0, dic1):
        """
            Find the most suitable sector to which s_pixel should belong. Eq.(12)
        :param s_pixel: a pixel in \Omega_U
        :type s_pixel: (x(int), y(int))
        :param dic0: \Omega_{N1}
        :type dic0: list of (x, y)
        :param dic1: \Omega_{N2}
        :type dic1: list of (x, y)
        :return: wihch sector should s_pixel enter
        :rtype: int
        """
        min_geo_dist0, min_geo_dist1 = np.int32(0x7FFFFFFF), np.int32(0x7FFFFFFF)
        for t_pixel in dic0:
            tmp_geo_dist0 = self.__geodesic_distance_simple(s_pixel, t_pixel)
            if tmp_geo_dist0 < min_geo_dist0:
                min_geo_dist0 = tmp_geo_dist0
        for t_pixel in dic1:
            tmp_geo_dist1 = self.__geodesic_distance_simple(s_pixel, t_pixel)
            if tmp_geo_dist1 < min_geo_dist1:
                min_geo_dist1 = tmp_geo_dist1
        return 0 if min_geo_dist0 < min_geo_dist1 else 1

    def __recolor_a_pixel(self, s, dic):
        """
            Recolor a pixel. Eq.(13)
        :param s: a pixel's coordinate.
        :type s: (x, y)
        :param dic: \Omega_{NS}
        :type dic: list of (x, y)
        :return: new hue value
        :rtype: float
        """
        numerator, denominator = np.float32(0), np.float32(0)
        weight = lambda d: 1.0 / d
        for t in dic:
            geo_dist = self.__geodesic_distance_simple(s, t)
            numerator += weight(geo_dist)*self.huechannel[s[0]][s[1]]
            denominator += weight(geo_dist)
        return numerator / denominator


    def __recolor_whole_image_in_one_sector(self, template):
        # There will be only one sector.
        hist = cv2.calcHist([self.huechannel], [0], None, [360], [0, 360])
        hist = {i: int(hist[i][0]) for i in range(360)}
        dic = []
        for k, v in hist.items():
            if v != 0:
                if template.covers_hue(k):
                    dic.append(k)
        weight = lambda d: 1.0 / d
        mapping = {}
        for k, v in hist.items():
            if v != 0:
                if not template.covers_hue(k):
                    numerator, denominator = 0.0, 0.0
                    for t in dic:
                        geo_dist = self.__geodesic_distance_simple(k, t)
                        numerator += weight(geo_dist)*t
                        denominator += weight(geo_dist)
                    mapping[k] = int(numerator / denominator)
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                if self.huechannel[i][j] in mapping:
                    self.__tf.huechannel[i][j] = mapping[self.huechannel[i][j]]

    def __recolor_whole_image_in_two_sectors(self, template):
        # There will be two sectors candidates.
        hist = cv2.calcHist([self.huechannel], [0], None, [360], [0, 360])
        hist = {i: int(hist[i][0]) for i in range(360)}
        dic0, dic1, dic = [], [], []
        for k, v in hist.items():
            if v != 0:
                if template.covers_hue(k, sector=0):
                    dic0.append(k)
                    dic.append(k)
                elif template.covers_hue(k, sector=1):
                    dic1.append(k)
                    dic.append(k)
        weight = lambda d: 1.0 / d
        mapping = {}
        for k, v in hist.items():
            if v != 0:
                if not template.covers_hue(k):
                    numerator, denominator = 0.0, 0.0
                    for t in dic0:
                        geo_dist = self.__geodesic_distance_simple(k, t)
                        numerator += weight(geo_dist)*t
                        denominator += weight(geo_dist)
                    map0 = int(numerator / denominator)
                    to0 = self.__geodesic_distance_simple(k, map0)
                    numerator, denominator = 0.0, 0.0
                    for t in dic1:
                        geo_dist = self.__geodesic_distance_simple(k, t)
                        numerator += weight(geo_dist)*t
                        denominator += weight(geo_dist)
                    map1 = int(numerator / denominator)
                    to1 = self.__geodesic_distance_simple(k, map1)
                    mapping[k] = map0 if to0 < to1 else map1
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                if self.huechannel[i][j] in mapping:
                    self.__tf.huechannel[i][j] = mapping[self.huechannel[i][j]]

    def recolor_image(self, template):
        """
            Recolor image with specific template, it will print the 
            information of the chosen template, and save it.
        """
        print template

        if template.snumber == 1:
            self.__recolor_whole_image_in_one_sector(template)
        elif template.snumber == 2:
            self.__recolor_whole_image_in_two_sectors(template)
        filename = ('_%s.'%template.type).join(self.filename.split('.'))
        self.__tf.save_new_image(filename)



    def main(self, ttype='b'):
        if ttype == 'b':
            self.recolor_image(self.__tf.best_template)
        else:
            self.recolor_image(self.__tf.templates[ttype][0])


if __name__ == '__main__':
    geo = Geodesic('tulips.png') # 1 sector
    geo.main('I')
