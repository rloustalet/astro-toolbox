"""This module contain Simbad Class.
"""
import urllib.request as urllib
import xmltodict

class Simbad():
    """This class allow to read astronomical catalogs over internet.
    """
    def __init__(self,object_name: str):
        """Construcotr method.

        Parameters
        ----------
        object_name : str
            Astronomical object name
        """
        object_name = object_name.replace(' ', '+')
        self.result = self._get_datas(object_name)

    def _get_datas(self, object_name: str):
        """Seraching datas method

        Parameters
        ----------
        object_name : str
            Astronomical object name

        Returns
        -------
        dict
            The caractheristics object dictionnary
        """
        link = 'https://cds.unistra.fr/cgi-bin/nph-sesame/-oIfx?'+object_name
        request=urllib.Request(link)
        with urllib.urlopen(request) as response:
            result = xmltodict.parse(response.read().decode('utf-8'))['Sesame']['Target']
        if 'Resolver' not in result:
            raise ValueError("Object doesn't exist")
        return result

    def get_coord(self):
        """Get RA/DEC aobject coords.

        Returns
        -------
        Tuple
            Tuple wich contain two tuples RA coords and DEC.
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
            Object name from Simbad
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
            for flux in flux_list:
                if flux['@band'] == 'V':
                    return float(flux['v'])
        return None
