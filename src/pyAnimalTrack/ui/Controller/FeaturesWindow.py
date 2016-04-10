import PyQt5.uic
from PyQt5.QtCore import pyqtSignal, pyqtSlot

from PyQt5.QtWidgets import QMainWindow

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

from src.pyAnimalTrack.backend.filters.low_pass_filter import LPF

uiFeaturesWindow = PyQt5.uic.loadUiType('./pyAnimalTrack/ui/View/FeaturesWindow.ui')[0]


class FeaturesWindow(QMainWindow, uiFeaturesWindow):

    def __init__(self, *args):
        super(FeaturesWindow, self).__init__(*args)
        self.setupUi(self)

        self.figure = plt.figure()
        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        self.lowPassPlotFrame.addWidget(self.canvas)

    def set_data(self, unfiltered_data, low_pass_data, high_pass_data):
        # create an axis
        ax = self.figure.add_subplot(111)
        # discards the old graph
        ax.hold(False)
        # plot data
        ax.plot(unfiltered_data.ax.values[::-1], 'g-', low_pass_data.ax.values[::-1], 'b-', high_pass_data.ax.values[::-1], 'r-')

        self.canvas.draw()