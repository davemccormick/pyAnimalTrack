from pyAnimalTrack.backend.filehandlers.input_data import InputData

import pandas as pd


class FeaturesModel(InputData):

    def __init__(self, dataset):

        """ Constructor

            :param data: Initial input data
            :returns: void
        """

        super(FeaturesModel, self).__init__()

        self.__dataset = dataset
        self.__df = None
        self.__names = ['axyz', 'sma','svm','movement_variation','energy','entropy','pitch','roll','inclination']
        self.__readableNames = ['Accelerometer (X, Y, Z)', 'SMA', 'SVM', 'Movement Variation', 'Energy', 'Entropy', 'Pitch (Degrees)', 'Roll (Degrees)', 'Inclination (Degrees)']

        return


    def getData(self):
        """ Get an object representation of the sensor CSV.

            :returns: A Pandas dataframe object.

        """

        # TODO: ...this is only working with a breakpoint?
        self.__df = pd.DataFrame(self.__dataset, columns=self.__names)

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
