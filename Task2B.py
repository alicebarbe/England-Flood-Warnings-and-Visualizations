# -*- coding: utf-8 -*-
"""
Created on Sun Jan 18 20:47:52 2020

@author: Daniel
"""

from floodsystem.stationdata import build_station_list, update_water_levels
from floodsystem.geo import rivers_with_stations, stations_by_river
from floodsystem.station import MonitoringStation
from floodsystem.flood import stations_level_over_threshold


def run():
    """Requirements for task 2B"""
    # build the station list and update the current levels
    station_list = build_station_list()
    update_water_levels(station_list, use_cache=True)

    threshold = 0.8
    over_thresh = stations_level_over_threshold(station_list, threshold)

    for station, level in over_thresh:
        print(station.name, level)

if __name__ == "__main__":
    print("*** Task 2B: CUED Part IA Flood Warning System ***")
    run()
