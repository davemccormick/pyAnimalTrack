import numpy as np
import pandas as pd

from pyAnimalTrack.backend.filehandlers.input_data import InputData


class SensorCSV(InputData):

    def __init__(self, filename, csv_separator):

        """ Constructor
        
            :param data: Initial input data
            :returns: void
        """

        super(SensorCSV,self).__init__()

        self.__filename = filename
        self.__csv_separator = csv_separator
        self.__df = None
        self.__fileheadings = ['ms','ay','az','ax','my','mz','mx','gx','gy','gz','temp','adjms']
        self.__names = ['ms','ax','ay','az','mx','my','mz','gx','gy','gz','temp','adjms']
        self.__readableNames = ['Milliseconds', 'AX', 'AY', 'AZ', 'MX', 'MY', 'MZ', 'GX', 'GY', 'GZ', 'Temperature', 'Adjusted Milliseconds']
        self.__types = {
            'ms': np.int64,
            'ax': np.float64,
            'ay': np.float64,
            'az': np.float64,
            'mx': np.float64,
            'my': np.float64,
            'mz': np.float64,
            'gx': np.float64,
            'gy': np.float64,
            'gz': np.float64,
            'temp': np.float64,
            'adjms': np.int64
        }

        return

    def getData(self):
        """ Get an object representation of the sensor CSV.

            :returns: A Pandas dataframe object.

        """

        self.__df = pd.read_csv(self.__filename, delimiter=self.__csv_separator, names=self.__fileheadings, dtype=np.float64)

        return self.__df[self.__names]

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
