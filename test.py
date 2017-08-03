#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: cirq
# Created Time: 2017-08-01 10:23:06

import pickle
from template_finder import TemplateFinder
from geodesic import Geodesic
from color_wheel import ColorWheel

def main():
    img = 'angel.jpg'
    ttype = 'b'
    if ttype is None:
        tf = TemplateFinder('images/' + img)
        tf.find_templates_with_dump(0.1)
        cw = ColorWheel('images/' + img)
        cw.draw_wheel()
    elif ttype != 'b':
        geo = Geodesic(img)
        geo.main(ttype)
        with open('%s.pickle'%('@'.join(img.split('.'))), 'r') as r:
            tf = pickle.load(r)
        cw = ColorWheel('after_images/%s_%s.%s' % (img.split('.')[0], ttype, img.split('.')[1]))
        cw.draw_wheel(tf.templates[ttype][0])
    else:
        geo = Geodesic(img)
        geo.main()
        with open('%s.pickle'%('@'.join(img.split('.'))), 'r') as r:
            tf = pickle.load(r)
        cw = ColorWheel('after_images/%s_%s.%s' % (img.split('.')[0], tf.best_template.type, img.split('.')[1]))
        cw.draw_wheel(tf.best_template)


main()