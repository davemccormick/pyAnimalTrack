import PyQt5.uic
from PyQt5.Qt import Qt
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QMainWindow

from src.pyAnimalTrack.backend.filehandlers import sensor_csv, filtered_sensor_data
from src.pyAnimalTrack.backend.filters.low_pass_filter import LPF
from src.pyAnimalTrack.backend.filters.high_pass_filter import HPF

from src.pyAnimalTrack.ui.Controller.LoadCSVDialog import LoadCSVDialog
from src.pyAnimalTrack.ui.Controller.FeaturesWindow import FeaturesWindow
from src.pyAnimalTrack.ui.Model.CSVFile import CSVFile

uiDataImportWindow = PyQt5.uic.loadUiType('./pyAnimalTrack/ui/View/DataImportWindow.ui')[0]


class DataImportWindow(QMainWindow, uiDataImportWindow):

    dataTable = None

    quitTrigger = pyqtSignal()

    def __init__(self, *args):
        """ Constructor

            :param args: -
            :returns: void
        """

        super(DataImportWindow, self).__init__(*args)
        self.setupUi(self)
        self.show()

        self.rawDataFile = None
        self.featuresWindow = FeaturesWindow()

        # Connect signals and slots
        self.quitTrigger.connect(QMainWindow.closeEvent)
        self.connect_ui_elements()

        # If the user cancels, quit
        if not self.show_load_dialog():
            self.quitTrigger.emit()

    def connect_ui_elements(self):
        """ Connect each UI element to it's functionality

            :returns: void
        """
        self.featuresButton.clicked.connect(self.show_features_window)

    def show_load_dialog(self):
        """ Show the user a dialog to load a data file(CSV)

            :returns: True if a file has been loaded, false otherwise
        """

        file_loader_dialog = LoadCSVDialog()
        dialog_result = file_loader_dialog.loadCSV(self)

        if dialog_result[0]:
            # Get the model back, build the view

            # Load the CSV data object into the table
            self.rawDataFile = CSVFile(sensor_csv.SensorCSV(dialog_result[1]))
            self.rawTableView.setModel(self.rawDataFile)

            # Load the graph from the backend

            return True
        else:
            return False

    @pyqtSlot()
    def show_features_window(self):
        self.featuresWindow.set_data(
            self.rawDataFile.get_dataset(),
            CSVFile(filtered_sensor_data.FilteredSensorData(LPF, self.rawDataFile.get_dataset(), {'ax': 10 }, { 'ax': 2 }, { 'ax': 59 })).get_dataset(),
            CSVFile(filtered_sensor_data.FilteredSensorData(HPF, self.rawDataFile.get_dataset(), {'ax': 10 }, { 'ax': 2 }, { 'ax': 59 })).get_dataset())
        self.featuresWindow.show()