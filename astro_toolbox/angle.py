import numpy as np
class Angle():
    def __init__(self, anglevalue, angleunit):
        self.anglevalue = anglevalue
        self.angleunit = angleunit
    def radtodeg(self):
        if self.angleunit == 'rad':
            return self.anglevalue*180/np.pi
        print(f'impossible convertion : angle is in {self.angleunit}')
        return self.anglevalue
    def degtorad(self):
        if self.angleunit == 'deg':
            return self.anglevalue*np.pi/180
        print(f'impossible convertion : angle is in {self.angleunit}')
        return self.anglevalue
    def dmstodeg(self):
        if self.angleunit == 'dms':
                
            return self.anglevalue*np.pi/180
        print(f'impossible convertion : angle is in {self.angleunit}')
        return self.anglevalue