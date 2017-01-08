#!/usr/bin/env python

import struct


class PageImage(object):
    """
    Used to get the dimensions of PNG image
    """
    @staticmethod
    def get_image_info(filename):
        with open(filename, 'rb') as image:
            data = image.read()

        if PageImage.is_png(data):
            w, h = struct.unpack('>LL', data[16:24])
            width = int(w)
            height = int(h)
        else:
            raise Exception('not a png image')
        return width, height

    @staticmethod
    def is_png(data):
        return data[:8] == '\211PNG\r\n\032\n' and (data[12:16] == 'IHDR')
