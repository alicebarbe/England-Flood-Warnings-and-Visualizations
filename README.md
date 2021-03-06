# CUED Part IA Flood Warning System

This is the Part IA Lent Term computing activity at the Department of
Engineering, University of Cambridge.

Documentation on the code in this repository can be found here:
https://alicebarbe.github.io/England-Flood-Warnings-and-Visualizations/

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

Warnings are displayed shaded regions within which they are in force, usually
defined by flood planes. The colour of the regions indicates severity of the warning,
as one of 4 severity levels:

* Severe
   Areas where severe flooding, posing a strong danger to life, is expected
* High
   Areas where flooding is expected, and the appropriate actions must be taken to ensure safety of
   people and belongings
* Moderate
   Areas where flooding may occur. People in the area should be prepared to take action
* Low
   severe, high and moderate warnings which were in force in the past 24hours, risk of flooding is
   now low, but river levels may still be higher than usual.

Hovering over the warning displays the name of the area which the warning is in, the severity,
and when the warning was last updated. A link is also provided to the Government Flood Information Service
page regarding the flood warning. The link contains information on what action needs to be taken
and a 5 day flood forecast.

A link is also provided to the Government Flood Information Service page regarding the flood warning. The link contains
information on what action needs to be taken and a 5 day flood forecast.

The locations of monitoring stations are plotted as points and are colour coded according to their
relative water level (which is relative to the typical low and high levels of the station).
Hovering over a station displays the station's absolute water level, typical low and high levels,
and town.

Maps produced are saved as an html file temp plot and are opened in the default browser
after creation.

The boundary polygon and other data associated with the warning regions are cached as pickle files
in order to reduce the time taken to map the warnings, especially if many warnings are present.
The first time warnings are fetched the program may take some time to create a warning list and
produce a plot, but for subsequent runs all warning severity levels are fetched but only new warnings'
region information needs to be fetched and processed.


## Extension demo program

The extension_demo.py script runs elements of the extension.
The parts run can be configured using a command line interface,
with the following options:
```
usage: extension_demo.py [-h] [-s {severe,high,moderate,low}] [-lat LATITUDE]
                         [-long LONGITUDE] [-c] [-dm] [-dw] [-ds]
                         [-tol GEOMETRY_TOLERANCE] [-buf GEOMETRY_BUFFER]
                         
optional arguments:
-h, --help            show this help message and exit
-s {severe,high,moderate,low}, --warning-min-severity {severe,high,moderate,low}
                      Fetches warnings only of the given severity level or
                      greater. Warnings of severity moderate and above are
                      active currently, while low severity warnings were
                      active in the past 24 hours
-lat LATITUDE, --latitude LATITUDE
                      The latitude, in degrees of a location to be checked
                      for any flood warnigns.
-long LONGITUDE, --longitude LONGITUDE
                      The longitude, in degrees of a location to be checked
                      for any flood warnigns.
-c, --overwrite-warning-cache
                      If true, pulls all data on flood warning regions and
                      rewrites cache files. Note warnings which havechanged
                      are always updated, thisoption fully rebuilds the
                      cache.
-dm, --disable-warning-messages
                      disables printing detailed flood warning messages
-dw, --disable-plot-warnings
                      disables plotting of warnings on a choropleth map.
-ds, --disable-plot-stations
                      disables plotting of station locations and their
                      relative water levels on a map
-tol GEOMETRY_TOLERANCE, --geometry-tolerance GEOMETRY_TOLERANCE
                      Simplifies warning region geometry before plotting to
                      keep the map responsive. The tolerance is given in
                      degrees and sets the maximum allowed deviation of the
                      approximated geometry from the true shape. By default,
                      settings which provide detailed warning regions and
                      keep the map responsive are used
-buf GEOMETRY_BUFFER, --geometry_buffer GEOMETRY_BUFFER
                      Simplifies warning region geometry before plotting to
                      keep the map responsive. The buffer smoothes geometry
                      and removes any voids by taking the locus of the shape
                      offset by a fixed value, in degrees. By default,
                      settings which provide detailed warning regions and
                      keep the map responsive are used
```

Full descriptions for each of the arguments can be printed using:

```
python extension_demo.py --help
```

# Documentation

This documentation is generated using Sphinx and the Napoleon extension for parsing
Numpy docstrings. The source/config files for this documentation are stored in
/docs-source.

They are then copied into the public folder and deployed using GitHub Pages.

To re-run documentation, modify the source files in the /docs folder and execute
```
make html
```
  
and copy the contents of /docs-source/_build/html to /docs.

# Known issues

The Flood Monitoring API uses different types of reference points from which the
water level at a monitoring station is measured. They can be relative to the 
Ordnance Survey datum, to a local stage datum, or below datum. As a result, a 
handful of stations have negative water levels.

When different flood warnings overlap on the map, it is sometimes not possible 
to hover over one of the warnings.

# Acknowledgements

This uses Environment Agency flood and river level data from the real-time data API (Beta)

The background of this activity is documented at
https://cued-partia-flood-warning.readthedocs.io/.
