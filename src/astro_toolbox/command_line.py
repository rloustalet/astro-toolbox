"""This module create the console interface
"""
import numpy as np
import pathlib
import click
from rich.progress import track
from matplotlib import pyplot as plt

from astro_toolbox.angle.hms import AngleHMS
from astro_toolbox.time import AstroDateTime
from astro_toolbox.location import Location
from astro_toolbox.coordinates.equatorial import Equatorial
from astro_toolbox.catalog import Simbad

def read_observatory_program(input_file: pathlib.Path):
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
    time = (0,0,0)
    with open(input_file, 'r') as file:
        location_str = file.readline().replace('\n', '').split(',')
        object_list = file.readlines()
        object_list = [n.replace('\n', '') for n in object_list]

    latitude = location_str[1].split(':')
    latitude = (int(latitude[0]), int(latitude[1]), float(latitude[2]))
    longitude = location_str[2].split(':')
    longitude = (int(longitude[0]), int(longitude[1]), float(longitude[2]))
    date = location_str[3].split(':')
    date = tuple([int(x) for x in date])
    location = Location(location_str[0], latitude=latitude, longitude=longitude)
    datetime = AstroDateTime(date+time)
    if '' in object_list:
        object_list.remove('')
    object_list.sort(reverse=True, key=str.casefold)
    objects_dict = {}
    for n in track(object_list, description="Processing..."):
        alpha, delta = Simbad(n).get_coords()
        objects_dict[n] = Equatorial(alpha, delta, n)
    return datetime, location, objects_dict


@click.group()
@click.option(
    "-v",
    "--verbose",
    count=True,
    default=0,
    help="-v for DEBUG",
)
def cli(verbose):
    pass

@cli.command("airmass")
@click.option("--begin", default=18, help='--begin to set begin hour as int, default=18')
@click.option("--end", default=31, help='--end to set end hour as int, default=18')
@click.argument('input_file', default = '')
def airmass_command(input_file, begin, end):
    """Airmasses calculations
    """
    if input_file == '':
        inputpath = pathlib.Path('observations.lst')
    else:
        inputpath = pathlib.Path(input_file)
        if inputpath.is_dir():
            inputpath = pathlib.Path(input_file+'/observations.lst')

    UTtime, location, object_dict = read_observatory_program(inputpath)

    year = UTtime.get_year()+(UTtime.get_month()-1.0)/12

    timelist = np.arange(begin,end,0.1)

    airmasses = np.empty((len(object_dict), np.shape(timelist)[0]))

    for key,j in zip(object_dict, range(len(object_dict))):
        object_dict[key].compute_on_date_coords(year = year)
        airmass = []
        for i in timelist:
            time = (int(i),(i-int(i))*60,00)
            UTtime = AstroDateTime(UTtime.get_date()+time)
            lst = UTtime.get_lst(location)
            lst = AngleHMS(lst)
            airmass.append(object_dict[key].calculate_airmass(lst, location))
        airmasses[j] = airmass
    outputpath = pathlib.Path(f'Airmasses_Map_{UTtime.get_day()}_{UTtime.get_month()}_{UTtime.get_year()}.pdf')
    plt.figure(figsize=(8.3, 11.7))
    plt.pcolormesh(airmasses, cmap='jet', shading='flat', vmin = 1, vmax = 3.5, label = 'airmasses')
    plt.colorbar(shrink = 0.5)
    plt.xticks(np.arange(0,130,10), np.arange(18,31))
    listname = [object_dict[key].name for key in object_dict]
    plt.yticks(np.arange(0.5,len(object_dict),1), listname)
    plt.tick_params(left = False)
    plt.grid(axis = 'x', color = 'k')
    plt.title(f'Airmasses: {UTtime.get_day()}/{UTtime.get_month()}/{UTtime.get_year()}')
    plt.tight_layout()
    plt.savefig(outputpath)

@cli.command('simbad')
@click.argument('object_name')
def simbad_command(object_name):
    """Get Simbad inormations
    """
    obj = Simbad(object_name)
    alpha = ':'.join((str(n) for n in obj.get_coords()[0]))
    delta = ':'.join((str(n) for n in obj.get_coords()[1]))
    print(f'{obj.get_name()}: '+
    f'\N{GREEK SMALL LETTER ALPHA}={alpha}; '+
    f'\N{GREEK SMALL LETTER DELTA}={delta}; '+
    f'v={obj.get_magnitude()}')

if __name__ == '__main__':
    cli()