import math
from astro_toolbox.angle.angle import Angle
class AstroDateTime():
    def __init__(self, ut_time):
        self.date = (ut_time[0], ut_time[1], ut_time[2])
        self.time = (ut_time[3], ut_time[4], ut_time[5])
        self.jd = 0
        self.gmst = 0
        self.lst = 0
    def __repr__(self):
        return f'{self.year}-{self.month}-{self.day} {self. hour}:{self.minute}:{self.second}'
    def get_date(self):
        return self.date
    def get_year(self):
        return self.date[0]
    def get_month(self):
        return self.date[1]
    def get_day(self):
        return self.date[2]
    def get_time(self):
        return self.time
    def compute_uttojd(self):
        """
        Convert a datetime object into julian float.
        Args:
            date: datetime-object of date in question

        Returns: float - Julian calculated datetime.
        Raises:
            TypeError : Incorrect parameter type
            ValueError: Date out of range of equation
        """
        julian_datetime = (367 * self.date[0] -
        int((7 * (self.date[0] + 
        int((self.date[1] + 9) / 12.0))) / 4.0) +
        int((275 * self.date[1]) / 9.0) +
        self.date[2] + 1721013.5 +
        (self.time[0] + self.time[1] / 60.0 + self.time[2] / 3600) / 24.0 -
        0.5 * math.copysign(1, 100 * self.date[0] + self.date[1] - 190002.5) + 0.5)
        self.jd = julian_datetime
    # ----------------------------------------------------------------------------------------------
    def compute_uttogmst(self):
        """
        Get Greenwich mean sidereal time
        Args:
            date: datetime-object of date in question

        Returns: float - Julian calculated datetime.
        Raises:
            TypeError : Incorrect parameter type
            ValueError: Date out of range of equation
        """
        self.compute_uttojd()
        gmst = (18.697375 + 24.065709824279 * (self.jd - 2451545)) % 24
        gmst_mm = (gmst - int(gmst))*60
        gmst_ss = (gmst_mm - int(gmst_mm))*60
        gmst_hh = int(gmst)
        gmst_mm = int(gmst_mm)
        gmst_ss = gmst_ss
        self.gmst = gmst
        return (gmst_hh,gmst_mm,gmst_ss)
    # ----------------------------------------------------------------------------------------------
    def compute_uttolst(self, longitude: Angle):
        self.compute_uttogmst()
        longitude = longitude.dmstodeg()/15
        lst = self.gmst + longitude
        if lst < 0:
            lst = lst + 24
        lst_mm = (lst - int(lst))*60
        lst_ss = (lst_mm - int(lst_mm))*60
        lst_hh = int(lst)
        lst_mm = int(lst_mm)
        lst_ss = lst_ss
        self.lst = lst
        return (lst_hh,lst_mm,lst_ss)
    # ----------------------------------------------------------------------------------------------
