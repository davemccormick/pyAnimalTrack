import os

import PyQt5.uic
from PyQt5.QtCore import pyqtSignal, pyqtSlot

from PyQt5.QtWidgets import QMainWindow

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

from pyAnimalTrack.backend.filters.low_pass_filter import LPF
from pyAnimalTrack.backend.utilities.calculate_features import CalculateFeatures

from pyAnimalTrack.ui.Controller.TableAndGraphView import TableAndGraphView
from pyAnimalTrack.ui.Model.FeaturesModel import FeaturesModel
from pyAnimalTrack.ui.Model.TableModel import TableModel

uiFeaturesWindow = PyQt5.uic.loadUiType(os.path.join(os.path.dirname(__file__), '../View/FeaturesWindow.ui'))[0]


class FeaturesWindow(QMainWindow, uiFeaturesWindow, TableAndGraphView):

    def __init__(self, *args):
        super(FeaturesWindow, self).__init__(*args)
        self.setupUi(self)
        TableAndGraphView.__init__(self, self.featureTableView, self.currentColumnComboBox, self.lowPassPlotFrame, self.legendFrame, self.redraw_graph)

        self.figure = plt.figure()
        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        self.lowPassPlotFrame.addWidget(self.canvas)

        self.featureModel = None
        self.tableDataFile = None

    def set_data(self, unfiltered_data, low_pass_data, high_pass_data):
        # create an axis
        #ax = self.figure.add_subplot(111)
        # discards the old graph
        #ax.hold(False)
        # plot data
        #ax.plot(unfiltered_data.ax.values[::-1], 'g-', low_pass_data.ax.values[::-1], 'b-', high_pass_data.ax.values[::-1], 'r-')

        #self.canvas.draw()

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
            1,#CalculateFeatures.calculate_sma(x, y, z),
            2,#CalculateFeatures.calculate_svm(x, y, z),
            3,#CalculateFeatures.calculate_movement_variation(x, y, z),
            4,#CalculateFeatures.calculate_energy(x, y, z),
            5,#CalculateFeatures.calculate_entropy(x, y, z),
            6,#CalculateFeatures.calculate_pitch(x, y, z),
            7,#CalculateFeatures.calculate_roll(y, z),
            8#CalculateFeatures.calculate_inclination(x, y, z)
        ]

    def test(self):
        pass

    def redraw_graph(self):
        """ Redraw the graph

            :returns: void
        """
        #current_column = self.featureModel.getColumns()[self.currentColumnComboBox.currentIndex()]

        lines = self.plot.plot(
            self.tableDataFile.get_dataset()[1].values[::-1], 'g-'
        )

        lines[0].set_label('Unfiltered')
        #lines[1].set_label('Low pass')
        #lines[2].set_label('High pass')

        self.legendPlot.legend(bbox_to_anchor=(-4, 0.9, 2., .102), loc=2, handles=lines)

        self.canvas.draw()
        #self.legendCanvas.draw()