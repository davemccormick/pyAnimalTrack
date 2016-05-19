from PyQt5.QtCore import QAbstractTableModel, QVariant
from PyQt5.Qt import Qt

from pyAnimalTrack.backend.filehandlers.input_data import InputData


class TableModel(QAbstractTableModel):

    def __init__(self, input_data):
        """ Constructor

        :returns: void
        """
        super(TableModel, self).__init__()

        self.__dataFile = input_data
        self.__dataSet = self.__dataFile.getData()

    def rowCount(self, QModelIndex_parent=None, *args, **kwargs):
        """ Gets the number of data rows. Used by PyQt.

        :param QModelIndex_parent: -
        :param args: -
        :param kwargs: -
        :return: The number of data rows
        """
        return len(self.__dataSet.index)

    def columnCount(self, QModelIndex_parent=None, *args, **kwargs):
        """ Gets the number of columns used in the dataset Used by PyQt.

        :param QModelIndex_parent: -
        :param args: -
        :param kwargs: -
        :return: The number of columns for the dataset
        """
        return len(self.__dataSet.columns)

    def headerData(self, index, Qt_Orientation, role=None):
        """ Gets a header for a row/column of data. Used by PyQt.

        :param index: The column/row index
        :param Qt_Orientation: The alignment of the header, Qt.Horizontal or Qt.Vertical
        :param role: ?
        :returns: A string containing the text to show as the header
        """
        if role == Qt.DisplayRole:
            if Qt_Orientation == Qt.Horizontal:
                return self.__dataFile.getReadableColumns()[index]
            else:
                return index + 1
        else:
            return QVariant()

    def data(self, QModelIndex, role=None):
        """ Gets an individual cell's value. Used by PyQt.

        :param QModelIndex: An object with a row() and column() function, used to determine the correct cell
        :param role:
        :return: A string representation of the cell's value
        """

        if role == Qt.DisplayRole:
            return str(self.__dataSet.iloc[QModelIndex.row()][QModelIndex.column()])
        else:
            return QVariant()

    def get_dataset(self):
        """ Retrieve the entire dataset

        :return: A pandas dataframe of the entire dataset
        """
        return self.__dataSet

    def get_epoch_dataset(self, start=0, end=0, step=1, isMilliseconds=False, sampleRatePerSecond=10):
        """ Retrieve a subset of the dataset, by rows or milliseconds

        :param start: The first row (or millisecond) to get
        :param end: The last row (or millisecond) to get
        :param step: How far between each row to return
        :param isMilliseconds: To go by row, or by time
        :param sampleRatePerSecond: If working in milliseconds, how many samples per second were taken
        :return: A pandas dataframe, sliced to the requested rows
        """

        # Make sure we are working with integer values for the numerical parameters
        try:
            start = int(start)
        except:
            start = 0

        try:
            end = int(end)
        except:
            end = 0

        try:
            step = int(step)
        except:
            step = 1

        try:
            sampleRatePerSecond = int(sampleRatePerSecond)
        except:
            sampleRatePerSecond = 10

        # If working time based, we need a conversion
        if isMilliseconds:
            start = int((start / 1000.0) * sampleRatePerSecond)
            end = int((end / 1000.0) * sampleRatePerSecond)

        # Sanity checks
        if end > len(self.__dataSet):
            end = len(self.__dataSet)
        elif end < 0:
            end = 0

        # Correct the end first, so the start doesn't get left incorrect if modified
        if start > end:
            start = end
        elif start < 0:
            start = 0

        # If the given end is 0, we actually want everything
        if end == 0:
            end = -1

        return self.__dataSet[start:end:step]

