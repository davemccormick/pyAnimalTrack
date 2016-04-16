class AngleException(Exception):
    """ Raised if Angle does not equal Angle enum value.

    """
    pass


class SpeedHorizontalException(Exception):
    """ Raised if SpeedHorizontal does not equal SpeedHorizontal enum value.

    """
    pass


class LengthException(Exception):
    """ Raised if uneven length between speed and heading data.

    """
    pass


class CourseSteeredNotCalculatedException(Exception):
    """ Raised if CourseNotSteered has not been run prior to CourseMadeGood.

    """
    pass