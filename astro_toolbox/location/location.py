"""This module contain Location class
"""
from astro_toolbox.angle.angle import Angle
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
        :param name: Location name
        :type name: str
        :param latitude: Location latitude tuple (°, ', '')
        :type name: tuple
        :param longitude: Location longitude tuple (°, ', '')
        :type name: tuple
        :param altitude: Loaction altitude(m), defaults to 0.0
        :type altitude: float, optional
        """
        self.name = name
        self.latitude = Angle(latitude, 'dms')
        self.longitude = Angle(longitude, 'dms')
        self.altitude = altitude

    def __repr__(self):
        """Representative method

        :return: Location class representation
        :rtype: str
        """
        return (f'{self.name}: latitude = {self.latitude} longitude = {self.longitude} '+
                f'altitude = {self.altitude}m')
