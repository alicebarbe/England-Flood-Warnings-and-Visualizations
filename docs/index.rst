.. Flood Warning System documentation master file, created by
   sphinx-quickstart on Fri Mar 20 23:29:11 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Flood Warning System's documentation!
================================================

Introduction
============
Probably identical to the beginning of readme

Dependencies
============

The flood warning system has been developed for Python versions 3.7 and later.
Additionally, the following packages are needed:

* numpy
* shapely
* plotly
* matplotlib
* pandas
* requests
* dateutils
* haversine

If you would like to run unit tests provided locally, pytest is also required.
Navigate to the libraries root directory and run ::
   python -m pytest


.. toctree::
   :maxdepth: 4
   :caption: Modules

   source/analysis
   source/datafetcher
   source/flood
   source/geo
   source/plot
   source/station
   source/stationdata
   source/utils
   source/warning
   source/warningdata

Demonstration programs
======================

A number of programs which demonstrate functions
of the library are included.
These may be run directly from a command-line, e.g. ::
   python Task1A.py

Note that functions which generate plots produce
an html file which is auto opened in the default browser

Known issues
============

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
