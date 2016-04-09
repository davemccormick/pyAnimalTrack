from PyQt5.QtCore import QAbstractTableModel, QVariant
from PyQt5.Qt import Qt


class CSVFile(QAbstractTableModel):

    def __init__(self):
        """ Constructor

        :returns: void
        """
        super(CSVFile, self).__init__()

        self.__rowTitles = [
            'Milliseconds',
            'Ax',
            'Ay',
            'Az',
            'Mx',
            'My',
            'Mz',
            'Gx',
            'Gy',
            'Gz',
            'Temperature',
            'Adjusted Milliseconds'
        ]
        self.rows = []

    def load_file(self, filename, separator=','):
        """  Load a CSV file into this object, with a given separator

        :param filename:
        :param separator:
        :returns: void
        """

        with open(filename) as file:
            for line in file.readlines():
                values = line.strip().split(separator)
                # TODO: Loop to object, append built object
                valueObject = {}

                for i in range(len(self.__rowTitles)):
                    valueObject[self.__rowTitles[i].replace(' ', '_')] = values[i]

                self.rows.append(valueObject)

    def rowCount(self, QModelIndex_parent=None, *args, **kwargs):
        """ Gets the number of data rows. Used by PyQt.

        :param QModelIndex_parent: -
        :param args: -
        :param kwargs: -
        :return: The number of data rows
        """
        return len(self.rows)

    def columnCount(self, QModelIndex_parent=None, *args, **kwargs):
        """ Gets the number of columns used in the dataset Used by PyQt.

        :param QModelIndex_parent: -
        :param args: -
        :param kwargs: -
        :return: The number of columns for the dataset
        """
        return len(self.__rowTitles)

    def headerData(self, index, Qt_Orientation, role=None):
        """ Gets a header for a row/column of data. Used by PyQt.

        :param index: The column/row index
        :param Qt_Orientation: The alignment of the header, Qt.Horizontal or Qt.Vertical
        :param role: ?
        :returns: A string containing the text to show as the header
        """
        if role == Qt.DisplayRole:
            if Qt_Orientation == Qt.Horizontal:
                return self.__rowTitles[index]
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
            return self.rows[QModelIndex.row()][self.__rowTitles[QModelIndex.column()].replace(' ', '_')]
        else:
            return QVariant()
