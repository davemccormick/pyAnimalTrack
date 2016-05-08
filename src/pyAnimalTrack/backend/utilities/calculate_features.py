
import numpy as np
from pyAnimalTrack.backend.utilities.enums import *

class CalculateFeatures(object):
    """ Utility Class for calculating specific features of the  accelerometer data.
        All methods are static, so no instantiation is required.
    """

    @staticmethod
    def calculate_sma(x, y, z):
        """ Calculate the Signal Magnitude Area (SMA).
            This can be used to distuingish between periods of activity vs rest.
            Mathematical Notation: abs(Xi)+abs(Yi)+abs(Zi)

            :param x: raw X axis accelerometer data
            :param y: raw Y axis accelerometer data
            :param z: raw Z axis accelerometer data

            :returns: An Numpy array representing the SMA of the input data. 

        """

        return np.absolute(x) + np.absolute(y) + np.absolute(z)


    @staticmethod
    def calculate_svm(x, y, z):
        """ Calculate the Signal Vector Magnitude (SVM).
            This indicates degree of movement intensity.
            Mathematical Notation: sqrt(Xi^2+Yi^2+Zi^2)

            :param x: raw X axis accelerometer data
            :param y: raw Y axis accelerometer data
            :param z: raw Z axis accelerometer data

            :returns: An Numpy array representing the SVM of the input data. 

        """

        return np.sqrt(np.square(x) + np.square(y) + np.square(z))


    @staticmethod
    def calculate_movement_variation(x, y, z):
        """ Calculate the movement_variation.
            Mathematical Notation: abs(Xi+1-Xi)+abs(Yi+1-Yi)+abs(Zi+1-Zi)

            :param x: raw X axis accelerometer data
            :param y: raw Y axis accelerometer data
            :param z: raw Z axis accelerometer data

            :returns: An Numpy array representing the movement variation of the input data. 

        """

        return np.absolute(np.diff(x)) + np.absolute(np.diff(y)) + np.absolute(np.diff(z))


    @staticmethod
    def calculate_energy(x, y, z):
        """ Calculate the Energy of the combined axes.
            Mathematical Notation: (Xi^2+Yi^2+Zi^2)^2

            :param x: raw X axis accelerometer data
            :param y: raw Y axis accelerometer data
            :param z: raw Z axis accelerometer data

            :returns: An Numpy array representing the energy of the input data. 

        """

        return np.square(np.square(x) + np.square(y) + np.square(z))


    @staticmethod
    def calculate_entropy(x, y, z):
        """ Calculate the Entropy of the combined axes.
            Mathematical Notation: (1+(Xi+Yi+Zi))2*ln(1+(Xi+Yi+Zi))2

            :param x: raw X axis accelerometer data
            :param y: raw Y axis accelerometer data
            :param z: raw Z axis accelerometer data

            :returns: An Numpy array representing the entropy of the input data. 

        """

        return np.square(1 + (x + y + z)) * np.log(np.square(1 + (x + y + z)))


    @staticmethod
    def calculate_pitch(x, y, z):
        """ Calculate the pitch in degrees of the combined axes.
            Mathematical Notation: tan^-1(-Xi/(sqrt(Yi+Zi)))*180/pi

            :param x: LPF X axis accelerometer data
            :param y: LPF Y axis accelerometer data
            :param z: LPF Z axis accelerometer data

            :returns: An Numpy array representing the pitch of the input data. 

        """

        return -np.arctan(x/np.sqrt(y**2 + z**2))

    
    @staticmethod
    def calculate_roll(y, z):
        """ Calculate the roll in degrees of the combined axes.
            Mathematical Notation: atan2(Yi,Zi)*180/pi

            :param y: LPF Y axis accelerometer data
            :param z: LPF Z axis accelerometer data

            :returns: An Numpy array representing the roll of the input data. 

        """

        return np.arctan2(y, z)

    
    @staticmethod
    def calculate_inclination(x, y, z):
        """ Calculate the inclination in degrees of the combined axes.
            Mathematical Notation: tan^-1((sqrt(Xi^2+Yi^2))/Zi)*180/pi

            :param x: raw X axis accelerometer data
            :param y: raw Y axis accelerometer data
            :param z: raw Z axis accelerometer data

            :returns: An Numpy array representing the inclination of the input data. 

        """

        return (np.tan(np.divide((np.sqrt(x**2 + y**2)), z) **-1)) * 180 / np.pi

    @staticmethod
    def calculate_heading(x, y, z, pitch, roll, declination=0, angle=Angle.degree):
        """ Calculate tilt compentated heading. 

            :param x: LPF X axis magnetometer data
            :param y: LPF Y axis magnetometer data
            :param z: LPF Z axis magnetometer data
            :param pitch: pre calculated pitch data
            :param roll: pre calculated roll data
            :param declination: delclination
            :param angle: Angle type, degree or radians

            :returns: A dictionary of numpy arrays representing heading.

        """

        sinp = np.sin(pitch)
        sinr = np.sin(roll)
        cosp = np.cos(pitch)
        cosr = np.cos(roll)

        xh = x*cosp + y*sinr*sinp + z*cosr*sinp
        yh = y*cosr - z*sinr

        azimuth90 = np.arctan(yh/xh)

        heading_mag = azimuth90
        for i in range(len(x)):
            if xh[i] < 0:
                heading_mag[i] = np.pi - azimuth90[i]

            if xh[i] > 0 and yh[i] < 0:
                heading_mag[i] = -azimuth90[i]

            if xh[i] > 0 and yh[i] > 0:
                heading_mag[i] = (2*np.pi) - azimuth90[i]

            if xh[i] == 0 and yh[i] < 0:
                heading_mag[i] = np.pi/2

            if xh[i] == 0 and yh[i] > 0:
                heading_mag[i] = (3*np.pi)/2

        if angle == Angle.degree:
            heading_geo = (heading_mag + (declination*(np.pi/180))) % (2*np.pi)

        if angle == Angle.radian:
            heading_geo = (heading_mag + declination) % (2*np.pi)

        heading_dict = {}
        heading_dict['xh'] = xh
        heading_dict['yh'] = yh
        heading_dict['heading_mag'] = heading_mag
        heading_dict['heading_geo'] = heading_geo

        return heading_dict

