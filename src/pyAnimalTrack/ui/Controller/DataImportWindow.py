import os

import PyQt5.uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow

from pyAnimalTrack.backend.filehandlers import sensor_csv, filtered_sensor_data
from pyAnimalTrack.backend.filters.low_pass_filter import LPF
from pyAnimalTrack.backend.filters.high_pass_filter import HPF

from pyAnimalTrack.ui.Controller.TableAndGraphView import TableAndGraphView
from pyAnimalTrack.ui.Controller.LoadCSVDialog import LoadCSVDialog
from pyAnimalTrack.ui.Controller.FeaturesWindow import FeaturesWindow
from pyAnimalTrack.ui.Controller.DeadReckoningWindow import DeadReckoningWindow
from pyAnimalTrack.ui.Model.TableModel import TableModel

uiDataImportWindow = PyQt5.uic.loadUiType(os.path.join(os.path.dirname(__file__), '../View/DataImportWindow.ui'))[0]


class DataImportWindow(QMainWindow, uiDataImportWindow, TableAndGraphView):

    # TODO: Read from config
    # Default values, used to initialise the model
    default_filter_parameters = {
        'SampleRate': 10,
        'CutoffFrequency': 2,
        'FilterLength': 59
    }

    default_colours = [
        'r',
        'g',
        'b'
    ]

    first_graphed_element = 1
    last_graphed_element = -2

    # Needs to be here, otherwise the connection fails
    quitTrigger = pyqtSignal()

    def __init__(self, *args):
        """ Constructor - This is actually the main function of the program

            :param args: -
            :returns: void
        """

        super(DataImportWindow, self).__init__(*args)
        self.setupUi(self)
        TableAndGraphView.__init__(self, self.rawTableView, self.currentColumnComboBox, self.plotFrame, self.legendFrame, self.redraw_graph)

        self.show()

        # Datasets
        self.rawDataFile = None
        self.lowPassData = None
        self.highPassData = None

        # The datafile used by tableview
        self.tableDataFile = None

        self.featuresWindow = FeaturesWindow()
        self.deadReckoningWindow = DeadReckoningWindow()
        self.quitTrigger.connect(QMainWindow.closeEvent)

        self.filterParameters = {}

        # If the user cancels, quit
        if not self.show_load_dialog():
            self.quitTrigger.emit()
        else:
            TableAndGraphView.after_init(self)

            # Connect signals and slots
            self.connect_ui_elements()

            self.setup_filter_parameters()

            self.refilter_datasets()

    def connect_ui_elements(self):
        """ Connect each UI element to it's functionality

            :returns: void
        """
        self.featuresButton.clicked.connect(self.show_features_window)
        self.deadReckoningButton.clicked.connect(self.show_dead_reckoning_window)

        # Connect the line edits to a single slot. Pass a second parameter to identify it
        self.refreshLineEdit.textChanged.connect(lambda val: self.parameter_value_changed(val, 'SampleRate'))
        self.cutoffLineEdit.textChanged.connect(lambda val: self.parameter_value_changed(val, 'CutoffFrequency'))
        self.filterLineEdit.textChanged.connect(lambda val: self.parameter_value_changed(val, 'FilterLength'))

        self.drawModeComboBox.currentIndexChanged.connect(self.refill_column_combobox)
        self.currentColumnComboBox.currentIndexChanged.connect(self.update_filter_params)

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

            self.refill_column_combobox()

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
        """ Take the filter params that have been specified, and apply them to the models

            :returns: void
        """
        self.lowPassData = TableModel(filtered_sensor_data
                                      .FilteredSensorData(LPF, self.tableDataFile.get_dataset(), self.filterParameters))
        self.highPassData = TableModel(filtered_sensor_data
                                       .FilteredSensorData(HPF, self.tableDataFile.get_dataset(), self.filterParameters))

        self.redraw_graph()

    def refill_column_combobox(self):
        """ Depending on how we want the data presented, the contents of the second combobox will change

        :return:
        """

        self.currentColumnComboBox.clear()
        current_type = self.drawModeComboBox.currentIndex()
        if current_type == 0:
            self.currentColumnComboBox.addItems(
                self.rawDataFile.getReadableColumns()[self.first_graphed_element:self.last_graphed_element]
            )
        else:
            self.currentColumnComboBox.addItems([
                'Accelerometer',
                'Magnetometer',
                'Gyroscope'
            ])

        self.currentColumnComboBox.setCurrentIndex(0)

        self.redraw_graph()

    def update_filter_params(self):
        self.refreshLineEdit.setText(str(self.filterParameters[self.rawDataFile.getColumns()[self.currentColumnComboBox.currentIndex() + self.first_graphed_element]]['SampleRate']))
        self.cutoffLineEdit.setText(str(self.filterParameters[self.rawDataFile.getColumns()[self.currentColumnComboBox.currentIndex() + self.first_graphed_element]]['CutoffFrequency']))
        self.filterLineEdit.setText(str(self.filterParameters[self.rawDataFile.getColumns()[self.currentColumnComboBox.currentIndex() + self.first_graphed_element]]['FilterLength']))

    def redraw_graph(self):
        """ Redraw the graph

            :returns: void
        """
        # Sanity check, before trying to join
        if not self.tableDataFile or not self.lowPassData or not self.highPassData:
            return

        current_type = self.drawModeComboBox.currentIndex()

        if current_type == 0:  # Separated.
            current_column = self.rawDataFile.getColumns()[self.currentColumnComboBox.currentIndex() + self.first_graphed_element]

            lines = self.plot.plot(
                self.tableDataFile.get_dataset()[current_column].values[::-1], self.default_colours[0] + '-',
                self.lowPassData.get_dataset()[current_column].values[::-1], self.default_colours[1] + '-',
                self.highPassData.get_dataset()[current_column].values[::-1], self.default_colours[2] + '-'
            )

            lines[0].set_label('Unfiltered')
            lines[1].set_label('Low pass')
            lines[2].set_label('High pass')
        else:
            # Choose the dataset based upon the first dropdown
            current_dataset = None
            if current_type == 1:
                current_dataset = self.tableDataFile.get_dataset()
            elif current_type == 2:
                current_dataset = self.lowPassData.get_dataset()
            else:
                current_dataset = self.highPassData.get_dataset()

            # Accelerometer, Magnetometer or Gyroscope
            if self.currentColumnComboBox.currentIndex() == 0:
                current_column = 'a'
            elif self.currentColumnComboBox.currentIndex() == 1:
                current_column = 'm'
            else:
                current_column = 'g'

            lines = self.plot.plot(
                current_dataset[current_column + 'x'].values[::-1], self.default_colours[0] + '-',
                current_dataset[current_column + 'y'].values[::-1], self.default_colours[1] + '-',
                current_dataset[current_column + 'z'].values[::-1], self.default_colours[2] + '-'
            )

            lines[0].set_label('X')
            lines[1].set_label('Y')
            lines[2].set_label('Z')


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

    def show_dead_reckoning_window(self):

        self.deadReckoningWindow.show()

    # TODO: Do we want this to happen? Unsure
    def change_selected_combo_column(self, selected, deselected):
        """ When the selected data cell changes, update the combobox that controls the parameters.

            :param selected: PyQt5. The cells that were selected.
            :param deselected: PyQt5. The cells that were deselected.
            :returns: void
        """
        #self.currentColumnComboBox.setCurrentIndex(selected.indexes()[0].column())

    def parameter_value_changed(self, new_value, parameter):
        """ Update the filter parameters model, redraw the graph

            :param new_value: PyQt5. The new filter parameter version
            :param parameter: Which filter parameter has changed
            :returns: void
        """
        if new_value == '':
            return

        self.filterParameters[self.rawDataFile.getColumns()[self.currentColumnComboBox.currentIndex() + self.first_graphed_element]][parameter] = int(new_value)
        self.refilter_datasets()