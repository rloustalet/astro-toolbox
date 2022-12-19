from astro_toolbox.angle.angle import Angle
class AngleHMS(Angle):
    def __init__(self, anglevalue: tuple):
        super().__init__(anglevalue, 'hms')

    def __repr__(self):
        return f'{self.anglevalue[0]:02d}h{self.anglevalue[1]:02d}m{self.anglevalue[2]:05.2f}s'