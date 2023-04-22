# Astro Toolbox

[![Read the Docs](https://img.shields.io/readthedocs/astro_toolbox)](https://astro-toolbox.readthedocs.io/en/latest/) [![GitHu](https://img.shields.io/github/license/rloustalet/astro_toolbox?color=green)](https://en.wikipedia.org/wiki/GNU_General_Public_License) [![image](https://img.shields.io/badge/code_style-pep8-blue)](https://www.python.org/dev/peps/pep-0008/)

The astro_toolbox project is developped to allow amateur astronomer and observatory to perform observationnal astronomy calculations. This repository contain the source code of the project. At this moment the project represent an alpha version.  

## Installation

Use `pip install astro_toolbox` to install last version or clone this repository and execute `make install`.

## Basic usage

### Synopsis

astro-toolbox \[options1\] \<command\> \<argument\> \[options2\]

# Options 1

**-v, \--verbose** Program verbosity.

# Commands

# airmass

This command allows you to plot airmass map of one or multiple objects.

# *argument*

You can enter one or many objects or a path to a file or a directory. If
you left it blank, it will search on your current directory a file named
observations.lst

You must end the name to a directory with a `/`

# *examples:*

`astro-toolbox airmass examples/`

`astro-toolbox airmass examples/examples.lst`

`astro-toolbox airmass betelgeuse vega`

# *options*

**-d, \--date** Option to inform a different date `-d 2022-12-18`,
default is None (today date).

**-l, \--location** Option to inform a location name `-l Greenwich`,
default is None (last location used).

**-o, \--output** Option to inform the output directory (must end with a
`/`) `-o examples/`, default is \'\' (current directory).

**\--bounds** Option which requires two hours arguments consider this
program calculates everything in UT `--bounds 19 33` mean we begin
calculations at 7pm and end these at 9am the next day.

# info

This command allows you to query Simbad (for stars and deep sky objects)
or JPL Horizons for solar system objects.

# *argument*

Enter the object name as argument

# *options*

**-d, \--date** Option to inform a different date `-d 2022-12-18`,
default is None (today date).

**-l, \--location** Option to inform a location name `-l Greenwich`,
default is None (last location used).

# location

This command allows you to add, update or read a location.

# *argument*

Enter the location name, list allow you to display all locations saved.

# *options*

**-a, \--add** Option to add a new location (if it doesn\'t exists). It
will ask you longitude, latitude in degrees (0.0) or DMS (0°0\'0\") and
elevation in meters.

**-d, \--delete** Option to delete a location (if it exists).

**-u, \--update** Option to update an existing location it will ask the
same thing as adding option but left blank the data, you don\'t want to
change.

# polaris

This command allows you to display the polaris position (northern and
southern hemisphere) in a polar finder. This command doesn\'t need any
argument.

# *options*

**-d, \--datetime** Option to inform a different date and time
`-d 2022-12-18:20:35:55`, default is None (today date).

**-l, \--location** Option to inform a location name `-l Greenwich`,
default is None (last location used).

# weather

This command allows you to display forecasts of a given location.
This command doesn\'t need any argument.

# *options*

**-l, \--location** Option to inform a location name `-l Greenwich`,
default is None (last location used).

**-d, \--days** Counter to inform the number of days to display,
default is 1.

**-p, \--past** Counter to inform the number of past days to display,
default is 0.

## Documentation

The documentation is availale on [readthedocs.io](https://astro-toolbox.readthedocs.io/en/latest/)

## License

Astropy is licensed under a GNU GPL license - see the [LICENSE](https://github.com/rloustalet/astro_toolbox/blob/main/LICENSE) file.