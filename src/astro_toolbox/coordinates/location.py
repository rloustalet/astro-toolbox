"""This module contain Location class
"""
import re
import json
import math
import pkg_resources

from astro_toolbox.angle.dms import AngleDMS

PATH = pkg_resources.resource_filename('astro_toolbox', 'coordinates/data/')
class Location():
    """This class represent the observer location
    """
    def __init__(self, name: str = 'None', latitude: tuple = 'None',
                longitude: tuple = 'None', elevation: float = float('nan')):
        """Constructor method

        Parameters
        ----------
        name : str
            Location name
        latitude : tuple
            Location latitude tuple (°, ', '')
        longitude : tuple
            Location longitude tuple (°, ', '')
        elevation : float, optional
            Loaction elevation (m), by default 0.0
        """
        if name == 'None':
            dict_site = self._get_site()
            name = list(dict_site.keys())[0]
        else:
            try:
                dict_site = self._get_site(name=name)
                name = list(dict_site.keys())[0]
            except ValueError:
                pass
        if latitude == 'None':
            latitude_str = re.split(r"[°'\"]",dict_site[name]['latitude'])[:3]
            latitude = (int(latitude_str[0]), int(latitude_str[1]), float(latitude_str[2]))
        if longitude == 'None':
            longitude_str = re.split(r"[°'\"]",dict_site[name]['longitude'])[:3]
            longitude = (int(longitude_str[0]), int(longitude_str[1]), float(longitude_str[2]))
        if math.isnan(elevation):
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
            Return a class representative string
        """
        return (f'{self.name}: latitude: {self.latitude} '+
                f'longitude: {self.longitude} '+
                f'elevation = {self.elevation} m')

    def save_site(self):
        """Method saving current site in sites file

        Raises
        ------
        KeyError
            The first level key already exist
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
        """Method deleting current site from saved sites file

        Raises
        ------
        KeyError
            The first level key doesn't exist
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
        """Method updating current site in saved sites file

        Raises
        ------
        KeyError
            The first level key doesn't exist
        """
        with open(PATH  + 'sites.json', encoding="utf-8") as json_file:
            dict_sites = json.load(json_file)
        if self.name.lower() in list(key.lower() for key in dict_sites):
            keys = list(key for key in dict_sites)
            idx = [key.lower() for key in dict_sites].index(self.name.lower())
            for key in dict_sites[keys[idx]]:
                if self.current_site[self.name][key] is not None:
                    dict_sites[keys[idx]][key] = self.current_site[self.name][key]
            with open(PATH  + 'sites.json', 'w', encoding="utf-8") as json_file:
                json.dump(dict_sites, json_file, indent=4)
            return None
        raise ValueError("Site doesn't exist")

    def _get_site(self, name: str = None):
        """Method to get a site with it datas

        Parameters
        ----------
        name : str, optional
            The site name, by default None

        Returns
        -------
        dict
            The location dictionnary of the site from his save data in saved sites file

        Raises
        ------
        KeyError
            The first level key doen't exist
        ValueError
            The site name is not given
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
