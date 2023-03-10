"""
This module contains AngleDMS class.
"""
import math
from astro_toolbox.utils.strparser import angle_parser
class AngleDMS():
    """AngleDMS define a dms angle with its conversions.

    Attributes
    ----------
    anglevalue : tuple
        The angle values as floats in tuple.
    """
    def __init__(self, anglevalue: tuple | str):
        """Constructor method

        Parameters
        ----------
        anglevalue : tuple | str
            The angle value in dms as a tuple of float or a string (`dd°dd'dd"` or `dd:dd:dd`).
        """
        if isinstance(anglevalue, str):
            anglevalue = angle_parser(anglevalue)
        self.anglevalue = anglevalue

    def __repr__(self):
        """Representative method.

        Returns
        -------
        str | None
            Return a class representative string.
        """
        return (f'{self.anglevalue[0]:+03.0f}°'+
                f'{self.anglevalue[1]:02.0f}\''+
                f'{self.anglevalue[2]:05.2f}\"')

    def dmstodeg(self):
        """DMS to degrees converting method.
        This method return angle in degrees from angle in DMS.

        Returns
        -------
        float
            The angle value in degrees.
        """
        return math.copysign(abs(self.anglevalue[0]) +
                self.anglevalue[1]/60 +
                self.anglevalue[2]/3600, self.anglevalue[0])

    def dmstorad(self):
        """DMS to Radians converting method.
        This method return angle in radians from angle in DMS.

        Returns
        -------
        float
            The angle value in radians.
        """
        return self.dmstodeg()*math.pi/180
