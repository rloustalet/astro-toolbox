"""This module contain Location class
"""
import json

from astro_toolbox.angle.dms import AngleDMS
class Location():
    """This class represent the observer location
    """
    def __init__(self, name: str = None, latitude: tuple = None,
                longitude: tuple = None, elevation: float = None):
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
        self.name = name
        self.latitude = AngleDMS(latitude)
        self.longitude = AngleDMS(longitude)
        self.elevation = elevation
        self.current_site = {self.name:
                            {
                                'latitude': self.latitude.anglevalue,
                                'longitude': self.longitude.anglevalue,
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
                f'altitude = {self.elevation}m')

    def save_site(self):
        """Method saving current site in sites file

        Raises
        ------
        KeyError
            The first level key already exist
        """
        with open("data/sites.json", encoding="utf-8") as json_file:
            dict_sites = json.load(json_file)
        if self.name not in dict_sites:
            current_site = {self.name:
                            {
                                'latitude': self.latitude.dmstodeg(),
                                'longitude': self.longitude.dmstodeg(),
                                'elevation': self.elevation
                            }
            }
            dict_sites.update(current_site)
            with open("data/sites.json", 'w', encoding="utf-8") as json_file:
                json.dump(dict_sites, json_file, indent=4)
        raise KeyError("Site already exist, use `update_site` instead")

    def delete_site(self):
        """Method deleting current site from saved sites file

        Raises
        ------
        KeyError
            The first level key doesn't exist
        """
        with open("data/sites.json", encoding="utf-8") as json_file:
            dict_sites = json.load(json_file)
        if self.name in dict_sites:
            del dict_sites[self.name]
        raise KeyError("Site doesn't exist")

    def update_site(self):
        """Method updating current site in saved sites file

        Raises
        ------
        KeyError
            The first level key doesn't exist
        """
        with open("data/sites.json", encoding="utf-8") as json_file:
            dict_sites = json.load(json_file)
        if self.name in dict_sites:
            for key in dict_sites:
                dict_sites[self.name][key] = self.current_site[self.name][key]
        raise KeyError("Site doesn't exist")

    def get_site(self, name: str = None):
        """Method to get a site with it datas

        Parameters
        ----------
        name : str, optional
            The site name, by default None

        Returns
        -------
        Location
            The Location class of the site from his save data in saved sites file

        Raises
        ------
        KeyError
            The first level key doen't exist
        ValueError
            The site name is not given
        """
        with open("data/sites.json", encoding="utf-8") as json_file:
            dict_sites = json.load(json_file)
        if name is not None:
            if name in dict_sites:
                return Location(name = name,
                                latitude = dict_sites[name]['latitude'],
                                longitude = dict_sites[name]['longitude'],
                                elevation = dict_sites[name]['elevation']
                        )
            raise KeyError ("Site doesn't exist")
        raise ValueError ("Site name not given")
