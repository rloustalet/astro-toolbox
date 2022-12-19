from astro_toolbox.angle.angle import Angle
class AngleDeg(Angle):
    def __init__(self, anglevalue: float):
        super().__init__(anglevalue, 'deg')
    
    def __repr__(self):
        return f'{self.anglevalue}°'


