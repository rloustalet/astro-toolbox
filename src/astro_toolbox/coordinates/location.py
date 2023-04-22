"""This module contains Location class.
"""
import re
import json
import pkg_resources
from astro_toolbox.angle.dms import AngleDMS
from astro_toolbox.utils.strparser import angle_parser

PATH = pkg_resources.resource_filename('astro_toolbox', 'coordinates/data/')
class Location():
    """This class represents the observer location.

    Attributes
    ----------
    name : str
        Location name.
    latitude : tuple | str
        Location latitude.
    longitude : tuple | str
        Location longitude.
    elevation : float
        Location elevation.
    """
    def __init__(self, name: str = None, latitude: tuple | str = None,
                longitude: tuple | str = None, elevation: float = None):
        """Constructor method.

        Parameters
        ----------
        name : str
            Location name.
        latitude : tuple | str
            Location latitude tuple or str (``dd:dd:dd.dd`` or ``dd°dd'dd.dd"``).
        longitude : tuple | str
            Location longitude tuple or str (``dd:dd:dd.dd`` or ``dd°dd'dd.dd"``).
        elevation : float, optional
            Location elevation (m), by default 0.0.
        """
        if name is None:
            dict_site = self._get_site()
            name = list(dict_site.keys())[0]
        else:
            try:
                dict_site = self._get_site(name=name)
                name = list(dict_site.keys())[0]
            except ValueError:
                pass
        if latitude is None:
            latitude_str = re.split(r"[°'\"]",dict_site[name]['latitude'])[:3]
            latitude = (float(latitude_str[0]), float(latitude_str[1]), float(latitude_str[2]))
        if isinstance(latitude, str) and latitude is not None:
            latitude = angle_parser(latitude)
        if longitude is None:
            longitude_str = re.split(r"[°'\"]",dict_site[name]['longitude'])[:3]
            longitude = (float(longitude_str[0]), float(longitude_str[1]), float(longitude_str[2]))
        if isinstance(longitude, str) and longitude is not None:
            longitude = angle_parser(longitude)
        if elevation is None:
            elevation = dict_site[name]['elevation']
        self.name = name
        self.latitude = AngleDMS(latitude)
        self.longitude = AngleDMS(longitude)
        self.elevation = elevation
        self.current_site = {self.name:
                            {
                                'latitude': repr(self.latitude),
                                'longitude': repr(self.longitude),
                                'elevation': self.elevation
                            }
            }

    def __repr__(self):
        """Representative method

        Returns
        -------
        string
            Return a class representative string.
        """
        return (f'{self.name}: latitude: {self.latitude} '+
                f'longitude: {self.longitude} '+
                f'elevation = {self.elevation} m')

    def compute_pressure_level(self):
        """Pressure level computing method.

        .. math:: P = 1013.25(1 - \\frac{h}{44307.694})^{5.25530}

        Returns
        -------
        float
            Pressure level in hPa.
        """
        return (1013.25 *
                (1 - self.elevation /
                44307.694) ** 5.25530)

    def save_site(self):
        """Method to save current site in sites file.

        Raises
        ------
        KeyError
            The first level key already exist.
        """
        with open(PATH  + 'sites.json', encoding="utf-8") as json_file:
            dict_sites = json.load(json_file)
        if self.name.lower() not in [key.lower() for key in dict_sites]:
            new_dict_sites = self.current_site
            new_dict_sites.update(dict_sites)
            with open(PATH  + 'sites.json', 'w', encoding="utf-8") as json_file:
                json.dump(new_dict_sites, json_file, indent=4)
            return None
        raise ValueError("Site already exist, use `update_site` instead")

    def delete_site(self):
        """Method to delete current site from saved sites file.

        Raises
        ------
        KeyError
            The first level key doesn't exist.
        """
        with open(PATH  + 'sites.json', encoding="utf-8") as json_file:
            dict_sites = json.load(json_file)
        if self.name.lower() in list(key.lower() for key in dict_sites):
            keys = list(key for key in dict_sites)
            idx = list(key.lower() for key in dict_sites).index(self.name.lower())
            del dict_sites[keys[idx]]
            with open(PATH  + 'sites.json', 'w', encoding="utf-8") as json_file:
                json.dump(dict_sites, json_file, indent=4)
            return None
        raise ValueError("Site already exist, use `update_site` instead")
    def update_site(self):
        """Method to update current site in saved sites file.

        Raises
        ------
        KeyError
            The first level key doesn't exist.
        """
        with open(PATH  + 'sites.json', encoding="utf-8") as json_file:
            dict_sites = json.load(json_file)
        if self.name.lower() in list(key.lower() for key in dict_sites):
            keys = list(key for key in dict_sites)
            idx = [key.lower() for key in dict_sites].index(self.name.lower())
            for key in dict_sites[keys[idx]]:
                dict_sites[keys[idx]][key] = self.current_site[self.name][key]
            with open(PATH  + 'sites.json', 'w', encoding="utf-8") as json_file:
                json.dump(dict_sites, json_file, indent=4)
            return None
        raise ValueError("Site doesn't exist")

    def _get_site(self, name: str = None):
        """Method to get a site with it data.

        Parameters
        ----------
        name : str, optional
            The site name, by default None.

        Returns
        -------
        dict
            The location dictionary from its saved data in saved sites file.

        Raises
        ------
        KeyError
            The first level key doesn't exist.
        ValueError
            The site name is not given.
        """
        with open(PATH  + 'sites.json', encoding="utf-8") as json_file:
            dict_sites = json.load(json_file)
        if name is None:
            name = list(dict_sites.keys())[0]
        if name.lower() in [key.lower() for key in dict_sites.keys()]:
            keys = list(key for key in dict_sites)
            idx = list(key.lower() for key in dict_sites).index(name.lower())
            dict_site = dict_sites[keys[idx]]
            new_dict_sites = {keys[idx]: dict_sites.pop(keys[idx]), **dict_sites}
            with open(PATH  + 'sites.json', 'w', encoding="utf-8") as json_file:
                json.dump(new_dict_sites, json_file, indent=4)
            return {keys[idx]: dict_site}
        raise ValueError(f"{name} site doesn't exist")
