"""This module contains scripts functions
"""
import math
import numpy as np
import pkg_resources

from matplotlib import pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox, TextArea

from astro_toolbox.angle.hms import AngleHMS
from astro_toolbox.angle.dms import AngleDMS
from astro_toolbox.time.core import AstroDateTime
from astro_toolbox.coordinates.location import Location
from astro_toolbox.coordinates.equatorial import Equatorial
from astro_toolbox.query.ephemeris import Horizons
from astro_toolbox.query.weather import OpenMeteo


PATH = pkg_resources.resource_filename('astro_toolbox', 'query/weather_icons/')

def offset_image(name, axis):
    """Add icons from query/weather_icons on plot.

    Parameters
    ----------
    name : str
        icon name.
    axis : Object
        Pyplot axis object.

    Returns
    -------
    Object
        Pyplot image object.
    """
    path = PATH + f'{name}.png'
    img = plt.imread(path)
    image = OffsetImage(img, zoom=0.5)
    image.image.axes = axis
    return image

def wmotoimage(code, axis):
    """Function to convert WMO code to icon.

    Parameters
    ----------
    code : str
        WMO code as str.
    axis : Object
        Axis object.

    Returns
    -------
    Object
        offset_image Object.
    """
    if code == '00':
        icon = offset_image('sunny', axis)
    elif code == '01':
        icon = offset_image('mainly_clear', axis)
    elif code == '02':
        icon = offset_image('partly_cloudy', axis)
    elif code == '03':
        icon = offset_image('cloudy', axis)
    elif code[0] == '4':
        icon = offset_image('fog', axis)
    elif code[0] == '5':
        icon = offset_image('drizzle', axis)
    elif code[0] == '6':
        icon = offset_image('rain', axis)
    elif code[0] == '7' or code in (85, 86):
        icon = offset_image('snow', axis)
    elif code in (80, 81, 82):
        icon = offset_image('showers', axis)
    elif code[0] == ('9'):
        icon = offset_image('thunderstorm', axis)
    else:
        icon = offset_image('na', axis)
    return icon

def winddirectiontoimage(wind_direction, axis):
    """Funcion to convert wind direction to icon.

    Parameters
    ----------
    wind_direction : float
        Wind direction
    axis : Object
        Axis object.

    Returns
    -------
    Object
        offset_image Object.
    """
    if 0 <= wind_direction <= 22.5 or 337.5 <= wind_direction <= 360:
        icon = offset_image('direction_up', axis)
    elif 22.5 < wind_direction < 67.5:
        icon = offset_image('direction_up_left', axis)
    elif 67.5 < wind_direction < 112.5:
        icon = offset_image('direction_left', axis)
    elif 112.5 < wind_direction < 157.5:
        icon = offset_image('direction_down_left', axis)
    elif 157.5 < wind_direction < 202.5:
        icon = offset_image('direction_down', axis)
    elif 202.5 < wind_direction < 247.5:
        icon = offset_image('direction_down_right', axis)
    elif 247.5 < wind_direction < 292.5:
        icon = offset_image('direction_right', axis)
    elif 292.5 < wind_direction < 337.5:
        icon = offset_image('direction_up_right', axis)
    return icon

def plot_weather(date, location, bounds, axis):
    """Plot weather on airmass map

    Parameters
    ----------
    date : str | tuple
        Plotting date.
    location : Location
        Location object.
    bounds : tuple
        Tuple containing observation bounds.
    axis : Object
        Pyplot axis object.
    """
    hours = list(np.mod(np.arange(bounds[0],bounds[1]), 24))
    weather_forecast = OpenMeteo(location=location)
    annotation_box = AnnotationBbox(TextArea('Weather\nforecasts',
                                            textprops=dict(rotation = 90, ha = 'center')),
                                            (0, 0),
                                            xybox=(-85, -55),
                                            frameon=False,
                                            xycoords='data',
                                            boxcoords="offset points",
                                            pad=0)
    axis.add_artist(annotation_box)
    weather_units = [TextArea('Temperature °C',
                            textprops=dict(size=6)),
                    TextArea('Humidity %',
                            textprops=dict(size=6)),
                    TextArea('Precipitation mm',
                            textprops=dict(size=6)),
                    TextArea('Wind Speed km/h',
                            textprops=dict(size=6)),
                    TextArea('Wind Direction',
                            textprops=dict(size=6))]
    for j, item in enumerate(weather_units):
        annotation_box = AnnotationBbox(item,
                                        (0, 0),
                                        xybox=(-40, -35 - 10 * j),
                                        frameon=False,
                                        xycoords='data',
                                        boxcoords="offset points",
                                        pad=0)
        axis.add_artist(annotation_box)
    last_time = 0
    for time in hours:
        if time - last_time < 0:
            date = AstroDateTime(date).get_gregorian(1)
        last_time = time
        datetime = date + (time, 0, 0)
        weather = [offset_image('na', axis)]
        weather += [TextArea(f'{weather_forecast.get_temperature(datetime)}',
                            textprops=dict(size=6)),
                    TextArea(f'{weather_forecast.get_humidity(datetime)}',
                            textprops=dict(size=6)),
                    TextArea(f'{weather_forecast.get_precipitation(datetime)}',
                            textprops=dict(size=6)),
                    TextArea(f'{weather_forecast.get_wind_speed(datetime)}',
                            textprops=dict(size=6))]
        weather.append(winddirectiontoimage(
                        weather_forecast.get_wind_direction(datetime), axis))
        weather[0] = wmotoimage(weather_forecast.get_wmo(datetime), axis)
        for j, item in enumerate(weather):
            annotation_box = AnnotationBbox(item,
                                            (hours.index(time) * 10, 0),
                                            xybox=(0., -25 - 10 * j),
                                            frameon=False,
                                            xycoords='data',
                                            boxcoords="offset points",
                                            pad=0)
            axis.add_artist(annotation_box)

def sun_impact(lines, site, date, bounds):
    """Function which plots sun impact.

    Parameters
    ----------
    lines : int
        number of lines plot.
    site : Location
        Location object.
    date : tuple | str
        Date to plot sun impact.
    bounds : list
        List of length 2 containing lower and upper time bounds.

    Returns
    -------
    list
        List of matplotlib.pyplot Rectangles objects.
    """
    ut_time = AstroDateTime(date)
    sun = Horizons('Sun', date, site)
    sun = Equatorial(name='Sun',
                    alpha=sun.get_equatorial_coord()[0],
                    delta=sun.get_equatorial_coord()[1],
                    magnitude=sun.get_magnitude)
    sun_rectangles_list = []
    for i, time in enumerate(np.arange(bounds[0],bounds[1],0.1)):
        time = (int(time),(time-int(time))*60,0)
        ut_time = AstroDateTime(ut_time.date+time)
        altitude = (AngleDMS(sun.to_horizontal(ut_time.get_lst(site), site)[1]).dmstodeg())
        if altitude <= 0:
            opacity = 1 + altitude/18
            if altitude < -18:
                opacity = 0
        elif altitude > 0:
            opacity = 1
        sun_rectangles_list.append(plt.Rectangle((i, 0), 1, lines,
                                                alpha=opacity, color='w', linewidth=3))
    return sun_rectangles_list

def moon_times(lines, site, date, bounds):
    """Moon observational impact.

    Parameters
    ----------
    lines : int
        number of lines plot.
    site : Location
        Location object.
    date : tuple | str
        Date to plot moon impact.
    bounds : list
        List of length 2 containing lower and upper time bounds.
    """
    moon = Horizons('Moon', date, site)
    moon = Equatorial(name='Moon',
                    alpha=moon.get_equatorial_coord()[0],
                    delta=moon.get_equatorial_coord()[1],
                    magnitude=0)
    rise_time = moon.calculate_rise_time(site,
                                        date,
                                        altitude_0=0)
    set_time = moon.calculate_set_time(site,
                                    date,
                                    altitude_0=0)
    rise_time = rise_time[0] + rise_time[1]/60 + rise_time[2]/3600
    set_time = set_time[0] + set_time[1]/60 + set_time[2]/3600
    lower_bound = [0] * (int((bounds[1] - bounds[0])/24)+2)
    upper_bound = [0] * (int((bounds[1] - bounds[0])/24)+2)
    for i in range(0,int((bounds[1] - bounds[0])/24)+2):
        lower_bound[i] += 24 * i
        upper_bound[i] += 24 + 24 * i
    lower_bound[0] = bounds[0]
    upper_bound[-1] = bounds[1]
    for lower, upper in zip(lower_bound, upper_bound):
        if lower < set_time + 24 * int(lower/24) < upper:
            plt.plot([(set_time + 24 * int(lower/24)-bounds[0])*10]*2,
                    [0, lines], '--', color='grey', linewidth=2, label='Moonset')
        if lower < rise_time + 24 * int(lower/24) < upper:
            plt.plot([(rise_time + 24 * int(lower/24)-bounds[0])*10]*2,
                    [0, lines], ':', color='grey', linewidth=2, label='Moonrise')
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(),
                by_label.keys(),
                bbox_to_anchor=(1.05, 1),
                loc=2, borderaxespad=0.,
                facecolor='k',
                labelcolor='red')

def airmas_map(object_dict,
                site: Location,
                date: tuple|str,
                bounds: tuple=(18,31)):
    """Airmass calculations.

    Parameters
    ----------
    object_dict : dict
        Dictionary containing object name ans theirs associated equatorial class.
    site : Location
        Location object.
    date : tuple | str
        Date to plot airmass map.
    bounds : tuple
        List of length 2 containing lower and upper time bounds.
    """
    ut_time = AstroDateTime(date)
    bounds = list(bounds)
    if bounds[1] <= bounds[0]:
        bounds[1] = bounds[1] + 24
    airmasses = np.empty((len(object_dict), np.shape(np.arange(bounds[0],bounds[1],0.1))[0]))
    alpha_visible = np.ones((np.shape(airmasses)[0], np.shape(airmasses)[1]))
    for j, key in enumerate(object_dict):
        object_dict[key].compute_on_date_coord(year = ut_time.get_year()+
                                                (ut_time.get_month()-1.0)/12)
        for i, time in enumerate(np.arange(bounds[0],bounds[1],0.1)):
            time = (int(time),(time-int(time))*60,0)
            ut_time = AstroDateTime(ut_time.date+time)
            airmasses[j][i] = object_dict[key].calculate_airmass(
                                ut_time.get_lst(site), site)
            if airmasses[j][i] >= 40:
                alpha_visible[len(object_dict)-j-1][i] = 0
    fig, axis = plt.subplots(figsize=(8.3, 11.7))
    moon_times(len(object_dict), site, date, bounds)
    mesh = axis.pcolormesh(airmasses[::-1],
                    cmap='jet',
                    shading='flat',
                    alpha=alpha_visible,
                    vmin = 1,
                    vmax = 3.5)
    for rect in sun_impact(len(object_dict), site, date, bounds):
        axis.add_patch(rect)
    fig.colorbar(mesh, ax=axis, shrink=0.5)
    plt.xticks(np.arange(0,len(np.arange(bounds[0],bounds[1],0.1)),10),
                                np.mod(np.arange(bounds[0],bounds[1]), 24))
    plt.yticks(np.arange(0.5,len(object_dict),1),
                [item[1].name + ' v='
                + str(item[1].magnitude)
                for item in reversed(object_dict.items())])
    plot_weather(ut_time.date, site, bounds, axis)
    axis.tick_params(left = False)
    axis.grid(axis = 'x', color = 'k')
    axis.set_title(f'Airmass: {ut_time.get_day():02.0f}/{ut_time.get_month():02.0f}'
            +f'/{ut_time.get_year():04.0f} UT @ {site.name}')
    axis.set_facecolor('k')
    fig.tight_layout()
    return fig

def polarstar_plt_northern(location: Location, datetime: tuple | str=None):
    """Polaris Polar Finder position for northern hemisphere.

    Parameters
    ----------
    site : Location
        Location object.
    datetime : tuple | str
        Date and time to plot Polaris position.
    """
    ut_time = AstroDateTime(datetime)
    fig, axis = plt.subplots(figsize=(5, 5), num='Polaris position')
    axis.add_patch(plt.Circle((0,0), 36, color='r', fill=False))
    axis.add_patch(plt.Circle((0,0), 40, color='r', linestyle='--', fill=False))
    axis.add_patch(plt.Circle((0,0), 44, color='r', fill=False))
    axis.plot([-21, 21], [0, 0], color='r')
    axis.plot([0, 0], [-21, 21], color='r')
    axis.text(-1, -50, '0', color='r')
    axis.text(47, -2, '6', color='r')
    axis.text(-3, 47, '12', color='r')
    axis.text(-52, -2, '18', color='r')
    polar_star = Equatorial(name='polaris',
                    alpha=(2, 32, 08.50),
                    delta=(+89, 16, 11.6),
                    magnitude=1.95)
    polar_star.compute_on_date_coord(year = ut_time.get_year()+
                                        (ut_time.get_month()-1.0)/12)
    polar_star_hour_angle = AngleHMS(polar_star.get_hourangle(
                                    ut_time.get_lst(location)))
    polar_star_distance = (90 - polar_star.delta.dmstodeg())*60
    x_polar_star, y_polar_star = (polar_star_distance*math.sin(polar_star_hour_angle.hmstorad()),
                                -polar_star_distance*math.cos(polar_star_hour_angle.hmstorad()))
    axis.plot(x_polar_star,y_polar_star, 'ow')
    axis.set_aspect('equal', adjustable='box')
    axis.axis('off')
    axis.set_xlim([-60, 60])
    axis.set_ylim([-60, 60])
    axis.text(20, 60, f"HA = {polar_star_hour_angle}", color='r')
    axis.text(20, 55, f"d (') = {round(polar_star_distance, 2)}", color='r')
    fig.tight_layout()
    fig.patch.set_facecolor('k')
    plt.show()

def polarstar_plt_southern(location: Location, datetime: tuple=None):
    """Polaris Polar Finder position for southern hemisphere

    Parameters
    ----------
    site : Location
        Location object.
    datetime : tuple | str
        Date and time to plot Polaris australis position.
    """
    ut_time = AstroDateTime(datetime)
    fig, axis = plt.subplots(figsize=(8, 8), num='Polaris position')
    axis.add_patch(plt.Circle((0,0), 60, color='r', fill=False))
    axis.add_patch(plt.Circle((0,0), 65, color='r', linestyle='--', fill=False))
    axis.add_patch(plt.Circle((0,0), 70, color='r', fill=False))
    axis.plot([-21, 21], [0, 0], color='r')
    axis.plot([0, 0], [-21, 21], color='r')
    axis.text(-1, -50, '0', color='r')
    axis.text(47, -2, '6', color='r')
    axis.text(-3, 47, '12', color='r')
    axis.text(-52, -2, '18', color='r')
    octans_constellation =[[
    Equatorial(name='\u03C4 Oct',
                alpha=(23, 27, 43.30),
                delta=(-87, 29, 11.0),
                magnitude=5.50),
    Equatorial(name='CG Oct',
                alpha=(22, 44, 41.05),
                delta=(-88, 49, 19.3),
                magnitude=6.50),
    Equatorial(name='\u03C3 Oct',
                alpha=(21, 7, 37.48),
                delta=(-88, 57, 27.9),
                magnitude=5.45),
    Equatorial(name='\u03C7 Oct',
                alpha=(18, 54, 16.53),
                delta=(-87, 36, 19.0),
                magnitude=5.25)], [], []]
    for star in octans_constellation[0]:
        star.compute_on_date_coord(year = ut_time.get_year()+
                                    (ut_time.get_month()-1.0)/12)
        octans_constellation[1].append((star.delta.dmstodeg() + 90)*60)
    for star in octans_constellation[0]:
        octans_constellation[2].append(
            AngleHMS(star.get_hourangle(ut_time.get_lst(location))).hmstorad())
    x_octans_stars = []
    y_octans_stars = []
    for i in range(len(octans_constellation[0])):
        x_octans_stars.append(-octans_constellation[1][i]*math.sin(octans_constellation[2][i]))
        y_octans_stars.append(octans_constellation[1][i]*math.cos(octans_constellation[2][i]))
    axis.plot(x_octans_stars, y_octans_stars, 'r', marker='o')
    axis.plot(x_octans_stars[2], y_octans_stars[2], 'ow')
    axis.text(x_octans_stars[0]-10, y_octans_stars[0]-10, '\u03C4', color='r')
    axis.set_aspect('equal', adjustable='box')
    axis.axis('off')
    axis.set_xlim([-160, 160])
    axis.set_ylim([-160, 160])
    fig.tight_layout()
    fig.patch.set_facecolor('k')
    plt.show()
