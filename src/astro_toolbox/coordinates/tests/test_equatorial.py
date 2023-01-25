"""Calculate for 2023-01-15 at 00h00m00s TU @Greenwich
"""
from pytest import approx

from astro_toolbox.coordinates.equatorial import Equatorial
from astro_toolbox.coordinates.horizontal import Horizontal
from astro_toolbox.time.core import AstroDateTime
from astro_toolbox.angle.hms import AngleHMS
from astro_toolbox.coordinates.location import Location

capella = Equatorial(name='Capella',alpha=(5, 16, 43.32), delta=(+45,59,48.3))
ut_time = AstroDateTime((2023, 1, 15, 0, 0, 0))
location = Location(name = 'Greenwich')
gamma = ut_time.get_lst(location)

def test_hour_angle():
    assert approx(AngleHMS(capella.get_hourangle(gamma)).hmstodeg(), rel=1e-6) == 35.01141593

def test_calculate_airmaass():
    assert approx(capella.calculate_airmass(gamma, location), rel=1e-2) == 1.09

def test_to_horizontal():
    assert capella.to_horizontal(gamma, location) == ((270, 24, approx(27.69, rel=1e-2)),
                                                    (+66, 30, approx(36.55, rel=1e-2)))

def test_compute_on_date_coord():
    capella.compute_on_date_coord(2023)
    assert (capella.alpha.anglevalue, capella.delta.anglevalue) == ((5, 18, approx(25.30, rel=1e-2)), (+46, 1, approx(14.83, rel=1e-2)))

sirius = Equatorial(name='Sirius', alpha=(6, 46, 10.54), delta=(-16, 44, 55.8))

def test_calculate_rise_time():
    assert sirius.calculate_rise_time(location, ut_time) == (18, 39, approx(8.87, rel=1e-2))

def test_calculate_set_time():
    assert sirius.calculate_set_time(location, ut_time) == (3, 39, approx(58.14, rel=1e-2))

capella_horiz = Horizontal(name='Capella', azimuth=(270, 24, 27.69), altitude=(+66, 30, 36.55))

def test_to_equatorial():
    assert capella_horiz.to_equatorial(gamma, location) == ((5, 16, approx(43.32, rel=1e-2)), (+45, 59, approx(48.3, rel=1e-2)))
