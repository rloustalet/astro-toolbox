"""This module creates the console interface.
"""
import pathlib
import json
import logging
import pkg_resources
import click
from matplotlib.backends.backend_pdf import PdfPages
from rich.progress import track
from rich.console import Console
from rich.table import Table

from astro_toolbox.angle.degrees import AngleDeg
from astro_toolbox.angle.hms import AngleHMS
from astro_toolbox.time.core import AstroDateTime
from astro_toolbox.coordinates.location import Location
from astro_toolbox.coordinates.equatorial import Equatorial
from astro_toolbox.query.ephemeris import Horizons
from astro_toolbox.query.catalogs import Simbad
from astro_toolbox.query.weather import OpenMeteo
from astro_toolbox.scripts.planning import read_observatory_program
from astro_toolbox.scripts.planning import get_multiple_informations
from astro_toolbox.scripts.plots import airmas_map
from astro_toolbox.scripts.plots import polarstar_plt_northern
from astro_toolbox.scripts.plots import polarstar_plt_southern

from astro_toolbox.query.ephemeris import DICT_OBJECTS

PATH = pkg_resources.resource_filename('astro_toolbox', 'coordinates/data/')
PATH_2 = pkg_resources.resource_filename('astro_toolbox', 'query/weather_icons/')

def wmototext(code):
    """Function to convert WMO code to text.

    Parameters
    ----------
    code : str
        WMO code as str.

    Returns
    -------
    Object
        offset_image Object.
    """
    if code == '00':
        text = 'Sunny'
    elif code == '01':
        text = 'Mainly Clear'
    elif code == '02':
        text = 'Partly Cloudy'
    elif code == '03':
        text = 'Cloudy'
    elif code[0] == '4':
        text = 'Fog'
    elif code[0] == '5':
        text = 'Drizzle'
    elif code[0] == '6':
        text = 'Rain'
    elif code[0] == '7' or code in (85, 86):
        text = 'Snow'
    elif code in (80, 81, 82):
        text = 'Showers'
    elif code[0] == ('9'):
        text = 'Thunderstorm'
    else:
        text = 'N/A'
    return text

def winddirectiontotext(wind_direction):
    """Funcion to convert wind direction to text.

    Parameters
    ----------
    wind_direction : float
        Wind direction

    Returns
    -------
    Object
        offset_image Object.
    """
    if 0 <= wind_direction <= 22.5 or 337.5 <= wind_direction <= 360:
        direction = 'N'
    elif 22.5 < wind_direction < 67.5:
        direction = 'NE'
    elif 67.5 < wind_direction < 112.5:
        direction = 'E'
    elif 112.5 < wind_direction < 157.5:
        direction = 'SE'
    elif 157.5 < wind_direction < 202.5:
        direction = 'S'
    elif 202.5 < wind_direction < 247.5:
        direction = 'SW'
    elif 247.5 < wind_direction < 292.5:
        direction = 'W'
    elif 292.5 < wind_direction < 337.5:
        direction = 'NW'
    return direction

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
    verbose : int
        Display verbose or not with logging levels
    """
    logging_levels = {1: logging.CRITICAL,
                          2: logging.ERROR,
                          3: logging.INFO,
                          4: logging.DEBUG}
    if verbose:
        logging.basicConfig(level = logging_levels[verbose],
                            format='%(levelname)s:astro_toolbox: %(message)s')

@cli.command("airmass")
@click.option("-d", "--date",
            type=click.STRING,
            default=None,
            help='-d, --date the date default is None if None, today date')
@click.option("-l", "--location",
            type=click.STRING,
            default=None,
            help='-l --location the site name default is None if None last site used')
@click.option("--bounds",
            nargs=2,
            type=click.INT,
            default=((18, 7)),
            help='--bounds to set airmass calculation hours bounds, default=(18, 31)')
@click.option("-o", "--output",
            type=click.STRING,
            default='',
            help='-o --output to set output path, default=\'\'')
@click.argument('input_file_objects',
            type=click.STRING,
            nargs=-1)
def airmass_map_command(input_file_objects, output, location, date, bounds):
    """Airmass calculations.

    Parameters
    ----------
    input_file_objects : str
        Multiple objects, directory or file (must contain '/' for path).
    output : str
        Outpt path, must contain '/' at the end.
    location : str
        Saved site name.
    date : str
        Specified date.
    bounds : tuple
        Tuple which contains night beginning bound and night ending bound.
    """
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
    object_dict = get_multiple_informations(object_list, site, date, bounds)
    temporary_dict = {}
    pdf = PdfPages(pathlib.Path(output +
                    f'Airmass_Map_{ut_time.get_day():02.0f}_{ut_time.get_month():02.0f}'
                    +f'_{ut_time.get_year():04.0f}_@_{site.name}.pdf'))
    for count, key in track(enumerate(object_dict), description='Plotting maps...'):
        temporary_dict.update({key:object_dict[key]})
        if count == len(object_dict)-1 or ((count+1)%50 == 0):
            pdf.savefig(airmas_map(temporary_dict, site, date, bounds))
            temporary_dict = {}
    del temporary_dict
    pdf.close()
    logging.info(f'Airmass: {ut_time.get_day():02.0f}/{ut_time.get_month():02.0f}'
                +f'/{ut_time.get_year():04.0f} UT @ {site.name}')

@cli.command('info')
@click.argument('objects_list',
                nargs=-1,
                type=click.STRING)
@click.option("-d", "--datetime",
            type=click.STRING,
            default=None,
            help='-t, --time the date default is None if None, now')
@click.option("-l", "--location",
            type=click.STRING,
            default=None,
            help='-l --location the site name default is None if None last site used')
def info_command(objects_list, datetime, location):
    """Getting celestial objects information.

    Parameters
    ----------
    objects_list : str
        Multiple objects list.
    time : str
        Date and time
    location : str
       Saved site name.
    """
    for object_name in objects_list:
        site = Location(name=location)
        if object_name.lower() in [key.lower() for key in DICT_OBJECTS]:
            obj = Horizons(object_name, datetime, site)
            alpha, delta = obj.get_equatorial_coord()
            obj_name = obj.get_name()
            obj_magnitude = obj.get_magnitude()
        else:
            obj = Simbad(object_name)
            alpha, delta = obj.get_equatorial_coord()
            obj_name = obj.get_name()
            obj_magnitude = obj.get_magnitude()
        coord = Equatorial(alpha=alpha, delta=delta, name=obj_name, magnitude=obj_magnitude)
        coord.compute_on_date_coord(AstroDateTime(datetime).get_year())
        gamma = AstroDateTime(datetime).get_lst(site)
        click.echo(f'{coord}' +
                f' HA = {AngleHMS(coord.get_hourangle(gamma=gamma))}'
                f' X = {coord.calculate_airmass(gamma=gamma, location=site):.2f}' +
                f' @ {site.name} {AstroDateTime(datetime)}')

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
    if add and location_name != 'list':
        latitude = str(input("Enter latitude in degrees (00.00) or in dms (00°00'00\"): "))
        if '.' in latitude and ('°' and "'") not in latitude:
            latitude = AngleDeg(float(latitude)).degtodms()
        longitude = str(input("Enter longitude in degrees (00.00) or in dms (00°00'00\"): "))
        if '.' in longitude and ('°' and "'") not in longitude:
            longitude = AngleDeg(float(longitude)).degtodms()
        elevation = float(input("Enter elevation in meters: ") or 0)
        Location(location_name, latitude, longitude, elevation).save_site()

    if delete and location_name != 'list':
        Location(name=location_name).delete_site()

    if update and location_name != 'list':
        click.echo('Enter only values to update')
        latitude = (str(input("Enter latitude in degrees (00.00) or in dms (00°00'00''): ")
                    or None))
        longitude = (str(input("Enter longitude in degrees (00.00) or in dms (00°00'00''): ")
                    or None))
        elevation = (str(input("Enter elevation in meters: "))
                    or None)
        location = Location(location_name)
        if latitude == "None":
            latitude = None
        elif '.' in latitude and ('°' and "'") not in latitude:
            latitude = AngleDeg(float(latitude)).degtodms()
        if longitude == "None":
            longitude = None
        elif '.' in longitude and ('°' and "'") not in longitude:
            longitude = AngleDeg(float(longitude)).degtodms()
        Location(location_name, latitude, longitude, elevation).update_site()

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

    if location_name != 'list':
        location = Location(location_name)
        click.echo(f"{location.name}: latitude: {location.latitude} "+
                f"longitude: {location.longitude} "+
                f"elevation = {location.elevation} m")

@cli.command('polaris')
@click.option("-t", "--time",
            type=click.STRING,
            default=None,
            help='-t, --time the date and time default is None if None, now')
@click.option("-l", "--location",
            type=click.STRING,
            default=None,
            help='-l --location the site name default is None if None last site used')
def polaris_command(location, time):
    """Polaris position calculation.

    Parameters
    ----------
    location : str
        Saved site name.
    time : str
        Date and time.
    """
    location = Location(location)
    if location.latitude.dmstodeg() > 0:
        polarstar_plt_northern(location, time)
    elif location.latitude.dmstodeg() < 0:
        polarstar_plt_southern(location, time)

@cli.command('weather')
@click.option("-l", "--location",
            type=click.STRING,
            default=None,
            help='-l --location the site name default is None if None last site used')
@click.option(
    "-d",
    "--days",
    count=True,
    default=1)
@click.option(
    "-p",
    "--past",
    count=True,
    default=0)
def weather_command(location, days, past):
    """Weather forecasts displayed from Open-Meteo

    Parameters
    ----------
    location : str
        Saved site name.
    days : int
        Number of days displayed.
    """
    last_time = '0000-00-00T00:00:00'
    print(f'weather_forecasts @ {Location(location)}')
    weather_forecasts = OpenMeteo(Location(location))
    console = Console()
    table = Table()
    for time in weather_forecasts.data['hourly']['time'][72 - 24 * past :72 + 24*days]:
        time += ':00'
        if int(time[8:10]) != int(last_time[8:10]):
            console.print(table)
            table = Table(title=f"Weather forecasts {time[:11]} " +
                          f"@ {weather_forecasts.location.name}",
                          show_lines=True)
            table.add_column("Time (UT)", justify="center")
            table.add_column("Temperature (°C)", justify="center")
            table.add_column("Humidity (%)", justify="center")
            table.add_column("Precipitation (mm)", justify="center")
            table.add_column("Wind speed (km/h)", justify="center")
            table.add_column("Wind Direction", justify="center")
            table.add_column("Cloud Coverage (%)", justify="center")
            table.add_column(justify="center")
            table.add_row(f'{time:^25}',
                        f'{weather_forecasts.get_temperature(time)}',
                        f'{weather_forecasts.get_humidity(time)}',
                        f'{weather_forecasts.get_precipitation(time)}',
                        f'{weather_forecasts.get_wind_speed(time)}',
                        f'{winddirectiontotext(weather_forecasts.get_wind_direction(time))}',
                        f'{weather_forecasts.get_cloud(time)}',
                        wmototext(weather_forecasts.get_wmo(time)))
        else:
            table.add_row(f'{time:^25}',
                        f'{weather_forecasts.get_temperature(time)}',
                        f'{weather_forecasts.get_humidity(time)}',
                        f'{weather_forecasts.get_precipitation(time)}',
                        f'{weather_forecasts.get_wind_speed(time)}',
                        f'{winddirectiontotext(weather_forecasts.get_wind_direction(time))}',
                        f'{weather_forecasts.get_cloud(time)}',
                        wmototext(weather_forecasts.get_wmo(time)))
        last_time = time
    console.print(table)

if __name__ == '__main__':
    cli(False)
