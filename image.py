#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: cirq
# Created Time: 2017-07-28 18:28:24

import cv2
import numpy as np
from matplotlib import pyplot as plt
from timer import timer

class Image(object):
    def __init__(self, filepath):
        self.__filename = filepath.split('/')[-1]
        self.__bgrimage, self.__hsvimage = self.__read_hsvimage(filepath)
        self.__shape = self.__bgrimage.shape[:2]
        self._huechannel = self.__read_huechannel(self.__hsvimage)

    @property
    def filename(self):
        return self.__filename
    @property
    def shape(self):
        return self.__shape

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
            To obtain the hue channel (a copy) of image, by expanding
            the hue value.
        :param hsvimage: the image with HSV_FULL color scheme in openCV.
        :type hsvimage: ndarray
        :return: the single hue channel of the input image.
        :rtype: ndarray (2-d array, shape like original image)
        """
        huechannel = np.zeros(shape=self.__shape, dtype='uint16')
        for i in range(self.__shape[0]):
            for j in range(self.__shape[1]):
                huechannel[i][j] = np.uint16(hsvimage[i][j][0] * 360.0 / 256)
        return huechannel

    def recover_huechannel(self):
        """
            To recover self.huechannel variable to initial state.
        :return: None
        :rtype: None
        """
        self._huechannel = self.__read_huechannel(self.__hsvimage)


    def show_image(self, after=False):
        """
            To show the image with color scheme transformation.
        :param after: whether to show the image after modification.
        :type after: bool
        :return: None
        :rtype: None
        """
        if after:
            hsvimage = np.copy(self.__hsvimage)
            for i in range(self.__shape[0]):
                for j in range(self.__shape[1]):
                    hsvimage[i][j][0] = np.uint8(self._huechannel[i][j] * 256.0 / 360)
            bgrimage = cv2.cvtColor(hsvimage, cv2.COLOR_HSV2BGR_FULL)
            cv2.imshow('after hue modification: %s' % self.__filename, bgrimage)
        else:
            cv2.imshow('before hue modification: %s' % self.__filename, self.__bgrimage)
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
            hist = cv2.calcHist([self._huechannel], [0], None, [360], [0, 360])
            plt.figure('histogram after modification: %s' % self.__filename)
        else:
            huechannel = self.__read_huechannel(self.__hsvimage)
            hist = cv2.calcHist([huechannel], [0], None, [360], [0, 360])
            plt.figure('histogram before modification: %s' % self.__filename)
        plt.plot(hist)
        plt.xlim([0, 360])
        plt.show('histogram')


if __name__ == '__main__':
    img = Image('images/pool.png')
    img.plothue_histogram()
