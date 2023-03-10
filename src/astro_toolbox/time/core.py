"""This module contains AstroDateTime class.
"""
import math
import datetime
from astro_toolbox.coordinates.location import Location
from astro_toolbox.utils.strparser import angle_parser
class AstroDateTime():
    """This module contains AngleRad class

    Attributes
    ----------
    ut_time : tuple | str
        Date and time as tuple or string in format (2000/01/01/12:00:00)
    """
    def __init__(self, ut_time: tuple | str = None):
        """Constructor method

        Parameters
        ----------
        ut_time : tuple
            Tuple of the date and time in format (year,month,day,hour,minute,second)
        """
        if ut_time is None:
            ut_time = datetime.datetime.now(datetime.timezone.utc).timetuple()
        elif isinstance(ut_time, str):
            ut_time = angle_parser(ut_time)
        if ut_time is not None and len(ut_time) == 3:
            ut_time += (12, 0, 0)
        self.date = (ut_time[0], ut_time[1], ut_time[2])
        self.time = (ut_time[3], ut_time[4], ut_time[5])

    def __repr__(self):
        """Representative method.

        Returns
        -------
        string
            Return a class representative string.
        """
        return (f'{self.date[0]:02d}-{self.date[1]:02d}-{self.date[2]:02d} '+
                f'{self.time[0]:02d}:{self.time[1]:02d}:{self.time[2]:02d}')

    def get_year(self):
        """Get year

        Returns
        -------
        int
            Year.
        """
        return self.date[0]

    def get_month(self):
        """Get month

        Returns
        -------
        int
            Month.
        """
        return self.date[1]

    def get_day(self):
        """Get day.

        Returns
        -------
        int
            Day.
        """
        return self.date[2]

    def get_time(self):
        """Get time.

        Returns
        -------
        tuple
            Time in format (hour,minute,second).
        """
        return self.time

    def get_jd(self):
        """Get julian day with USNO formula.

        .. math:: JD=367year-\\frac{7(year+\\frac{month+9}{12})}{4}>+\\frac{275month}{9}+
                day+1721013.5+\\frac{UT}{24}-\n
        .. math:: 0.5sign(100year+month-190002.5)+0.5

        Returns
        -------
        float
            Julian day.
        """
        julian_day = (367 * self.date[0] -
        int((7 * (self.date[0] +
        int((self.date[1] + 9) / 12.0))) / 4.0) +
        int((275 * self.date[1]) / 9.0) +
        self.date[2] + 1721013.5 +
        (self.time[0] + self.time[1] / 60.0 + self.time[2] / 3600) / 24.0 -
        0.5 * math.copysign(1, 100 * self.date[0] + self.date[1] - 190002.5) + 0.5)
        return julian_day

    def get_year_day(self):
        """Get day of year.

        .. math:: N1 = floor(275 * month / 9)
        .. math:: N2 = floor((month + 9) / 12)
        .. math:: N3 = (1 + floor((year - 4 * floor(year / 4) + 2) / 3))
        .. math:: N = N1 - (N2 * N3) + day - 30

        Returns
        -------
        int
            Day of year.
        """
        n_1 = math.floor(275 * self.get_month() / 9)
        n_2 = math.floor((self.get_month() + 9) / 12)
        n_3 = 1 + math.floor((self.get_year() - 4 * math.floor(self.get_year() / 4) + 2) / 3)
        return n_1 - (n_2 * n_3) + self.get_day() - 30

    def get_gmst(self):
        """Get Greenwich mean sidereal time with USNO formula.

        .. math:: gmst=mod(18.697375+24.065709824279(JD-2451545), 24)

        Returns
        -------
        tuple
            Greenwich mean sidereal time.
        """
        julian_day = self.get_jd()
        gmst = (18.697375 + 24.065709824279 * (julian_day - 2451545)) % 24
        gmst_mm = (gmst - int(gmst))*60
        gmst_ss = (gmst_mm - int(gmst_mm))*60
        gmst_hh = int(gmst)
        gmst_mm = int(gmst_mm)
        return (gmst_hh,gmst_mm,gmst_ss)

    def get_lst(self, location: Location):
        """Get local mean sidereal time with USNO formula.

        .. math:: lst=gmst+\\frac{\\lambda}{15}

        Parameters
        ----------
        location : Location
            Observer location.

        Returns
        -------
        tuple
            Local mean sidereal time.
        """
        gmst = self.get_gmst()
        longitude = location.longitude.dmstodeg()/15
        lst = (gmst[0]+gmst[1]/60+gmst[2]/3600) + longitude
        if lst < 0:
            lst = lst + 24
        lst_mm = (lst - int(lst))*60
        lst_ss = (lst_mm - int(lst_mm))*60
        lst_hh = int(lst)
        lst_mm = int(lst_mm)
        return (lst_hh,lst_mm,lst_ss)
