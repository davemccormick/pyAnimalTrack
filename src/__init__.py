import sys

from PyQt5.QtWidgets import QApplication

from src.pyAnimalTrack.ui import UIMain

app = QApplication(sys.argv)
entrypoint = UIMain.UIMain()
entrypoint.run()
sys.exit(app.exec_())