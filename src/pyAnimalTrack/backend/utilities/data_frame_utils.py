from __future__ import division

import numpy as np
from pyAnimalTrack.backend.utilities.enums import *

class DataFrameUtils(object):
    """ Utility Class manipulating data frames and np arrays.
    """

    @staticmethod
    def convert_to_NED(x, y, z):
        """ Rotate xyz axis such that:
            x = z
            y = x
            z = y

            :param x: raw X axis accelerometer data
            :param y: raw Y axis accelerometer data
            :param z: raw Z axis accelerometer data

            :returns: tuple of rotated arrays

        """
        x1 = z
        y1 = x
        z1 = y

        return (x1,y1,z1)
        
    
    @staticmethod
    def invert_axis(x):
        """ Inverts the axis x such that all its positive elements are made negative,
            and its negative elements are made positive.
        """
        return -x