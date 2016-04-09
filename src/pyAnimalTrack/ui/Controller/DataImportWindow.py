import PyQt5.uic
from PyQt5.QtCore import pyqtSignal, pyqtSlot

from PyQt5.QtWidgets import QMainWindow

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

from src.pyAnimalTrack.ui.Controller.LoadCSVDialog import LoadCSVDialog
from src.pyAnimalTrack.ui.Model.CSVFile import CSVFile

uiDataImportWindow = PyQt5.uic.loadUiType('./pyAnimalTrack/ui/View/DataImportWindow.ui')[0]


class DataImportWindow(QMainWindow, uiDataImportWindow):

    dataTable = None

    quitTrigger = pyqtSignal()

    def __init__(self, *args):
        super(DataImportWindow, self).__init__(*args)
        self.setupUi(self)

        self.figure = plt.figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        data = [3, 4, 5, 1, 7, 2, 4, 7, 1, 9]

        # create an axis
        ax = self.figure.add_subplot(111)

        # discards the old graph
        ax.hold(False)

        # plot data
        ax.plot(data, '*-')

        #self.plotFrame.addWidget(self.canvas)

        self.show()

        file_loader_dialog = LoadCSVDialog()

        self.quitTrigger.connect(QMainWindow.closeEvent)

        dialog_result = file_loader_dialog.loadCSV(self)

        if dialog_result[0]:
            # Get the model back, build the view

            # Load the CSV data object into the table
            self.rawDataTable = CSVFile()
            self.rawDataTable.load_file(dialog_result[1], dialog_result[2])
            self.rawTableView.setModel(self.rawDataTable)

            # Load the graph from the backend

        else:
            self.quitTrigger.emit()