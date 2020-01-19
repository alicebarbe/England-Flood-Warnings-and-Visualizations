"""Unit test for the geo module"""

import floodsystem.geo as geo
import floodsystem.stationdata as stationdata

def test_rivers_with_stations():

    # make a station list
    station_list = stationdata.build_station_list()
    rivers = geo.rivers_with_stations(station_list)

    # check number of rivers does not exceed number of stations
    assert(len(rivers) <= len(station_list))

def test_stations_by_river():

    # make a station list
    station_list = stationdata.build_station_list()
    stations_by_river = geo.stations_by_river(station_list)

    # check for known stations by certain rivers
