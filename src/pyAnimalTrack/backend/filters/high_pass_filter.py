from pyAnimalTrack.backend.filters.base_filter import BaseFilter
import numpy as np

class HPF(BaseFilter):
    """ Class for Low Pass Filter algorithm
    """

    def __init__(self, signal):
        """ Constructor
        
            :param data: Initial input data
            :returns: void
        """
        super(HPF, self).__init__()

        self.signal = signal
        return


    def filter(self, samplingRate, cutoffFrequency, filterLength):
        """Applies filter to signal.

        :param samplingRate: Rate at which the signal should be sampled in Hz
        :param cutoffFrequency: Frequency at which we should begin filtering
        :param filterLength: Length of the filter.

        :returns: A low pass filtered signal as NP array.
        """
        h = super().filter(samplingRate, cutoffFrequency, filterLength)

        # Use spectral inverse to turn this into high pass filter.
        h = -h
        h[(filterLength - 1) / 2] += 1

        s = np.convolve(self.signal, h, mode='same')

        return s
