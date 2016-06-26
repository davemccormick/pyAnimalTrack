import numpy as np
import pandas as pd

from pyAnimalTrack.backend.filehandlers.input_data import InputData

global_count = 0

def get_secs(s):
    
    try:
        return np.float(s)
    except:
        global global_count
        global_count += 1
        return np.float(global_count)

class SensorCSV(InputData):

    def __init__(self, filename, csv_separator, reference_frame):

        """ Constructor
        
            :param data: Initial input data
            :returns: void
        """

        super(SensorCSV, self).__init__()

        self.__filename = filename
        self.__csv_separator = csv_separator
        self.__df = None
        self.__names = ['ms','ax','ay','az','mx','my','mz','gx','gy','gz','temp','adjms']
        self.__readableNames = ['Milliseconds', 'AX', 'AY', 'AZ', 'MX', 'MY', 'MZ', 'GX', 'GY', 'GZ', 'Temperature', 'Adjusted Milliseconds']
        self.__types = {
            'ms': str,
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
            'adjms': np.float64
        }

        self.__NED = False

        if reference_frame == 'NED':
            self.__NED = True

        self.__df = pd.read_csv(self.__filename, delimiter=self.__csv_separator, names=self.__names, dtype=self.__types, converters={'ms':get_secs})


    def getData(self):
        """ Get an object representation of the sensor CSV.

            :returns: A Pandas dataframe object.

        """

        self.__df.fillna(inplace=True, method='ffill')

        if self.__NED:
            self.__df['ax1'] = self.__df['az']
            self.__df['ay1'] = self.__df['ax']
            self.__df['az1'] = self.__df['ay']
            self.__df['mx1'] = self.__df['mz']
            self.__df['my1'] = self.__df['mx']
            self.__df['mz1'] = self.__df['my']

            self.__df['ax'] = self.__df['ax1']
            self.__df['ay'] = self.__df['ay1']
            self.__df['az'] = self.__df['az1']
            self.__df['mx'] = self.__df['mx1']
            self.__df['my'] = self.__df['my1']
            self.__df['mz'] = self.__df['mz1']

            self.__df = self.__df.drop('ax1', 1)
            self.__df = self.__df.drop('ay1', 1)
            self.__df = self.__df.drop('az1', 1)
            self.__df = self.__df.drop('mx1', 1)
            self.__df = self.__df.drop('my1', 1)
            self.__df = self.__df.drop('mz1', 1)

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

        return list(self.__df)

    def getReadableColumns(self):
        """ Get a list of (human readable) column names from the CSV

            :returns: An array of names
        """

        return self.__readableNames
