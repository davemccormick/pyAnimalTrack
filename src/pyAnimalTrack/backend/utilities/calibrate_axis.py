
import numpy as np

class CalibrateAxis(object):
    """ Utility Class for calibrating an axis.
    """

    def calibrate(self, x, min_, max_, scale=1):
        """ Calibrate the axes of magnetometers/accelerometers and
            correct hard-iron distortion. Taken from animalTrackR.
            TODO: speak to robin to understand what this is doing.

            :param x: The data from an axis
            :param min_: Minimum value of x
            :param max_: Maximum value of x
            :param scale: Multiplier for the axis.

            :returns: A scaled set of axis data.

        """

        total = np.absolute(min_ - max_)
        dist = total / 2
        offset = (min_ + max_) / 2
        scaled = ((x - offset ) / dist) * scale
        return scaled


