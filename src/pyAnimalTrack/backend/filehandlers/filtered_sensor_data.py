import pandas as pd

from pyAnimalTrack.backend.filehandlers.input_data import InputData


class FilteredSensorData(InputData):

    def __init__(self, filter_class, df, filter_parameters):
        """ Constructor

            :param filter_class: The filter to use
            :param df: The Pandas dataframe to filter
            :param sample_rate: The sample rate of the data, in Hz
            :param cutoff_frequency: ???
            :param filter_length: ???
            :returns: void
        """

        super(FilteredSensorData, self).__init__()

        self.__df = df.copy()
        # TODO: Remove this duplication of names - potentially into input_data, or a new parent class?
        self.__names =['ms','ax','ay','az','mx','my','mz','gx','gy','gz','temp','adjms']
        self.__readableNames = ['Milliseconds', 'AX', 'AY', 'AZ', 'MX', 'MY', 'MZ', 'GX', 'GY', 'GZ', 'Temperature', 'Adjusted Milliseconds']

        filtered_names = self.__names[1:-2]

        new_values = {}

        # We need to filter the data, with the provided parameters
        for column in range(0, len(self.__names)):
            curr_name = self.__names[column]

            # Only run the filter on the columns that require it
            if curr_name in filtered_names:
                # Create a new column of data
                new_values[curr_name] = filter_class(getattr(self.__df, curr_name).values)\
                    .filter(
                    filter_parameters[curr_name]['SampleRate'],
                    filter_parameters[curr_name]['CutoffFrequency'],
                    filter_parameters[curr_name]['FilterLength']
                )
            else:
                # Otherwise, just copy the value
                new_values[curr_name] = getattr(self.__df, curr_name).values

        self.__df = pd.DataFrame(new_values)

    def getData(self):
        return self.__df

    def getColumns(self):
        return self.__names

    def getReadableColumns(self):
        return self.__readableNames

