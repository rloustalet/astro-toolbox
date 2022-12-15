import math
class Angle():
    def __init__(self, anglevalue: float | tuple, angleunit: str):
        self.anglevalue = anglevalue
        self.angleunit = angleunit
    
    def __repr__(self):
        if self.angleunit == 'deg':
            return f'{self.anglevalue}°'
        elif self.angleunit == 'rad':
            return f'{self.anglevalue}rad'
        elif self.angleunit == 'dms':
            return f'{self.anglevalue[0]:+03d}°{self.anglevalue[1]:02d}\'{self.anglevalue[2]:05.2f}\'\''
        elif self.angleunit == 'hms':
            return f'{self.anglevalue[0]:02d}h{self.anglevalue[1]:02d}m{self.anglevalue[2]:05.2f}s'
    
    def radtodeg(self):
        if self.angleunit == 'rad':
            return self.anglevalue*180/math.pi
        print(f'impossible convertion : angle is in {self.angleunit}')
        return self.anglevalue
    
    def degtorad(self):
        if self.angleunit == 'deg':
            return self.anglevalue*math.pi/180
        print(f'impossible convertion : angle is in {self.angleunit}')
        return self.anglevalue
    
    def dmstodeg(self):
        if self.angleunit == 'dms':
            return (self.anglevalue[0] +
                self.anglevalue[1]/60 +
                self.anglevalue[2]/3600)
        print(f'impossible convertion : angle is in {self.angleunit}')
        return self.anglevalue
    
    def dmstorad(self):
        if self.angleunit == 'dms':
            return self.dmstodeg()*math.pi/180
        print(f'impossible convertion : angle is in {self.angleunit}')
        return self.anglevalue
    
    def degtodms(self):
        if self.angleunit == 'deg':
            result = (int(self.anglevalue),)
            value = (self.anglevalue - int(self.anglevalue)) * 60
            result = result + (int(value),)
            value = (value - int(value)) * 60
            result = result + (value,)
            return result
        print(f'impossible convertion : angle is in {self.angleunit}')
        return self.anglevalue
    
    def radtodms(self):
        if self.angleunit == 'rad':
            value = self.radtodeg()
            result = (int(value),)
            value = (value - int(value)) * 60
            result = result + (int(value),)
            value = (value - int(value)) * 60
            result = result + (value,)
            return result
        print(f'impossible convertion : angle is in {self.angleunit}')
        return self.anglevalue
    
    def hmstodeg(self):
        if self.angleunit == 'hms':
            return ((self.anglevalue[0] +
                self.anglevalue[1]/60 +
                self.anglevalue/3600)*180/12)
        print(f'impossible convertion : angle is in {self.angleunit}')
        return self.anglevalue
    
    def degtohms(self):
        if self.angleunit == 'deg':
            value = self.anglevalue*12/180
            result = (int(value),)
            value = (value - int(value)) * 60
            result = result + (int(value),)
            value = (value - int(value)) * 60
            result = result + (value,)
            return result
        print(f'impossible convertion : angle is in {self.angleunit}')
        return self.anglevalue
    
    def radtohms(self):
        if self.angleunit == 'rad':
            value = self.radtodeg()*12/180
            result = (int(value),)
            value = (value - int(value)) * 60
            result = result + (int(value),)
            value = (value - int(value)) * 60
            result = result + (value,)
            return result
        print(f'impossible convertion : angle is in {self.angleunit}')
        return self.anglevalue

class AngleDeg(Angle):
    def __init__(self, anglevalue: float):
        self.anglevalue = anglevalue
        self.angleunit = 'deg'
    
    def __repr__(self):
        return f'{self.anglevalue}°'

class AngleRad(Angle):
    def __init__(self, anglevalue: float):
        self.anglevalue = anglevalue
        self.angleunit = 'rad'
    
    def __repr__(self):
        return f'{self.anglevalue}rad'
    
class AngleDMS(Angle):
    def __init__(self, anglevalue: tuple):
        self.anglevalue = anglevalue
        self.angleunit = 'dms'
    def __repr__(self):
        return f'{self.anglevalue[0]:+03d}°{self.anglevalue[1]:02d}\'{self.anglevalue[2]:05.2f}\'\''

class AngleHMS(Angle):
    def __init__(self, anglevalue: tuple):
        self.anglevalue = anglevalue
        self.angleunit = 'hms'
    def __repr__(self):
        return f'{self.anglevalue[0]:02d}h{self.anglevalue[1]:02d}m{self.anglevalue[2]:05.2f}s'
