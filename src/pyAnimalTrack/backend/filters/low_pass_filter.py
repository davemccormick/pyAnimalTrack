from base_filter import BaseFilter
import numpy as np

class LPF(BaseFilter):
    """ Class for Low Pass Filter algorithm
    """

    def __init__(self, signal):
        """ Constructor
        
            :param data: Initial input data
            :returns: void
        """
        super(LPF, self).__init__()

        self.signal = signal
        return


    def low_pass_filter(self, samplingRate, cutoffFrequency, filterLength):
        """Applies filter to signal.

        :param samplingRate: Rate at which the signal should be sampled in Hz
        :param cutoffFrequency: Frequency at which we should begin filtering
        :param filterLength: Length of the filter.

        :returns: A low pass filtered signal as NP array.
        """
        h = self.filter(samplingRate, cutoffFrequency, filterLength)
        s = np.convolve(self.signal, h, mode='same')

        return s

