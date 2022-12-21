import urllib.request as urllib
import xmltodict

class Simbad():
    def __init__(self,object_name: str):
        self.result = self._get_datas(object_name)
    
    def _get_datas(self, object_name: str):
        link = 'http://cds.unistra.fr/cgi-bin/nph-sesame/-oIfx?'+object_name
        request=urllib.Request(link)
        response=urllib.urlopen(request)
        return xmltodict.parse(response.read().decode('utf-8'))['Sesame']['Target']

    def get_coords(self):
        alpha, delta = self.result['Resolver']['jpos'].split(' ')
        return((int(alpha[0]), int(alpha[1]), float(alpha[2])),
                (int(delta[0]), int(delta[1]), float(delta[2])))
    
