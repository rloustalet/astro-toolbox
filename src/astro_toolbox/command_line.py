"""This module create the console interface
"""
import re
import pathlib
import json
import pkg_resources
import numpy as np
import click
from rich.progress import track
from matplotlib import pyplot as plt

from astro_toolbox.angle.hms import AngleHMS
from astro_toolbox.angle.degrees import AngleDeg
from astro_toolbox.time.core import AstroDateTime
from astro_toolbox.coordinates.location import Location
from astro_toolbox.coordinates.equatorial import Equatorial
from astro_toolbox.query.catalogs import Simbad

PATH = pkg_resources.resource_filename(__name__, '/coordinates/data/')

def _read_observatory_program(input_file: pathlib.Path):
    """Read an observatory program from a list.

    Parameters
    ----------
    input_file : pathlib.Path
        input file path.

    Returns
    -------
    Location, AstroDateTime, dict
        Location class, DateTime as AstroDateTime class and object dictionnary
    """
    with open(input_file, 'r', encoding="utf-8") as file:
        object_list = file.readlines()
        object_list = [n.replace('\n', '') for n in object_list]
    if '' in object_list:
        object_list.remove('')
    object_list.sort(reverse=True, key=str.casefold)
    objects_dict = {}
    for name in track(object_list, description="Processing..."):
        simbad_object = Simbad(name)
        alpha, delta = simbad_object.get_coords()
        objects_dict[name] = Equatorial(alpha=alpha, delta=delta, name=name,
                            magnitude=simbad_object.get_magnitude())
    return objects_dict

def _verify_coords(latitude, longitude, elevation):
    """_summary_

    Parameters
    ----------
    latitude : str
        Latitude string
    longitude : str
        Longitude string
    elevation : float
        Elevation floar

    Returns
    -------
    list
        Coords list

    Raises
    ------
    ValueError
        Latitude or Longitude is not in necessary format
    ValueError
        Elevation is not a number
    """
    coords = [latitude, longitude]
    for count, value in enumerate(coords):
        value_flag = True
        if ('°' and "'") in value:
            coord_str = re.split(r"[°']",value)[:3]
            coords[count] = (int(coord_str[0]), int(coord_str[1]), float(coord_str[2]))
            value_flag = False
        elif '.' in value and not ('°' and "'") in value:
            coords[count] = AngleDeg(float(value)).degtodms()
            value_flag = False
        elif value_flag is False and (value != 'None' or float('nan')):
            raise ValueError(f"{value} Latitude or longitude is not in format 0.0 or 0°0'0''")
        if not isinstance(elevation, float):
            raise ValueError((f"{value} Elevation value is not a number"))
        return coords

@click.group()
@click.option(
    "-v",
    "--verbose",
    count=True,
    default=0,
    help="-v for DEBUG",
)
def cli(verbose):
    """Display verbose for command line

    Parameters
    ----------
    verbose : boolean
        Display verbos or not
    """
    click.echo(f"Verbosity: {verbose}")

@cli.command("airmass")
@click.option("-d", "--date",
            default=None,
            help='-d, --date the date default is None if None, today date')
@click.option("-l", "--location",
            default='None',
            help='-l --location the site name default is None if None last site used')
@click.option("--begin",
            default=18,
            help='--begin to set begin hour as int, default=18')
@click.option("--end",
            default=31,
            help='--end to set end hour as int, default=18')
@click.argument('input_file',
            default = '')
def airmasses_map_command(input_file,location, date,  begin, end):
    """Airmasses calculations
    """
    if input_file == '':
        inputpath = pathlib.Path('observations.lst')
    else:
        inputpath = pathlib.Path(input_file)
        if inputpath.is_dir():
            inputpath = pathlib.Path(input_file+'/observations.lst')
    if date is not None:
        date = date+(0,0,0)
    object_dict = _read_observatory_program(inputpath)
    ut_time = AstroDateTime(date)
    site = Location(location)
    timelist = np.arange(begin,end,0.1)
    airmasses = np.empty((len(object_dict), np.shape(timelist)[0]))
    for j, key in enumerate(object_dict):
        object_dict[key].compute_on_date_coords(year = ut_time.get_year()+
                                                (ut_time.get_month()-1.0)/12)
        for i, time in enumerate(timelist):
            time = (int(time),(time-int(time))*60,00)
            ut_time = AstroDateTime(ut_time.get_date()+time)
            airmasses[j][i] = object_dict[key].calculate_airmass(
                                AngleHMS(ut_time.get_lst(site)), site)
    plt.figure(figsize=(8.3, 11.7))
    plt.pcolormesh(airmasses, cmap='jet', shading='flat', vmin = 1, vmax = 3.5, label = 'airmasses')
    plt.colorbar(shrink = 0.5)
    plt.xticks(np.arange(0,len(timelist),10), np.arange(begin,end))
    plt.yticks(np.arange(0.5,len(object_dict),1),
                [item[1].name + ' v='
                + str(item[1].magnitude)
                for item in object_dict.items()]
                )
    plt.tick_params(left = False)
    plt.grid(axis = 'x', color = 'k')
    plt.title(f'Airmasses: {ut_time.get_day():02d}/{ut_time.get_month():02d}'
            +f'/{ut_time.get_year()} @ {site.name}')
    plt.tight_layout()
    plt.savefig(pathlib.Path(f'Airmasses_Map_{ut_time.get_day():02d}_{ut_time.get_month():02d}'
                            +f'_{ut_time.get_year()}_@_{site.name}.pdf'))
    print(f'Airmasses: {ut_time.get_day():02d}/{ut_time.get_month():02d}'
        +f'/{ut_time.get_year()} @ {site.name}')

@cli.command('simbad')
@click.argument('object_name')
@click.option("-d", "--date",
            default=None,
            help='-d, --date the date default is None if None, today date')
@click.option("-l", "--location",
            default=None,
            help='-l --location the site name default is None if None last site used')
def simbad_command(object_name, date, location):
    """Get Simbad inormations
    """
    obj = Simbad(object_name)
    alpha, delta = obj.get_coords()
    coords = Equatorial(alpha=alpha, delta=delta,name=obj.get_name(), magnitude=obj.get_magnitude())
    site = Location(name=location)
    ut_time = AstroDateTime(date)
    gamma = AngleHMS(ut_time.get_lst(site))
    print(f'{coords} X = {coords.calculate_airmass(gamma=gamma, location=site)} @ {site.name}')

@cli.command('location')
@click.argument('location_name')
@click.option("-a", "--add",
            count=True,
            default=0,
            help='-a, --add to add location')
@click.option('-d', '--delete',
            count=True,
            default=0,
            help='-d, --delete to delete location')
@click.option('-u', '--update',
            count=True,
            default=0,
            help='-u, --update to update location')
def location_command(location_name, add, delete, update):
    """_summary_

    Parameters
    ----------
    location_name : str
        Location name
    add : bool
        Command to add site
    delete : bool
        Command to delete site
    update : bool
        Command to update site
    """

    if add:
        latitude = str(input("Enter latitude in degrees (00.00) or in dms (00°00'00''): "))
        longitude = str(input("Enter longitude in degrees (00.00) or in dms (00°00'00''): "))
        elevation = float(input("Enter elevation in meters: ") or 0)
        coords = _verify_coords(latitude=latitude, longitude=longitude, elevation=elevation)
        Location(location_name, coords[0], coords[1], elevation).save_site()

    if delete:
        Location(name=location_name).delete_site()

    if update:
        print('Enter only values to update')
        latitude = (str(input("Enter latitude in degrees (00.00) or in dms (00°00'00''): ")
                    or None))
        longitude = (str(input("Enter longitude in degrees (00.00) or in dms (00°00'00''): ")
                    or None))
        elevation = (float(input("Enter elevation in meters: ")
                    or 'nan'))
        coords = _verify_coords(latitude=latitude, longitude=longitude, elevation=elevation)
        Location(location_name, coords[0], coords[1], elevation).update_site()

    if location_name == 'list':
        with open(PATH  + 'sites.json', encoding="utf-8") as json_file:
            dict_sites = json.load(json_file)
        name_list = list(dict_sites.keys())
        count = 1
        for name in name_list:
            print(f"{count}: " + f"{name}: latitude: {dict_sites[name]['latitude']} "+
                f"longitude: {dict_sites[name]['longitude']} "+
                f"elevation = {dict_sites[name]['elevation']} m")
            count = count + 1

if __name__ == '__main__':
    cli(False)
