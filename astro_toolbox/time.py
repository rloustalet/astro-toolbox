import math

class Time():
    def __init__(self, ut_time):
        self.year = ut_time[0]
        self.month = ut_time[1]
        self.day = ut_time[2]
        self.hour = ut_time[3]
        self.minute = ut_time[4]
        self.second = ut_time[5]
        self.jd = 0
        self.gmst = 0
        self.lst = 0
    def __repr__(self):
        return f'{self.year}-{self.month}-{self.day} {self. hour}:{self.minute}:{self.second}'
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
        julian_datetime = (367 * self.year -
        int((7 * (self.year + int((self.month + 9) / 12.0))) / 4.0) +
        int((275 * self.month) / 9.0) +
        self.day + 1721013.5 +
        (self.hour + self.minute / 60.0 + self.second / 3600) / 24.0 -
        0.5 * math.copysign(1, 100 * self.year + self.month - 190002.5) + 0.5)
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
        self.compute_ut2jd()
        gmst = (18.697375 + 24.065709824279 * (self.jd - 24515145)) % 24
        gmst_mm = (gmst - int(gmst))*60
        gmst_ss = (gmst_mm - int(gmst_mm))*60
        gmst_hh = int(gmst)
        gmst_mm = int(gmst_mm)
        gmst_ss = int(gmst_ss)
        self.gmst = gmst
        return f'{gmst_hh}:{gmst_mm}:{gmst_ss}'
    # ----------------------------------------------------------------------------------------------
    def compute_uttolst(self, longitude):
        longitude = longitude/15
        lst = self.gmst + longitude
        if lst < 0:
            lst = lst + 24
        lst_mm = (lst - int(lst))*60
        lst_ss = (lst_mm - int(lst_mm))*60
        lst_hh = int(lst)
        lst_mm = int(lst_mm)
        lst_ss = int(lst_ss)
        self.lst = lst
        return f'{lst_hh}:{lst_mm}:{lst_ss}'
    # ----------------------------------------------------------------------------------------------
