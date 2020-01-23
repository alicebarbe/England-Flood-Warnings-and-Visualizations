# -*- coding: utf-8 -*-
"""
Created on Sun Jan 18 20:47:52 2020

@author: Daniel
"""

from floodsystem.stationdata import build_station_list
from floodsystem.geo import rivers_with_stations, stations_by_river


def run():
    """Requirements for Task 1D"""
    # print first 10 rivers with at least one monitoring station
    station_list = build_station_list()
    river_set = rivers_with_stations(station_list)

    print("First 10 rivers with monitoring stations, in alphabetical order: \n {}".format(sorted(river_set)[:10]))

    # print the stations which are near specific rivers, in alphabetical order
    station_river_dict = stations_by_river(station_list)

    rivers = ['River Aire', 'River Cam', 'River Thames']
    for river in rivers:
        # make a list of station names for each river
        station_names = [s.name for s in station_river_dict[river]]
        print("Stations near {}: \n {}".format(river, sorted(station_names)))


if __name__ == "__main__":
    print("*** Task 1D: CUED Part IA Flood Warning System ***")
    run()
