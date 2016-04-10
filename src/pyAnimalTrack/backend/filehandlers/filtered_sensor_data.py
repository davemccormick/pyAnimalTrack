from src.pyAnimalTrack.backend.filehandlers.input_data import InputData


class FilteredSensorData(InputData):

    def __init__(self, filter_class, df, sample_rates, cutoff_frequencies, filter_lengths):
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

        # We need to filter the data, with the provided parameters
        for column in range(len(self.__names)):
            curr_name = self.__names[1]

            # Create a new column of data
            new_values = filter_class(getattr(self.__df, curr_name).values)\
                .filter(sample_rates[curr_name], cutoff_frequencies[curr_name], filter_lengths[curr_name])

            # Replace each value in the column
            for row in range(len(self.__df.index)):
                self.__df.iloc[row][column] = new_values[row]

    def getData(self):
        return self.__df

    def getColumns(self):
        return self.__names

    def getReadableColumns(self):
        return self.__readableNames

