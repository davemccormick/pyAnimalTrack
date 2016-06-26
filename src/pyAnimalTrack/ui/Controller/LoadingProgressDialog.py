import os

from PyQt5 import uic

from PyQt5.QtWidgets import QDialog, QFileDialog
from PyQt5.QtCore import pyqtSlot

from pyAnimalTrack.ui.Model.SettingsModel import SettingsModel


viewFilePath = os.path.join(os.path.dirname(__file__), '../../../../View/')
if not os.path.exists(viewFilePath):
    viewFilePath = os.path.join(os.path.dirname(__file__), '../View/')

uiLoadingProgressDialog = uic.loadUiType(os.path.join(viewFilePath, 'LoadingProgressDialog.ui'))[0]


class LoadingProgressDialog(QDialog, uiLoadingProgressDialog):

    dialog = None

    def __init__(self, *args):
        super(LoadingProgressDialog, self).__init__(*args)
        self.setupUi(self)

    def show_loading(self, parent):
        self.dialog = LoadingProgressDialog(parent)
        self.dialog.open()

    def update_progress(self, progress):
        self.dialog.progressBar.setValue(progress)

        if progress == 100:
            self.dialog.hide()