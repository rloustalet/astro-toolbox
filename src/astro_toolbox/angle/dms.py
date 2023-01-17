"""
This module contain AngleDMS class
"""
import math
class AngleDMS():
    """AngleDMS define a dms angle with his conversions
    """
    def __init__(self, anglevalue: tuple):
        """Constructor method

        Parameters
        ----------
        anglevalue : tuple
            The angle value in dms
        """
        self.anglevalue = anglevalue

    def __repr__(self):
        """Representative method

        Returns
        -------
        str | None
            Return a class representative string
        """
        return f'{self.anglevalue[0]:+03d}°{self.anglevalue[1]:02d}\'{self.anglevalue[2]:05.2f}\"'

    def dmstodeg(self):
        """DMS to Degrees converting method
        This method return angle in degrees from angle in dms

        Returns
        -------
        float
            The angle value in degrees
        """
        return math.copysign(abs(self.anglevalue[0]) +
                self.anglevalue[1]/60 +
                self.anglevalue[2]/3600, self.anglevalue[0])

    def dmstorad(self):
        """DMS to Radians converting method
        This method return angle in radians from angle in dms

        Returns
        -------
        float
            The angle value in radians
        """
        return self.dmstodeg()*math.pi/180

    def get_angle(self):
        """Angle value returning method

        Returns
        -------
        float | tuple
            The angle value in dms
        """
        return self.anglevalue
