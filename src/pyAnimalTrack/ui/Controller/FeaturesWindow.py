# TODO: Stop the overflow: None of the plot legend
# TODO: Saving to file with a particular separator.
# TODO: Saving to file, output folder the same as where we loaded from maybe?

import os

import PyQt5.uic
from PyQt5.QtCore import pyqtSignal, pyqtSlot

from PyQt5.QtWidgets import QMainWindow, QFileDialog

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

from pyAnimalTrack.backend.filters.low_pass_filter import LPF
from pyAnimalTrack.backend.utilities.calculate_features import CalculateFeatures

from pyAnimalTrack.ui.Controller.TableAndGraphView import TableAndGraphView
from pyAnimalTrack.ui.Model.FeaturesModel import FeaturesModel
from pyAnimalTrack.ui.Model.TableModel import TableModel

uiFeaturesWindow = PyQt5.uic.loadUiType(os.path.join(os.path.dirname(__file__), '../View/FeaturesWindow.ui'))[0]


class FeaturesWindow(QMainWindow, uiFeaturesWindow, TableAndGraphView):

    lowPassData = None
    saveFormat = 'csv'

    def __init__(self, *args):
        """ Constructor

            :param args: PyQt program arguments
            :return: void
        """

        super(FeaturesWindow, self).__init__(*args)
        self.setupUi(self)
        TableAndGraphView.__init__(self, self.featureTableView, self.currentColumnComboBox, self.plotFrame, self.legendFrame, self.redraw_graph)

        self.featureModel = None
        self.tableDataFile = None

        self.saveToFileButton.clicked.connect(self.save_to_file)

    def set_data(self, unfiltered_data, low_pass_data, high_pass_data):
        """ Set the datasets for the features window

            :param unfiltered_data: A pandas dataset, as read from the input stream
            :param low_pass_data: A pandas dataset, after running through the low-pass filter
            :param high_pass_data: A pandas dataset, after running through the high-pass filter
            :return: void
        """

        # Cache the dataset for the graph
        self.lowPassData = low_pass_data

        features = []
        for row in zip(low_pass_data['ax'], low_pass_data['ay'], low_pass_data['az']):
            features.append(self.calculate_features(row[0], row[1], row[2]))

        self.featureModel = FeaturesModel(features)
        self.tableDataFile = TableModel(self.featureModel)
        self.featureTableView.setModel(self.tableDataFile)

        TableAndGraphView.after_init(self)

        # Load filter controlling dropdown
        self.currentColumnComboBox.clear()
        self.currentColumnComboBox.addItems(self.featureModel.getReadableColumns())

    def calculate_features(self, x, y, z):
        return [
            ', '.join([str(x), str(y), str(z)]),
            CalculateFeatures.calculate_sma(x, y, z),
            CalculateFeatures.calculate_svm(x, y, z),
            3,#CalculateFeatures.calculate_movement_variation(x, y, z),
            CalculateFeatures.calculate_energy(x, y, z),
            CalculateFeatures.calculate_entropy(x, y, z),
            CalculateFeatures.calculate_pitch(x, y, z),
            CalculateFeatures.calculate_roll(y, z),
            CalculateFeatures.calculate_inclination(x, y, z)
        ]

    def test(self):
        pass

    def redraw_graph(self):
        """ Redraw the graph

            :returns: void
        """

        current_column = self.currentColumnComboBox.currentIndex()

        if current_column == 0:
            lines = self.plot.plot(
                self.lowPassData['ax'], 'r-',
                self.lowPassData['ay'], 'g-',
                self.lowPassData['az'], 'b-'
            )

            lines[0].set_label('X')
            lines[1].set_label('Y')
            lines[2].set_label('Z')

            self.legendPlot.legend(bbox_to_anchor=(-4, 0.9, 2., .102), loc=2, handles=lines)
        else:
            lines = self.plot.plot(
                self.tableDataFile.get_dataset()[self.featureModel.getColumns()[current_column]].values[::-1], 'r-'
            )

            lines[0].set_label(self.featureModel.getReadableColumns()[current_column])

            self.legendPlot.legend(bbox_to_anchor=(-4, 0.9, 2., .102), loc=2, handles=lines)

        self.canvas.draw()
        self.legendCanvas.draw()

    def save_to_file(self):
        filename = QFileDialog.getSaveFileName(filter='*.' + self.saveFormat)[0]

        # No filename, cancelled
        if filename == '':
            return

        # If we don't have a extension, add one
        if not filename.endswith('.' + self.saveFormat):
            filename += '.' + self.saveFormat

        # Save the pandas dataframe and alert the user
        self.tableDataFile.get_dataset().to_csv(filename)
        self.featuresStatusBar.showMessage('Saved to ' + filename, 2000)