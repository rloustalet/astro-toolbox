from astro_toolbox.angle.angle import Angle
class AngleRad(Angle):
    def __init__(self, anglevalue: float):
        super().__init__(anglevalue, 'rad')
        self.anglevalue = anglevalue
        self.angleunit = 'rad'
    
    def __repr__(self):
        return f'{self.anglevalue}rad'
    
