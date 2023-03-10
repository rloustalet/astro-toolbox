"""
This module contains AngleDeg class.
"""
import math
class AngleDeg():
    """AngleDeg define degrees angle with its conversions.

    Attributes
    ----------
    anglevalue: float
        The angle value in degrees.
    """
    def __init__(self, anglevalue: float):
        """Constructor method

        Parameters
        ----------
        anglevalue : float
            The angle value in degrees.
        """
        self.anglevalue = anglevalue

    def __repr__(self):
        """Representative method.

        Returns
        -------
        string
            Return a class representative string.
        """
        return f'{self.anglevalue}°'

    def degtorad(self):
        """Degrees to radians converting method.
        This method returns angle in radians from angle in degrees.

        Returns
        -------
        float
            The angle value in radians.
        """
        return self.anglevalue*math.pi/180

    def degtodms(self):
        """Degrees to DMS converting method.
        This method returns angle in DMS from angle in degrees.

        Returns
        -------
        tuple
            The angle values in DMS.
        """
        deg_dms_result = (math.copysign(int(self.anglevalue), self.anglevalue),)
        deg_dms_value = abs(self.anglevalue - int(self.anglevalue)) * 60
        deg_dms_result = deg_dms_result + (int(deg_dms_value),)
        deg_dms_value = abs(deg_dms_value - int(deg_dms_value)) * 60
        deg_dms_result = deg_dms_result + (deg_dms_value,)
        return deg_dms_result

    def degtohms(self):
        """Degrees to HMS converting method.
        This method returns angle in HMS from angle in degrees.

        Returns
        -------
        tuple
            The angle values in HMS.
        """
        deg_hms_value = (self.anglevalue*12/180)%24
        deg_hms_result = (int(deg_hms_value),)
        deg_hms_value = (deg_hms_value - int(deg_hms_value)) * 60
        deg_hms_result = deg_hms_result + (int(deg_hms_value),)
        deg_hms_value = (deg_hms_value - int(deg_hms_value)) * 60
        deg_hms_result = deg_hms_result + (deg_hms_value,)
        return deg_hms_result
