
import numpy as np

class CalculateFeatures(object):
    """ Utility Class for calculating specific features of the  accelerometer data.
        All methods are static, so no instantiation is required.
    """

    @staticmethod
    def calculate_sma(self, x, y, z):
        """ Calculate the Signal Magnitude Area (SMA).
            This can be used to distuingish between periods of activity vs rest.
            Mathematical Notation: |Xi|+|Yi|+|Zi|

            :param x: raw X axis accelerometer data
            :param y: raw Y axis accelerometer data
            :param z: raw Z axis accelerometer data

            :returns: An Numpy array representing the SMA of the input data. 

        """

        return np.add(np.absolute(x) + np.absolute(y) + np.absolute(z))


    @staticmethod
    def calculate_svm(self, x, y, z):
        """ Calculate the Signal Vector Magnitude (SVM).
            This indicates degree of movement intensity.
            Mathematical Notation: √Xi^2+Yi^2+Zi^2

            :param x: raw X axis accelerometer data
            :param y: raw Y axis accelerometer data
            :param z: raw Z axis accelerometer data

            :returns: An Numpy array representing the SVM of the input data. 

        """

        return np.sqrt(np.square(x) + np.square(y) + np.square(z))


    @staticmethod
    def calculate_movement_variation(self, x, y, z):
        """ Calculate the movement_variation.
            Mathematical Notation: |Xi+1-Xi|+|Yi+1-Yi|+|Zi+1-Zi|

            :param x: raw X axis accelerometer data
            :param y: raw Y axis accelerometer data
            :param z: raw Z axis accelerometer data

            :returns: An Numpy array representing the movement variation of the input data. 

        """

        return np.add(np.absolute(np.add(x, np.subtract(1-x)) + np.absolute(np.add(y, np.subtract(1-y)) + np.absolute(np.add(z, np.subtract(1-z)))


    @staticmethod
    def calculate_energy(self, x, y, z):
        """ Calculate the Energy of the combined axes.
            Mathematical Notation: (Xi^2+Yi^2+Zi^2)^2

            :param x: raw X axis accelerometer data
            :param y: raw Y axis accelerometer data
            :param z: raw Z axis accelerometer data

            :returns: An Numpy array representing the energy of the input data. 

        """

        return np.square(np.add(np.square(x) + np.square(y) + np.square(z)))


    @staticmethod
    def calculate_entropy(self, x, y, z):
        """ Calculate the Entropy of the combined axes.
            Mathematical Notation: (1+(Xi+Yi+Zi))2*ln(1+(Xi+Yi+Zi))2

            :param x: raw X axis accelerometer data
            :param y: raw Y axis accelerometer data
            :param z: raw Z axis accelerometer data

            :returns: An Numpy array representing the entropy of the input data. 

        """

        return np.square(np.add(1, np.add(x + y + z))) * np.log(np.square(np.add(1, np.add(x + y + z))))


    @staticmethod
    def calculate_pitch(self, x, y, z):
        """ Calculate the pitch in degrees of the combined axes.
            Mathematical Notation: tan^-1(-Xi/(√Yi+Zi))*180/π

            :param x: raw X axis accelerometer data
            :param y: raw Y axis accelerometer data
            :param z: raw Z axis accelerometer data

            :returns: An Numpy array representing the pitch of the input data. 

        """

        return (np.tan(np.divide((-1 * x), np.sqrt(y+z))**1) * 180 / np.pi)

    
    @staticmethod
    def calculate_roll(self, y, z):
        """ Calculate the roll in degrees of the combined axes.
            Mathematical Notation: atan2(Yi,Zi)*180/π

            :param y: raw Y axis accelerometer data
            :param z: raw Z axis accelerometer data

            :returns: An Numpy array representing the roll of the input data. 

        """

        return np.arctan2(y, z) * 180 / np.pi

    
    @staticmethod
    def calculate_inclination(self, x, y, z):
        """ Calculate the inclination in degrees of the combined axes.
            Mathematical Notation: tan^-1((√Xi^2+Yi^2)/Zi)*180/π

            :param x: raw X axis accelerometer data
            :param y: raw Y axis accelerometer data
            :param z: raw Z axis accelerometer data

            :returns: An Numpy array representing the inclination of the input data. 

        """

        return (np.tan(np.divide((np.sqrt(np.square(x)+np.square(y)) / z) ** 1) * 180 / np.pi)

