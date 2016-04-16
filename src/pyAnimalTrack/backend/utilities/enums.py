from enum import Enum # Requires enum34 lib

class Angle(Enum):
    degree = 1
    radian = 2


class SpeedHorizontal(Enum):
    corrected = 1
    pitch = 2
    depth = 3
