"""This module contain Horizontal class
"""
import math
from astro_toolbox.angle.hms import AngleHMS
from astro_toolbox.angle.dms import AngleDMS
from astro_toolbox.angle.radians import AngleRad
from astro_toolbox.angle.degrees import AngleDeg
from astro_toolbox.coordinates.location import Location
from astro_toolbox.utils.strparser import angle_parser

class Horizontal():
    """This class represent horizontals coordinates
    """
    def __init__(self, azimuth:
                tuple | str,
                altitude: tuple | str,
                name: str = None,
                magnitude: float = None):
        """Constructor method

        Parameters
        ----------
        altitude : tuple | str
            Altitude of the object a tuple (°,','')
        azimuth : tuple | str
            Azimuth of the object a tuple (°,','')
        name : str, optional
            Object name, by default None
        """
        if isinstance(azimuth, str):
            azimuth = angle_parser(azimuth)
        if isinstance(altitude, str):
            altitude = angle_parser(altitude)
        self.name = name
        self.azimuth = AngleDMS(azimuth)
        self.altitude = AngleDMS(altitude)
        self.magnitude = magnitude

    def __repr__(self):
        """Representative method

        Returns
        -------
        string
            Return a class representative string
        """
        return f'{self.name}: A = {self.azimuth} h = {self.altitude} v = {self.magnitude}'

    def calculate_airmass(self):
        """Airmass calculation method
        The airmass is calculate with the Pickering(2002) formula from DIO,
        The International Journal of Scientific History vol. 12

        .. math:: X = \\frac{1}{sin(h+\\frac{244}{165+47h^{1.1}})}

        Returns
        -------
        float
            Object airmass
        """
        altitude = self.altitude
        if altitude < 0:
            return 40
        return abs(1/(math.sin(AngleDeg(altitude + 244/(165 + 47 * (altitude) ** 1.1)).degtorad())))

    def to_equatorial(self, gamma: tuple | str, location: Location):
        """Horizontal to Equation converting method

        .. math:: \\delta=sin^{-1}(sin \\Phi sin h-cos \\Phi cos h cos A)

        .. math:: \\alpha=sin^{-1}(\\frac{-cosh cosA}{cos\\delta})-\\gamma

        Parameters
        ----------
        gamma : AngleHMS
            Sidereal Time angle in hms
        location : Location
            observer location

        Returns
        -------
        Equatorial
            Equatorial coordinates of the object
        """
        if isinstance(gamma, str):
            gamma = angle_parser(gamma)
        gamma_angle =  AngleHMS(gamma)
        lat = location.latitude.dmstorad()
        delta = AngleRad(math.asin(math.sin(lat) *
                math.sin(self.altitude.dmstorad()) +
                math.cos(lat) *
                math.cos(self.altitude.dmstorad()) *
                math.cos(self.azimuth.dmstorad())))
        alpha = AngleRad(gamma_angle.hmstorad() - math.asin(-math.cos(self.altitude.dmstorad()) *
                math.sin(self.azimuth.dmstorad()) / math.cos(delta.anglevalue)))
        return alpha.radtohms(), delta.radtodms()
