"""This module contain Location class
"""
from astro_toolbox.angle.dms import AngleDMS
class Location():
    """This class represent the observer location
    :param name: Location name
    :type name: str
    :param latitude: Location latitude tuple (°, ', '')
    :type name: tuple
    :param longitude: Location longitude tuple (°, ', '')
    :type name: tuple
    :param altitude: Location altitude(m)
    :type name: float
    """
    def __init__(self, name: str, latitude: tuple, longitude: tuple, altitude: float = 0.0):
        """Constructor method

        Parameters
        ----------
        name : str
            Location name
        latitude : tuple
            Location latitude tuple (°, ', '')
        longitude : tuple
            Location longitude tuple (°, ', '')
        altitude : float, optional
            Loaction altitude(m), by default 0.0
        """
        self.name = name
        self.latitude = AngleDMS(latitude)
        self.longitude = AngleDMS(longitude)
        self.altitude = altitude
    # ----------------------------------------------------------------------------------------------
    def __repr__(self):
        """Representative method

        Returns
        -------
        string
            Return a class representative string
        """
        return (f'{self.name}: latitude: {self.latitude} '+
                f'longitude: {self.longitude} '+
                f'altitude = {self.altitude}m')
    # ----------------------------------------------------------------------------------------------
