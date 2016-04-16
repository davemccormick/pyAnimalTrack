from enum import Enum # Requires enum34 lib

class Angle(Enum):
    """ Angle Enum. Degree = 1, Radian = 2.

    """
    degree = 1
    radian = 2


class SpeedHorizontal(Enum):
    """ SpeedHorizonal Enum. Correct = 1, Pitch = 2, Depth = 3.

    """ 
    corrected = 1
    pitch = 2
    depth = 3
