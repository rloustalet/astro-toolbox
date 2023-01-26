"""This module create the console interface
"""
import re
import pathlib
import json
import logging
import pkg_resources
import click
from matplotlib.backends.backend_pdf import PdfPages
from rich.progress import track

from astro_toolbox.angle.degrees import AngleDeg
from astro_toolbox.time.core import AstroDateTime
from astro_toolbox.coordinates.location import Location
from astro_toolbox.coordinates.equatorial import Equatorial
from astro_toolbox.query.ephemeris import Horizons
from astro_toolbox.query.catalogs import Simbad
from astro_toolbox.scripts.planning import read_observatory_program
from astro_toolbox.scripts.planning import get_multiple_informations
from astro_toolbox.scripts.plots import airmas_map
from astro_toolbox.scripts.plots import polarstar_plt_northern
from astro_toolbox.scripts.plots import polarstar_plt_southern

from astro_toolbox.query.ephemeris import DICT_OBJECTS

PATH = pkg_resources.resource_filename('astro_toolbox', 'coordinates/data/')

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
    if verbose:
        logging.basicConfig(level=logging.INFO)

@cli.command("airmass")
@click.option("-d", "--date",
            default=None,
            help='-d, --date the date default is None if None, today date')
@click.option("-l", "--location",
            default='None',
            help='-l --location the site name default is None if None last site used')
@click.option("--bounds",
            nargs=2,
            type=click.INT,
            default=((18, 7)),
            help='--bounds to set airmass calculation hours bounds, default=(18, 31)')
@click.option("-o", "--output",
            default='',
            help='-o --output to set output path, default=\'\'')
@click.argument('input_file_objects',
            nargs=-1)
def airmass_map_command(input_file_objects, output, location, date, bounds):
    """Airmass calculations
    """
    if date is not None:
        date = date.split('-')
        date = ((val) for val in date)+(0, 0, 0)
    inputpath = False
    if len(input_file_objects) == 0:
        inputpath = pathlib.Path('observations.lst')
    else:
        if '/' in input_file_objects[0]:
            inputpath = pathlib.Path(input_file_objects[0])
            if inputpath.is_dir():
                inputpath = pathlib.Path(input_file_objects[0]+'observations.lst')
        else:
            object_list = list(input_file_objects)
            object_list.sort(key=str.casefold)
    if inputpath is not False:
        object_list = read_observatory_program(inputpath)
    ut_time = AstroDateTime(date)
    site = Location(location)
    object_dict = get_multiple_informations(object_list, site, ut_time, bounds)
    temporary_dict = {}
    pdf = PdfPages(pathlib.Path(output +
                    f'Airmass_Map_{ut_time.get_day():02d}_{ut_time.get_month():02d}'
                    +f'_{ut_time.get_year()}_@_{site.name}.pdf'))
    for count, key in track(enumerate(object_dict), description='Plotting maps...'):
        temporary_dict.update({key:object_dict[key]})
        if count == len(object_dict)-1 or ((count+1)%50 == 0):
            pdf.savefig(airmas_map(temporary_dict, site, ut_time, bounds))
            temporary_dict = {}
    del temporary_dict
    pdf.close()

@cli.command('info')
@click.argument('object_name')
@click.option("-d", "--date",
            default=None,
            help='-d, --date the date default is None if None, today date')
@click.option("-l", "--location",
            default=None,
            help='-l --location the site name default is None if None last site used')
def info_command(object_name, date, location):
    """Get Simbad inormations
    """
    if date is not None:
        date = date.split('-')
        date = ((val) for val in date)+(0, 0, 0)
    site = Location(name=location)
    ut_time = AstroDateTime(date)
    if object_name.lower() in [key.lower() for key in DICT_OBJECTS]:
        obj = Horizons(object_name, ut_time, site)
        alpha, delta = obj.get_coord()
        obj_name = obj.get_name()
        obj_magnitude = obj.get_magnitude()
    else:
        obj = Simbad(object_name)
        alpha, delta = obj.get_coord()
        obj_name = obj.get_name()
        obj_magnitude = obj.get_magnitude()
    coord = Equatorial(alpha=alpha, delta=delta, name=obj_name, magnitude=obj_magnitude)
    coord.compute_on_date_coord(ut_time.get_year())
    gamma = ut_time.get_lst(site)
    click.echo(f'{coord}' +
               f'X = {coord.calculate_airmass(gamma=gamma, location=site):.2f}' +
               f'@ {site.name}')

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
    """Command to make action son saved locations

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
    def _verify_coords(latitude, longitude, elevation):
        """Function to verify coords

        Parameters
        ----------
        latitude : str
            Latitude string
        longitude : str
            Longitude string
        elevation : float
            Elevation float

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
                coords[count] = AngleDeg(float(value)).degtodms
                value_flag = False
            elif value_flag is False and (value != 'None'):
                raise ValueError(f"{value} Latitude or longitude is not in format 0.0 or 0°0'0''")
            if not isinstance(elevation, float):
                raise ValueError((f"{value} Elevation value is not a number"))
        return coords
    if add:
        latitude = str(input("Enter latitude in degrees (00.00) or in dms (00°00'00''): "))
        longitude = str(input("Enter longitude in degrees (00.00) or in dms (00°00'00''): "))
        elevation = float(input("Enter elevation in meters: ") or 0)
        coords = _verify_coords(latitude=latitude, longitude=longitude, elevation=elevation)
        Location(location_name, coords[0], coords[1], elevation).save_site()

    if delete:
        Location(name=location_name).delete_site()

    if update:
        click.echo('Enter only values to update')
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
            click.echo(f"{count}: " + f"{name}: latitude: {dict_sites[name]['latitude']} "+
                f"longitude: {dict_sites[name]['longitude']} "+
                f"elevation = {dict_sites[name]['elevation']} m")
            count = count + 1

@cli.command('polaris')
@click.option("-d", "--datetime",
            default=None,
            help='-d, --datetime the date default is None if None, today date')
@click.option("-l", "--location",
            default='None',
            help='-l --location the site name default is None if None last site used')
def polaris_command(location, datetime):
    """Polaris position calculation
    """
    if datetime is not None:
        datetime =  re.split(r"[-:]",datetime)
        datetime = ((val) for val in datetime)
    location = Location(location)
    if location.latitude.dmstodeg() > 0:
        polarstar_plt_northern(location, datetime)
    elif location.latitude.dmstodeg() < 0:
        polarstar_plt_southern(location, datetime)


if __name__ == '__main__':
    cli(False)
