import numpy as np

class Location():

    def __init__(self, name, latitude, longitude):
        self.name = name
        if type(latitude) is tuple:
            latitude = latitude[0]
        self.latitude = latitude
        self.longitude = longitude
        
