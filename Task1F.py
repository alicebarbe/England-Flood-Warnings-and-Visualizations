# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 12:22:45 2020

@author: Alice
"""

from floodsystem.stationdata import build_station_list
from floodsystem.station import MonitoringStation


def run():
    """Requirements for Task 1F"""
    # create list of systems with inconsistent typical range
    inconsistent_stations = MonitoringStation.inconsistent_typical_range_stations(
            build_station_list())

    # print their names in alphabetical order
    names = [station.name for station in inconsistent_stations]
    print(sorted(names))


if __name__ == "__main__":
    print("*** Task 1F: CUED Part IA Flood Warning System ***")
    run()
