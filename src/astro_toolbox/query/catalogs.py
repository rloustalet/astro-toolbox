"""This module contains Simbad class.
"""
import urllib.request as urllib
import xmltodict

class Simbad():
    """This class allows to read astronomical catalogs over internet.

    Attributes
    ----------
    object_name : str

    """
    def __init__(self,object_name: str):
        """Constructor method.

        Parameters
        ----------
        object_name : str
            Astronomical object name.
        result : dict
            The object dictionary returned from Simbad.
        """
        object_name = object_name.replace(' ', '+')
        self.result = self._get_datas(object_name)

    def _get_datas(self, object_name: str):
        """Seraching datas method

        Parameters
        ----------
        object_name : str
            Astronomical object name.

        Returns
        -------
        dict
            The object dictionary returned from Simbad.
        """
        link = 'https://cds.unistra.fr/cgi-bin/nph-sesame/-oIfx?'+object_name
        request=urllib.Request(link)
        with urllib.urlopen(request) as response:
            result = xmltodict.parse(response.read().decode('utf-8'))['Sesame']['Target']
        if 'Resolver' not in result:
            raise ValueError("Object doesn't exist")
        return result

    def get_equatorial_coord(self):
        """Get RA/DEC object coordinates.

        Returns
        -------
        Tuple
            Tuple which contains two tuples RA/DEC coordinates.
        """
        alpha, delta = self.result['Resolver']['jpos'].split(' ')
        alpha = alpha.split(':')
        delta = delta.split(':')
        return((int(alpha[0]), int(alpha[1]), float(alpha[2])),
                (int(delta[0]), int(delta[1]), float(delta[2])))

    def get_name(self):
        """Get object name.

        Returns
        -------
        str
            Object name from Simbad.
        """
        return self.result['name']

    def get_magnitude(self):
        """Get visual magnitude.

        Returns
        -------
        float, None
            The object magnitude if available.
        """
        if 'mag' in self.result['Resolver']:
            flux_list = self.result['Resolver']['mag']
            if isinstance(flux_list, dict):
                flux_list = [flux_list]
            for flux in flux_list:
                if flux['@band'] == 'V':
                    return float(flux['v'])
        return None
