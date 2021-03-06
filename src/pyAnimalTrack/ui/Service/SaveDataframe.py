# TODO: Saving to file with a particular separator.
# TODO: Saving to file, output folder the same as where we loaded from maybe?

from PyQt5.QtWidgets import QFileDialog

from pyAnimalTrack.ui.Model.SettingsModel import SettingsModel


class SaveDataframe:

    @staticmethod
    def save(data, format, save=True):
        save_result = QFileDialog.getSaveFileName(filter=SettingsModel.get_value(format + '_SaveFormatsFilter'))

        filename = save_result[0]

        # No filename, cancelled
        if filename == '':
            return

        # If we don't have a extension, add one
        if not SettingsModel.get_value(format + '_SaveFormats').__contains__(filename.split('.')[-1]):
            filename += '.' + save_result[1].split('.')[-1]

        # Save the pandas dataframe and alert the user
        if not save:
            return filename
        elif format == 'data':
            data.to_csv(filename)
            return filename
        elif format == 'graph':
            data.savefig(filename)
            return filename

        return False