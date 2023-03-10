"""This module contains Ephemeris class.
"""
import math
import json
import pkg_resources

from astro_toolbox.angle.radians import AngleRad
from astro_toolbox.time.core import AstroDateTime

PATH = pkg_resources.resource_filename('astro_toolbox', 'coordinates/data/')

class Ephemeris():
    """Ephemeris class computing solar system objects positions in different referential.
    Orbital elements calculated by JPL.

    Attributes
    ----------
    name : str
        Planet name.
    n_centuries : float
        Number of centuries from J2000.
    orbital_elements : dict
        Dictionary which contains object orbital elements for current date.
    """
    def __init__(self, name: str, datetime: tuple | str):
        """Constructor method

        Parameters
        ----------
        name : str
            Planet name.
        datetime : tuple | str
            Date and time as tuple or str (``dd:dd:dd.dd`` or ``ddhddmdd.dds``).
        """
        self.name = name
        self.n_centuries = (AstroDateTime(datetime).get_jd() - 2451545)/36525
        if self.name.lower() == 'sun':
            self.orbital_elements = self._get_orbital_elements('EM Bary')
        else:
            self.orbital_elements = self._get_orbital_elements(self.name)

    def _get_orbital_elements(self, name: str):
        """Get on date orbital elements.

        Parameters
        ----------
        name : str
            Object name.

        Returns
        -------
        dict
            Dictionary which contains object orbital elements for current date.

        Raises
        ------
        ValueError
            Unknown Object.
        """
        with open(PATH  + 'orbital_elements.json', encoding="utf-8") as json_file:
            dict_orbital_elements = json.load(json_file)
        if name.lower() in [key.lower() for key in dict_orbital_elements.keys()]:
            keys = list(key for key in dict_orbital_elements)
            idx = list(key.lower() for key in dict_orbital_elements).index(name.lower())
            name = keys[idx]
            orbital_elements = dict_orbital_elements[name]
        else:
            raise ValueError ("Unknown object")
        for key, value in orbital_elements.items():
            if ',' in value:
                parsed_value = value.split(',')
                value = (float(parsed_value[0]) +
                        float(parsed_value[1]) * self.n_centuries)
                if key in ('L', 'I', 'longperi', 'longnode'):
                    value = value%360
            if key == 'a':
                value = value * 149597870.700
            orbital_elements[key] = float(value)
        orbital_elements.update({"perihelion": (orbital_elements['longperi'] -
                                    orbital_elements['longnode'])%360})
        orbital_elements.update({"M": (orbital_elements['L'] -
                                    orbital_elements['longperi'])%360})
        eccentric_anomaly = (orbital_elements['M'] -
                            (orbital_elements['e']*180/math.pi) *
                            math.sin(orbital_elements['M']*math.pi/180))
        delta_eccentric_anomaly = 1
        while abs(delta_eccentric_anomaly) > 1e-6:
            delta_mean_anomaly = (orbital_elements['M'] - (
                                eccentric_anomaly -
                                (orbital_elements['e']*180/math.pi) *
                                math.sin(eccentric_anomaly*math.pi/180)))
            delta_eccentric_anomaly = (delta_mean_anomaly / (
                                    1 - orbital_elements['e'] *
                                    math.cos(eccentric_anomaly*math.pi/180)))
            eccentric_anomaly = (eccentric_anomaly +
                                delta_eccentric_anomaly)
        orbital_elements.update({"E": eccentric_anomaly%360})
        return orbital_elements

    def compute_earth_position(self):
        """Sun position from earth.
        Distance and true anomaly are computed by _compute_true_anomaly_distance method.

        lonearth = v + w

        .. math:: xs = r * cos(lonsun)
        .. math:: ys = r * sin(lonsun)

        Returns
        -------
        tuple
            Tuple containing sun position from earth
        """
        earth_orbital_elements = self._get_orbital_elements('EM Bary')
        true_anomaly, radius = self.compute_true_anomaly_distance(**earth_orbital_elements)
        lonearth = (true_anomaly*180/math.pi + earth_orbital_elements['perihelion'])
        x_sun = -radius * math.cos(lonearth*math.pi/180)
        y_sun = -radius * math.sin(lonearth*math.pi/180)
        return x_sun, y_sun

    def compute_true_anomaly_distance(self, **orbital_elements):
        """Compute object distance and true anomaly.

        .. math:: xv = a(cos(E) - e)
        .. math:: yv = a\\sqrt{1 - e^2} * sin(E)
        .. math:: v = atan2(yv, xv)
        .. math:: r = \\sqrt{xv^2 + yv^2}

        Returns
        -------
        tuple
            Tuple which contains true anomaly and distance.
        """
        x_true_anomaly = orbital_elements['a'] * (math.cos(orbital_elements['E']*math.pi/180) -
                                                        orbital_elements['e'])
        y_true_anomaly = orbital_elements['a'] * (math.sqrt(1 - orbital_elements['e']**2) *
                                                        math.sin(orbital_elements['E']*math.pi/180))
        return (math.atan2(y_true_anomaly, x_true_anomaly),
                math.sqrt(x_true_anomaly**2 + y_true_anomaly**2))

    def compute_ecliptic_position(self, **orbital_elements):
        """Compute the heliocentric ecliptic object position.

        .. math:: xh = r*(cos(\\Omega)*cos(v+\\omega)-sin(\\Omega)*sin(v+\\omega)*cos(I))
        .. math:: yh = r*(sin(\\Omega)*cos(v+\\omega)+cos(\\Omega)*sin(v+\\omega)*cos(I))
        .. math:: zh = r*(sin(v+\\omega)*sin(I))

        Returns
        -------
        tuple
            Tuple which contains object position around the sun.
        """
        true_anomaly, radius = self.compute_true_anomaly_distance(**orbital_elements)
        true_longitude = (true_anomaly*180/math.pi + orbital_elements['perihelion'])
        x_ecliptic = radius * (math.cos(orbital_elements['longnode']*math.pi/180) *
                                    math.cos(true_longitude*math.pi/180) -
                                    math.sin(orbital_elements['longnode']*math.pi/180) *
                                    math.sin(true_longitude*math.pi/180) *
                                    math.cos(orbital_elements['I']*math.pi/180))
        y_ecliptic = radius * (math.sin(orbital_elements['longnode']*math.pi/180) *
                                    math.cos(true_longitude*math.pi/180) +
                                    math.cos(orbital_elements['longnode']*math.pi/180) *
                                    math.sin(true_longitude*math.pi/180) *
                                    math.cos(orbital_elements['I']*math.pi/180))
        z_ecliptic = radius * (math.sin(true_longitude*math.pi/180) *
                                    math.sin(orbital_elements['I']*math.pi/180))
        return x_ecliptic, y_ecliptic, z_ecliptic

    def compute_geocentric_position(self, **orbital_elements):
        """Compute geocentric object position.

        .. math:: xg = xh + xs
        .. math:: yg = yh + ys
        .. math:: zg = zh

        Where, xs and ys are the geocentric earth coordinates.

        Returns
        -------
        tuple
            Tuple which contains the geocentric position.
        """
        (x_heliocentric,
        y_heliocentric,
        z_heliocentric) = self.compute_ecliptic_position(**orbital_elements)
        x_sun, y_sun = self.compute_earth_position()
        x_geocentric = x_heliocentric + x_sun
        y_geocentric = y_heliocentric + y_sun
        z_geocentric = z_heliocentric
        return x_geocentric, y_geocentric, z_geocentric

    def compute_equatorial_position(self, **orbital_elements):
        """Compute equatorial object position.

        For the sun:

        .. math:: xe = xs
        .. math:: ye = ys * cos(ecl)
        .. math:: ze = ys * sin(ecl)

        For the moon:

        .. math:: xe = r*(cos(\\Omega)*cos(v+\\omega)-sin(\\Omega)*sin(v+\\omega)*cos(I))
        .. math:: ye = r*(sin(\\Omega)*cos(v+\\omega)+cos(\\Omega)*sin(v+\\omega)*cos(I))
        .. math:: ze = r*(sin(v+\\omega)*sin(I))

        For the planets:

        .. math:: xe = xg
        .. math:: ye = yg * cos(ecl) - zg * sin(ecl)
        .. math:: ze = yg * sin(ecl) + zg * cos(ecl)

        Returns
        -------
        tuple
            Tuple which contains the geocentric position.
        """
        ecliptic_obliquity = self.calculate_ecliptic_obliquity()*math.pi/180
        if self.name.lower() == 'sun':
            x_sun, y_sun = self.compute_earth_position()
            x_equatorial = x_sun
            y_equatorial = y_sun * math.cos(ecliptic_obliquity)
            z_equatorial = y_sun * math.sin(ecliptic_obliquity)
        else:
            if self.name.lower() == 'moon':
                (x_geocentric,
                y_geocentric,
                z_geocentric) = self.compute_ecliptic_position(**orbital_elements)
            else:
                (x_geocentric,
                y_geocentric,
                z_geocentric) = self.compute_geocentric_position(**orbital_elements)
        x_equatorial = x_geocentric
        y_equatorial = (math.cos(ecliptic_obliquity) * y_geocentric -
                        math.sin(ecliptic_obliquity) * z_geocentric)
        z_equatorial = (math.sin(ecliptic_obliquity) * y_geocentric +
                        math.cos(ecliptic_obliquity) * z_geocentric)
        return(x_equatorial, y_equatorial, z_equatorial)

    def calculate_ecliptic_obliquity(self):
        """Calculate on date ecliptic obliquity.

        Returns
        -------
        float
            Ecliptic obliquity in degrees.
        """
        return (23.439279444444445 -
                0.013010213611111111 * self.n_centuries**1 -
                5.0861111111111115e-08 * self.n_centuries**2 +
                5.565e-07 * self.n_centuries**3 -
                1.6e-10 * self.n_centuries**4 -
                1.2055555555555555e-11 * self.n_centuries**5)

    def get_equatorial_coord(self):
        """Calculate equatorial coordinates.

        .. math:: RA = atan2(ye, xe)
        .. math:: DEC = atan2(ze, \\sqrt{xe^2 + ye^2})

        Returns
        -------
        tuple
            Tuple which contains right-ascension as HMS tuple and declination as DMS tuple.
        """
        (x_equatorial,
        y_equatorial,
        z_equatorial) = self.compute_equatorial_position(**self.orbital_elements)
        right_ascencion = math.atan2(y_equatorial, x_equatorial)
        declination = math.atan2(z_equatorial, math.sqrt(x_equatorial**2 +
                                                         y_equatorial**2))
        return (AngleRad(right_ascencion).radtohms(),
                AngleRad(declination).radtodms())

    def get_magnitude(self):
        """Get solar system objects magnitude.

        Returns
        -------
        float
            Solar system object magnitude.
        """
        solar_system_objects_magnitude = {'sun': -26.83,
                                          'mercury': 0.23,
                                          'venus': -4.14,
                                          'moon': -12.90,
                                          'mars': 0.71,
                                          'jupiter': -2.20,
                                          'saturn': 0.46,
                                          'uranus': 6.03,
                                          'Neptune': 7.78}
        return solar_system_objects_magnitude[self.name.lower()]
