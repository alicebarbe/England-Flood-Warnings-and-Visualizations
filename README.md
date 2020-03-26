# CUED Part IA Flood Warning System

This is the Part IA Lent Term computing activity at the Department of
Engineering, University of Cambridge.

Documentation on the code in this repository can be found here:
https://daniel345.gitlab.io/partia-flood-warning-system/

# Introduction

The aim of this library is to provide accurate and near real-time flood warnings and
river water level data, fetched from the Flood Monitoring API: 
https://environment.data.gov.uk/flood-monitoring/doc/reference

Data analysis, filtering and plotting capability is built-in.

# Dependencies

The flood warning system has been developed for Python versions 3.7 and later.
Additionally, the following packages are needed:

* numpy
* shapely
* plotly
* pandas
* requests
* dateutils
* haversine
* argparse
* progressbar2

If you would like to run the unit tests provided locally, pytest is also required.
Navigate to the library's root directory and run:

```
python -m pytest
```

# Demonstration programs

A number of programs which demonstrate functions
of the library are included.
These may be run directly from a command-line, e.g.

```
python Task1A.py
```

# Extension

## Environmental Agency Flood Warnings
The flood warnings produced by the are made available via the Flood Warning API.
They are produced by taking into account tidal, meteorological, groundwater and river level
data, as well as the locations of flood planes surrounding rivers. The warnings provide
information on the type and severity of flooding and also define the region in which
they are enforced.

Our extension collects this data and can display warning descriptions,
plot the regions affected by warnings on a map, and determine if any warnings
are active at a given location. Additionally, data from individual river monitoring
stations is obtained and can be plotted on the map.

## Map Plotting Functionality

Both current flood warnings and the relative water levels of monitoring stations can be
plotted on a map.

Warnings are displayed shaded regions within which they are in force, usually
defined by flood planes. The colour of the regions indicates severity of the warning.
Hovering over the warning displays the name of the area which the warning is in, the severity,
and when the warning was last updated.

A link is also provided to the Government Flood Information Service page regarding the flood warning. The link contains
information on what action needs to be taken and a 5 day flood forecast.

The locations of monitoring stations are plotted as points and are colour coded according to their
relative water level (which is relative to the typical low and high levels of the station).
Hovering over a station displays the absolute water level, the typical low and high levels
and the town the station is in.

Maps produced are saved as a html file temp plot and are also opened in the default browser
after creation.


## Extension demo program

The extension_demo.py script runs elements of the extension.
The parts run can be configured using a command line interface,
with the following options:
```
usage: extension_demo.py [-h] [-s {severe,high,moderate,low}] [-lat LATITUDE]
                         [-long LONGITUDE] [-c] [-dm] [-dw] [-ds]
                         [-tol GEOMETRY_TOLERANCE] [-buf GEOMETRY_BUFFER]
```

Full descriptions for each of the arguments can be printed using:

```
python extension_demo.py --help
```

# Known issues

# Acknowledgements

This uses Environment Agency flood and river level data from the real-time data API (Beta)

The background of this activity is documented at
https://cued-partia-flood-warning.readthedocs.io/.
