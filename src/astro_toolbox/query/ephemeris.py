"""This module contains Horizon class
"""
import re
import json
import urllib.request as urllib

from astro_toolbox.time.core import AstroDateTime
from astro_toolbox.coordinates.location import Location

DICT_OBJECTS = {
                'Sun': 10,
                'Mercury': 199,
                'Venus': 299,
                'Moon': 301,
                'Mars': 499,
                'Jupiter': 599,
                'Saturn': 699,
                'Uranus': 799,
                'Neptune': 899,
                'Pluto': 999
                }

class Horizons():
    """JPL Horizons ephemeris request and parsing
    """
    def __init__(self, object_name: str | int, time: AstroDateTime, location: Location):
        """Constructor method

        Parameters
        ----------
        object_name : str | int
            The object name or integer reference according to JPL Horizons
        time : AstroDateTime
            Date and time as AstroDateTime class
        location : Location
            Observer location as Location class
        """
        self.name = object_name
        self.time = time
        self.location = location
        self.object_data = self._get_data()

    def _get_data(self):
        """JPL data query method

        Returns
        -------
        list
            A list containing the request result

        Raises
        ------
        ValueError
            Unknown object
        """
        if isinstance(self.name, int):
            object_ref = self.name
        if self.name.lower() in [key.lower() for key in DICT_OBJECTS]:
            keys = list(key for key in DICT_OBJECTS)
            idx = list(key.lower() for key in DICT_OBJECTS).index(self.name.lower())
            object_ref = DICT_OBJECTS[keys[idx]]
        else:
            raise ValueError ("Object doesn't exist verify value")
        dict_parameters = {'COMMAND': object_ref,
                            'SITE_COORD': 500,
                            'TLIST': f"{self.time.get_jd()}"
                            }
        link = ("https://ssd.jpl.nasa.gov/api/horizons.api?" +
                "format=json&OBJ_DATA=%27NO%27&QUANTITIES=%271,9%27")
        for key, value in dict_parameters.items():
            link = link + f"&{key}=%27{value}%27"
        request=urllib.Request(link)
        with urllib.urlopen(request) as response:
            result = json.loads(response.read().decode('utf-8'))['result']
        return re.split(r"\*+",result)

    def get_coord(self):
        """Get equatorial coordinates from JPL Horizons

        Returns
        -------
        tuple
            Equatorial coordinates right_ascencion as HMS angle and declination as DMS angle
        """
        result = self.object_data[6]
        result = re.split(r"\s",re.split(r"\s{2,}",result)[2])
        return ((int(result[0]), int(result[1]), float(result[2])),
                (int(result[3]), int(result[4]), float(result[5])))

    def get_magnitude(self):
        """Get magnitude from JPL Horizons

        Returns
        -------
        int
            Magnitude
        """
        result = self.object_data[6]
        result = re.split(r"\s",re.split(r"\s{2,}",result)[3])[0]
        return float(result)

    def get_name(self):
        """Get object name from JPL Horizons

        Returns
        -------
        str
            Object name
        """
        result = self.object_data[2]
        result = re.findall(r"Target body name: (\w+)", result)
        return result[0]