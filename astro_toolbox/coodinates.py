import math
from astro_toolbox.angle import Angle
class Equatorial():
    def __init__(self, alpha, delta):
        self.alpha = Angle(alpha, 'hms')
        self.delta = Angle(delta, 'dms')
    
    def __repr__(self):
        return (f'\N{GREEK SMALL LETTER ALPHA} = {self.alpha} \N{GREEK SMALL LETTER DELTA} = {self.delta}')
    
    def get_hourangle(self, gamma):
        HA = Angle(gamma.hmstodeg - self.alpha.hmstodeg, 'deg')
        return Angle(HA.degtohms(), 'hms')
    
    def gat_airmass(self, gamma, latitude):
        '''Pickering Air Mass
        '''
        if latitude.angleunit == 'dms':
            lat = latitude.dmstorad()
        elif latitude.angleunit == 'deg':
            lat = latitude.degtorad()
        HA = self.get_hourangle(gamma=gamma).hmstorad()
        alt = Angle(math.asin(math.cos(lat) * math.cos(HA) * math.cos(self.delta.dmstorad())
            + math.sin(lat) * math.sin(self.delta.dmstorad())), 'rad')
        return 1/(math.sin(alt.radtodeg() + 244/(165 + 47 * alt.radtodeg() ** 1.1)))
    
    def to_horizontal(self, latitude, gamma):
        if latitude.angleunit == 'dms':
            lat = latitude.dmstorad()
        elif latitude.angleunit == 'deg':
            lat = latitude.degtorad()
        HA = self.get_hourangle(gamma=gamma).hmstorad()
        alt = Angle(math.asin(math.cos(lat) * math.cos(HA) * math.cos(self.delta.dmstorad())
            + math.sin(lat) * math.sin(self.delta.dmstorad())), 'rad')
        az = Angle(math.asin(-math.sin(HA) * math.cos(self.delta.dmstorad)) / math.cos(alt), 'rad')
        return Horizontal(alt=Angle(alt.radtodms(), 'dms'), az=Angle(az.radtodms(), 'dms'))
    
class Horizontal():
    def __init__(self, alt, az):
        self.azimuth = Angle(az, 'dms')
        self.altitude = Angle(alt, 'dms')
    
    def __repr__(self):
        altstr = f'{self.altitude.anglevalue[0]:+03d}°{self.altitude.anglevalue[1]:02d}m{self.altitude.anglevalue[2]:05.2f}s'
        azstr = f'{self.azimuth.anglevalue[0]:03d}°{self.azimuth.anglevalue[1]:02d}\'{self.azimuth.anglevalue[2]:05.2f}\'\''
        return (f'A = {azstr} h = {altstr}')
    
    def get_airmass(self):
        alt = self.altitude
        return 1/(math.sin(alt.radtodeg() + 244/(165 + 47 * alt.radtodeg() ** 1.1)))
    
    def to_equatorial(self, latitude, gamma):
        if latitude.angleunit == 'dms':
            lat = latitude.dmstodeg()
        elif latitude.angleunit == 'deg':
            lat = latitude.degtorad()
        delta = Angle(math.asin(math.sin(lat) * math.sin(self.altitude.dmstorad() -
                math.cos(lat) * math.cos(self.altitude.dmstorad()) * self.azimuth.dmstorad())), 'rad')
        alpha = Angle(math.asin(-math.cos(self.altitude.dmstorad()) * math.cos(self.azimuth.dmstorad)) / math.cos(delta) -
                gamma.hmstorad(), 'rad')
        return Equatorial(alpha=Angle(alpha.radtohms(), 'hms'), delta=Angle(delta.radtodms(), 'dms'))
