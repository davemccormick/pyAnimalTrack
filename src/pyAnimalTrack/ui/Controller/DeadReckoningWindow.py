import os

import PyQt5.uic
from PyQt5.QtWidgets import QMainWindow

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

from pyAnimalTrack.backend.utilities.enums import *
from pyAnimalTrack.backend.utilities.calculate_features import CalculateFeatures
from pyAnimalTrack.backend.deadreckoning.dead_reckoning import DeadReckoning

from pyAnimalTrack.ui.Model.FeaturesCalculator import FeaturesCalculator


uiDeadReckoningWindow = PyQt5.uic.loadUiType(os.path.join(os.path.dirname(__file__), '../View/DeadReckoningWindow.ui'))[0]


class DeadReckoningWindow(QMainWindow, uiDeadReckoningWindow):

    # TODO: Read from config
    # Default values, used to initialise the model

    default_colours = [
        'r',
        'g',
        'b'
    ]

    def __init__(self, *args):
        """ Constructor - This is actually the main function of the program

            :param args: -
            :returns: void
        """

        super(DeadReckoningWindow, self).__init__(*args)
        self.setupUi(self)

        # Normal matplotlib graphing components
        self.steeredFigure = plt.figure(facecolor='none')
        self.steeredTimeFigure = plt.figure(facecolor='none')

        self.steeredCanvas = FigureCanvas(self.steeredFigure)
        self.steeredTimeCanvas = FigureCanvas(self.steeredTimeFigure)

        self.mapFrame.addWidget(self.steeredCanvas)
        self.timeFrame.addWidget(self.steeredTimeCanvas)

        self.steeredPlot = self.steeredFigure.add_subplot(111)
        self.steeredTimePlot = self.steeredTimeFigure.add_subplot(111)

        self.steeredPlot.hold(False)
        self.steeredTimePlot.hold(False)

    def set_data(self, unfiltered_data, low_pass_data, high_pass_data):
        features = FeaturesCalculator.calculate(unfiltered_data, low_pass_data)

        headings = CalculateFeatures.calculate_heading(
            unfiltered_data['mx'],
            unfiltered_data['my'],
            unfiltered_data['mz'],
            features['PIT'],
            features['ROL'],
            angle=Angle.radian
        )

        dr = DeadReckoning(features['SVM'], headings['heading_geo'], angle=Angle.radian)
        dr.courseSteered()

        self.create_graphs(dr)

    def create_graphs(self, dead_reckoning):
        self.steeredPlot.plot(dead_reckoning.cdrx, dead_reckoning.cdry)
        self.steeredTimePlot.plot(
            dead_reckoning.cdrx, self.default_colours[0] + '-',
            dead_reckoning.cdry, self.default_colours[1] + '-'
        )