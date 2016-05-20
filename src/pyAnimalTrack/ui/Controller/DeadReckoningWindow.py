import os

import PyQt5.uic
import matplotlib.pyplot as plt
import pandas as pd
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from pyAnimalTrack.backend.deadreckoning.dead_reckoning import DeadReckoning
from pyAnimalTrack.backend.utilities.calculate_features import CalculateFeatures
from pyAnimalTrack.backend.utilities.enums import *
from pyAnimalTrack.ui.Model.SettingsModel import SettingsModel

from pyAnimalTrack.ui.Service.FeaturesCalculator import FeaturesCalculator
from pyAnimalTrack.ui.Service.SaveDataframe import SaveDataframe


uiDeadReckoningWindow = PyQt5.uic.loadUiType(os.path.join(os.path.dirname(__file__), '../View/DeadReckoningWindow.ui'))[0]


class DeadReckoningWindow(QMainWindow, uiDeadReckoningWindow):

    def __init__(self, *args):
        """ Constructor - This is actually the main function of the program

            :param args: -
            :returns: void
        """

        super(DeadReckoningWindow, self).__init__(*args)
        self.setupUi(self)

        self.headings = None
        self.dead_reckoning = None

        # Normal matplotlib graphing components
        self.steeredFigure = plt.figure(facecolor='none')
        self.steeredTimeFigure = plt.figure(facecolor='none')
        self.steeredTimeLegendFigure = plt.figure(facecolor='none')

        self.steeredCanvas = FigureCanvas(self.steeredFigure)
        self.steeredTimeCanvas = FigureCanvas(self.steeredTimeFigure)
        self.steeredTimeLegendCanvas = FigureCanvas(self.steeredTimeLegendFigure)

        self.mapFrame.addWidget(self.steeredCanvas)
        self.timeFrame.addWidget(self.steeredTimeCanvas)
        self.timeLegendFrame.addWidget(self.steeredTimeLegendCanvas)

        self.steeredPlot = self.steeredFigure.add_subplot(111)
        self.steeredTimePlot = self.steeredTimeFigure.add_subplot(111)
        self.steeredTimeLegendPlot = self.steeredTimeLegendFigure.add_axes([-0.2,0,-0.045,0.85])

        self.steeredPlot.hold(False)
        self.steeredTimePlot.hold(False)
        self.steeredTimeLegendPlot.hold(False)

        # PyQt Connections
        self.saveToDataFileButton.clicked.connect(self.save_to_data_file)
        self.saveGraphsButton.clicked.connect(self.save_graphs_to_file)

    def set_data(self, unfiltered_data, low_pass_data, high_pass_data):
        features = FeaturesCalculator.calculate(unfiltered_data, low_pass_data)

        self.headings = CalculateFeatures.calculate_heading(
            unfiltered_data['mx'],
            unfiltered_data['my'],
            unfiltered_data['mz'],
            features['PIT'],
            features['ROL'],
            angle=Angle.radian
        )

        self.dead_reckoning = DeadReckoning(features['SVM'], self.headings['heading_geo'], angle=Angle.radian)
        self.dead_reckoning.courseSteered()

        self.create_graphs()

    def create_graphs(self):
        self.steeredPlot.plot(self.dead_reckoning.cdrx, self.dead_reckoning.cdry, SettingsModel.get_value('lines')[0])

        # TODO: Constant tick values for the graph, so the X and Y coords match (No stretching)
        # self.steeredPlot.set_xlim((0, 40))
        # self.steeredPlot.set_ylim((0, 40))

        time_lines = self.steeredTimePlot.plot(
            self.dead_reckoning.cdrx, SettingsModel.get_value('lines')[0],
            self.dead_reckoning.cdry, SettingsModel.get_value('lines')[1]
        )

        time_lines[0].set_label('X')
        time_lines[1].set_label('Y')

        self.steeredTimeLegendPlot.legend(bbox_to_anchor=(-4, 0.9, 2., .102), loc=2, handles=time_lines)

    def save_to_data_file(self):
        filename = SaveDataframe.save(pd.DataFrame(
            {
                'x': self.dead_reckoning.cdrx,
                'y': self.dead_reckoning.cdry,
                'heading': self.dead_reckoning.heading,
                'speed': self.dead_reckoning.speed
            }
        ), 'data')

        if filename:
            self.savingStatusBar.showMessage('Saved to ' + filename)

    def save_graphs_to_file(self):
        filename = SaveDataframe.save(None, 'graph', False)
        time_filename = filename.split('.')[0] + '_time.' + filename.split('.')[1]

        self.steeredFigure.savefig(filename)
        self.steeredTimeFigure.savefig(time_filename)

        if filename:
            self.savingStatusBar.showMessage('Saved to ' + filename + ' and ' + time_filename)