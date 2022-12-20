"""
This module contain AngleDeg class
"""
import math
class AngleDeg():
    """AngleDeg define a Degrees angle with his conversions
    """
    def __init__(self, anglevalue: float):
        """Constructor method

        Parameters
        ----------
        anglevalue : float
            The angle value in degrees
        """
        self.anglevalue = anglevalue
    # ----------------------------------------------------------------------------------------------
    def __repr__(self):
        """Representative method

        Returns
        -------
        string
            Return a class representative string
        """
        return f'{self.anglevalue}°'
    # ----------------------------------------------------------------------------------------------
    def degtorad(self):
        """Degrees to Radians converting method
        This method return angle in degrees from angle in radians

        Returns
        -------
        float
            The angle value in radians
        """
        return self.anglevalue*math.pi/180
    # ----------------------------------------------------------------------------------------------
    def degtodms(self):
        """Degrees to DMS converting method
        This method return angle in dms from angle in degrees

        Returns
        -------
        tuple
            The angle values in dms
        """
        deg_dms_result = (int(self.anglevalue),)
        deg_dms_value = (self.anglevalue - int(self.anglevalue)) * 60
        deg_dms_result = deg_dms_result + (int(deg_dms_value),)
        deg_dms_value = (deg_dms_value - int(deg_dms_value)) * 60
        deg_dms_result = deg_dms_result + (deg_dms_value,)
        return deg_dms_result
    # ----------------------------------------------------------------------------------------------
    def degtohms(self):
        """Degrees to HMS converting method
        This method return angle in hms from angle in degrees

        Returns
        -------
        tuple
            The angle values in hms
        """
        deg_hms_value = self.anglevalue*12/180
        deg_hms_result = (int(deg_hms_value),)
        deg_hms_value = (deg_hms_value - int(deg_hms_value)) * 60
        deg_hms_result = deg_hms_result + (int(deg_hms_value),)
        deg_hms_value = (deg_hms_value - int(deg_hms_value)) * 60
        deg_hms_result = deg_hms_result + (deg_hms_value,)
        return deg_hms_result
