import os

import PyQt5.uic

from PyQt5.QtWidgets import QDialog, QFileDialog
from PyQt5.QtCore import pyqtSlot

from pyAnimalTrack.ui.Model.SettingsModel import SettingsModel

# TODO: Load path from config
uiLoadCSVDialog = PyQt5.uic.loadUiType(os.path.join(os.path.dirname(__file__), '../View/LoadCSVDialog.ui'))[0]


class LoadCSVDialog(QDialog, uiLoadCSVDialog):

    dialog = None

    def __init__(self, *args):
        super(LoadCSVDialog, self).__init__(*args)
        self.setupUi(self)

    def loadCSV(self, parent=None):
        self.dialog = LoadCSVDialog(parent)
        self.dialog.separator_textbox.setText(SettingsModel.get_value('csv_separator'))

        result = self.dialog.exec_()
        return (result == QDialog.Accepted, self.dialog.location_textbox.text(), self.dialog.separator_textbox.text())

    @pyqtSlot()
    def showReadFile(self):
        self.location_textbox.setText(QFileDialog.getOpenFileName()[0])