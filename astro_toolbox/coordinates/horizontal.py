"""This module contain Horizontal class
"""
import math
from astro_toolbox.angle.angle_hms import AngleHMS
from astro_toolbox.angle.angle_dms import AngleDMS
from astro_toolbox.angle.angle_rad import AngleRad
from astro_toolbox import coordinates
class Horizontal():
    """This class represent horizontals coordinates
    :param name: Object name
    :type name: str
    :param azimuth: Azimuth of the object a tuple (°,','')
    :type azimuth: tuple
    :param altitude: Altitude of the object a tuple (°,','')
    :type altitude: tuple
    """
    def __init__(self, altitude: tuple, azimuth: tuple, name = None):
        """Constructor method

        :param altitude: Altitude of the object a tuple (°,','')
        :type altitude: tuple
        :param azimuth: Azimuth of the object a tuple (°,','')
        :type azimuth: tuple
        :param name: Object name, defaults to None
        :type name: _type_, optional
        """
        self.name = name
        self.azimuth = AngleDMS(azimuth)
        self.altitude = AngleDMS(altitude)

    def __repr__(self):
        """Class representation method

        :return: Class representation
        :rtype: str
        """
        altstr = (f'{self.altitude.anglevalue[0]:+03d}°{self.altitude.anglevalue[1]:02d}m'+
                f'{self.altitude.anglevalue[2]:05.2f}s')
        azstr = (f'{self.azimuth.anglevalue[0]:03d}°{self.azimuth.anglevalue[1]:02d}\''+
                f'{self.azimuth.anglevalue[2]:05.2f}\'\'')
        return f'{self.name}: A = {azstr} h = {altstr}'

    def calculate_airmass(self):
        """Airmass calculation method
        The airmass is calculate with the Pickering(2002) formula from DIO,
        The International Journal of Scientific History vol. 12
        :math: \\frac{1}{sin(h+\\frac{244}{165+47h^{1.1})}

        :return: Airmass value of the object
        :rtype: float
        """
        altitude = self.altitude
        return 1/(math.sin(altitude.radtodeg() + 244/(165 + 47 * altitude.radtodeg() ** 1.1)))

    def to_equatorial(self, gamma: AngleHMS, latitude: AngleDMS):
        """Horizontal to Equation converting method

        :param gamma: Sidereal Time angle in hms
        :type gamma: AngleHMS
        :param latitude: observer's location latitude
        :type latitude: AngleDMS
        :return: Equatorial coordinates of the object
        :rtype: Equatorial
        """
        lat = latitude.dmstodeg()
        delta = AngleRad(math.asin(math.sin(lat) * math.sin(self.altitude.dmstorad() -
                math.cos(lat) * math.cos(self.altitude.dmstorad()) * self.azimuth.dmstorad())))
        alpha = AngleDMS(math.asin(-math.cos(self.altitude.dmstorad()) *
                math.cos(self.azimuth.dmstorad)) / math.cos(delta) - gamma.hmstorad())
        return coordinates.equatorial.Equatorial(alpha=AngleHMS(alpha.radtohms()),
                                                 delta=AngleDMS(delta.radtodms()))
