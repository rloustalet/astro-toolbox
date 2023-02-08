"""This module contains scripts functions.
"""
import pathlib
import pkg_resources
from rich.progress import track

from astro_toolbox.coordinates.equatorial import Equatorial
from astro_toolbox.query.ephemeris import Horizons
from astro_toolbox.query.catalogs import Simbad

from astro_toolbox.query.ephemeris import DICT_OBJECTS

PATH = pkg_resources.resource_filename('astro_toolbox', '/coordinates/data/')

def read_observatory_program(input_file: pathlib.Path):
    """Read an observatory program from a list.

    Parameters
    ----------
    input_file : pathlib.Path
        Input file path.

    Returns
    -------
    object_list : list
        Objects list.
    """
    with open(input_file, 'r', encoding="utf-8") as file:
        object_list = file.readlines()
        object_list = [n.replace('\n', '') for n in object_list]
    if '' in object_list:
        object_list.remove('')
    object_list.sort(key=str.casefold)
    return object_list

def get_multiple_informations(object_list, site, datetime, bounds):
    """Getting multiple objects equatorial information.
    """
    bounds = list(bounds)
    if bounds[1] <= bounds[0]:
        bounds[1] = bounds[1] + 24
    object_dict = {}
    for name in track(object_list, description="Querying information..."):
        try:
            if name.lower() in list(key.lower() for key in DICT_OBJECTS):
                obj = Horizons(name, datetime, site)
            else:
                obj = Simbad(name)
            object_dict[name] = Equatorial(alpha=obj.get_equatorial_coord()[0],
                                        delta=obj.get_equatorial_coord()[1], name=name,
                                        magnitude=obj.get_magnitude())
        except ValueError:
            pass
    return object_dict
