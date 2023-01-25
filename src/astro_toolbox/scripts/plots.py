"""This module contains scripts functions
"""
import math
import numpy as np
from matplotlib import pyplot as plt

from astro_toolbox.angle.hms import AngleHMS
from astro_toolbox.time.core import AstroDateTime
from astro_toolbox.coordinates.location import Location
from astro_toolbox.coordinates.equatorial import Equatorial
from astro_toolbox.query.ephemeris import Horizons

def sun_impact(lines, site, ut_time, bounds):
    """Sun observational impact
    """
    sun = Horizons('Sun', ut_time, site)
    sun = Equatorial(name='Sun',
                    alpha=sun.get_coord()[0],
                    delta=sun.get_coord()[1],
                    magnitude=sun.get_magnitude)
    rise_time = sun.calculate_rise_time(site,
                                        ut_time,
                                        altitude_0=-18)
    set_time = sun.calculate_set_time(site,
                                    ut_time,
                                    altitude_0=-18)
    rise_time = rise_time[0] + rise_time[1]/60 + rise_time[2]/3600
    set_time = set_time[0] + set_time[1]/60 + set_time[2]/3600
    if bounds[0] < set_time:
        plt.plot([(set_time-bounds[0])*10]*2,
                [0, lines], '--', color='white', linewidth=2, label='Sunset')
    elif bounds[1] - 24 > set_time:
        plt.plot([(24 + set_time-bounds[0])*10]*2,
                [0, lines], '--', color='white', linewidth=2, label='Sunset')
    if bounds[1] - 24 > rise_time:
        plt.plot([(24+rise_time-bounds[0])*10]*2,
                [0, lines], ':', color='white', linewidth=2, label='Sunrise')
    elif bounds[0] < rise_time:
        plt.plot([(rise_time-bounds[0])*10]*2,
                [0, lines], ':', color='white', linewidth=2, label='Sunrise')
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., facecolor='k', labelcolor='red')

def moon_impact(lines, site, ut_time, bounds):
    """Sun observational impact
    """
    moon = Horizons('Moon', ut_time, site)
    moon = Equatorial(name='Moon',
                    alpha=moon.get_coord()[0],
                    delta=moon.get_coord()[1],
                    magnitude=moon.get_magnitude)
    rise_time = moon.calculate_rise_time(site,
                                        ut_time,
                                        altitude_0=0)
    set_time = moon.calculate_set_time(site,
                                    ut_time,
                                    altitude_0=0)
    rise_time = rise_time[0] + rise_time[1]/60 + rise_time[2]/3600
    set_time = set_time[0] + set_time[1]/60 + set_time[2]/3600
    if bounds[0] < set_time:
        plt.plot([(set_time-bounds[0])*10]*2,
                [0, lines], '--', color='grey', linewidth=2, label='Moonset')
    elif bounds[1] - 24 > set_time:
        plt.plot([(24 + set_time-bounds[0])*10]*2,
                [0, lines], '--', color='grey', linewidth=2, label='Moonset')
    if bounds[1] - 24 > rise_time:
        plt.plot([(24+rise_time-bounds[0])*10]*2,
                [0, lines], ':', color='grey', linewidth=2, label='Moonrise')
    elif bounds[0] < rise_time:
        plt.plot([(rise_time-bounds[0])*10]*2,
                [0, lines], ':', color='grey', linewidth=2, label='Moonrise')
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., facecolor='k', labelcolor='red')

def airmas_map(object_dict,
                site: Location,
                ut_time: AstroDateTime,
                bounds: tuple=(18,31)):
    """Airmass calculations
    """
    bounds = list(bounds)
    if bounds[1] <= bounds[0]:
        bounds[1] = bounds[1] + 24
    if bounds[1] - bounds[0] > 24:
        raise ValueError("This program can't plot airmass map on duration exceeding 24 hours")
    airmasses = np.empty((len(object_dict), np.shape(np.arange(bounds[0],bounds[1],0.1))[0]))
    for j, key in enumerate(object_dict):
        object_dict[key].compute_on_date_coord(year = ut_time.get_year()+
                                                (ut_time.get_month()-1.0)/12)
        for i, time in enumerate(np.arange(bounds[0],bounds[1],0.1)):
            time = (int(time),(time-int(time))*60,00)
            ut_time = AstroDateTime(ut_time.date+time)
            airmasses[j][i] = object_dict[key].calculate_airmass(
                                ut_time.get_lst(site), site)
    fig = plt.figure(figsize=(8.3, 11.7))
    sun_impact(len(object_dict), site, ut_time, bounds)
    moon_impact(len(object_dict), site, ut_time, bounds)
    plt.pcolormesh(airmasses[::-1], cmap='jet', shading='flat', vmin = 1, vmax = 3.5)
    plt.colorbar(shrink = 0.5)
    plt.xticks(np.arange(0,len(np.arange(bounds[0],bounds[1],0.1)),10),
                                np.mod(np.arange(bounds[0],bounds[1]), 24))
    plt.yticks(np.arange(0.5,len(object_dict),1),
                [item[1].name + ' v='
                + str(item[1].magnitude)
                for item in reversed(object_dict.items())]
                )
    plt.tick_params(left = False)
    plt.grid(axis = 'x', color = 'k')
    plt.title(f'Airmass: {ut_time.get_day():02d}/{ut_time.get_month():02d}'
            +f'/{ut_time.get_year()} UT @ {site.name}')
    plt.tight_layout()
    return fig

def polarstar_plt_northern(location: Location, datetime: tuple=None):
    """Polaris Polar Finder possiton for northern emisphere
    """
    ut_time = AstroDateTime(datetime)
    fig, axis = plt.subplots(figsize=(5, 5))
    axis.add_patch(plt.Circle((0,0), 36, color='r', fill=False))
    axis.add_patch(plt.Circle((0,0), 40, color='r', linestyle='--', fill=False))
    axis.add_patch(plt.Circle((0,0), 44, color='r', fill=False))
    axis.plot([-21, 21], [0, 0], color='r')
    axis.plot([0, 0], [-21, 21], color='r')
    axis.text(-1, 47, '0', color='r')
    axis.text(47, -2, '6', color='r')
    axis.text(-3, -50, '12', color='r')
    axis.text(-52, -2, '18', color='r')
    polar_star = Equatorial(name='polaris',
                    alpha=(2, 32, 08.50),
                    delta=(+89, 16, 11.6),
                    magnitude=1.95)
    polar_star.compute_on_date_coord(year = ut_time.get_year()+
                                        (ut_time.get_month()-1.0)/12)
    polar_star_hour_angle = AngleHMS(polar_star.get_hourangle(
                                    ut_time.get_lst(location))).hmstorad()
    polar_star_distance = (90 - polar_star.delta.dmstodeg())*60
    x_polar_star, y_polar_star = (polar_star_distance*math.sin(polar_star_hour_angle),
                                -polar_star_distance*math.cos(polar_star_hour_angle))
    axis.plot(x_polar_star,y_polar_star, 'ow')
    axis.set_aspect('equal', adjustable='box')
    axis.axis('off')
    axis.set_xlim([-60, 60])
    axis.set_ylim([-60, 60])
    fig.tight_layout()
    fig.patch.set_facecolor('k')
    plt.show()

def polarstar_plt_southern(location: Location, datetime: tuple=None):
    """Polaris Polar Finder possiiton for souhern emisphere
    """
    ut_time = AstroDateTime(datetime)
    fig, axis = plt.subplots(figsize=(8, 8))
    axis.add_patch(plt.Circle((0,0), 60, color='r', fill=False))
    axis.add_patch(plt.Circle((0,0), 65, color='r', linestyle='--', fill=False))
    axis.add_patch(plt.Circle((0,0), 70, color='r', fill=False))
    axis.plot([-21, 21], [0, 0], color='r')
    axis.plot([0, 0], [-21, 21], color='r')
    axis.text(-1, 47, '0', color='r')
    axis.text(47, -2, '6', color='r')
    axis.text(-3, -50, '12', color='r')
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
