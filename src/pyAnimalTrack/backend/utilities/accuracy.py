
import numpy as np

class Accuracy(object):
    """ Utility Class for checking accuracy.
    """

    def check_accuracy(self, x, y, z):
        """This function checks the accuracy of an accelerometer.

        :param x: low pass filtered X axis accelerometer data
        :param y: low pass filtered Y axis accelerometer data
        :param z: low pass filtered Z axis accelerometer data

        :returns: A dictionary with keys: acc, std and var.
        """

        accuracy_dict = {}
        accuracy_dict['acc'] = np.sqrt(np.square(x) + np.square(y) + np.square(z))
        
        accuracy_dict['var'] = np.var(accuracy_dict['acc'])
        accuracy_dict['var2'] = np.mean((1-accuracy_dict['acc'])**2)
        
        accuracy_dict['std'] = np.std(accuracy_dict['acc']) 
        accuracy_dict['std2'] = np.sqrt(accuracy_dict['var2']) 

        return accuracy_dict


    def improve_accuracy(self, x, y, z):
        """ Create an estimate of the Z axis value using the X,Y axis values.
            This also improves the accuracy of the data. The Z-axis estimate gives a value for Z that makes
            the vector norm 1boldg (i.e. all three axes are perfectly orthogonal and X and Y are 
            assumed to be correct). This estimate for Z can then be used to evaluate error that may 
            correspond to pitch angle, or may be a constant error.

            :param x: low pass filtered X axis accelerometer data
            :param y: low pass filtered Y axis accelerometer data
            :param z: low pass filtered Z axis accelerometer data

            :returns: A dictionary of accuracy dictionaries with keys: input_accuracy and improved_accuracy.

        """
        x1 = np.sqrt(1-x**2)

        y1 = (y / np.sqrt(1 - np.square(x))) * (-1 * x)
        y2 = np.sqrt((1 - np.square(x) - np.square(y)) / 1 - np.square(x))
        y3 = (y / np.sqrt(1 - np.square(x)) * np.sqrt(1 - np.square(x)))

        z1 = y2 * (-1 * x)

        z2 = -1 * (y / np.sqrt(1 - np.square(x)))
        z3 = y2 * x1

        z_estimate = z3
        z_residual = z3 - z
        accuracy_input = self.check_accuracy(x,y,z)
        accuracy_improve = self.check_accuracy(x,y,z3)

        accuracies_dict = {}
        accuracies_dict['input_accuracy'] = accuracy_input
        accuracies_dict['improved_accuracy'] = accuracy_improve

        return accuracies_dict


