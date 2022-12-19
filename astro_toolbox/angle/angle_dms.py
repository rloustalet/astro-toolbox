from astro_toolbox.angle.angle import Angle
class AngleDMS(Angle):
    def __init__(self, anglevalue: tuple):
        super().__init__(anglevalue, 'dms')
    
    def __repr__(self):
        return f'{self.anglevalue[0]:+03d}°{self.anglevalue[1]:02d}\'{self.anglevalue[2]:05.2f}\'\''

