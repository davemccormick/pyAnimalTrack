
import numpy as np

class Accuracy(object):
    """ Utility Class for checking accuracy.
    """
    def __init__(self):

    	self.accuracy_dict = {}
    	

    def check_accuracy(self, x, y, z):
        """This function checks the accuracy of an accelerometer.

        :param x: low pass filtered X axis accelerometer data
        :param y: low pass filtered Y axis accelerometer data
        :param z: low pass filtered Z axis accelerometer data

        :returns: A dictionary with keys: acc, std and var.
        """
        self.accuracy_dict['acc'] = np.sqrt(np.square(x) + np.square(y) + np.square(z))
        self.accuracy_dict['var'] = np.var(self.accuracy_dict['acc'])
        self.accuracy_dict['std'] = np.std(self.accuracy_dict['acc']) 
        return self.accuracy_dict