from pytest import approx

from astro_toolbox.angle.degrees import AngleDeg
from astro_toolbox.angle.dms import AngleDMS
from astro_toolbox.angle.hms import AngleHMS
from astro_toolbox.angle.radians import AngleRad

def test_degtorad():
    angle = AngleDeg(33)
    assert approx(angle.degtorad(), rel=1e-6) == 0.575958653

def test_degtodms():
    angle = AngleDeg(33)
    assert angle.degtodms() == (33, 0, 0)

def test_degtodms():
    angle = AngleDeg(33)
    assert angle.degtohms() == (2, 12, approx(0, rel=1e-6))

def test_radtodeg():
    angle = AngleRad(0.5759586531581288)
    assert approx(angle.radtodeg(), rel=1e-6) == 33.0

def test_radtodms():
    angle = AngleRad(0.5759586531581288)
    assert angle.radtodms() == (33, 0, 0)

def test_radtoms():
    angle = AngleRad(0.5759586531581288)
    assert angle.radtohms() == (2, 12, approx(0, rel=1e-6))

def test_dmstodeg():
    angle = AngleDMS((33, 0, 0))
    assert approx(angle.dmstodeg(), rel=1e-6) == 33.0

def test_dmstorad():
    angle = AngleDMS((33, 0, 0))
    assert approx(angle.dmstorad(), rel=1e-6) == 0.575958653

def test_hmstodeg():
    angle = AngleHMS((2, 12, 0))
    assert approx(angle.hmstodeg(), rel=1e-6) == 33.0

