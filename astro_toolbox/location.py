from astro_toolbox import Angle
class Location():

    def __init__(self, name, latitude, longitude, altitude):
        self.name = name
        self.latitude = Angle(latitude, 'dms')
        self.longitude = Angle(longitude, 'dms')
        self.altitude = altitude