import math

class Angle():
    @staticmethod
    def dms2deg():
        return
    @staticmethod
    def deg2dms():
        return

class Time():
    def __init__(self, ut_time):
        self.year = ut_time[0]
        self.month = ut_time[1]
        self.day = ut_time[2]
        self.hour = ut_time[3]
        self.minute = ut_time[4]
        self.second = ut_time[5]
    def compute_ut2jd(self):
        """
        Convert a datetime object into julian float.
        Args:
            date: datetime-object of date in question

        Returns: float - Julian calculated datetime.
        Raises:
            TypeError : Incorrect parameter type
            ValueError: Date out of range of equation
        """
        julian_datetime = (367 * self.year - 
        int((7 * (self.year + int((self.month + 9) / 12.0))) / 4.0) +
        int((275 * self.month) / 9.0) + 
        self.day + 1721013.5 +
        (self.hour + self.minute / 60.0 + self.second / 3600) / 24.0 -
        0.5 * math.copysign(1, 100 * self.year + self.month - 190002.5) + 0.5)
        self.jd = julian_datetime
    def compute_ut2gmst(self):
        self.compute_ut2sidereal()
        T0 = (self.jd - 2451545.)/36525.
        
