from PyQt5.QtCore import QAbstractTableModel, QVariant
from PyQt5.Qt import Qt

from pyAnimalTrack.backend.filehandlers.input_data import InputData


class CSVFile(QAbstractTableModel):

    def __init__(self, input_data):
        """ Constructor

        :returns: void
        """
        super(CSVFile, self).__init__()

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
        return self.__dataSet