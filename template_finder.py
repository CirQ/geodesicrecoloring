#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: cirq
# Created Time: 2017-07-29 10:54:38

import cv2
import pickle
import numpy as np
from timer import timer
from image import Image
from template import Template

# This solution is abort for performance reason
#
# class TemplateFinder(Image, Template):
#     def __init__(self, filepath, ttype):
#         super(TemplateFinder, self).__init__(filepath)
#         super(Image, self).__init__(ttype)
#
# if __name__ == '__main__':
#     tf = TemplateFinder('images/pool.png', 'X')
#     print tf.covers_hue(90)

class TemplateFinder(Image):
    type_list = ['i', 'V', 'T', 'L', 'I', 'Y', 'X']

    def __init__(self, filepath):
        super(TemplateFinder, self).__init__(filepath)
        self.__templates = {}
        self.__best_template = None

    @property
    def templates(self):
        return self.__templates
    @property
    def best_template(self):
        return self.__best_template

    def __potential(self, template):
        """
            Calculate the potential function defined in Eq.(1)
        :param template: A (maybe) harmonic template.
        :type template: Template
        :return: value of potential function.
        :rtype: float
        """
        hist = cv2.calcHist([self._huechannel], [0], None, [360], [0, 360])
        numerator, denominator = np.float32(0), np.float32(0)
        one = np.float32(1)
        for i in range(360):
            if template.covers_hue(i):
                numerator += hist[i][0]
                denominator += one
        potential = numerator / denominator
        return potential

    def __find_one_template(self, ttype):
        """
            Find most suitable rotate angle, i.e., Eq.(3).
        :param ttype: the model type.
        :type ttype: char
        :return: The most suitable template instance with corresponding
                 potential will be recorded in the dictionary.
        :rtype: None
        """
        t = Template(ttype)
        max_potential, max_theta = np.float32(-1), -1
        ###############################################################
        #
        # Have you remember that there is a problem in Leetcode which
        # requires to find the maximal in a rotated sorted array?
        #
        ###############################################################
        for theta in range(0, 360):
            t.theta = theta
            tmp_potential = self.__potential(t)
            if tmp_potential > max_potential:
                max_potential, max_theta = tmp_potential, theta
        t.theta = max_theta
        self.__templates[ttype] = (t, max_potential)

    def __find_better_template(self, p, q, beta):
        """
            To judge whether template p is better or q. Eq.(4)
        :param p, q: type name of a template.
        :type p, q: char
        :param beta: parameter $\beta'$
        :type beta: float
        :return: a partial ordering
        :rtype: (better_template(char), worse_template(char))
        """
        template_p, template_q = self.__templates[p][0], self.__templates[q][0]
        potential_p, potential_q = self.__templates[p][1], self.__templates[q][1]
        area_p, area_q = 0, 0
        if template_p.snumber == 1:
            area_p = template_p.end[0] - template_p.start[0]
        elif template_p.snumber == 2:
            area_p = (template_p.end[0] - template_p.start[0]) + (template_p.end[1] - template_p.start[1])
        if template_q.snumber == 1:
            area_q = template_q.end[0] - template_q.start[0]
        elif template_q.snumber == 2:
            area_q = (template_q.end[0] - template_q.start[0]) + (template_q.end[1] - template_q.start[1])
        if area_p < area_q:
            p, q = q, p
            potential_p, potential_q = potential_q, potential_p
            area_p, area_q = area_q, area_p
        alpha = float(area_p) / float(area_q)
        gamma = alpha / (1 + beta * (alpha - 1))
        cpq = gamma * potential_p / potential_q
        if cpq > 1.0:
            return p, q
        else:
            return q, p

    def find_seven_templates(self):
        """
            Search for seven templates, along with potential values.
        """
        print '###################################'
        print '###   Start Finding Templates   ###'
        print '###################################'
        for i, ttype in enumerate(self.type_list, start=1):
            self.__find_one_template(ttype)
            print '%7s Found one template. %-7s' % ('>'*(8-i), '<'*i)
        print '###################################'
        print '###  Seven Templates are Found  ###'
        print '###################################'

    def find_best_template(self, beta):
        """
            To find a best template in 7.
        :param beta: parameter $\beta'$
        :type beta: float
        """
        wins = {t:0 for t in self.type_list}
        for index_p in range(6):
            for index_q in range(index_p+1, 7):
                p, q = self.type_list[index_p], self.type_list[index_q]
                partial_order = self.__find_better_template(p, q, beta)
                wins[partial_order[0]] += 1
        competition = sorted(wins.items(), key=lambda t: -t[1])
        self.__best_template = self.__templates[competition[0][0]][0]
        print '###################################'
        print '# Most harmonic Template is Found #'
        print '###################################'

    def find_templates_with_dump(self, beta):
        """
            An all-in-one method that integrate the procedure needed
            for finding templates (harmonic and best harmonic), then
            dumps the current object into a pickle file.
        :param beta: the same as method self.find_best_template.
        :type beta: float
        :return: the object will be saved with pickle.
        :rtype: None
        """
        self.find_seven_templates()
        print '\n'
        self.find_best_template(beta)
        print '\n'
        filename = self.filename.replace('.', '@') + '.pickle'
        with open(filename, 'w') as w:
            pickle.dump(self, w)
        print 'Object dumped successfully!'


if __name__ == '__main__':
    tf = TemplateFinder('images/cat.png')
    tf.find_templates_with_dump(0.1)
