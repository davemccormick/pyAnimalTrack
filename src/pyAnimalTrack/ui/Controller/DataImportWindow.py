import os

import numpy

import PyQt5.uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow

from pyAnimalTrack.backend.filehandlers import sensor_csv, filtered_sensor_data, sensor_data_clone
from pyAnimalTrack.backend.utilities.calibrate_axis import CalibrateAxis
from pyAnimalTrack.backend.utilities.accuracy import Accuracy
from pyAnimalTrack.backend.filters.low_pass_filter import LPF
from pyAnimalTrack.backend.filters.high_pass_filter import HPF

from pyAnimalTrack.ui.Controller.TableAndGraphView import TableAndGraphView
from pyAnimalTrack.ui.Controller.LoadCSVDialog import LoadCSVDialog
from pyAnimalTrack.ui.Controller.FeaturesWindow import FeaturesWindow
from pyAnimalTrack.ui.Controller.DeadReckoningWindow import DeadReckoningWindow
from pyAnimalTrack.ui.Model.TableModel import TableModel
from pyAnimalTrack.ui.Model.SettingsModel import SettingsModel

uiDataImportWindow = PyQt5.uic.loadUiType(os.path.join(os.path.dirname(__file__), '../View/DataImportWindow.ui'))[0]


class DataImportWindow(QMainWindow, uiDataImportWindow, TableAndGraphView):

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

        SettingsModel.load_from_config()

        # Datasets
        self.rawDataFile = None
        self.calibratedData = None
        self.accuracyData = None
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

            #self.calibratedData = TableModel(sensor_data_clone.SensorDataClone(self.tableDataFile.get_dataset()))

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

    def check_accuracy(self):
        ac = Accuracy()

        dataset = self.accuracyData.get_dataset()
        #dataset = self.calibratedData.get_dataset()

        for i in range(0, len(dataset)):
            print(ac.improve_accuracy(dataset['ax'][i], dataset['ay'][i], dataset['az'][i]))

    def calibrate_axis(self):
        ca = CalibrateAxis()

        dataset = self.calibratedData.get_dataset()

        for col in enumerate(['ax', 'ay', 'az', 'mx', 'my', 'mz', 'gx', 'gy', 'gz']):
            changed = ca.calibrate(dataset[col[1]], numpy.min(dataset[col[1]]), numpy.max(dataset[col[1]]), SettingsModel.get_value('scaling')[col[1]])
            for i in range(0, len(dataset[col[1]])):
                self.calibratedData.get_dataset().iloc[i][col[0] + 1] = changed[i]

    def show_load_dialog(self):
        """ Show the user a dialog to load a data file(CSV)

            :returns: True if a file has been loaded, false otherwise
        """

        # TODO: Don't clear the existing path on cancel

        file_loader_dialog = LoadCSVDialog()
        dialog_result = file_loader_dialog.loadCSV(self)

        if dialog_result[0]:
            # Get the model back, build the view

            SettingsModel.set_temp_value('ground_reference_frame', dialog_result[3])

            # Load the CSV data object into the table
            self.rawDataFile = sensor_csv.SensorCSV(
                dialog_result[1],
                dialog_result[2],
                dialog_result[3]
            )
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
                'SampleRate':       SettingsModel.get_value('filter_parameters')['SampleRate'],
                'CutoffFrequency':  SettingsModel.get_value('filter_parameters')['CutoffFrequency'],
                'FilterLength':     SettingsModel.get_value('filter_parameters')['FilterLength']
            }

    def refilter_datasets(self):
        """ Take the filter params that have been specified, and apply them to the models

            :returns: void
        """
        self.calibratedData = TableModel(sensor_data_clone.SensorDataClone(self.tableDataFile.get_dataset()))

        self.calibrate_axis()

        self.lowPassData = TableModel(filtered_sensor_data
                                      .FilteredSensorData(LPF, self.calibratedData.get_dataset(), self.filterParameters))
        self.highPassData = TableModel(filtered_sensor_data
                                       .FilteredSensorData(HPF, self.calibratedData.get_dataset(), self.filterParameters))

        self.accuracyData = TableModel(sensor_data_clone.SensorDataClone(self.lowPassData.get_dataset()))

        self.check_accuracy()

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
        if not self.calibratedData or not self.lowPassData or not self.highPassData:
            return

        current_type = self.drawModeComboBox.currentIndex()

        if current_type == 0:  # Separated.
            current_column = self.rawDataFile.getColumns()[self.currentColumnComboBox.currentIndex() + self.first_graphed_element]

            lines = self.plot.plot(
                self.calibratedData.get_dataset()[current_column].values, SettingsModel.get_value('lines')[0],
                self.lowPassData.get_dataset()[current_column].values, SettingsModel.get_value('lines')[1],
                self.highPassData.get_dataset()[current_column].values, SettingsModel.get_value('lines')[2]
            )

            lines[0].set_label('Unfiltered')
            lines[1].set_label('Low pass')
            lines[2].set_label('High pass')
        else:
            # Choose the dataset based upon the first dropdown
            current_dataset = None
            if current_type == 1:
                current_dataset = self.calibratedData.get_dataset()
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
                current_dataset[current_column + 'x'].values[::-1], SettingsModel.get_value('lines')[0],
                current_dataset[current_column + 'y'].values[::-1], SettingsModel.get_value('lines')[1],
                current_dataset[current_column + 'z'].values[::-1], SettingsModel.get_value('lines')[2]
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
            self.calibratedData.get_dataset(),
            self.lowPassData.get_dataset(),
            self.highPassData.get_dataset()
        )
        self.featuresWindow.show()

    def show_dead_reckoning_window(self):
        """ Set the data for the dead reckoning window, and display it

            :returns: void
        """

        self.deadReckoningWindow.set_data(
            self.calibratedData.get_dataset(),
            self.lowPassData.get_dataset(),
            self.highPassData.get_dataset()
        )
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