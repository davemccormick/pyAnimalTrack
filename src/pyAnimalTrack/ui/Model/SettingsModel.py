import os
import json


class SettingsModel:
    __settings_filename = 'settings.json'

    __defaults = {
        'lines': [
            'r-',
            'g-',
            'b-'
        ],

        'data_SaveFormats': [
            'csv',
            'txt'
        ],

        'graph_SaveFormats': [
            'png'
        ],

        'csv_separator': ';'
    }

    __settings = {}

    @staticmethod
    def load_from_config():
        if os.path.exists(SettingsModel.__settings_filename):
            file = open(SettingsModel.__settings_filename, 'r')
            SettingsModel.__settings = json.loads(file.read())
            file.close()
        else:
            SettingsModel.__settings = SettingsModel.__defaults
            #SettingsModel._save_config() TODO Reenable

    @staticmethod
    def _save_config():
        file = open(SettingsModel.__settings_filename, 'w')
        file.write(json.dumps(SettingsModel.__settings))
        file.close()

    @staticmethod
    def set_value(key, value):
        SettingsModel.__settings[key] = value
        SettingsModel._save_config()

    @staticmethod
    def get_value(key):
        if SettingsModel.__settings.__contains__(key):
            return SettingsModel.__settings[key]
        else:
            if key.endswith('SaveFormatsFilter'):
                format = key.split('_')[0]
                return '*.' + ';;*.'.join(SettingsModel.__settings[format + '_SaveFormats'])
