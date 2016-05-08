from pyAnimalTrack.backend.utilities.enums import *
from pyAnimalTrack.backend.utilities.exceptions import *

import numpy as np

class DeadReckoning(object):
    """ Class for Dead Reckoning algorithm
    """

    def __init__(self, speed,
                       heading,
                       angle=Angle.degree, 
                       returnToStart=True, 
                       depth=None, 
                       pitch=None, 
                       endcoords=None, 
                       speedhorizontal = SpeedHorizontal.corrected):

        """ Constructor
            :param speed: Speed
            :param heading: Data
            :param angle: Data
            :param returnToStart: Data
            :param depth: Data
            :param pitch: Data
            :param endcoords: Data
            :param speedhorizontal: Data
        """

        #Input data
        self.speed = speed
        self.heading = heading
        self.angle = angle
        self.returnToStart = returnToStart
        self.depth = depth
        self.pitch = pitch
        self.endcoords = endcoords
        self.speedhorizontal = speedhorizontal

        # Other instance variables
        self.dataLength = len(self.speed)

        self.cdrx = None
        self.cdry = None
        self.endx = None
        self.endy = None

        if self.returnToStart:
            self.endx = 0
            self.endy = 0

        # State
        self.courseSteeredCalculated = False

        return


    def compute(self):
        """ Convenience wrapper to run dead reckoning in required order.

            :returns: Data dictionary.
        """

        self.validateInputs()
        self.calculateSpeed()
        self.courseSteered()
        ddict = self.courseMadeGood()

        return ddict


    def validateInputs(self):
        """ Initial input validation. Uses instance variables.

        """

        if (self.angle != Angle.degree) and (self.angle != Angle.radian):
            raise AngleException("Heading parameter must be either degree or radian") 

        if (self.speedhorizontal != SpeedHorizontal.corrected) and (self.speedhorizontal != SpeedHorizontal.pitch) and (self.speedhorizontal != SpeedHorizontal.depth):
            raise SpeedHorizontalException("SpeedHorizontal must be either corrected, pitch or depth.")

        if len(self.speed) != len(self.heading):
            raise LengthException("Data length mismatch between speed and heading")

        return


    def calculateSpeed(self):
        """ Calculate Horizontal Speed Values.

        """

        if (self.speedhorizontal == SpeedHorizontal.pitch) and (self.pitch != None):
            self.speed = np.cos(self.pitch) * self.speed
            print("Horizontal speed is calculated as cos(pitch)*speed")

        return


    def courseSteered(self):
        """ Determine course steered via dead reckoning.

        """

        if self.angle == Angle.degree:
            drx = self.speed*np.sin(self.heading/(180/np.pi))
            dry = self.speed*np.cos(self.heading/(180/np.pi))


        if self.angle == Angle.radian:
            drx = self.speed*np.sin(self.heading)
            dry = self.speed*np.cos(self.heading)

        # Start from 0
        drx[0] = 0
        dry[0] = 0

        self.cdrx = np.cumsum(drx)
        self.cdry = np.cumsum(dry)

        self.courseSteeredCalculated = True

        return

    def courseMadeGood(self):
        """ Determine course made good. Must be called after courseSteered is calculated.

        """
        if not self.courseSteeredCalculated:
            raise CourseSteeredNotCalculatedException("Course Steered not yet calculated.")


        drdict = {}
        driftx = (self.cdrx[-1] - self.endx) / self.dataLength
        drifty = (self.cdry[-1] - self.endy) / self.dataLength
        errorDistance = np.sqrt(((self.cdrx[-1] - self.endx) ** 2) + ((self.cdry[-1] - self.endy) ** 2))
        drift = errorDistance / self.dataLength
        set_ = np.arctan2((self.y - self.cdry[-1]), (self.x - self.cdrx[-1]))
        set_ = ((2*np.pi) - (set_ - (np.pi/2))) % (2*np.pi)

        # Initial values for CMG
        xcmg = self.cdrx[0]
        ycmg = self.cdry[0]

        tty = range(1, self.dataLength + 1)
        xcmg = self.cdrx - (driftx * tty)
        xcmy = self.cdry - (drifty * tty)
        xcmg[0] = 0
        ycmg[0] = 0

        smg = np.sqrt(np.diff(xcmg)**2 + np.diff(ycmg)**2)
        smg = np.insert(smg,0,0)

        #Persist to dict and return.
        drdict['CourseSteeredX'] = self.cdrx
        drdict['CourseSteeredY'] = self.cdry
        drdict['CourseMadeGoodX'] = xcmg
        drdict['CourseMadeGoodY'] = ycmg
        drdict['SpeedH'] = self.speed
        drdict['SpeedMadeGood'] = smg
        drdict['CourseMadeGoodX'] = xcmg
        drdict['Drift'] = drift
        drdict['ErrorDistance'] = errorDistance
        drdict['Set_'] = set_

        return drdict
