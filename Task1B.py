# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 17:22:45 2020

@author: Alice
"""

from floodsystem.stationdata import build_station_list
from floodsystem.geo import stations_by_distance

def run():
    """Requirements for Task 1B"""

    # Build list of stations and distances
    stations_distances = stations_by_distance(build_station_list(), (52.2053, 0.1218))

    # initialize output lists
    output_closest = []
    output_furthest = []

    # get name and town and distance of the ten closest stations
    for pair in stations_distances[:10]:
        output_closest.append((pair[0].name, pair[0].town, pair[1]))

    # get name and town and distance of the ten furthest stations
    for pair in stations_distances[-10:]:
        output_furthest.append((pair[0].name, pair[0].town, pair[1]))

    print(output_closest, output_furthest)


if __name__ == "__main__":
    print("*** Task 1B: CUED Part IA Flood Warning System ***")
    run()
