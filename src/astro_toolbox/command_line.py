"""This module create the console interface
"""
import numpy as np
import pathlib
import click
from matplotlib import pyplot as plt

from astro_toolbox.angle.hms import AngleHMS
from astro_toolbox.time import AstroDateTime
from astro_toolbox.location import Location
from astro_toolbox.coordinates.equatorial import Equatorial

def read_observatory_program(input_file: pathlib.Path):
    time = (0,0,0)
    observation_datas = np.loadtxt(input_file, dtype = str, delimiter = ',')
    latitude = observation_datas[0][1].split('/')
    latitude = (int(latitude[0]), int(latitude[1]), float(latitude[2]))
    longitude = observation_datas[0][2].split('/')
    longitude = (int(longitude[0]), int(longitude[1]), float(longitude[2]))
    date = observation_datas[0][3].split('/')
    date = tuple([int(x) for x in date])
    location = Location(observation_datas[0][0], latitude=latitude, longitude=longitude)
    datetime = AstroDateTime(date+time)
    objects_list = []
    for i in range(1,np.shape(observation_datas)[0]):
        alpha = observation_datas[i][1].split('/')
        alpha = (int(alpha[0]), int(alpha[1]), float(alpha[2]))
        delta = observation_datas[i][2].split('/')
        delta = (int(delta[0]), int(delta[1]), float(delta[2]))
        objects_list.append(Equatorial(alpha, delta, observation_datas[i][0]))
    return datetime, location, objects_list

@click.command()
@click.argument("script")
@click.option("-i", "--input", default='')
@click.option("-o", "--output", default='')
@click.option("--begin", default=18)
@click.option("--end", default=31)
def main(script: str, input: str, output: str, begin: int, end: int):
    if script == 'airmass':
        if input == '':
            inputpath = pathlib.Path('/observations.lst')
        else:
            inputpath = pathlib.Path(input)
            if inputpath.is_dir():
                inputpath = pathlib.Path(input+'/observations.lst')

        UTtime, location, object_list = read_observatory_program(inputpath)

        year = UTtime.get_year()+(UTtime.get_month()-1.0)/12

        timelist = np.arange(begin,end,0.1)

        airmasses = np.empty((len(object_list), np.shape(timelist)[0]))

        for j in range(len(object_list)):
            object_list[j].compute_on_date_coords(year = year)
            airmass = []
            for i in timelist:
                time = (int(i),(i-int(i))*60,00)
                UTtime = AstroDateTime(UTtime.get_date()+time)
                lst = UTtime.get_lst(location)
                lst = AngleHMS(lst)
                airmass.append(object_list[j].calculate_airmass(lst, location))
            airmasses[j] = airmass
        if output == '':
            outputpath = pathlib.Path(f'/Airmass_Map_{UTtime.get_day()}_{UTtime.get_month()}_{UTtime.get_year()}.pdf')
        else:
            outputpath = pathlib.Path(output)
            if outputpath.is_dir():
                outputpath = pathlib.Path(input+f'/Airmass_Map_{UTtime.get_day()}_{UTtime.get_month()}_{UTtime.get_year()}.pdf')

        plt.figure(figsize=(8.3, 11.7))

        plt.pcolormesh(airmasses, cmap='jet', shading='flat', vmin = 1, vmax = 3.5, label = 'airmasses')
        plt.colorbar(shrink = 0.5)
        plt.xticks(np.arange(0,130,10), np.arange(18,31))
        listname = [i.name for i in object_list]
        plt.yticks(np.arange(0.5,len(object_list),1), listname)
        plt.tick_params(left = False)
        plt.grid(axis = 'x', color = 'k')
        plt.title(f'Airmasses: {UTtime.get_day()}/{UTtime.get_month()}/{UTtime.get_year()}')
        plt.tight_layout()
        plt.savefig(outputpath)


if __name__ == "__main__":
    main()