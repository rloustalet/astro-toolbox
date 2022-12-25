"""This module contain AstroDateTime class
"""
import math
from astro_toolbox.location import Location
class AstroDateTime():
    """This module contain AngleRad class
    """
    def __init__(self, ut_time):
        """Constructor method

        Parameters
        ----------
        ut_time : tuple
            tuple of the date and time in format (year,month,day,hour,minute,second)
        """
        self.date = (ut_time[0], ut_time[1], ut_time[2])
        self.time = (ut_time[3], ut_time[4], ut_time[5])
    # ----------------------------------------------------------------------------------------------
    def __repr__(self):
        """Representative method

        Returns
        -------
        string
            Return a class representative string
        """
        return (f'{self.date[0]}-{self.date[1]}-{self.date[2]} '+
                f'{self.time[0]}:{self.time[1]}:{self.time[2]}')
    # ----------------------------------------------------------------------------------------------
    def get_date(self):
        """Get date

        Returns
        -------
        tuple
            date in format (year,month,day)
        """
        return self.date
    # ----------------------------------------------------------------------------------------------
    def get_year(self):
        """Get year

        Returns
        -------
        int
            year
        """
        return self.date[0]
    # ----------------------------------------------------------------------------------------------
    def get_month(self):
        """Get month

        Returns
        -------
        int
            month
        """
        return self.date[1]
    # ----------------------------------------------------------------------------------------------
    def get_day(self):
        """Get day

        Returns
        -------
        int
            day
        """
        return self.date[2]
    # ----------------------------------------------------------------------------------------------
    def get_time(self):
        """Get time

        Returns
        -------
        tuple
            time in format (hour,minute,second)
        """
        return self.time
    # ----------------------------------------------------------------------------------------------
    def get_jd(self):
        """UT time to Julian day float converting method
        get Julain day

        .. math:: JD=367year-\\frac{7(year+\\frac{month+9}{12}}{4}>+\\frac{275month}{9}+
                day+1721013.5+\\frac{UT}{24}-0.5sign(100year+month-190002.5)+0.5
        
        Returns
        -------
        float
            Julian day
        """
        julian_day = (367 * self.date[0] -
        int((7 * (self.date[0] +
        int((self.date[1] + 9) / 12.0))) / 4.0) +
        int((275 * self.date[1]) / 9.0) +
        self.date[2] + 1721013.5 +
        (self.time[0] + self.time[1] / 60.0 + self.time[2] / 3600) / 24.0 -
        0.5 * math.copysign(1, 100 * self.date[0] + self.date[1] - 190002.5) + 0.5)
        return julian_day
    # ----------------------------------------------------------------------------------------------
    def get_gmst(self):
        """UT time to Greenwich mean sidereal time converting method
        Get Greenwich mean sidereal time

        .. math:: gmst=mod(18.697375+24.065709824279(JD-2451545), 24)

        Returns
        -------
        tuple
            Greenwich mean sidereal time
        """
        julian_day = self.get_jd()
        gmst = (18.697375 + 24.065709824279 * (julian_day - 2451545)) % 24
        gmst_mm = (gmst - int(gmst))*60
        gmst_ss = (gmst_mm - int(gmst_mm))*60
        gmst_hh = int(gmst)
        gmst_mm = int(gmst_mm)
        return (gmst_hh,gmst_mm,gmst_ss)
    # ----------------------------------------------------------------------------------------------
    def get_lst(self, location: Location):
        """UT time to local mean sidereal time converting method
        Get local mean sidereal time

        .. math:: lst=gmst+\\frac{\\lambda}{15}

        Parameters
        ----------
        location : Location
            Observer location
        
        Returns
        -------
        tuple
            local mean sidereal time
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
    # ----------------------------------------------------------------------------------------------