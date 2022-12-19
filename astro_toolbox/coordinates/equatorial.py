"""This module contain Equatorial class
"""
import math
from astro_toolbox.angle.angle_hms import AngleHMS
from astro_toolbox.angle.angle_dms import AngleDMS
from astro_toolbox.angle.angle_deg import AngleDeg
from astro_toolbox.angle.angle_rad import AngleRad
from astro_toolbox import coordinates
class Equatorial():
    """
    This class represent astronomical equatorials coodinates
    :param name: Object name
    :type name: str
    :param alpha: Right Ascencion of the object a tuple (h,m,s)
    :type alpha: tuple
    :param delta: Declination of the object a tuple (°,','')
    :type delta: tuple
    """
    def __init__(self, alpha: tuple, delta: tuple, name: str = None):
        """Constructor method

        :param alpha: Right-Ascencion of the object
        :type alpha: tuple
        :param delta: Declination of the object
        :type delta: tuple
        :param name: _description_, defaults to None
        :type name: str, optional
        """
        self.name = name
        self.alpha = AngleHMS(alpha)
        self.delta = AngleDMS(delta)

    def __repr__(self):
        """Representative method

        :return: Equatorial class representation
        :rtype: str
        """
        return (f'{self.name}: \N{GREEK SMALL LETTER ALPHA} = {self.alpha}' +
                f'\N{GREEK SMALL LETTER DELTA} = {self.delta}')

    def get_hourangle(self, gamma: AngleHMS):
        """Riht-Ascencion to Hour-Angle conversion method
        :math: HA = RA - \\gamma

        :param gamma: Sidereal Time angle in hms
        :type gamma: AngleHMS
        :return: Hour-Angle object at needed time
        :rtype: AngleHMS
        """
        hour_angle = AngleDeg(gamma.hmstodeg() - self.alpha.hmstodeg())
        return AngleHMS(hour_angle.degtohms())

    def calculate_airmass(self, gamma: AngleHMS, latitude: AngleDMS):
        """Airmass calculation method
        The airmass is calculate with the Pickering(2002) formula from DIO,
        The International Journal of Scientific History vol. 12
        :math: \\frac{1}{sin(h+\\frac{244}{165+47h^{1.1})}
        :param gamma: Sidereal Time angle in hms
        :type gamma: AngleHMS
        :param latitude: observer's location latitude
        :type latitude: AngleDMS
        :return: Airmass value of the object
        :rtype: float
        """

        lat = latitude.dmstorad()
        hour_angle = self.get_hourangle(gamma=gamma).hmstorad()
        altitude = AngleRad(math.asin(math.cos(lat) * math.cos(hour_angle) *
                    math.cos(self.delta.dmstorad()) + math.sin(lat) *
                    math.sin(self.delta.dmstorad()))).radtodeg()
        return 1/(math.sin(AngleDeg(altitude + 244/(165 + 47 * (altitude) ** 1.1)).degtorad()))

    def to_horizontal(self, gamma: AngleHMS, latitude: AngleDMS):
        """Equatorial to Horizontal converting method

        :param gamma: Sidereal Time angle in hms
        :type gamma: AngleHMS
        :param latitude: observer's location latitude
        :type latitude: AngleDMS
        :return: Horizontal coordinates of the object
        :rtype: Horizontal
        """
        if latitude.angleunit == 'dms':
            lat = latitude.dmstorad()
        elif latitude.angleunit == 'deg':
            lat = latitude.degtorad()
        hour_angle = self.get_hourangle(gamma=gamma).hmstorad()
        altitude = AngleRad(math.asin(math.cos(lat) * math.cos(hour_angle) *
                            math.cos(self.delta.dmstorad())
            + math.sin(lat) * math.sin(self.delta.dmstorad())))
        azimuth = AngleRad(math.asin(-math.sin(hour_angle) *
            math.cos(self.delta.dmstorad)) / math.cos(altitude.get_angle()))
        return coordinates.horizontal.Horizontal(altitude=AngleDMS(altitude.radtodms()),
                                                azimuth=AngleDMS(azimuth.radtodms()))

    def compute_on_date_coords(self, year: float):
        """On date Equatorial coordinates calculation method from j2000 Equatorial coordinates

        :param year: the cuurent year (months and days can be counted as year fraction)
        :type year: float
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
