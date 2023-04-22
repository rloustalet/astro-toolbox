"""This module contains Open_Meteo class.
"""
import json
import urllib.request as urllib
import math

from astro_toolbox.time.core import AstroDateTime
from astro_toolbox.coordinates.location import Location

OPENMETEO_LEVELS = [1000,
                    975,
                    950,
                    925,
                    900,
                    850,
                    800,
                    700,
                    600,
                    500,
                    400,
                    300,
                    250,
                    200,
                    150,
                    100,
                    70,
                    50,
                    30]

class OpenMeteo():
    """OpenMeteo service request and parsing.

    Attributes
    ----------
    location : Location
            Observer location as Location class.
    model : str, optional
        Weather model (https://open-meteo.com/en/docs), by default 'best_match'
    """
    def __init__(self, location : Location, model : str = 'best_match'):
        """Constructor method

        Parameters
        ----------
        location : Location
            Observer location as Location class.
        model : str, optional
            Weather model (https://open-meteo.com/en/docs), by default 'best_match'
        """
        self.location = location
        pressure_level = self.location.compute_pressure_level()
        index_pressure_level = list(abs(openmeteo_pressure_level - pressure_level)
                                for openmeteo_pressure_level in OPENMETEO_LEVELS).index(
                                min(list(abs(openmeteo_pressure_level - pressure_level)
                                for openmeteo_pressure_level in OPENMETEO_LEVELS)))
        self.pressure_level = OPENMETEO_LEVELS[index_pressure_level]
        self.model = model
        self.data = self._get_data()

    def __repr__(self):
        """Representative method.

        Returns
        -------
        str
            representative string
        """
        return (f'Temperature: {self.get_temperature()} °C' +
                f'Humidity: {self.get_humidity()} %' +
                f'Precipitation: {self.get_precipitation()} mm' +
                f'Wind Speed: {self.get_wind_speed()} km/h' +
                f'Wind Direction: {self.get_wind_direction()} °' +
                f'Cloud Coverage: {self.get_cloud()} %')

    def _get_data(self):
        """Open Meteo query method.

        Returns
        -------
        dict
            Dict containing all the datas requested.
        """
        link = 'https://api.open-meteo.com/v1/forecast?'
        link += (f'latitude={str(self.location.latitude.dmstodeg())}&' +
                f'longitude={str(self.location.longitude.dmstodeg())}&' +
                'hourly=' +
                f'temperature_{self.pressure_level}hPa,' +
                f'relativehumidity_{self.pressure_level}hPa,' +
                'dewpoint_2m,' +
                'precipitation_probability,' +
                'precipitation,' +
                'weathercode,' +
                'pressure_msl,' +
                f'cloudcover_{self.pressure_level}hPa,' +
                f'windspeed_{self.pressure_level}hPa,' +
                f'winddirection_{self.pressure_level}hPa')

        link += f'&models={self.model}&current_weather=false&past_days=3&forecast_days=16'
        request=urllib.Request(link)
        with urllib.urlopen(request) as response:
            result = json.loads(response.read().decode('utf-8'))
        result.pop('generationtime_ms')
        return result

    def _get_index(self, datetime: str | tuple):
        """Time searching method.

        Parameters
        ----------
        datetime : str | tuple
            Date and Time as tuple (YYYY,MM,DD,hh,mm,ss) or YYYY-MM-DDThh:mm:ss.

        Returns
        -------
        int
            Time index.
        """
        datetime = AstroDateTime(datetime)
        datetime_str = str(datetime)[:-5]+'00'
        if datetime_str not in self.data['hourly']['time']:
            return float('nan')
        return self.data['hourly']['time'].index(datetime_str)

    def get_temperature(self, datetime: str | tuple = None):
        """Get temperature method.

        Parameters
        ----------
        datetime : str | tuple, optional
            Date and Time as tuple (``YYYY,MM,DD,hh,mm,ss`` or ``YYYY-MM-DDThh:mm:ss``),
            by default None.

        Returns
        -------
        float
            Temperature
        """
        index = self._get_index(datetime)
        if math.isnan(index):
            return float('nan')
        return self.data['hourly'][f'temperature_{self.pressure_level}hPa'][index]

    def get_humidity(self, datetime: str | tuple = None):
        """Get humidity method.

        Parameters
        ----------
        datetime : str | tuple, optional
            Date and Time as tuple (``YYYY,MM,DD,hh,mm,ss`` or ``YYYY-MM-DDThh:mm:ss``),
            by default None.

        Returns
        -------
        float
            Humidity
        """
        index = self._get_index(datetime)
        if math.isnan(index):
            return float('nan')
        return self.data['hourly'][f'relativehumidity_{self.pressure_level}hPa'][index]

    def get_dewpoint(self, datetime: str | tuple = None):
        """Get dewpoint method.

        Parameters
        ----------
        datetime : str | tuple, optional
            Date and Time as tuple (``YYYY,MM,DD,hh,mm,ss`` or ``YYYY-MM-DDThh:mm:ss``),
            by default None.

        Returns
        -------
        float
            Dewpoint
        """
        index = self._get_index(datetime)
        if math.isnan(index):
            return float('nan')
        return self.data['hourly']['dewpoint_2m'][index]

    def get_precipitation(self, datetime: str | tuple = None):
        """Get precipitation method.

        Parameters
        ----------
        datetime : str | tuple, optional
            Date and Time as tuple (``YYYY,MM,DD,hh,mm,ss`` or ``YYYY-MM-DDThh:mm:ss``),
            by default None.

        Returns
        -------
        float
            Precipitation
        """
        index = self._get_index(datetime)
        if math.isnan(index):
            return float('nan')
        return self.data['hourly']['precipitation'][index]

    def get_precipitation_probability(self, datetime: str | tuple = None):
        """Get precipitation probability method.

        Parameters
        ----------
        datetime : str | tuple, optional
            Date and Time as tuple (``YYYY,MM,DD,hh,mm,ss`` or ``YYYY-MM-DDThh:mm:ss``),
            by default None.

        Returns
        -------
        float
            Precipitation probability
        """
        index = self._get_index(datetime)
        if math.isnan(index):
            return float('nan')
        return self.data['hourly']['precipitation_probability'][index]

    def get_wmo(self, datetime: str | tuple = None):
        """Get World Meteorological Organization code method.

        Parameters
        ----------
        datetime : str | tuple, optional
            Date and Time as tuple (``YYYY,MM,DD,hh,mm,ss`` or ``YYYY-MM-DDThh:mm:ss``),
            by default None.

        Returns
        -------
        float
            WMO cod
        """
        index = self._get_index(datetime)
        if math.isnan(index):
            return float('nan')
        code = self.data['hourly']['weathercode'][index]
        return f'{code:02d}'

    def get_msl_pressure(self, datetime: str | tuple = None):
        """Get sea level pressure method.

        Parameters
        ----------
        datetime : str | tuple, optional
            Date and Time as tuple (``YYYY,MM,DD,hh,mm,ss`` or ``YYYY-MM-DDThh:mm:ss``),
            by default None.

        Returns
        -------
        float
            Sea level pressure
        """
        index = self._get_index(datetime)
        if math.isnan(index):
            return float('nan')
        return self.data['hourly']['pressure_msl'][index]

    def get_cloud(self, datetime: str | tuple = None):
        """Get cloud coverage method.

        Parameters
        ----------
        datetime : str | tuple, optional
            Date and Time as tuple (``YYYY,MM,DD,hh,mm,ss`` or ``YYYY-MM-DDThh:mm:ss``),
            by default None.

        Returns
        -------
        float
            Cloud coverage
        """
        index = self._get_index(datetime)
        if math.isnan(index):
            return float('nan')
        return self.data['hourly'][f'cloudcover_{self.pressure_level}hPa'][index]

    def get_wind_speed(self, datetime: str | tuple = None):
        """Get wind speed method.

        Parameters
        ----------
        datetime : str | tuple, optional
            Date and Time as tuple (``YYYY,MM,DD,hh,mm,ss`` or ``YYYY-MM-DDThh:mm:ss``),
            by default None.

        Returns
        -------
        float
            Wind speed
        """
        index = self._get_index(datetime)
        if math.isnan(index):
            return float('nan')
        return self.data['hourly'][f'windspeed_{self.pressure_level}hPa'][index]

    def get_wind_direction(self, datetime: str | tuple = None):
        """Get wind direction method.

        Parameters
        ----------
        datetime : str | tuple, optional
            Date and Time as tuple (``YYYY,MM,DD,hh,mm,ss`` or ``YYYY-MM-DDThh:mm:ss``),
            by default None.

        Returns
        -------
        float
            Wind direction
        """
        index = self._get_index(datetime)
        if math.isnan(index):
            return float('nan')
        return self.data['hourly'][f'winddirection_{self.pressure_level}hPa'][index]

    def get_units(self):
        """Get units.

        Returns
        -------
        dict
            Dict containing units.
        """
        return self.data['hourly_units']
