
import numpy as np

class TimeWindow(object):
    """ Object to handle creating a time window, from a timeseries. 
    """

    def __init__(self, data, isSeconds=False, sampleRate=10):
    	""" 
    	    :param data: An array of data points.
    		:param isSeconds: Bool to determine whether the user has specifed the time window in seconds.
    						  Defaults to false, which assumes that the user is specifying time in samples.
    		:param sampleRate: Sample rate of the data. Used for conversion if isSeconds=True.
    	"""

    	self.__data = np.asarray(data)
    	self.__isSeconds = isSeconds
    	self.__sampleRate = sampleRate
    	return


    def extract(self, start=0, end=0, step=1):
    	""" Extract a time window from the data. If both start and end are 0, assume
    		all elements are wanted, and step is the only param that will be applied.

            :param start: The start of the slice required.
            :param end: The end of the slice required.
            :param step: Steps between elements in array to return. Defaults to 1 (all data).

            :returns: An Numpy array of length "length", beginning at index "offset".
    	"""

    	if self.__isSeconds:
    		start = start * self.__sampleRate
    		end   = end   * self.__sampleRate
    		step  = step  * self.__sampleRate

    	# Return copy so as not to have object tied by reference to original time window object.
    	if not start and not end:
    		return self.__data[::step].copy()

    	return self.__data[start:end:step].copy()


    def split(self, nWindows):
    	""" Split the data into nWindows of equal size. If data isnt equally divisible, the final
    		window will include a shorter duration.

            :param nWindows: Amount of sub arrays to return.

            :returns: A list of arrays.
    	"""
    	return np.split_array(self.__data, nWindows)

