#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: cirq
# Created Time: 2017-07-28 15:35:59

import json

class template(object):
    @classmethod
    def loadmodel(cls, ttype):
        with open('models.json', 'r') as reader:
            dic = json.load(reader)
        return dic[ttype]

    def __init__(self, ttype):
        model = template.loadmodel(ttype)
        self.type = str(model['type'])
        self.snumber = model['snumber']
        self.start = model['start']
        self.end = model['end']
        self.theta = None

if __name__ == '__main__':
    t = template('X')
