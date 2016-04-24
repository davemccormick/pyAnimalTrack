import os

import PyQt5.uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

from pyAnimalTrack.backend.filehandlers import sensor_csv, filtered_sensor_data
from pyAnimalTrack.backend.filters.low_pass_filter import LPF
from pyAnimalTrack.backend.filters.high_pass_filter import HPF

from pyAnimalTrack.ui.Controller.LoadCSVDialog import LoadCSVDialog
from pyAnimalTrack.ui.Controller.FeaturesWindow import FeaturesWindow
from pyAnimalTrack.ui.Model.TableModel import TableModel

uiDataImportWindow = PyQt5.uic.loadUiType(os.path.join(os.path.dirname(__file__), '../View/DataImportWindow.ui'))[0]

# TODO: Second table of filtered data? Or show the graph there instead?


class DataImportWindow(QMainWindow, uiDataImportWindow):

    # TODO: Read from config?
    # Default values, used to initialise the model
    default_filter_parameters = {
        'SampleRate': 10,
        'CutoffFrequency': 2,
        'FilterLength': 59
    }
    default_column = 1

    # Needs to be here, otherwise the connection fails
    quitTrigger = pyqtSignal()

    def __init__(self, *args):
        """ Constructor - This is actually the main function of the program

            :param args: -
            :returns: void
        """

        super(DataImportWindow, self).__init__(*args)
        self.setupUi(self)

        # Programatically create the graph widget, as it is not available in the designer
        # Also create a separate graph to display the legend without resizing issues
        self.figure = plt.figure(facecolor='none')
        self.legendFigure = plt.figure(facecolor='none')
        self.canvas = FigureCanvas(self.figure)
        self.legendCanvas = FigureCanvas(self.legendFigure)
        self.plotFrame.addWidget(self.canvas)
        self.legendFrame.addWidget(self.legendCanvas)
        # The plot, used on the graph
        self.plot = self.figure.add_subplot(111)
        self.plot.hold(False)
        self.legendPlot = self.legendFigure.add_axes([-0.2,0,-0.045,0.85])
        self.legendPlot.hold(False)

        self.show()

        # Datasets
        self.rawDataFile = None
        self.lowPassData = None
        self.highPassData = None

        # The datafile used by tableview
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

            self.refilter_datasets()

    def connect_ui_elements(self):
        """ Connect each UI element to it's functionality

            :returns: void
        """
        self.featuresButton.clicked.connect(self.show_features_window)

        self.rawTableView.selectionModel().selectionChanged.connect(self.change_selected_combo_column)

        self.currentColumnComboBox.currentIndexChanged.connect(self.redraw_graph)

        # Connect the line edits to a single slot. Pass a second parameter to identify it
        self.refreshLineEdit.textChanged.connect(lambda val: self.parameter_value_changed(val, 'SampleRate'))
        self.cutoffLineEdit.textChanged.connect(lambda val: self.parameter_value_changed(val, 'CutoffFrequency'))
        self.filterLineEdit.textChanged.connect(lambda val: self.parameter_value_changed(val, 'FilterLength'))

    def show_load_dialog(self):
        """ Show the user a dialog to load a data file(CSV)

            :returns: True if a file has been loaded, false otherwise
        """

        # TODO: Don't clear the existing path on cancel

        file_loader_dialog = LoadCSVDialog()
        dialog_result = file_loader_dialog.loadCSV(self)

        if dialog_result[0]:
            # Get the model back, build the view

            # Load the CSV data object into the table
            self.rawDataFile = sensor_csv.SensorCSV(dialog_result[1])
            self.tableDataFile = TableModel(self.rawDataFile)
            self.rawTableView.setModel(self.tableDataFile)

            # Load filter controlling dropdown
            self.currentColumnComboBox.clear()
            self.currentColumnComboBox.addItems(self.rawDataFile.getReadableColumns())
            self.currentColumnComboBox.setCurrentIndex(self.default_column)

            return True
        else:
            return False

    def setup_filter_parameters(self):
        """ Initialise the model behind the textboxes

            :returns: void
        """

        for key in self.rawDataFile.getColumns():
            self.filterParameters[key] = {
                'SampleRate':       self.default_filter_parameters['SampleRate'],
                'CutoffFrequency':  self.default_filter_parameters['CutoffFrequency'],
                'FilterLength':     self.default_filter_parameters['FilterLength']
            }

    def refilter_datasets(self):
        """

            :returns: void
        """
        self.lowPassData = TableModel(filtered_sensor_data
                                      .FilteredSensorData(LPF, self.tableDataFile.get_dataset(), self.filterParameters))
        self.highPassData = TableModel(filtered_sensor_data
                                       .FilteredSensorData(HPF, self.tableDataFile.get_dataset(), self.filterParameters))

        self.redraw_graph()

    def redraw_graph(self):
        """ Redraw the graph

            :returns: void
        """
        current_column = self.rawDataFile.getColumns()[self.currentColumnComboBox.currentIndex()]

        lines = self.plot.plot(
            self.tableDataFile.get_dataset()[current_column].values[::-1], 'g-',
            self.lowPassData.get_dataset()[current_column].values[::-1], 'b-',
            self.highPassData.get_dataset()[current_column].values[::-1], 'r-'
        )

        lines[0].set_label('Unfiltered')
        lines[1].set_label('Low pass')
        lines[2].set_label('High pass')

        self.legendPlot.legend(bbox_to_anchor=(-4, 0.9, 2., .102), loc=2, handles=lines)

        self.canvas.draw()
        self.legendCanvas.draw()

    # PyQt5 Slots
    def show_features_window(self):
        """ Set the data for the feature window, and display it

            :returns: void
        """
        self.featuresWindow.set_data(
            self.tableDataFile.get_dataset(),
            self.lowPassData.get_dataset(),
            self.highPassData.get_dataset()
        )
        self.featuresWindow.show()

    # TODO: Do we want this to happen? Unsure
    def change_selected_combo_column(self, selected, deselected):
        """ When the selected data cell changes, update the combobox that controls the parameters.

            :param selected: PyQt5. The cells that were selected.
            :param deselected: PyQt5. The cells that were deselected.
            :returns: void
        """
        self.currentColumnComboBox.setCurrentIndex(selected.indexes()[0].column())

    def parameter_value_changed(self, new_value, parameter):
        """ Update the filter parameters model, redraw the graph

            :param new_value: PyQt5. The new filter parameter version
            :param parameter: Which filter parameter has changed
            :returns: void
        """
        if new_value == '':
            return

        self.filterParameters[self.rawDataFile.getColumns()[self.currentColumnComboBox.currentIndex()]][parameter] = int(new_value)
        self.refilter_datasets()