"""
This module contains AngleRad class.
"""
import math
class AngleRad():
    """AngleRad define radians angle with its conversions.

    Attributes
    ----------
        anglevalue : float
            The angle value in radians.
    """
    def __init__(self, anglevalue: float):
        """Constructor method.

        Parameters
        ----------
        anglevalue : float
            The angle value in radians.
        """
        self.anglevalue = anglevalue

    def __repr__(self):
        """Representative method.

        Returns
        -------
        string
            Return a class representative string.
        """
        return f'{self.anglevalue}rad'

    def radtodeg(self):
        """Radians to Degrees converting method.
        This method returns angle in radians from angle in degrees.

        Returns
        -------
        float
            The angle value in degrees.
        """
        return self.anglevalue*180/math.pi

    def radtodms(self):
        """Radians to DMS converting method.
        This method returns angle in DMS from angle in radians.

        Returns
        -------
        tuple
            The angle values in DMS.
        """
        rad_dms_value = self.anglevalue*180/math.pi
        rad_dms_result = (math.copysign(int(rad_dms_value), rad_dms_value), )
        rad_dms_value = abs(rad_dms_value - int(rad_dms_value)) * 60
        rad_dms_result = rad_dms_result + (int(rad_dms_value),)
        rad_dms_value = abs(rad_dms_value - int(rad_dms_value)) * 60
        rad_dms_result = rad_dms_result + (rad_dms_value,)
        return rad_dms_result

    def radtohms(self):
        """Radians to HMS converting method.
        This method returns angle in HMS from angle in radians.

        Returns
        -------
        tuple
            The angle values in HMS.
        """
        rad_hms_value = (self.anglevalue*12/math.pi)%24
        rad_hms_result = (int(rad_hms_value),)
        rad_hms_value = (rad_hms_value - int(rad_hms_value)) * 60
        rad_hms_result = rad_hms_result + (int(rad_hms_value),)
        rad_hms_value = (rad_hms_value - int(rad_hms_value)) * 60
        rad_hms_result = rad_hms_result + (rad_hms_value,)
        return rad_hms_result
