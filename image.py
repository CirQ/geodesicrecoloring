#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: cirq
# Created Time: 2017-07-28 18:28:24

import cv2
import numpy as np
from matplotlib import pyplot as plt

class image(object):
    def __init__(self, filepath):
        self.filename = filepath.split('/')[-1]
        self.bgrimage, self.hsvimage = self.__read_hsvimage(filepath)
        self.shape = self.bgrimage.shape[:2]
        self.huechannel = self.__read_huechannel(self.hsvimage)

    def __read_hsvimage(self, filepath):
        """
            Read a BGR image from file path and covert it
            into HSV color space, then return it.
        :param filepath: the path of the image.
        :type filepath: string
        :return: two images, one in BGR, another in HSV
        :rtype: (ndarray, ndarray)
        """
        bgrimage = cv2.imread(filepath)
        hsvimage = cv2.cvtColor(bgrimage, cv2.COLOR_BGR2HSV_FULL)
        return bgrimage, hsvimage

    def __read_huechannel(self, hsvimage):
        """
            To obtain the hue channel of image, by expanding
            the hue value.
        :param hsvimage: the image with HSV_FULL color scheme in openCV.
        :type hsvimage: ndarray
        :return: the single hue channel of the input image.
        :rtype: ndarray (2-d array, shape like original image)
        """
        huechannel = np.zeros(shape=self.shape, dtype='uint16')
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                huechannel[i][j] = np.uint16(hsvimage[i][j][0] * 360.0 / 256)
        return huechannel

    def show_image(self, after=False):
        """
            To show the image with color scheme transformation.
        :param after: whether to show the image after modification.
        :type after: bool
        :return: None
        :rtype: None
        """
        if after:
            hsvimage = np.copy(self.hsvimage)
            for i in range(self.shape[0]):
                for j in range(self.shape[1]):
                    hsvimage[i][j][0] = np.uint8(self.huechannel[i][j] * 256.0 / 360)
            bgrimage = cv2.cvtColor(hsvimage, cv2.COLOR_HSV2BGR_FULL)
            cv2.imshow('after hue modification', bgrimage)
        else:
            cv2.imshow('before hue modification', self.bgrimage)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def plothue_histogram(self, after=False):
        """
            To show the histogram of hue channel.
        :param after: whether to print the modified hue channel.
        :type after: bool
        :return: None
        :rtype: None
        """
        if after:
            hist = cv2.calcHist([self.huechannel], [0], None, [360], [0, 360])
        else:
            huechannel = self.__read_huechannel(self.hsvimage)
            hist = cv2.calcHist([huechannel], [0], None, [360], [0, 360])
        plt.plot(hist)
        plt.xlim([0, 360])
        plt.show()

if __name__ == '__main__':
    img = image('images/pool.png')
    img.plothue_histogram(True)
