import pyAnimalTrack.ui.Controller.DataImportWindow


class UIMain(object):
    """ UI Entrypoint
    """
    window = None

    def __init__(self):
        """
            Null constructor
        """

    def run(self):
        """ run
            Gets program flow control, creates the main window
            :returns:
        """
        self.window = pyAnimalTrack.ui.Controller.DataImportWindow.DataImportWindow()
        self.window.show()
