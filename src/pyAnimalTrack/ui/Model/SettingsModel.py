import os
import json


class SettingsModel:
    __settings_filename = 'settings.json'

    __defaults = {
        # Choices:
        # b: blue
        # g: green
        # r: red
        # c: cyan
        # m: magenta
        # y: yellow
        # k: black
        # w: white

        'lines': [
            'k',
            'b',
            'm'
        ],

        'data_SaveFormats': [
            'csv',
            'txt'
        ],

        'graph_SaveFormats': [
            'png'
        ],

        'csv_separator': ';',

        # Data manipulation

        'ground_reference_frame_options': ['NED', 'ENU'],

        'filter_parameters': {
            'SampleRate': 10,
            'CutoffFrequency': 2,
            'FilterLength': 59
        },

        'scaling': {
            'ax': -1,
            'ay': -1,
            'az': 1,
            'mx': 1,
            'my': 1,
            'mz': 1,
            'gx': 1,
            'gy': 1,
            'gz': 1,
        }
    }

    __settings = {}

    __temporary_settings = {
        'ground_reference_frame': 'NED'
    }

    @staticmethod
    def load_from_config():
        if os.path.exists(SettingsModel.__settings_filename):
            file = open(SettingsModel.__settings_filename, 'r')
            SettingsModel.__settings = json.loads(file.read())
            file.close()
        else:
            SettingsModel.__settings = SettingsModel.__defaults
            SettingsModel._save_config()

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
    def set_temp_value(key, value):
        SettingsModel.__temporary_settings[key] = value

    @staticmethod
    def get_value(key):
        if SettingsModel.__settings.__contains__(key):
            return SettingsModel.__settings[key]
        elif SettingsModel.__temporary_settings.__contains__(key):
            return SettingsModel.__temporary_settings[key]
        else:
            if key.endswith('SaveFormatsFilter'):
                format = key.split('_')[0]
                return '*.' + ';;*.'.join(SettingsModel.__settings[format + '_SaveFormats'])
