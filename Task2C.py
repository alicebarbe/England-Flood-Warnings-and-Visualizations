# -*- coding: utf-8 -*-
"""
Created on Mon Feb 3 21:02:52 2020

@author: Daniel
"""

from floodsystem.stationdata import build_station_list, update_water_levels
from floodsystem.geo import rivers_with_stations, stations_by_river
from floodsystem.station import MonitoringStation
from floodsystem.flood import stations_level_over_threshold, stations_highest_rel_level


def run():
    """Requirements for task 2C"""
    # build the station list and update the current levels
    station_list = build_station_list()
    update_water_levels(station_list, use_cache=True)

    num_stations = 10
    highest_level_stations = stations_highest_rel_level(station_list, num_stations)

    print("{} stations with the highest relative water levels, in descending order:".format(num_stations))
    for station in highest_level_stations:
        print(station.name, station.relative_water_level())


if __name__ == "__main__":
    print("*** Task 2C: CUED Part IA Flood Warning System ***")
    run()
