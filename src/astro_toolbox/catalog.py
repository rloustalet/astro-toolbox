import urllib.request as urllib
import xmltodict

class Simbad():
    def __init__(self,object_name: str):
        object_name = object_name.replace(' ', '+')
        self.result = self._get_datas(object_name)

    def _get_datas(self, object_name: str):
        link = 'https://cds.unistra.fr/cgi-bin/nph-sesame/-oIfx?'+object_name
        request=urllib.Request(link)
        response=urllib.urlopen(request)
        return xmltodict.parse(response.read().decode('utf-8'))['Sesame']['Target']

    def get_coords(self):
        alpha, delta = self.result['Resolver']['jpos'].split(' ')
        alpha = alpha.split(':')
        delta = delta.split(':')
        return((int(alpha[0]), int(alpha[1]), float(alpha[2])),
                (int(delta[0]), int(delta[1]), float(delta[2])))
    
    def get_name(self):
        return(self.result['name'])

    def get_magnitude(self):
        if 'mag' in self.result['Resolver']:
            flux_list = self.result['Resolver']['mag']
            for n in flux_list:
                if n['@band'] == 'V':
                    return float(n['v'])
        return None