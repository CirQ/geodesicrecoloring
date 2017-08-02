#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: cirq
# Created Time: 2017-08-01 10:23:06

import pickle
from template_finder import TemplateFinder
from geodesic import Geodesic
from color_wheel import ColorWheel

def main():
    img = 'drops.jpg'
    ttype = None
    # tf = TemplateFinder('images/' + img)
    # tf.find_templates_with_dump(0.1)
    if ttype is None:
        cw = ColorWheel('images/' + img)
        cw.draw_wheel()
    elif ttype != 'b':
        geo = Geodesic(img)
        geo.main(ttype)
        cw = ColorWheel('images/' + img)
        with open('%s.pickle'%('@'.join(img.split('.'))), 'r') as r:
            tf = pickle.load(r)
        cw.draw_wheel(tf.templates[ttype][0])
    else:
        geo = Geodesic(img)
        geo.main()
        cw = ColorWheel('images/' + img)
        with open('%s.pickle'%('@'.join(img.split('.'))), 'r') as r:
            tf = pickle.load(r)
        cw.draw_wheel(tf.best_template)


main()