
import numpy as np

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

            :param x: raw X axis accelerometer data
            :param y: raw Y axis accelerometer data
            :param z: raw Z axis accelerometer data

            :returns: An Numpy array representing the pitch of the input data. 

        """

        return (np.tan(np.divide((-x), np.sqrt(y**2 + z**2))**-1) * 180 / np.pi)

    
    @staticmethod
    def calculate_roll(y, z):
        """ Calculate the roll in degrees of the combined axes.
            Mathematical Notation: atan2(Yi,Zi)*180/pi

            :param y: raw Y axis accelerometer data
            :param z: raw Z axis accelerometer data

            :returns: An Numpy array representing the roll of the input data. 

        """

        return np.arctan2(y, z) * 180 / np.pi

    
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

