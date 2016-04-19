from pyAnimalTrack.backend.filehandlers.input_data import InputData

import pandas as pd

class SensorCSV(InputData):

    def __init__(self, filename):

        """ Constructor
        
            :param data: Initial input data
            :returns: void
        """

        super(SensorCSV,self).__init__()

        self.__filename = filename
        self.__df = None
        self.__names =['ms','ax','ay','az','mx','my','mz','gx','gy','gz','temp','adjms']
        self.__readableNames = ['Milliseconds', 'AX', 'AY', 'AZ', 'MX', 'MY', 'MZ', 'GX', 'GY', 'GZ', 'Temperature', 'Adjusted Milliseconds']

        return


    def getData(self):
        """ Get an object representation of the sensor CSV.

            :returns: A Pandas dataframe object.

        """

        self.__df = pd.read_csv(self.__filename, delimiter=";", names=self.__names)

        return self.__df


    def getColumn(self, columnName):
        """ Gets a column of data.

            
            :param columnName: The name of the column to retrieve.
            :returns: A numpy array of data for processing.
        """

        return getattr(self.__df,columnName).values[::-1]

    def getColumns(self):
        """ Lists all available column names.
            
            :returns: A list of strings representing the available column names.
        """

        return self.__names

    def getReadableColumns(self):
        """ Get a list of (human readable) column names from the CSV

            :returns: An array of names
        """

        return self.__readableNames
