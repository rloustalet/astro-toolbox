"""
This module init all the public classes.
"""
from astro_toolbox.time.core import AstroDateTime
from astro_toolbox.angle.degrees import AngleDeg
from astro_toolbox.angle.radians import AngleRad
from astro_toolbox.angle.dms import AngleDMS
from astro_toolbox.angle.hms import AngleHMS
from astro_toolbox.coordinates.equatorial import Equatorial
from astro_toolbox.coordinates.horizontal import Horizontal
from astro_toolbox.coordinates.location import Location
from astro_toolbox.coordinates.solar_system import Ephemeris
from astro_toolbox.query.ephemeris import Horizons
from astro_toolbox.query.catalogs import Simbad
from astro_toolbox.query.weather import OpenMeteo

from astro_toolbox.query.ephemeris import DICT_OBJECTS

__all__ = [
    "AstroDateTime",
    "AngleDeg",
    "AngleRad",
    "AngleDMS",
    "AngleHMS",
    "Equatorial",
    "Horizontal",
    "Location",
    "Ephemeris",
    "Simbad",
    "Horizons",
    "OpenMeteo",
]

__version__ = "0.1.2"
