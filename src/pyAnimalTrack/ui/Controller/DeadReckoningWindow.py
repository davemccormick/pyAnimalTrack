import os

import PyQt5.uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow

from pyAnimalTrack.backend.filehandlers import sensor_csv, filtered_sensor_data
from pyAnimalTrack.backend.filters.low_pass_filter import LPF
from pyAnimalTrack.backend.filters.high_pass_filter import HPF

from pyAnimalTrack.backend.deadreckoning.dead_reckoning import DeadReckoning

from pyAnimalTrack.ui.Controller.TableAndGraphView import TableAndGraphView
from pyAnimalTrack.ui.Controller.LoadCSVDialog import LoadCSVDialog
from pyAnimalTrack.ui.Controller.FeaturesWindow import FeaturesWindow
from pyAnimalTrack.ui.Model.TableModel import TableModel

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