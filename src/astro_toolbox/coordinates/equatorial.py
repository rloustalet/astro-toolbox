"""This module contains Equatorial class.
"""
import math

from astro_toolbox.angle.hms import AngleHMS
from astro_toolbox.angle.dms import AngleDMS
from astro_toolbox.angle.degrees import AngleDeg
from astro_toolbox.angle.radians import AngleRad
from astro_toolbox.coordinates.location import Location
from astro_toolbox.time.core import AstroDateTime

class Equatorial():
    """This class represents astronomical equatorial coordinate system.

    Attributes
    ----------
    alpha : tuple
        Object right-ascension.
    delta : tuple
        Object declination.
    name : str
        Object name.
    magnitude : float
        Object magnitude.
    """
    def __init__(self, alpha: tuple | str,
                delta: tuple | str,
                name: str = None,
                magnitude: float = None):
        """Constructor method

        Parameters
        ----------
        alpha : tuple | str
            Object right-ascension as tuple or str (``dd:dd:dd.dd`` or ``ddhddmdd.dds``).
        delta : tuple | str
            Object declination as tuple or str (``dd:dd:dd.dd`` or ``dd°dd'dd.dd"``).
        name : str, optional
            Object name, by default None.
        magnitude : float
            Object magnitude, by default is None.
        """
        self.name = name
        self.alpha = AngleHMS(alpha)
        self.delta = AngleDMS(delta)
        self.magnitude = magnitude

    def __repr__(self):
        """Representative method.

        Returns
        -------
        str
            Return a class representative string.
        """
        return (f'{self.name}: \N{GREEK SMALL LETTER ALPHA} = {self.alpha} ' +
                f'\N{GREEK SMALL LETTER DELTA} = {self.delta} '
                f'v = {self.magnitude}')

    def get_hourangle(self, gamma: tuple | str):
        """Right-Ascension to Hour-Angle converting method.

        .. math:: HA = RA - \\gamma

        Parameters
        ----------
        gamma : tuple | str
            Sidereal Time angle as tuple or string.

        Returns
        -------
        tuple
            Hour-Angle tuple as tuple.
        """
        gamma_angle = AngleHMS(gamma)
        hour_angle = AngleDeg(gamma_angle.hmstodeg() - self.alpha.hmstodeg())
        return hour_angle.degtohms()

    def calculate_airmass(self, gamma: tuple | str, location: Location):
        """Airmass calculation method.
        The airmass is calculate with the Pickering (2002) formula from DIO,
        The International Journal of Scientific History vol. 12.

        .. math:: X = \\frac{1}{sin(h+\\frac{244}{165+47h^{1.1}})}

        For altitude angle calculation c.f. to_horizontal method.

        Parameters
        ----------
        gamma : tuple | str
            Sidereal Time angle in hms.
        location : Location
            observer location.

        Returns
        -------
        float
            Airmass value of the object.
        """
        lat = location.latitude.dmstorad()
        hour_angle = AngleHMS(self.get_hourangle(gamma=gamma)).hmstorad()
        altitude = AngleRad(math.asin(math.cos(lat) * math.cos(hour_angle) *
                    math.cos(self.delta.dmstorad()) + math.sin(lat) *
                    math.sin(self.delta.dmstorad()))).radtodeg()
        if altitude < 0:
            return 40
        return 1/(math.sin(AngleDeg(altitude + 244/(165 + 47 * altitude ** 1.1)).degtorad()))

    def to_horizontal(self, gamma: tuple | str, location: Location):
        """Equatorial to Horizontal converting method.

        .. math:: h=sin^{-1}(cos\\Phi cos H cos\\delta+sin\\Phi sin\\delta)

        .. math:: A=sin^{-1}(\\frac{-sin H cos \\delta}{cosh})

        Parameters
        ----------
        gamma : tuple | str
             Sidereal Time angle as tuple or string.
        location : Location
            observer location.

        Returns
        -------
        tuple
            Tuple containing two tuple in DMS with (azimuth, altitude).
        """
        lat = location.latitude.dmstorad()
        hour_angle = AngleHMS(self.get_hourangle(gamma=gamma)).hmstorad()
        altitude = AngleRad((math.asin(math.cos(lat) * math.cos(hour_angle) *
                            math.cos(self.delta.dmstorad())
            + math.sin(lat) * math.sin(self.delta.dmstorad()))))
        azimuth = AngleRad((math.asin(-math.sin(hour_angle) *
            math.cos(self.delta.dmstorad()) / math.cos(altitude.anglevalue)))%(2*math.pi))
        return (azimuth.radtodms(), altitude.radtodms())

    def compute_on_date_coord(self, year: float):
        """On date Equatorial coordinates calculation method from J2000 Equatorial coordinate.

        .. math:: \\Delta year = \\frac{(year-2000)}{100}

        .. math:: M=1.2812323\\Delta year+0.0003879\\Delta year^2+0.0000101\\Delta year^3

        .. math:: N=0.5567530\\Delta year-0.0001185\\Delta year^2+0.0000116\\Delta year^3

        .. math:: \\Delta \\alpha=M+Nsin\\alpha tan\\delta

        .. math:: \\Delta \\delta=Ncos\\alpha

        .. math:: \\alpha=\\alpha_{J2000}+\\Delta \\alpha

        .. math:: \\delta=\\delta_{J2000}+\\Delta \\delta

        Parameters
        ----------
        year : float
            Current year (months and days can be counted as year fraction).
        """
        var_year = (year - 2000.0)/100
        m_coeff = (1.2812323 * var_year + 0.0003879 *
                var_year**2 + 0.0000101 * var_year**3) * math.pi/180
        n_coeff = (0.5567530 * var_year - 0.0001185 *
                var_year**2 + 0.0000116 * var_year**3) * math.pi/180
        var_alpha = (m_coeff + n_coeff * math.sin(self.alpha.hmstorad()) *
                    math.tan(self.delta.dmstorad()))
        var_delta = n_coeff * math.cos(self.alpha.hmstorad())
        alpha = AngleHMS(AngleRad(self.alpha.hmstorad() + var_alpha).radtohms())
        delta = AngleDMS(AngleRad(self.delta.dmstorad() + var_delta).radtodms())
        self.alpha = alpha
        self.delta = delta

    def calculate_rise_time(self, location:Location, date: tuple | str, altitude_0: float=0.0):
        """Rise time calculation method.

        Parameters
        ----------
        location : Location
            Observer location as Location class.
        date : tuple | str
            Date as tuple or str (``yyyy-mm-dd`` or ``yyyy:mm:dd``).

        Returns
        -------
        tuple
            Tuple containing the rising time in HMS.
        """
        time = AstroDateTime(date)
        hour_angle = math.acos((math.sin(altitude_0*math.pi/180) -
                    math.sin(location.latitude.dmstorad()) *
                    math.sin(self.delta.dmstorad())) /
                    (math.cos(location.latitude.dmstorad()) *
                    math.cos(self.delta.dmstorad())))*180/math.pi
        tsg0 = AngleHMS(AstroDateTime(time.date+(0 , 0, 0)).get_gmst()).hmstodeg()
        return AngleDeg((self.alpha.hmstodeg() -
                                hour_angle +
                                location.longitude.dmstodeg() -
                                tsg0) /
                                1.002737909).degtohms()

    def calculate_set_time(self, location:Location, date: tuple | str, altitude_0: float=0.0):
        """Set time calculation method.

        Parameters
        ----------
        location : Location
            Observer location as Location class.
        date : tuple | str
            Date as tuple or str (``yyyy-mm-dd`` or ``yyyy:mm:dd``).

        Returns
        -------
        tuple
            Tuple containing the setting time in HMS.
        """
        time = AstroDateTime(date)
        hour_angle = math.acos((math.sin(altitude_0*math.pi/180) -
                    math.sin(location.latitude.dmstorad()) *
                    math.sin(self.delta.dmstorad())) /
                    (math.cos(location.latitude.dmstorad()) *
                    math.cos(self.delta.dmstorad())))*180/math.pi
        tsg0 = AngleHMS(AstroDateTime(time.date+(0, 0, 0)).get_gmst()).hmstodeg()
        return AngleDeg((self.alpha.hmstodeg() +
                                hour_angle +
                                location.longitude.dmstodeg() -
                                tsg0) /
                                1.002737909).degtohms()
