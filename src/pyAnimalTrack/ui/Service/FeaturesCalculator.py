from pyAnimalTrack.backend.utilities.calculate_features import CalculateFeatures

from pyAnimalTrack.ui.Model.SettingsModel import SettingsModel

class FeaturesCalculator:
    def __init__(self):
        pass

    @staticmethod
    def calculate(unfiltered_data, low_pass_data):
        features = FeaturesCalculator._calculate_features([
            unfiltered_data['ax'],
            unfiltered_data['ay'],
            unfiltered_data['az']
        ], [
            low_pass_data['ax'],
            low_pass_data['ay'],
            low_pass_data['az']
        ])

        return features

    @staticmethod
    def _calculate_features(unfiltered, LPF):
        roll_multiplier = -1 if SettingsModel.get_value('ground_reference_frame') == 'NED' else 1

        return {
            'SMA': CalculateFeatures.calculate_sma(*unfiltered),
            'SVM': CalculateFeatures.calculate_svm(*unfiltered),
            'MOV': CalculateFeatures.calculate_movement_variation(*unfiltered),
            'ENG': CalculateFeatures.calculate_energy(*unfiltered),
            'ENT': CalculateFeatures.calculate_entropy(*unfiltered),
            'PIT': CalculateFeatures.calculate_pitch(*LPF),
            'ROL': CalculateFeatures.calculate_roll(LPF[0], LPF[2] * roll_multiplier),
            'INC': CalculateFeatures.calculate_inclination(*unfiltered)
        }