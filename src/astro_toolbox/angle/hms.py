"""
This module contain AngleHMS class
"""
import math
class AngleHMS():
    """AngleHMS define a hms angle with his conversions
    """
    def __init__(self, anglevalue: tuple):
        """Constructor method

        Parameters
        ----------
        anglevalue : tuple
            The angle value in hms
        """
        self.anglevalue = anglevalue

    def __repr__(self):
        """Representative method

        Returns
        -------
        string
            Return a class representative string
        """
        return f'{self.anglevalue[0]:02d}h{self.anglevalue[1]:02d}m{self.anglevalue[2]:05.2f}s'

    def hmstodeg(self):
        """HMS to Degrees converting method
        This method return angle in degrees from angle in hms

        Returns
        -------
        float
            The angle value in degrees
        """
        return ((self.anglevalue[0] +
            self.anglevalue[1]/60 +
            self.anglevalue[2]/3600)*180/12)

    def hmstorad(self):
        """HMS to Radians converting method
        This method return angle in radians from angle in hms

        Returns
        -------
        float
            The angle value in radians
        """
        return self.hmstodeg() * math.pi/180
