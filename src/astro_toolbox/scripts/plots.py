"""This module contains scripts functions.
"""
import math
import numpy as np
from matplotlib import pyplot as plt

from astro_toolbox.angle.hms import AngleHMS
from astro_toolbox.angle.dms import AngleDMS
from astro_toolbox.time.core import AstroDateTime
from astro_toolbox.coordinates.location import Location
from astro_toolbox.coordinates.equatorial import Equatorial
from astro_toolbox.query.ephemeris import Horizons

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
                for item in reversed(object_dict.items())]
                )
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
