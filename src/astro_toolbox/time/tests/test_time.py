"""All calculations are performed for 2023-01-15 @ Greenwich
"""
from pytest import approx

from astro_toolbox.time.core import  AstroDateTime
from astro_toolbox.coordinates.location import Location

location = Location(name='Greenwich')
ut_time = AstroDateTime((2023, 1, 15, 0, 0, 0))

def test_get_jd():
    assert  ut_time.get_jd() == 2459959.500000

def test_get_gmst():
    assert ut_time.get_gmst() == (7, 36, approx(45.9, rel=1e-2))

def test_get_lst():
    assert ut_time.get_lst(location) == (7, 36, approx(45.32, rel=1e-2))

def test_get_year_day():
    assert ut_time.get_year_day() == 15