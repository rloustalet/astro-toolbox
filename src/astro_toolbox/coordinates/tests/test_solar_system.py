from pytest import approx

from astro_toolbox.coordinates.solar_system import Ephemeris
from astro_toolbox.time.core import AstroDateTime

saturn = Ephemeris('Saturn', (2023, 1, 15, 0, 0, 0))

def test_get_equatorial_coord():
    assert saturn.get_equatorial_coord() == ((21, 45, approx(33.51, rel=1e-2)), (-14, 48, approx(38.49, rel=1e-2)))

def test_get_magnitude():
    assert saturn.get_magnitude() == 0.46
