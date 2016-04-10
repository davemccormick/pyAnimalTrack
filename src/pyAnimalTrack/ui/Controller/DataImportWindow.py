import PyQt5.uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow

from src.pyAnimalTrack.backend.filehandlers import sensor_csv, filtered_sensor_data
from src.pyAnimalTrack.backend.filters.low_pass_filter import LPF
from src.pyAnimalTrack.backend.filters.high_pass_filter import HPF

from src.pyAnimalTrack.ui.Controller.LoadCSVDialog import LoadCSVDialog
from src.pyAnimalTrack.ui.Controller.FeaturesWindow import FeaturesWindow
from src.pyAnimalTrack.ui.Model.CSVFile import CSVFile

uiDataImportWindow = PyQt5.uic.loadUiType('./pyAnimalTrack/ui/View/DataImportWindow.ui')[0]

# TODO: Second table of filtered data? Or show the graph there instead?

class DataImportWindow(QMainWindow, uiDataImportWindow):

    # TODO: Read from config?
    # Default values, used to initialise the model
    defaults = {
        'SampleRate': 10,
        'CutoffFrequency': 2,
        'FilterLength': 59
    }

    # Needs to be here, otherwise the connection fails
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
        self.tableDataFile = None

        self.featuresWindow = FeaturesWindow()

        self.quitTrigger.connect(QMainWindow.closeEvent)

        self.filterParameters = {}

        # If the user cancels, quit
        if not self.show_load_dialog():
            self.quitTrigger.emit()
        else:
            # Connect signals and slots
            self.connect_ui_elements()

            self.setup_filter_parameters()

    def connect_ui_elements(self):
        """ Connect each UI element to it's functionality

            :returns: void
        """
        self.featuresButton.clicked.connect(self.show_features_window)

        self.rawTableView.selectionModel().selectionChanged.connect(self.change_selected_combo_column)

        # Connect the line edits to a single slot. Pass a second parameter to identify it
        self.refreshLineEdit.textChanged.connect(lambda val: self.parameter_value_changed(val, 'SampleRate'))
        self.cutoffLineEdit.textChanged.connect(lambda val: self.parameter_value_changed(val, 'CutoffFrequency'))
        self.filterLineEdit.textChanged.connect(lambda val: self.parameter_value_changed(val, 'FilterLength'))

    def show_load_dialog(self):
        """ Show the user a dialog to load a data file(CSV)

            :returns: True if a file has been loaded, false otherwise
        """

        file_loader_dialog = LoadCSVDialog()
        dialog_result = file_loader_dialog.loadCSV(self)

        if dialog_result[0]:
            # Get the model back, build the view

            # Load the CSV data object into the table
            self.rawDataFile = sensor_csv.SensorCSV(dialog_result[1])
            self.tableDataFile = CSVFile(self.rawDataFile)
            self.rawTableView.setModel(self.tableDataFile)

            # Load filter controlling dropdown
            self.currentColumnComboBox.clear()
            self.currentColumnComboBox.addItems(self.rawDataFile.getReadableColumns())

            return True
        else:
            return False

    def setup_filter_parameters(self):
        """ Initialise the model behind the textboxes

            :returns: void
        """

        for key in self.rawDataFile.getColumns():
            self.filterParameters[key] = {
                'SampleRate':       self.defaults['SampleRate'],
                'CutoffFrequency':  self.defaults['CutoffFrequency'],
                'FilterLength':     self.defaults['FilterLength']
            }

    # PyQt5 Slots
    def show_features_window(self):
        """ Set the data for the feature window, and display it

            :returns: void
        """
        self.featuresWindow.set_data(
            self.tableDataFile.get_dataset(),
            CSVFile(filtered_sensor_data.FilteredSensorData(LPF, self.tableDataFile.get_dataset(), self.filterParameters)).get_dataset(),
            CSVFile(filtered_sensor_data.FilteredSensorData(HPF, self.tableDataFile.get_dataset(), self.filterParameters)).get_dataset())
        self.featuresWindow.show()

    # TODO: Do we want this to happen? Unsure
    def change_selected_combo_column(self, selected, deselected):
        """ When the selected data cell changes, update the combobox that controls the parameters

            :param selected: PyQt5. The cells that were selected.
            :param deselected: PyQt5. The cells that were deselected.
            :returns: void
        """
        self.currentColumnComboBox.setCurrentIndex(selected.indexes()[0].column())

    def parameter_value_changed(self, new_value, parameter):
        """ Update the filter parameters model

            :param new_value: PyQt5. The new filter parameter version
            :param parameter: Which filter parameter has changed
            :returns: void
        """
        self.filterParameters[self.rawDataFile.getColumns()[self.currentColumnComboBox.currentIndex()]][parameter] = int(new_value)