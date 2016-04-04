from __future__ import print_function, division

import numpy as np

class BaseFilter(object):
    """ Class for FIR Filter algorithm
    """

    def filter(self, samplingRate, cutoffFrequency, filterLength):
        """This function creates a base filter, in this case a low pass filter.

        :param samplingRate: Rate at which the signal should be sampled in Hz
        :param cutoffFrequency: Frequency at which we should begin filtering
        :param filterLength: Length of the filter.
        :returns: A sinc filter
        """

        # Configuration.
        fS = samplingRate  # Sampling rate.
        fL = cutoffFrequency  # Cutoff frequency.
        N = filterLength  # Filter length, must be odd.

        # Compute sinc filter.
        h = np.sinc(2 * fL / fS * (np.arange(N) - (N - 1) / 2.))

        # Apply window.
        h *= np.blackman(N)

        # Normalize to get unity gain.
        h /= np.sum(h)

        return h
