# TODO: Stop the overflow: None of the plot legend
# TODO: Time epochs

import os

import PyQt5.uic
from PyQt5.QtWidgets import QMainWindow

from pyAnimalTrack.ui.Controller.TableAndGraphView import TableAndGraphView
from pyAnimalTrack.ui.Model.FeaturesModel import FeaturesModel
from pyAnimalTrack.ui.Model.SettingsModel import SettingsModel
from pyAnimalTrack.ui.Model.TableModel import TableModel

from pyAnimalTrack.ui.Service.FeaturesCalculator import FeaturesCalculator
from pyAnimalTrack.ui.Service.SaveDataframe import SaveDataframe

uiFeaturesWindow = PyQt5.uic.loadUiType(os.path.join(os.path.dirname(__file__), '../View/FeaturesWindow.ui'))[0]


class FeaturesWindow(QMainWindow, uiFeaturesWindow, TableAndGraphView):

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
        self.lowPassData = None

        self.saveToDataFileButton.clicked.connect(self.save_data_to_file)
        self.saveGraphButton.clicked.connect(self.save_graph_to_file)

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
        out = FeaturesCalculator.calculate(unfiltered_data, low_pass_data)

        for row in range(0, len(unfiltered_data) - 1):
            features.append([
                ', '.join([str(unfiltered_data['ax'][row]), str(unfiltered_data['ay'][row]),
                           str(unfiltered_data['az'][row])]),
                out['SMA'][row],
                out['SVM'][row],
                out['MOV'][row],
                out['ENG'][row],
                out['ENT'][row],
                out['PIT'][row],
                out['ROL'][row],
                out['INC'][row]
            ])

        self.featureModel = FeaturesModel(features)
        self.tableDataFile = TableModel(self.featureModel)
        self.featureTableView.setModel(self.tableDataFile)

        TableAndGraphView.after_init(self)

        # Load filter controlling dropdown
        self.currentColumnComboBox.clear()
        self.currentColumnComboBox.addItems(self.featureModel.getReadableColumns())

    def redraw_graph(self):
        """ Redraw the graph

            :returns: void
        """

        current_column = self.currentColumnComboBox.currentIndex()

        # TODO: Read lines from config
        if current_column == 0:
            lines = self.plot.plot(
                self.lowPassData['ax'], SettingsModel.get_value('lines')[0],
                self.lowPassData['ay'], SettingsModel.get_value('lines')[1],
                self.lowPassData['az'], SettingsModel.get_value('lines')[2]
            )

            lines[0].set_label('X')
            lines[1].set_label('Y')
            lines[2].set_label('Z')

            self.legendPlot.legend(bbox_to_anchor=(-4, 0.9, 2., .102), loc=2, handles=lines)
        else:
            lines = self.plot.plot(
                self.tableDataFile.get_dataset()[self.featureModel.getColumns()[current_column]].values, SettingsModel.get_value('lines')[0]
            )

            lines[0].set_label(self.featureModel.getReadableColumns()[current_column].replace(' ', '\n'))

            self.legendPlot.legend(bbox_to_anchor=(-3.5, 0.9, 2., .102), loc=2, handles=lines)

        self.canvas.draw()
        self.legendCanvas.draw()

    def save_data_to_file(self):
        filename = SaveDataframe.save(self.tableDataFile.get_dataset(), 'data')

        if filename:
            self.featuresStatusBar.showMessage('Saved to ' + filename)

    def save_graph_to_file(self):
        filename = SaveDataframe.save(self.figure, 'graph')

        if filename:
            self.featuresStatusBar.showMessage('Saved to ' + filename)