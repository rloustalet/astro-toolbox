"""
This module contains AngleHMS class.
"""
import math
from astro_toolbox.utils.strparser import angle_parser
class AngleHMS():
    """AngleHMS define a HMS angle with its conversions.

    Attributes
    ----------
    anglevalue : tuple
        The angle value as floats in tuple.
    """
    def __init__(self, anglevalue: tuple | str):
        """Constructor method

        Parameters
        ----------
        anglevalue : tuple | str
            The angle value in hms as a tuple of float or a string (``ddhddmdds`` or ``dd:dd:dd``).
        """
        if isinstance(anglevalue, str):
            anglevalue = angle_parser(anglevalue)
        self.anglevalue = anglevalue

    def __repr__(self):
        """Representative method.

        Returns
        -------
        string
            Return a class representative string.
        """
        return f'{self.anglevalue[0]:02.0f}h{self.anglevalue[1]:02.0f}m{self.anglevalue[2]:05.2f}s'

    def hmstodeg(self):
        """HMS to Degrees converting method.
        This method return angle in degrees from angle in HMS.

        Returns
        -------
        float
            The angle value in degrees
        """
        return ((self.anglevalue[0] +
            self.anglevalue[1]/60 +
            self.anglevalue[2]/3600)*180/12)

    def hmstorad(self):
        """HMS to Radians converting method.
        This method return angle in radians from angle in HMS.

        Returns
        -------
        float
            The angle value in radians.
        """
        return self.hmstodeg() * math.pi/180
