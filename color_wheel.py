#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: cirq
# Created Time: 2017-08-01 14:55:22

import cv2
import numpy as np
from math import radians, sin, cos
from template_finder import TemplateFinder

class ColorWheel(object):
    def __init__(self, filename):
        """
            Store two instance vaiable:
            filename: the name of image, to save wheel's image.
            histogram: the filtered histogram value with hue.
        """
        self.filename = filename.split('/')[-1]
        bgr = cv2.imread(filename)
        hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV_FULL)
        huechannel = np.zeros(shape=bgr.shape, dtype='uint16')
        for i in range(bgr.shape[0]):
            for j in range(bgr.shape[1]):
                huechannel[i][j] = np.uint16(hsv[i][j][0] * 360.0 / 256)
        hist = cv2.calcHist([huechannel], [0], None, [360], [0, 360])
        hist = [hist[i][0]/np.max(hist, axis=0) for i in range(360)]
        self.histogram = filter(lambda t: t[1]>1e-4, enumerate(hist))

    def draw_wheel(self, template=None):
        canvas = cv2.imread('wheel_base.png')
        def color(h):
            bgr = np.array([[[int(h*255.0/360), 255, 255]]], dtype='uint8')
            hsv = cv2.cvtColor(bgr, cv2.COLOR_HSV2BGR_FULL)[0][0]
            return int(hsv[0]), int(hsv[1]), int(hsv[2])
        radius, offset = 190, 260
        for hue, hist in self.histogram:
            sp = (int(offset+radius*cos(radians(hue))), int(offset+radius*sin(radians(hue))))
            ep = (int(offset+(1-hist)*radius*cos(radians(hue))), int(offset+(1-hist)*radius*sin(radians(hue))))
            cv2.line(canvas, sp, ep, color(hue), 2)
        if template:
            sp = (offset, offset)
            ep1 = (template.start[0] - 1 + template.theta) % 360
            ep2 = (template.end[0] + 1 + template.theta) % 360
            ep = (int(offset+radius*cos(radians(ep1))), int(offset+radius*sin(radians(ep1))))
            cv2.line(canvas, sp, ep, (0, 0, 0), 1)
            ep = (int(offset+radius*cos(radians(ep2))), int(offset+radius*sin(radians(ep2))))
            cv2.line(canvas, sp, ep, (0, 0, 0), 1)
            if ep1 > ep2:
                cv2.ellipse(canvas, (offset, offset), (radius+2, radius+2), 0, ep1, 360, (0, 0, 0), 1)
                cv2.ellipse(canvas, (offset, offset), (radius+2, radius+2), 0, 0, ep2, (0, 0, 0), 1)
            else:
                cv2.ellipse(canvas, (offset, offset), (radius+2, radius+2), 0, ep1, ep2, (0, 0, 0), 1)
            if template.snumber == 2:
                ep1 = (template.start[1] - 1 + template.theta) % 360
                ep2 = (template.end[1] + 1 + template.theta) % 360
                ep = (int(offset+radius*cos(radians(ep1))), int(offset+radius*sin(radians(ep1))))
                cv2.line(canvas, sp, ep, (0, 0, 0), 1)
                ep = (int(offset+radius*cos(radians(ep2))), int(offset+radius*sin(radians(ep2))))
                cv2.line(canvas, sp, ep, (0, 0, 0), 1)
                if ep1 > ep2:
                    cv2.ellipse(canvas, (offset, offset), (radius+2, radius+2), 0, ep1, 360, (0, 0, 0), 1)
                    cv2.ellipse(canvas, (offset, offset), (radius+2, radius+2), 0, 0, ep2, (0, 0, 0), 1)
                else:
                    cv2.ellipse(canvas, (offset, offset), (radius+2, radius+2), 0, ep1, ep2, (0, 0, 0), 1)
        filename = '%s_wheel.png' % self.filename.split('.')[0]
        cv2.imwrite('wheel_images/'+filename, canvas)


if __name__ == '__main__':
    import pickle
    cw = ColorWheel('images/drops.jpg')
    # with open('drops@jpg.pickle', 'r') as r:
    #     tf = pickle.load(r)
    # cw.draw_wheel(tf.templates['Y'][0])
    cw.draw_wheel()